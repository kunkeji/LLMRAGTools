"""
邮件解析模块
"""
import email
from datetime import datetime
from email.header import decode_header
from email.utils import parseaddr, parsedate_to_datetime
from typing import Tuple, List, Optional
import pytz
import logging
from dateutil import parser

from app.schemas.email import EmailAttachmentCreate

logger = logging.getLogger(__name__)

def decode_mime_words(text: str) -> str:
    """解码MIME编码的文本"""
    if not text:
        return ""
    decoded_parts = []
    for part, charset in decode_header(text):
        if isinstance(part, bytes):
            try:
                decoded_parts.append(part.decode(charset or 'utf-8', errors='replace'))
            except:
                decoded_parts.append(part.decode('utf-8', errors='replace'))
        else:
            decoded_parts.append(str(part))
    return ''.join(decoded_parts)

def parse_email_address(addr: str) -> Tuple[str, str]:
    """解析邮件地址,返回(名称,地址)"""
    name, address = parseaddr(addr)
    return decode_mime_words(name), address

def get_email_body(msg: email.message.Message) -> Tuple[str, str]:
    """获取邮件正文内容和类型"""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_maintype() == 'text':
                return part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace'), part.get_content_type()
    else:
        return msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='replace'), msg.get_content_type()
    return "", "text/plain"

def get_attachment_info(part: email.message.Message, email_id: int) -> Optional[EmailAttachmentCreate]:
    """获取邮件附件信息"""
    try:
        filename = part.get_filename()
        if not filename:
            return None
            
        filename = decode_mime_words(filename)
        content_type = part.get_content_type()
        content_id = part.get('Content-ID')
        if content_id:
            content_id = content_id.strip('<>')
            
        # 获取附件大小
        payload = part.get_payload(decode=True)
        size = len(payload) if payload else 0
            
        return EmailAttachmentCreate(
            email_id=email_id,
            filename=filename,
            content_type=content_type,
            size=size,
            storage_path="",
            content_id=content_id,
            is_inline=bool(content_id)
        )
    except Exception as e:
        logger.error(f"获取附件信息失败: {str(e)}")
        return None

def parse_email_date(date_str: str) -> datetime:
    """解析邮件日期"""
    try:
        # 尝试解析 RFC 2822 格式 (邮件标准格式)
        try:
            dt = parsedate_to_datetime(date_str)
            if dt.tzinfo:
                # 转换为 UTC 时间并移除时区信息
                return dt.astimezone(pytz.UTC).replace(tzinfo=None)
            return dt
        except (TypeError, ValueError):
            pass
            
        # 尝试解析 ISO 8601 格式
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
            return dt  # ISO 8601 'Z' 格式本身就是 UTC 时间
        except ValueError:
            pass
            
        # 尝试其他 ISO 8601 变体
        try:
            dt = parser.isoparse(date_str)
            if dt.tzinfo:
                # 转换为 UTC 时间并移除时区信息
                return dt.astimezone(pytz.UTC).replace(tzinfo=None)
            return dt
        except (ValueError, TypeError):
            pass
        
        # 尝试其他常见格式
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
                
        # 如果所有格式都失败,记录警告并返回当前时间
        logger.warning(f"无法解析日期格式: {date_str}, 使用当前时间")
        return datetime.utcnow()
        
    except Exception as e:
        logger.error(f"解析日期出错: {str(e)}, date_str: {date_str}")
        return datetime.utcnow()

def parse_email_addresses(addresses: List[str]) -> List[str]:
    """解析邮件地址列表"""
    result = []
    for addr in addresses:
        _, address = parse_email_address(addr)
        if address:
            result.append(address)
    return result 