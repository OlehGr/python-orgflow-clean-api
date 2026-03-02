import logging
from typing import override

from app.core.application.interfaces.services.email import IEmailService
from app.infrastructure.services.email.base import BaseEmailService


logger = logging.getLogger(__name__)


class LoggerEmailService(BaseEmailService, IEmailService):
    def __init__(self) -> None:
        super().__init__()

    @override
    async def _send_email(self, *, email: str, subject: str, body: str) -> None:
        logger.info(f"\nTo: {email}.\nSubject: {subject}.\nBody: {body}")
