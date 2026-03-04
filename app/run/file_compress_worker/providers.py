from dishka import Provider, Scope, provide

from app.core.application.interfaces.repository.file import IFileRepository
from app.core.application.interfaces.services.file import IFileStorage, IImageCompressor, IImageHasher
from app.core.application.services.file import FileOptimizeService
from app.infrastructure.database.repository.file import FileRepository
from app.infrastructure.services.files.s3 import S3FileStorage
from app.infrastructure.services.images.compress.pillow import PillowImageCompressor
from app.infrastructure.services.images.hash.blurhash import BlurHashImageHasher


class AppInjectionsProvider(Provider):
    scope = Scope.APP

    file_repository = provide(FileRepository, provides=IFileRepository)
    file_storage = provide(S3FileStorage, provides=IFileStorage)
    image_compressor = provide(PillowImageCompressor, provides=IImageCompressor)
    image_hasher = provide(BlurHashImageHasher, provides=IImageHasher)
    file_optimize_service = provide(FileOptimizeService)
