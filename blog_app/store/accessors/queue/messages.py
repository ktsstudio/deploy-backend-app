import json
from dataclasses import dataclass, asdict
from enum import Enum, auto
from typing import ClassVar

from aio_pika import Message as AioPikaMessage


class MessageType(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    create_post = auto()


@dataclass
class Message:
    type: ClassVar[MessageType]

    def to_payload(self) -> AioPikaMessage:
        data = asdict(self)
        data["type"] = self.type
        return AioPikaMessage(json.dumps(data).encode())


@dataclass
class CreatePostMessage(Message):
    type = MessageType.create_post
    user_id: int
    text: str


MESSAGE_MAP = {MessageType.create_post: CreatePostMessage}
