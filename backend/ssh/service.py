from fastapi import WebSocket, WebSocketDisconnect
import logging

from api import expose

from plugins.plugins.A_SSH.backend.ssh import client


def init() -> None:
    expose.subscribe_websocket('/ssh', service)


async def service(_: str, websocket: WebSocket) -> None:
    ssh_client = client.SSHClientWrapper()
    await websocket.accept()
    await websocket.send_text('Welcome to A-SSH!\nPlease provide host and credentials\n>>>')
    # Login
    host, port, username, password = await websocket.receive_text().split(',')
    ssh_client.connect(host, port, username, password)
    while True:
        try:
            data = await websocket.receive_text()
            result = ssh_client.run_command(data)
            await websocket.send_text(result.decode('utf-8'))
        except WebSocketDisconnect:
            ssh_client.close()
            logging.info('WebSocket disconnected')
            break
