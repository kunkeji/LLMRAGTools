"""
IMAP客户端模块
"""
import imaplib
import email
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

async def test_imap_connection(
    host: str,
    port: int,
    username: str,
    password: str,
    use_ssl: bool = True
) -> Dict[str, Any]:
    """测试IMAP连接
    
    Args:
        host: IMAP服务器地址
        port: IMAP端口
        username: 用户名
        password: 密码
        use_ssl: 是否使用SSL
        
    Returns:
        Dict[str, Any]: 测试结果
        {
            "success": bool,
            "error": Optional[str],
            "test_time": datetime,
            "folders": Optional[List[str]]
        }
    """
    try:
        if use_ssl:
            client = imaplib.IMAP4_SSL(host, port)
        else:
            client = imaplib.IMAP4(host, port)
            
        client.login(username, password)
        
        # 获取文件夹列表
        _, folders = client.list()
        folder_list = []
        for folder in folders:
            try:
                # 解析文件夹名称
                folder_name = folder.decode().split('"/"')[-1].strip('" ')
                folder_list.append(folder_name)
            except:
                continue
        
        client.logout()
        
        return {
            "success": True,
            "error": None,
            "test_time": datetime.now(),
            "folders": folder_list
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"IMAP连接测试失败: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "test_time": datetime.now(),
            "folders": None
        }

class IMAPClient:
    """IMAP客户端类"""
    
    def __init__(self, host: str, port: int, use_ssl: bool = True):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.client = None
    
    async def test_connection(self, username: str, password: str) -> Dict[str, Any]:
        """测试连接"""
        return await test_imap_connection(
            host=self.host,
            port=self.port,
            username=username,
            password=password,
            use_ssl=self.use_ssl
        )
    
    def connect(self, username: str, password: str) -> None:
        """连接IMAP服务器"""
        try:
            if self.use_ssl:
                self.client = imaplib.IMAP4_SSL(self.host, self.port)
            else:
                self.client = imaplib.IMAP4(self.host, self.port)
            self.client.login(username, password)
        except Exception as e:
            raise ConnectionError(f"连接IMAP服务器失败: {str(e)}")
    
    def disconnect(self) -> None:
        """断开IMAP连接"""
        if self.client:
            try:
                self.client.close()
                self.client.logout()
            except:
                pass
            finally:
                self.client = None
    
    def select_folder(self, folder: str = "INBOX") -> int:
        """选择邮件文件夹"""
        if not self.client:
            raise ConnectionError("未连接到IMAP服务器")
        try:
            _, data = self.client.select(folder)
            return int(data[0])
        except Exception as e:
            raise ValueError(f"选择文件夹失败: {str(e)}")
    
    def search_emails(self, criteria: List[str] = None) -> List[bytes]:
        """搜索邮件"""
        if not self.client:
            raise ConnectionError("未连接到IMAP服务器")
        try:
            if not criteria:
                criteria = ['ALL']
            _, message_numbers = self.client.search(None, *criteria)
            return message_numbers[0].split()
        except Exception as e:
            raise ValueError(f"搜索邮件失败: {str(e)}")
    
    def fetch_email(self, num: bytes) -> Tuple[bytes, email.message.Message]:
        """获取单封邮件"""
        if not self.client:
            raise ConnectionError("未连接到IMAP服务器")
        try:
            _, msg_data = self.client.fetch(num, '(RFC822)')
            email_body = msg_data[0][1]
            return email_body, email.message_from_bytes(email_body)
        except Exception as e:
            raise ValueError(f"获取邮件失败: {str(e)}")
    
    def get_emails_since(self, since_date: Optional[datetime] = None) -> List[Tuple[bytes, email.message.Message]]:
        """获取指定日期之后的所有邮件"""
        try:
            criteria = ['ALL']
            if since_date:
                date_str = since_date.strftime("%d-%b-%Y")
                criteria = ['SINCE', date_str]
            
            message_numbers = self.search_emails(criteria)
            results = []
            
            for num in message_numbers:
                try:
                    email_body, msg = self.fetch_email(num)
                    results.append((email_body, msg))
                except Exception as e:
                    continue
                    
            return results
            
        except Exception as e:
            raise ValueError(f"获取邮件列表失败: {str(e)}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect() 