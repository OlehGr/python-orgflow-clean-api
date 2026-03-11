from math import ceil
from typing import NotRequired, TypedDict, TypeVar

import msgspec


ItemDto = TypeVar("ItemDto")


class Paginated[ItemDto](msgspec.Struct, frozen=True):
    data: list[ItemDto]
    next: int | None
    prev: int | None
    pages: int

    @classmethod
    def to_paginated(cls, data: list[ItemDto], *, page: int, limit: int | None, count: int) -> "Paginated[ItemDto]":
        if limit is None:
            return cls(
                next=None,
                prev=None,
                data=data,
                pages=1,
            )

        page = max(page, 1)
        total_pages = ceil(count / limit)
        next_page = page + 1 if count > page * limit else None
        prev_page = page - 1 if page > 1 else None

        return cls(
            next=next_page,
            prev=prev_page,
            data=data,
            pages=total_pages,
        )

    @classmethod
    def from_paginated(cls, data: list[ItemDto], paginated: "Paginated") -> "Paginated[ItemDto]":
        return cls(
            next=paginated.next,
            prev=paginated.prev,
            data=data,
            pages=paginated.pages,
        )


class Paged[ItemDto](msgspec.Struct, frozen=True):
    data: list[ItemDto]
    next: int | None
    prev: int | None

    @classmethod
    def to_paged(cls, over_data: list[ItemDto], *, page: int, limit: int | None) -> "Paged[ItemDto]":
        if limit is None:
            return cls(
                next=None,
                prev=None,
                data=over_data,
            )

        page = max(page, 1)
        next_page = page + 1 if len(over_data) > limit else None
        prev_page = page - 1 if page > 1 else None

        return cls(
            next=next_page,
            prev=prev_page,
            data=over_data[:-1] if next_page else over_data,
        )


class LimitationGetParams(TypedDict):
    page: NotRequired[int]
    limit: NotRequired[int]
