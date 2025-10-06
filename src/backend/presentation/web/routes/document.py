from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, Request

from backend.application.contracts.documents.create import (
    CreateDocumentRequest,
    CreateDocumentResponse,
)
from backend.application.contracts.documents.delete import (
    DeleteDocumentRequest,
    DeleteDocumentResponse,
)
from backend.application.contracts.documents.document import DocumentResponse
from backend.application.contracts.documents.get import GetDocumentRequest
from backend.application.contracts.documents.upload import UploadDocumentRequest
from backend.application.usecases.documents.create import CreateDocumentUseCase
from backend.application.usecases.documents.delete import DeleteDocumentUseCase
from backend.application.usecases.documents.get import GetDocumentUseCase
from backend.application.usecases.documents.upload import UploadDocumentUseCase
from backend.presentation.web.dependencies.authorization import authorization_header

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    route_class=DishkaRoute,
    dependencies=[Depends(authorization_header)],
)


@router.get("/{document_id}")
async def get_document_by_id(
    document_id: int, interactor: FromDishka[GetDocumentUseCase]
) -> DocumentResponse:
    return await interactor(GetDocumentRequest(id=document_id))


@router.delete("/{document_id}")
async def delete_document(
    document_id: int, interactor: FromDishka[DeleteDocumentUseCase]
) -> DeleteDocumentResponse:
    return await interactor(DeleteDocumentRequest(id=document_id))


@router.post("")
async def create_document(
    req: CreateDocumentRequest, interactor: FromDishka[CreateDocumentUseCase]
) -> CreateDocumentResponse:
    return await interactor(req)


@router.post("/{ticket_uuid}/upload")
async def upload_document(
    ticket_uuid: UUID, request: Request, interactor: FromDishka[UploadDocumentUseCase]
) -> DocumentResponse:
    body = await request.body()

    return await interactor(UploadDocumentRequest(ticket=ticket_uuid, body=body))
