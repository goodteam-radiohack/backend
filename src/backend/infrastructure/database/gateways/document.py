from dataclasses import dataclass

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.application.gateways.document import DocumentReader, DocumentWriter
from backend.domain.dto.document import CreateDocumentDTO
from backend.domain.entities.document import DocumentEntity
from backend.infrastructure.database.models.document import DocumentModel
from backend.infrastructure.database.models.user import UserModel
from backend.infrastructure.errors.gateways.document import DocumentNotFoundError

_OPTIONS = [
    joinedload(DocumentModel.created_by).joinedload(UserModel.helper),
    joinedload(DocumentModel.created_by).joinedload(UserModel.helping_to),
]


@dataclass
class DocumentGateway(DocumentReader, DocumentWriter):
    session: AsyncSession

    async def with_id(self, document_id: int) -> DocumentEntity:
        stmt = (
            select(DocumentModel)
            .where(DocumentModel.id == document_id)
            .options(*_OPTIONS)
        )

        try:
            result = (await self.session.scalars(stmt)).one()
        except NoResultFound as exc:
            raise DocumentNotFoundError from exc

        return result.to_entity()

    async def create(self, dto: CreateDocumentDTO) -> DocumentEntity:
        stmt = (
            insert(DocumentModel).values(**dto.model_dump()).returning(DocumentModel.id)
        )

        document_id = (await self.session.execute(stmt)).scalar_one()

        return await self.with_id(document_id)

    async def delete(self, document_id: int) -> None:
        stmt = delete(DocumentModel).where(DocumentModel.id == document_id)

        await self.session.execute(stmt)
