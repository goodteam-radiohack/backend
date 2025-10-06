from typing import Annotated

from fastapi import Header


async def authorization_header(authorization: Annotated[str, Header()]) -> None:
    return
