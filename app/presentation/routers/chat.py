from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.application.use_cases.message import SendMessageUseCase
from app.application.use_cases.chat import CreateChatUseCase # Импорт нового Use Case
from app.domain.entities import User
from app.presentation.schemas import MessageCreate, MessageResponse, ChatCreate, ChatResponse
from app.presentation.dependencies import get_current_user, get_chat_repo, get_message_repo
from app.infrastructure.repositories import ChatRepository, MessageRepository


router = APIRouter(prefix="/api/chats", tags=["Chats"])


@router.post("/", response_model=ChatResponse)
async def create_chat(chat_data: ChatCreate, current_user: User = Depends(get_current_user), chat_repo: ChatRepository = Depends(get_chat_repo)):
    use_case = CreateChatUseCase(chat_repo)
    try:
        chat = await use_case.execute(name=chat_data.name, is_group=chat_data.is_group, creator=current_user)
        return ChatResponse(id=chat.id, name=chat.name, is_group=chat.is_group, created_at=chat.created_at)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_messages(chat_id: int, current_user: User = Depends(get_current_user), msg_repo: MessageRepository = Depends(get_message_repo)):
    # Проверка прав доступа на чат должна быть в Use Case
    messages = await msg_repo.get_history(chat_id=chat_id)
    return [MessageResponse(**msg.__dict__) for msg in messages]


@router.post("/{chat_id}/messages", response_model=MessageResponse)
async def send_message_rest(chat_id: int, msg_data: MessageCreate, current_user: User = Depends(get_current_user), msg_repo: MessageRepository = Depends(get_message_repo), chat_repo: ChatRepository = Depends(get_chat_repo)):
    use_case = SendMessageUseCase(msg_repo, chat_repo)
    try:
        message = await use_case.execute(chat_id=chat_id, sender_id=current_user.id, content=msg_data.content)
        return MessageResponse(**message.__dict__)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
