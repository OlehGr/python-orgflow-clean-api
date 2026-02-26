from app.core.exceptions.base import BasicMessageError


class EntityNotFoundError(BasicMessageError):
    def __init__(self, entity_name: str) -> None:
        super().__init__(f"{entity_name} не найден", 404)
