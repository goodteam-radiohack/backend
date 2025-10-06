from backend.application.errors import AppError


class SessionExpiredError(AppError):
    code = 401
    message = "Session expired"


class SessionNotFoundError(AppError):
    code = 404
    message = "Session not found"
