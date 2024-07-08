from fastapi import Request

from api import expose, serve


def init() -> None:
    expose.subscribe_get('/fulscreen', callback_print)


async def callback_print(_: str, __: Request) -> None:
    return serve.page('fullscreen')
