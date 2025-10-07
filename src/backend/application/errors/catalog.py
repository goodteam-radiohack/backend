from backend.application.errors import AppError


class CatalogNotEmptyError(AppError):
    code = 400
    message = "Catalog not empty"
