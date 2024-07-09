from fastapi import Request

from api import expose, serve


def init() -> None:
    expose.subscribe_get('/fullscreen', fullscreen)


async def fullscreen(_: str, __: Request) -> None:
    return await serve.page('fullscreen')
