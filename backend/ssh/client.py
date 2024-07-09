import paramiko


class SSHClient:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

    def connect(self, hostname: str, port: int, username: str, password: str):
        self.client.connect(hostname, port, username, password)

    def run_command(self, command: str) -> bytes:
        _, stdout, _ = self.client.exec_command(command)
        return stdout.read()

    def close(self):
        self.client.close()
