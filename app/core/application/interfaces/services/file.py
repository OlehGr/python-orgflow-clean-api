from abc import abstractmethod
from typing import Protocol

from app.core.application.dto.file import FileUploadData, FileUploadResult, FileUploadStreamData


class IFileStorage(Protocol):
    @abstractmethod
    async def upload_file_stream(self, data: FileUploadStreamData) -> FileUploadResult: ...

    @abstractmethod
    async def upload_file_data(self, data: FileUploadData) -> FileUploadResult: ...
