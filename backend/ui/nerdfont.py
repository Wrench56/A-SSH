from fastapi import Request
from fastapi.responses import FileResponse

from api import expose


def init() -> None:
    expose.subscribe_get('/nerdfont', fullscreen)


async def fullscreen(_: str, __: Request) -> FileResponse:
    return FileResponse('plugins/plugins/A_SSH/fonts/FiraCodeNerdFont.ttf')
