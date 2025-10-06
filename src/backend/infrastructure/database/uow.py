from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.common.uow import UnitOfWork


@dataclass
class UnitOfWorkImpl(UnitOfWork):
    session: AsyncSession

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def flush(self) -> None:
        await self.session.flush()
