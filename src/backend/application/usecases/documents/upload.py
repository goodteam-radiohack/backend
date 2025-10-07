import asyncio
import hashlib
import logging
from dataclasses import dataclass
from datetime import timedelta
from functools import partial

import magic

from backend.application.common.id_provider import IdProvider
from backend.application.common.interactor import Interactor
from backend.application.common.uow import UnitOfWork
from backend.application.contracts.documents.document import DocumentResponse
from backend.application.contracts.documents.upload import UploadDocumentRequest
from backend.application.errors.access import UnauthorizedError
from backend.application.errors.upload import (
    FileTooLargeError,
    InvalidFileExtensionError,
)
from backend.application.gateways.document import DocumentWriter
from backend.domain.dto.document import CreateDocumentDTO
from backend.domain.services.s3 import S3Service
from backend.infrastructure.errors.cache.ticket import DocumentTicketGateway

m = magic.Magic(mime=True)

EXPIRES_IN = timedelta(hours=3)
MAX_SIZE = 50 * 1024 * 1024

MIME_TO_EXT = {
    "application/pdf": ".pdf",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/vnd.ms-powerpoint": ".ppt",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
    "application/vnd.openxmlformats-officedocument.presentationml.slideshow": ".ppsx",
    "application/vnd.oasis.opendocument.text": ".odt",
    "application/vnd.oasis.opendocument.spreadsheet": ".ods",
    "application/vnd.oasis.opendocument.presentation": ".odp",
    "application/rtf": ".rtf",
    "text/plain": ".txt",
    "text/csv": ".csv",
    "text/tab-separated-values": ".tsv",
    "text/css": ".css",
    "text/markdown": ".md",
    "application/xml": ".xml",
    "application/x-yaml": ".yaml",
    "application/sql": ".sql",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
    "image/avif": ".avif",
    "image/svg+xml": ".svg",
    "image/tiff": ".tif",
    "image/bmp": ".bmp",
    "image/x-icon": ".ico",
    "audio/mpeg": ".mp3",
    "audio/wav": ".wav",
    "audio/ogg": ".ogg",
    "audio/flac": ".flac",
    "audio/aac": ".aac",
    "audio/webm": ".weba",
    "audio/mp4": ".m4a",
    "video/mp4": ".mp4",
    "video/quicktime": ".mov",
    "video/x-msvideo": ".avi",
    "video/x-matroska": ".mkv",
    "video/webm": ".webm",
    "video/ogg": ".ogv",
    "application/zip": ".zip",
    "application/x-7z-compressed": ".7z",
    "application/x-rar-compressed": ".rar",
    "application/gzip": ".gz",
    "application/x-bzip2": ".bz2",
    "application/x-tar": ".tar",
    "application/java-archive": ".jar",
    "application/x-iso9660-image": ".iso",
    "application/vnd.android.package-archive": ".apk",
    "application/x-apple-diskimage": ".dmg",
    "font/ttf": ".ttf",
    "font/otf": ".otf",
    "font/woff": ".woff",
    "font/woff2": ".woff2",
}

logger = logging.getLogger(__name__)


@dataclass
class UploadDocumentUseCase(Interactor[UploadDocumentRequest, DocumentResponse]):
    id_provider: IdProvider

    s3_service: S3Service
    ticket: DocumentTicketGateway

    document_writer: DocumentWriter

    uow: UnitOfWork

    async def __call__(self, data: UploadDocumentRequest) -> DocumentResponse:
        # TODO: move this logic into worker?

        user = await self.id_provider.get_user()
        upload_state = await self.ticket.with_uuid(data.ticket)

        if upload_state.user_id not in (user.id, user.helping_to_id):
            raise UnauthorizedError

        await self.ticket.delete(data.ticket)

        size = len(data.body)

        if size > MAX_SIZE:
            raise FileTooLargeError

        logger.info("Detecting mime-type of uploaded file...")

        loop = asyncio.get_running_loop()
        mime = await loop.run_in_executor(None, partial(m.from_buffer, data.body))

        if mime is None or mime not in MIME_TO_EXT:
            raise InvalidFileExtensionError

        logger.info("Calculating checksum...")

        key = f"documents/{data.ticket}{MIME_TO_EXT[mime]}"
        checksum = hashlib.sha256(data.body).hexdigest()

        logger.info("Uploading to S3")

        await self.s3_service.upload(key, data.body)

        logger.info("Committing into DB")

        async with self.uow:
            document = await self.document_writer.create(
                CreateDocumentDTO(
                    catalog_id=upload_state.catalog_id,
                    name=upload_state.name,
                    mime=mime,
                    size=size,
                    storage_key=key,
                    checksum=checksum,
                    created_by_id=upload_state.user_id,
                    visibility=upload_state.visibility,
                )
            )

            await self.uow.commit()

        url = await self.s3_service.get_url(key, EXPIRES_IN)
        return DocumentResponse.from_entity(document, url)
