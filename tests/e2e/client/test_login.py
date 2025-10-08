import aiobcrypt
import pytest
from dishka import AsyncContainer
from fastapi.testclient import TestClient

from backend.application.common.uow import UnitOfWork
from backend.application.gateways.user import UserWriter
from backend.domain.dto.user import CreateUserDTO
from backend.domain.enum.user import UserRole


@pytest.mark.asyncio
async def test_login(client: TestClient, container: AsyncContainer):
    async with container() as req:
        user_writer = await req.get(UserWriter)
        uow = await req.get(UnitOfWork)

        await user_writer.create(
            CreateUserDTO(
                username="test",
                hashed_password=(await aiobcrypt.hashpw_with_salt(b"123123")).decode(),
                role=UserRole.ADMIN,
                helping_for_id=None,
                name=None,
                avatar_url=None,
            )
        )
        await uow.commit()

    response = client.post(
        "/auth/signin", json={"username": "test", "password": "123123"}
    )

    assert response.status_code == 200
    assert response.json().get("token")
