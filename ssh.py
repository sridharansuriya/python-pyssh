import paramiko
import interactive


class Client:
    def __init__(self, host: str, username: str, password: str):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        port = 22
        if ":" in host:
            host, port = host.split(":")
            port = int(port)
        self.client.connect(
            hostname=host, port=port, username=username, password=password
        )

    def disconnect(self):
        self.client.close()

    def invoke_shell(self):
        # Fail safe in case the upcoming attempt blows up
        channel = self.client.invoke_shell()
        channel.send("stty -echo\n")
        interactive.interactive_shell(channel)
