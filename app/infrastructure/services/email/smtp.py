from email.message import EmailMessage
from typing import override

import aiosmtplib

from app.core.application.interfaces.services.email import IEmailService
from app.core.config import env_config
from app.infrastructure.services.email.base import BaseEmailService


class SmtpEmailService(BaseEmailService, IEmailService):
    def __init__(self) -> None:
        super().__init__()

    @override
    async def _send_email(self, *, email: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = env_config.email_from
        message["To"] = email
        message.set_content(body, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=env_config.smtp_host,
            port=env_config.smtp_port,
            username=str(env_config.smtp_user),
            password=str(env_config.smtp_password),
            start_tls=True,
        )
