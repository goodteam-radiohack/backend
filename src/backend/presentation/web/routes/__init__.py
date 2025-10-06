from fastapi import FastAPI

from . import auth


def setup_routes(app: FastAPI) -> None:
    app.include_router(auth.router)
