"""
邮件相关工具包
"""
from app.utils.email.parser import (
    decode_mime_words,
    parse_email_address,
    get_email_body,
    get_attachment_info,
    parse_email_date,
    parse_email_addresses
)
from app.utils.email.imap_client import IMAPClient, test_imap_connection
from app.utils.email.smtp_client import (
    SMTPClient,
    send_verification_email,
    send_reset_password_email,
    send_test_email,
    test_smtp_connection
)

__all__ = [
    # IMAP相关
    "IMAPClient",
    "test_imap_connection",
    "decode_mime_words",
    "parse_email_address",
    "get_email_body",
    "get_attachment_info",
    "parse_email_date",
    "parse_email_addresses",
    
    # SMTP相关
    "SMTPClient",
    "test_smtp_connection",
    "send_verification_email",
    "send_reset_password_email",
    "send_test_email",
    "send_email"
]