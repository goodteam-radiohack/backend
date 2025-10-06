from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.application.errors import AppError


async def handle_error(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AppError):
        return JSONResponse(
            {"success": False, "message": exc.message}, status_code=exc.code
        )

    return JSONResponse({"success": False, "message": "Internal Server Error"})


def setup_errors_handler(app: FastAPI) -> None:
    app.add_exception_handler(Exception, handle_error)
