from backend.application.errors import AppError


class ModelNotFoundError(AppError):
    code = 404
    message = "Model not found"
