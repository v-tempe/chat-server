from app.domain.entities import Chat, User
from app.domain.repositories import IChatRepository


class CreateChatUseCase:
    def __init__(self, chat_repo: IChatRepository):
        self.chat_repo = chat_repo

    async def execute(self, name: str, is_group: bool, creator: User) -> Chat:
        if is_group and not name:
            raise ValueError("Group chat must have a name")

        chat_name = name if is_group else None

        new_chat = Chat(
            id=None,
            name=chat_name,
            is_group=is_group
        )

        saved_chat = await self.chat_repo.create(new_chat)

        return saved_chat
