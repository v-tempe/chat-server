from app.domain.entities import User, Chat, Message
from app.infrastructure.models import DBUser, DBChat, DBMessage


class UserMapper:
    @staticmethod
    def to_entity(db_user: DBUser) -> User:
        return User(
            id=db_user.id,
            username=db_user.username,
            password_hash=db_user.password_hash,
            created_at=db_user.created_at
        )

    @staticmethod
    def to_db(user: User) -> DBUser:
        db_user = DBUser(
            id=user.id or None, 
            username=user.username,
            password_hash=user.password_hash,
            created_at=user.created_at
        )
        if user.id:
            db_user._saved_in_db = True
        return db_user

class ChatMapper:
    @staticmethod
    def to_entity(db_chat: DBChat) -> Chat:
        return Chat(
            id=db_chat.id,
            name=db_chat.name or "Private Chat",
            is_group=db_chat.is_group,
            created_at=db_chat.created_at
        )

class MessageMapper:
    @staticmethod
    def to_entity(db_msg: DBMessage) -> Message:
        return Message(
            id=db_msg.id,
            chat_id=db_msg.chat_id,
            sender_id=db_msg.sender_id,
            content=db_msg.content,
            created_at=db_msg.created_at
        )

    @staticmethod
    def to_db(message: Message) -> DBMessage:
        return DBMessage(
            id=message.id,
            chat_id=message.chat_id,
            sender_id=message.sender_id,
            content=message.content,
            created_at=message.created_at
        )
