from fastapi import FastAPI

from . import auth, catalogs, document, events, users


def setup_routes(app: FastAPI) -> None:
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(events.router)
    app.include_router(catalogs.router)
    app.include_router(document.router)
