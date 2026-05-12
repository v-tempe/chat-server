from dataclasses import dataclass, field
from datetime import datetime


MAX_MESSAGE_LENGTH = 2000


@dataclass
class User:
    id: int | None
    username: str
    password_hash: str
    created_at: datetime = field(default_factory=datetime.now)

    # business-rule: check password complexity
    def is_valid_username(self) -> bool:
        return len(self.username) >= 3


@dataclass
class Chat:
    id: int | None
    name: str
    is_group: bool = False
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Message:
    id: int | None
    chat_id: int
    sender_id: int
    content: str
    created_at: datetime = field(default_factory=datetime.now)

    # business-rule: message cannot be empty
    def is_content_valid(self) -> bool:
        return bool(self.content.strip())

    # business-rule: constraint of message length
    def is_length_valid(self, max_length: int = MAX_MESSAGE_LENGTH) -> bool:
        return len(self.content) <= max_length
