from fastapi import Request

from api import expose


def init() -> None:
    expose.subscribe_get(callback_print)


def callback_print(endpoint: str, request: Request) -> None:
    print(f'Received GET for endpoint "{endpoint}" with request {request.json()}')
