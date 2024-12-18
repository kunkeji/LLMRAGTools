"""
SMTP客户端模块
"""
import logging
from typing import List, Optional, Dict, Any
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import aiosmtplib
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

from app.core.config import settings

logger = logging.getLogger(__name__)

# 初始化Jinja2环境
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "email_templates")
env = Environment(loader=FileSystemLoader(template_dir))

async def test_smtp_connection(
    host: str,
    port: int,
    username: str,
    password: str,
    use_ssl: bool = True,
    use_tls: bool = False
) -> Dict[str, Any]:

    try:
        smtp = aiosmtplib.SMTP(
            hostname=host,
            port=port,
            use_tls=use_ssl,
            start_tls=use_tls
        )
        
        await smtp.connect()
        await smtp.login(username, password)
        await smtp.quit()
        
        return {
            "success": True,
            "error": None,
            "test_time": datetime.now()
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"SMTP连接测试失败: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "test_time": datetime.now()
        }

class SMTPClient:
    """SMTP客户端类"""
    
    def __init__(self, host: str, port: int, username: str, password: str, use_ssl: bool = True, use_tls: bool = False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
        self.use_tls = use_tls
    
    async def test_connection(self) -> Dict[str, Any]:
        """测试连接"""
        return await test_smtp_connection(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            use_ssl=self.use_ssl,
            use_tls=self.use_tls
        )
    
    async def send_email(
        self,
        to_addresses: List[str],
        subject: str,
        content: str,
        content_type: str = "html",
        cc_addresses: Optional[List[str]] = None,
        bcc_addresses: Optional[List[str]] = None,
        from_name: Optional[str] = None
    ) -> None:
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = formataddr((from_name or self.display_name, self.username))
            msg["To"] = ", ".join(to_addresses)
            
            if cc_addresses:
                msg["Cc"] = ", ".join(cc_addresses)
            if bcc_addresses:
                msg["Bcc"] = ", ".join(bcc_addresses)
            # 添加正文
            msg.attach(MIMEText(content, 'html', "utf-8"))
            # 连接SMTP服务器并发送
            smtp = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                use_tls=self.use_ssl,
                start_tls=self.use_tls
            )
            await smtp.connect()
            await smtp.login(self.username, self.password)
            
            # 合并所有收件人
            all_recipients = to_addresses.copy()
            if cc_addresses:
                all_recipients.extend(cc_addresses)
            if bcc_addresses:
                all_recipients.extend(bcc_addresses)
            
            await smtp.send_message(msg, self.username, all_recipients)
            await smtp.quit()
        except Exception as e:
            logger.error(f"发送邮件失败: {str(e)}")
            raise

async def send_verification_email(email: str, code: str) -> None:
    """发送验证码邮件"""
    try:
        # 获取模板
        template = env.get_template("verification_code.html")
        content = template.render(code=code)
        
        # 创建SMTP客户端
        smtp = SMTPClient(
            host=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_ssl=settings.SMTP_SSL,
            use_tls=settings.SMTP_TLS
        )
        
        # 发送邮件
        await smtp.send_email(
            to_addresses=[email],
            subject="验证码",
            content=content,
            content_type="html"
        )


    except Exception as e:
        logger.error(f"发送验证码邮件失败: {str(e)}")
        raise

async def send_reset_password_email(email: str, code: str) -> None:
    """发送重置密码邮件"""
    try:
        # 获取模板
        template = env.get_template("reset_password.html")
        content = template.render(code=code)
        
        # 创建SMTP客户端
        smtp = SMTPClient(
            host=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_ssl=settings.SMTP_SSL,
            use_tls=settings.SMTP_TLS
        )
        
        # 发送邮件
        await smtp.send_email(
            to_addresses=[email],
            subject="重置密码",
            content=content,
            content_type="html"
        )
        
    except Exception as e:
        logger.error(f"发送重置密码邮件失败: {str(e)}")
        raise

async def send_test_email(
    email: str,
    host: str,
    port: int,
    username: str,
    password: str,
    use_ssl: bool = True,
    use_tls: bool = False
) -> None:
    """发送测试邮件"""
    try:
        # 获取模板
        template = env.get_template("test_email.html")
        content = template.render()
        
        # 创建SMTP客户端
        smtp = SMTPClient(
            host=host,
            port=port,
            username=username,
            password=password,
            use_ssl=use_ssl,
            use_tls=use_tls
        )
        
        # 发送邮件
        await smtp.send_email(
            to_addresses=[email],
            subject="测试邮件",
            content=content,
            content_type="html"
        )
        
    except Exception as e:
        logger.error(f"发送测试邮件失败: {str(e)}")
        raise 