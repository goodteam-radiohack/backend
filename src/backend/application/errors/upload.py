from backend.application.errors import AppError


class InvalidFileExtensionError(AppError):
    code = 400
    message = "Invalid file extension"


class FileTooLargeError(AppError):
    code = 400
    message = "File too large"
