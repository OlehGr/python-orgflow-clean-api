from typing import TYPE_CHECKING, TypeVar

from sqlalchemy import Select, func, select

from app.core.models import BaseModel


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

TModel = TypeVar("TModel", bound=BaseModel)


class DataLoadHelper:
    @classmethod
    async def load_select_count(cls, query: Select, session: AsyncSession) -> int:
        query_count = select(func.count()).select_from(query.order_by(None).distinct().alias())
        return int(await session.scalar(query_count) or 0)

    @classmethod
    async def load_models_list(cls, query: Select[tuple[TModel]], session: AsyncSession) -> list[TModel]:
        query_result = await session.scalars(query)
        return list(query_result.all())
