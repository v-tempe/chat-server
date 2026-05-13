from typing import Optional, List
from app.domain.entities import User, Chat, Message
from app.domain.repositories import IUserRepository, IChatRepository, IMessageRepository
from app.infrastructure.models import DBUser, DBChat, DBMessage
from app.infrastructure.mappers import UserMapper, ChatMapper, MessageMapper


class UserRepository(IUserRepository):
    async def create(self, user: User) -> User:
        db_user = UserMapper.to_db(user)
        await db_user.save()
        return UserMapper.to_entity(db_user)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        db_user = await DBUser.get_or_none(id=user_id)
        return UserMapper.to_entity(db_user) if db_user else None

    async def get_by_username(self, username: str) -> Optional[User]:
        db_user = await DBUser.get_or_none(username=username)
        return UserMapper.to_entity(db_user) if db_user else None


class ChatRepository(IChatRepository):
    async def create(self, chat: Chat) -> Chat:
        db_chat = DBChat(name=chat.name, is_group=chat.is_group)
        await db_chat.save()
        return ChatMapper.to_entity(db_chat)

    async def get_by_id(self, chat_id: int) -> Optional[Chat]:
        db_chat = await DBChat.get_or_none(id=chat_id)
        return ChatMapper.to_entity(db_chat) if db_chat else None


class MessageRepository(IMessageRepository):
    async def create(self, message: Message) -> Message:
        db_msg = MessageMapper.to_db(message)
        await db_msg.save()
        return MessageMapper.to_entity(db_msg)

    async def get_history(self, chat_id: int, limit: int = 50) -> List[Message]:
        db_msgs = await DBMessage.filter(chat_id=chat_id).order_by("-created_at").limit(limit)
        db_msgs.reverse()
        return [MessageMapper.to_entity(msg) for msg in db_msgs]

    async def get_last_message(self, chat_id: int) -> Optional[Message]:
        db_msg = await DBMessage.filter(chat_id=chat_id).order_by("-created_at").first()
        return MessageMapper.to_entity(db_msg) if db_msg else None
