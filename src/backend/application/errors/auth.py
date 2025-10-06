from backend.application.errors import AppError


class CredentialsInvalidError(AppError):
    code = 401
    message = "Credentials invalid"
