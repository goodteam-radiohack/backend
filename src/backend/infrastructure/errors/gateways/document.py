from backend.infrastructure.errors.gateways import ModelNotFoundError


class DocumentNotFoundError(ModelNotFoundError):
    message = "Document not found"
