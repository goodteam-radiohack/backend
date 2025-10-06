from backend.application.errors import AppError


class UnauthenticatedError(AppError):
    code = 401
    message = "Unauthenticated"
