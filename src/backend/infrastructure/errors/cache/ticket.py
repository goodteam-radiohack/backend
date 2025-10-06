from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID, uuid4

from redis.asyncio import Redis

from backend.domain.entities.ticket import TicketEntity
from backend.infrastructure.errors.gateways import ModelNotFoundError

EXPIRES_IN = timedelta(hours=3)


@dataclass
class DocumentTicketGateway:
    redis: Redis

    KEY = "document:tickets:{ticket}"

    async def with_uuid(self, ticket: UUID) -> TicketEntity:
        fields = list(TicketEntity.model_fields.keys())
        data = await self.redis.hmget(self.KEY.format(ticket=ticket), fields)  # type: ignore

        if all(item is None for item in data):
            raise ModelNotFoundError("Ticket not found")

        return TicketEntity(**dict(zip(fields, data, strict=True)))

    async def save(self, entity: TicketEntity) -> UUID:
        ticket = uuid4()

        await self.redis.hmset(self.KEY.format(ticket=ticket), entity.model_dump())
        await self.redis.expire(self.KEY.format(ticket=ticket), time=EXPIRES_IN)

        return ticket

    async def delete(self, ticket: UUID) -> None:
        await self.redis.delete(self.KEY.format(ticket=ticket))
