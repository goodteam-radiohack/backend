from backend.infrastructure.errors.gateways import ModelNotFoundError


class CatalogNotFoundError(ModelNotFoundError):
    message = "Catalog not found"
