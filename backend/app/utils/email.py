import logging
from typing import Any, Dict, List
from pathlib import Path
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings

# 配置Jinja2模板环境
template_env = Environment(
    loader=FileSystemLoader(str(Path(__file__).parent / "email_templates")),
    autoescape=True
)

class EmailClient:
    def __init__(self):
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.use_tls = settings.SMTP_TLS
        self.use_ssl = settings.SMTP_SSL
        self.from_email = settings.EMAILS_FROM_EMAIL
        self.from_name = settings.EMAILS_FROM_NAME

    async def _get_smtp_client(self) -> aiosmtplib.SMTP:
        """
        获取SMTP客户端连接
        """
        if self.use_ssl:
            client = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port,
                use_tls=True
            )
        else:
            client = aiosmtplib.SMTP(
                hostname=self.host,
                port=self.port
            )
        
        await client.connect()
        
        if self.use_tls and not self.use_ssl:
            await client.starttls()
        
        await client.login(self.username, self.password)
        return client

    async def send_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        template_data: Dict[str, Any],
    ) -> None:
        """
        发送电子邮件
        Args:
            to_email: 收件人邮箱
            subject: 邮件主题
            template_name: 模板文件名
            template_data: 模板数据
        """
        try:
            # 渲染模板
            template = template_env.get_template(template_name)
            html_content = template.render(**template_data)

            # 创建邮件
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.from_name} <{self.from_email}>"
            message['To'] = to_email

            # 添加HTML内容
            html_part = MIMEText(html_content, 'html', 'utf-8')
            message.attach(html_part)

            # 发送邮件
            async with await self._get_smtp_client() as client:
                await client.send_message(message)
            
            logging.info(f"发送邮件成功: {to_email}")
        except Exception as e:
            logging.error(f"发送邮件失败: {str(e)}")
            raise

email_client = EmailClient()

async def send_verification_email(email_to: str, code: str) -> None:
    """
    发送验证码邮件
    """
    template_data = {
        "code": code,
        "expires_minutes": 10
    }
    
    await email_client.send_email(
        to_email=email_to,
        subject="验证码 - 注册验证",
        template_name="verification_code.html",
        template_data=template_data
    )

async def send_reset_password_email(email_to: str, code: str, username: str) -> None:
    """
    发送重置密码验证码邮件
    """
    template_data = {
        "username": username,
        "code": code,
        "expires_minutes": 10
    }
    
    await email_client.send_email(
        to_email=email_to,
        subject="重置密码验证码",
        template_name="reset_password.html",
        template_data=template_data
    )
