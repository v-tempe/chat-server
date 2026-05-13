from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.application.use_cases.auth import RegisterUserUseCase, LoginUserUseCase
from app.presentation.schemas import UserCreate, UserResponse, Token
from app.presentation.dependencies import get_user_repo, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, user_repo = Depends(get_user_repo)):
    use_case = RegisterUserUseCase(user_repo)
    try:
        user = await use_case.execute(username=user_data.username, password=user_data.password)
        return UserResponse(id=user.id, username=user.username, created_at=user.created_at)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repo = Depends(get_user_repo)):
    use_case = LoginUserUseCase(user_repo)
    try:
        user = await use_case.execute(username=form_data.username, password=form_data.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
