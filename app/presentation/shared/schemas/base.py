import msgspec


class MessageResultDto(msgspec.Struct, frozen=True):
    message: str
