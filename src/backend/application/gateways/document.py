from typing import Protocol

from backend.domain.dto.document import CreateDocumentDTO
from backend.domain.entities.document import DocumentEntity


class DocumentReader(Protocol):
    async def with_id(self, document_id: int) -> DocumentEntity: ...


class DocumentWriter(Protocol):
    async def create(self, dto: CreateDocumentDTO) -> DocumentEntity: ...
    async def delete(self, document_id: int) -> None: ...
