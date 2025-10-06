from backend.application.errors import AppError


class UnauthorizedError(AppError):
    code = 403
    message = "Unauthorized"
