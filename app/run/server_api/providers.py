from dishka import Provider, Scope, provide

from app.core.application.interfaces.producer.file import IFileCompressProducer
from app.core.application.interfaces.projection.organization import IOrganizationProjection
from app.core.application.interfaces.projection.organization_member import IOrganizationMemberProjection
from app.core.application.interfaces.projection.user import IUserProjection
from app.core.application.interfaces.repository.file import IFileRepository
from app.core.application.interfaces.repository.organization import IOrganizationRepository
from app.core.application.interfaces.repository.organization_member import IOrganizationMemberRepository
from app.core.application.interfaces.repository.user import IUserRepository
from app.core.application.interfaces.services.email import IEmailService
from app.core.application.interfaces.services.file import IFileStorage
from app.core.application.interfaces.services.tokens import ITokensService
from app.core.application.services.auth import AuthService
from app.core.application.services.file import FileService
from app.core.application.services.organization_member import OrganizationMemberService
from app.core.application.services.orgnaization import OrganizationService
from app.core.application.services.user import UserService
from app.infrastructure.database.projection.organization import OrganizationProjection
from app.infrastructure.database.projection.organization_member import OrganizationMemberProjection
from app.infrastructure.database.projection.user import UserProjection
from app.infrastructure.database.repository.file import FileRepository
from app.infrastructure.database.repository.organization import OrganizationRepository
from app.infrastructure.database.repository.organization_member import OrganizationMemberRepository
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

    organization_repository = provide(OrganizationRepository, provides=IOrganizationRepository)
    organization_projection = provide(OrganizationProjection, provides=IOrganizationProjection)
    organization_service = provide(OrganizationService)

    organization_member_repository = provide(OrganizationMemberRepository, provides=IOrganizationMemberRepository)
    organization_member_projection = provide(OrganizationMemberProjection, provides=IOrganizationMemberProjection)
    organization_member_service = provide(OrganizationMemberService)


class LocalMockInjectionsProvider(Provider):
    scope = Scope.APP

    email_service = provide(LoggerEmailService, provides=IEmailService)
