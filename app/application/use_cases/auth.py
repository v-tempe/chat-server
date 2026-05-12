from passlib.context import CryptContext
from app.domain.entities import User, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH
from app.domain.repositories import IUserRepository
from app.domain.exceptions import UserNotFoundError, IncorrectPasswordError


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class RegisterUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    @staticmethod
    def is_valid_password(password: str) -> bool:
        return MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH

    async def execute(self, username: str, password: str) -> User:
        # check if user already exist
        existing_user = await self.user_repo.get_by_username(username)
        if existing_user:
            raise ValueError("User with this username already exists")

        # validate entity
        temp_user = User(id=None, username=username, password_hash="")
        if not temp_user.is_valid_username():
            raise ValueError("Username must be at least 3 characters long")
        if not self.is_valid_password(password):
            raise IncorrectPasswordError()

        # hash password
        password_hash = pwd_context.hash(password)

        # create entity
        new_user = User(
            id=None,  # ID will be assigned by DB
            username=username,
            password_hash=password_hash
        )

        # 5. save using repo interface
        return await self.user_repo.create(new_user)


class LoginUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, username: str, password: str) -> User:
        user = await self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundError("User not found")

        if not pwd_context.verify(password, user.password_hash):
            raise ValueError("Invalid password")

        return user
