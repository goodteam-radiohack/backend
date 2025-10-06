from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from backend.application.contracts.documents.document import DocumentResponse
from backend.application.contracts.documents.get import GetDocumentRequest
from backend.application.usecases.documents.get import GetDocumentUseCase

router = APIRouter(prefix="/documents", tags=["Documents"], route_class=DishkaRoute)


@router.get("/{document_id}")
async def get_document_by_id(
    document_id: int, interactor: FromDishka[GetDocumentUseCase]
) -> DocumentResponse:
    return await interactor(GetDocumentRequest(id=document_id))
