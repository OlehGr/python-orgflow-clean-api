import logging
from dataclasses import dataclass, field

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.application.interfaces.services.email import IEmailService
from app.core.config import env_config


logger = logging.getLogger(__name__)


@dataclass
class EmailLoggerService(IEmailService):
    templates: Environment = field(
        default_factory=lambda: Environment(
            loader=FileSystemLoader("./app/infrastructure/services/email/templates"),
            autoescape=select_autoescape(["html"]),
        ),
        init=False,
    )

    async def send_confirmation_email(self, *, email: str, username: str, token: str) -> None:
        template = self.templates.get_template("confirmation.html")

        html_body = template.render(
            username=username, confirmation_url=f"{env_config.confirmation_url}/?{token}", base_url=env_config.base_url
        )

        await self._send_email(email=email, subject="Активация аккаунта", body=html_body)

    async def send_recovery_email(self, *, email: str, username: str, token: str) -> None:
        template = self.templates.get_template("recovery.html")

        html_body = template.render(
            name=username, recovery_url=f"{env_config.recovery_url}/?token={token}", base_url=env_config.base_url
        )

        await self._send_email(email=email, subject="Восстановление пароля", body=html_body)

    async def _send_email(self, *, email: str, subject: str, body: str) -> None:
        logger.info(f"To: {email}.\nSubject: {subject}.\nBody: {body}")
