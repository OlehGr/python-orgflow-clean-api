import uuid

from sqlalchemy import Select, select

from app.core.models import FileModel
from app.infrastructure.database.builders.base import BaseSelectBuilder


SelectFileModel = Select[tuple[FileModel]]


class FileSelectBuilder(BaseSelectBuilder):
    @classmethod
    def build_get_by_id_select(cls, file_id: uuid.UUID) -> SelectFileModel:
        return select(FileModel).where(FileModel.id == file_id).limit(1)
