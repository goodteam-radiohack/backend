from fastapi import FastAPI

from . import auth, events, users



def setup_routes(app: FastAPI) -> None:
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(events.router)
