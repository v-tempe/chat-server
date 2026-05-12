from app.domain.entities import Message
from app.domain.repositories import IMessageRepository, IChatRepository
from app.domain.exceptions import EmptyMessageError, MessageTooLongError, ChatNotFoundError


class SendMessageUseCase:
    def __init__(self, message_repo: IMessageRepository, chat_repo: IChatRepository):
        self.message_repo = message_repo
        self.chat_repo = chat_repo

    async def execute(self, chat_id: int, sender_id: int, content: str) -> Message:
        # 1. check if chat already exist
        chat = await self.chat_repo.get_by_id(chat_id)
        if not chat:
            raise ChatNotFoundError(f"Chat with id {chat_id} not found")

        # 2. create message entity
        message = Message(
            id=None,
            chat_id=chat_id,
            sender_id=sender_id,
            content=content
        )

        # 3. apply business-rules
        if not message.is_content_valid():
            raise EmptyMessageError("Message content cannot be empty")

        if not message.is_length_valid():
            raise MessageTooLongError("Message is too long")

        # 4. save using repo interface
        return await self.message_repo.create(message)
