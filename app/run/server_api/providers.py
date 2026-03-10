from dishka import Provider, Scope, provide

from app.core.application.interfaces.producer.file import IFileCompressProducer
from app.core.application.interfaces.projection.user import IUserProjection
from app.core.application.interfaces.repository.file import IFileRepository
from app.core.application.interfaces.repository.user import IUserRepository
from app.core.application.interfaces.services.email import IEmailService
from app.core.application.interfaces.services.file import IFileStorage
from app.core.application.interfaces.services.tokens import ITokensService
from app.core.application.services.auth import AuthService
from app.core.application.services.file import FileService
from app.core.application.services.user import UserService
from app.infrastructure.database.projection.user import UserProjection
from app.infrastructure.database.repository.file import FileRepository
from app.infrastructure.database.repository.user import UserRepository
from app.infrastructure.producer.file import RabbitFileCompressProducer
from app.infrastructure.services.email.local import LoggerEmailService
from app.infrastructure.services.email.smtp import SmtpEmailService
from app.infrastructure.services.files.s3 import S3FileStorage
from app.infrastructure.services.tokens.jwt import JwtService


class AppInjectionsProvider(Provider):
    scope = Scope.APP

    tokens_service = provide(JwtService, provides=ITokensService)
    email_service = provide(SmtpEmailService, provides=IEmailService)

    user_repository = provide(UserRepository, provides=IUserRepository)
    user_projection = provide(UserProjection, provides=IUserProjection)
    user_service = provide(UserService)
    auth_service = provide(AuthService)

    file_repository = provide(FileRepository, provides=IFileRepository)
    file_storage = provide(S3FileStorage, provides=IFileStorage)
    file_compress_producer = provide(RabbitFileCompressProducer, provides=IFileCompressProducer)
    file_service = provide(FileService)


class LocalMockInjectionsProvider(Provider):
    scope = Scope.APP

    email_service = provide(LoggerEmailService, provides=IEmailService)
