from abc import abstractmethod
from typing import Protocol

from app.core.application.dto.file import FileUploadData, FileUploadResult, FileUploadStreamData, ImagerCompressResult
from app.core.models import FileModel


class IFileStorage(Protocol):
    @abstractmethod
    async def upload_file_stream(self, data: FileUploadStreamData) -> FileUploadResult: ...

    @abstractmethod
    async def upload_file_data(self, data: FileUploadData) -> FileUploadResult: ...

    @abstractmethod
    async def get_uploaded_file(self, file: FileModel) -> bytes: ...


class IImageCompressor(Protocol):
    @abstractmethod
    async def compress_image(self, *, image_data: bytes, image_name: str) -> ImagerCompressResult: ...


class IImageHasher(Protocol):
    @abstractmethod
    async def hash_image(self, image_data: bytes) -> str: ...
