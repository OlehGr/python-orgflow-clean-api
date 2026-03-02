from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.core.config import env_config


class BaseEmailService(ABC):
    templates: Environment
    confirmation_url: str
    recovery_url: str

    def __init__(self) -> None:
        self.templates = Environment(
            loader=FileSystemLoader("./app/infrastructure/services/email/templates"),
            autoescape=select_autoescape(["html"]),
        )
        self.confirmation_url = f"{env_config.base_url}/confirm"
        self.recovery_url = f"{env_config.base_url}/recovery-password"

    async def send_confirmation_email(self, *, email: str, username: str, token: str) -> None:
        template = self.templates.get_template("confirmation.html")

        html_body = template.render(
            username=username, confirmation_url=f"{self.confirmation_url}/?token={token}", base_url=env_config.base_url
        )

        await self._send_email(email=email, subject="Активация аккаунта", body=html_body)

    async def send_recovery_email(self, *, email: str, username: str, token: str) -> None:
        template = self.templates.get_template("recovery.html")

        html_body = template.render(
            name=username, recovery_url=f"{self.recovery_url}/?token={token}", base_url=env_config.base_url
        )

        await self._send_email(email=email, subject="Восстановление пароля", body=html_body)

    @abstractmethod
    async def _send_email(self, *, email: str, subject: str, body: str) -> None:
        raise NotImplementedError
