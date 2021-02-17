import json
from dataclasses import dataclass, asdict
from enum import Enum, auto

from aio_pika import Message as AioPikaMessage


class MessageType(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    create_post = auto()


@dataclass
class Message:
    def to_payload(self) -> AioPikaMessage:
        data = asdict(self)
        data["type"] = TYPE_BY_MESSAGE[self.__class__]
        return AioPikaMessage(json.dumps(data).encode())


@dataclass
class CreatePostMessage(Message):
    user_id: int
    text: str


MESSAGE_MAP = {MessageType.create_post: CreatePostMessage}
TYPE_BY_MESSAGE = {cls: type for type, cls in MESSAGE_MAP.items()}
