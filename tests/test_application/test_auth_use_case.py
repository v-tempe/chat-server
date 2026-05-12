import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.auth import RegisterUserUseCase
from app.domain.entities import User


@pytest.fixture
def mock_user_repo():
    return AsyncMock()


@pytest.mark.asyncio
async def test_register_user_success(mock_user_repo):
    # user does not exist
    mock_user_repo.get_by_username = AsyncMock(return_value=None)

    # imitation of saving
    saved_user = User(id=1, username="testuser", password_hash="$hashed$")
    mock_user_repo.create = AsyncMock(return_value=saved_user)

    use_case = RegisterUserUseCase(mock_user_repo)
    result = await use_case.execute(username="testuser", password="securepassword123")

    assert result.username == "testuser"
    assert result.id == 1
    # check password was hashed
    assert result.password_hash != "securepassword123"
    assert "$" in result.password_hash  # bcrypt hash begins with $


@pytest.mark.asyncio
async def test_register_user_already_exists(mock_user_repo):
    existing_user = User(id=1, username="testuser", password_hash="...")
    mock_user_repo.get_by_username = AsyncMock(return_value=existing_user)

    use_case = RegisterUserUseCase(mock_user_repo)

    with pytest.raises(ValueError, match="already exists"):
        await use_case.execute(username="testuser", password="pass")