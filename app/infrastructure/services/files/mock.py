import aiohttp

from app.core.application.dto.file import FileUploadData, FileUploadResult, FileUploadStreamData
from app.core.application.interfaces.services.file import IFileStorage
from app.core.models import FileModel


class MockFileStorage(IFileStorage):
    PUBLIC_FILE_URL = "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"

    async def upload_file_stream(self, data: FileUploadStreamData) -> FileUploadResult:
        size = 0
        async for chunk in data.file_stream:
            size += len(chunk)

        return FileUploadResult(
            file_url=self.PUBLIC_FILE_URL,
            file_size=size,
        )

    async def upload_file_data(self, data: FileUploadData) -> FileUploadResult:
        return FileUploadResult(
            file_url=self.PUBLIC_FILE_URL,
            file_size=len(data.file_data),
        )

    async def get_uploaded_file(self, file: FileModel) -> bytes:
        url = file.url
        async with aiohttp.ClientSession() as session, session.get(url) as response:
            response.raise_for_status()
            return await response.read()
