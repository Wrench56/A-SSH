import asyncio
from fastapi import WebSocket, WebSocketDisconnect
import logging

from api import expose

from plugins.plugins.A_SSH.backend.ssh import client, login


TIMEOUT = 1/30


def init() -> None:
    expose.subscribe_websocket('/ssh', service)


async def service(_: str, websocket: WebSocket) -> None:
    ssh_client = client.SSHClient()
    await websocket.accept()
    await websocket.send_text('Welcome to A-SSH!\n')
    data = await websocket.receive_json()
    host, port, un, pw = await login.parse(data)
    ssh_client.connect(host, port, un, pw)

    # Initial terminal size
    dims = await websocket.receive_json()
    ssh_client.shell(int(dims.get('cols')), int(dims.get('rows')))

    while True:
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=TIMEOUT)
            type_ = data.get('type')
            if type_ == 'KEY':
                key = data.get('key')
                ssh_client.enter_key(key)
            elif type_ == 'RESIZE':
                # TODO: Support resize
                pass

            await _send_data(ssh_client, websocket)
        except asyncio.TimeoutError:
            # No input from frontend
            await _send_data(ssh_client, websocket)
        except WebSocketDisconnect:
            ssh_client.close()
            logging.info('WebSocket disconnected')
            break


async def _send_data(sshc: client.SSHClient, ws: WebSocket) -> None:
    async for data in sshc.fetch_console():
        print(data)
        await ws.send_text(data.decode('utf-8'))
