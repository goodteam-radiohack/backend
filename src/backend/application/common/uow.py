from typing import Protocol


class UnitOfWork(Protocol):
    async def commit(self) -> None: ...
    async def flush(self) -> None: ...
    async def rollback(self) -> None: ...

    async def __aenter__(self) -> None:
        return

    async def __aexit__(
        self, exc_type: object, exc_val: object, exc_tb: object
    ) -> None:
        if exc_val:
            await self.rollback()
