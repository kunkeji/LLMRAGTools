import logging
from typing import Any, Dict, Optional
from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

from app.core.config import settings

class EmailSender:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.SMTP_USER,
            MAIL_PASSWORD=settings.SMTP_PASSWORD,
            MAIL_FROM=settings.EMAILS_FROM_EMAIL,
            MAIL_PORT=settings.SMTP_PORT,
            MAIL_SERVER=settings.SMTP_HOST,
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True
        )
        self.fast_mail = FastMail(self.conf)

    async def send_email(
        self,
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
    ) -> None:
        """
        发送电子邮件
        """
        try:
            message = MessageSchema(
                subject=subject_template,
                recipients=[email_to],
                body=html_template,
                subtype="html"
            )
            await self.fast_mail.send_message(message)
            logging.info(f"发送邮件成功: {email_to}")
        except Exception as e:
            logging.error(f"发送邮件失败: {str(e)}")
            raise

email = EmailSender()
