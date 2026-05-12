from abc import ABC, abstractmethod
from .entities import User, Chat, Message


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        pass


class IChatRepository(ABC):
    @abstractmethod
    async def create(self, chat: Chat) -> Chat:
        pass

    @abstractmethod
    async def get_by_id(self, chat_id: int) -> Chat | None:
        pass


class IMessageRepository(ABC):
    @abstractmethod
    async def create(self, message: Message) -> Message:
        pass

    @abstractmethod
    async def get_history(self, chat_id: int, limit: int = 50) -> list[Message]:
        pass

    @abstractmethod
    async def get_last_message(self, chat_id: int) -> Message | None:
        pass
