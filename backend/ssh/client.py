from typing import AsyncGenerator

import paramiko


class SSHClient:
    def __init__(self) -> None:
        self.channel: paramiko.Channel = None
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

    def connect(self, hostname: str, port: int, username: str, password: str) -> None:
        self.client.connect(hostname, port, username, password)

    def shell(self, cols: int = 80, rows: int = 24) -> None:
        self.channel = self.client.invoke_shell(width=cols, height=rows)

    def enter_key(self, key: str) -> bool:
        if self.channel.send_ready():
            self.channel.sendall(key.encode())
            return True
        return False

    async def fetch_console(self) -> AsyncGenerator[bytes, None]:
        while self.channel.recv_ready():
            yield self.channel.recv(1024)

    def close(self) -> None:
        self.client.close()
