from typing import TypeVar

from sqlalchemy import Select, func, select

from app.core.models import BaseModel


TModel = TypeVar("TModel", bound=BaseModel)


class BaseSelectBuilder:
    @staticmethod
    def with_pagination(
        query: Select[tuple[TModel]],
        *,
        page: int,
        limit: int | None,
    ) -> Select[tuple[TModel]]:
        if limit is None:
            return query

        return query.offset((page - 1) * limit).limit(limit)

    @staticmethod
    def with_paged_limit(
        query: Select[tuple[TModel]],
        *,
        page: int,
        limit: int | None,
    ) -> Select[tuple[TModel]]:
        if limit is None:
            return query

        query_limit = limit + 1

        return query.offset((page - 1) * query_limit).limit(query_limit)

    @staticmethod
    def to_count_query(query: Select) -> Select[tuple[int]]:
        return select(func.count()).select_from(query.order_by(None).alias())
