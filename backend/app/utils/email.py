import logging
from typing import Any, Dict
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.core.config import settings

# 设置模板环境
template_dir = Path(__file__).parent / "email_templates"
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True
)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_FROM_NAME="Agent Tools",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

class EmailClient:
    def __init__(self):
        self.fast_mail = FastMail(conf)

    async def send_email(
        self,
        email_to: str,
        subject: str,
        template_name: str,
        template_data: Dict[str, Any],
    ) -> None:
        """
        发送电子邮件
        Args:
            email_to: 收件人邮箱
            subject: 邮件主题
            template_name: 模板名称（相对于 email_templates 目录）
            template_data: 模板数据
        """
        try:
            # 获取模板
            template = env.get_template(template_name)
            
            # 渲染模板
            html_content = template.render(**template_data)
            
            # 创建消息
            message = MessageSchema(
                subject=subject,
                recipients=[email_to],
                body=html_content,
                subtype=MessageType.html
            )

            # 发送邮件
            await self.fast_mail.send_message(message)
            logging.info(f"发送邮件成功: {email_to}")
        except Exception as e:
            logging.error(f"发送邮件失败: {str(e)}")
            raise

email_client = EmailClient()

async def send_verification_email(email_to: str, code: str) -> None:
    """
    发送验证码邮件
    """
    await email_client.send_email(
        email_to=email_to,
        subject="验证码 - 注册验证",
        template_name="verification_code.html",
        template_data={"code": code}
    )

async def send_reset_password_email(email_to: str, code: str, username: str) -> None:
    """
    发送重置密码验证码邮件
    """
    await email_client.send_email(
        email_to=email_to,
        subject="重置密码验证码",
        template_name="reset_password.html",
        template_data={
            "code": code,
            "username": username
        }
    )
