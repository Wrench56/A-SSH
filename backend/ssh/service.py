from fastapi import WebSocket, WebSocketDisconnect
import logging

from api import expose

from plugins.plugins.A_SSH.backend.ssh import client
from plugins.plugins.A_SSH.backend.ssh import login


def init() -> None:
    expose.subscribe_websocket('/ssh', service)


async def service(_: str, websocket: WebSocket) -> None:
    ssh_client = client.SSHClient()
    await websocket.accept()
    await websocket.send_text('Welcome to A-SSH!\n')
    data = await websocket.receive_json()
    host, port, un, pw = await login.parse(data)
    ssh_client.connect(host, port, un, pw)
    while True:
        try:
            cmd = await websocket.receive_text()
            result = ssh_client.run_command(cmd)
            await websocket.send_text(result.decode('utf-8'))
        except WebSocketDisconnect:
            ssh_client.close()
            logging.info('WebSocket disconnected')
            break
