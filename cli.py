import cmd
import subprocess
import argparse
from getpass import getpass
from ssh import Client

BANNER = """
Welcome to pyssh. For more info type help or ?
"""


class Cli(cmd.Cmd):
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.client = None

    def close(self):
        """closes the active ssh connection"""
        if self.client is not None:
            self.client.disconnect()
            self.client = None

    def cmdloop(self, intro=BANNER):
        try:
            super().cmdloop(intro)
        except KeyboardInterrupt:
            self.close()
            return self.do_exit("exit")

    def do_clear(self, _):
        "clears the screen"
        subprocess.run("cls", shell=True)

    def do_login(self, line):
        "Log in to a remote host using ssh"
        while True:
            try:
                parser = argparse.ArgumentParser()
                parser.add_argument(
                    "host",
                    help="hostname or ip address of the remote machine to login into",
                )
                args = parser.parse_args(line.split())
                username = input("Username: ").strip()
                password = getpass(prompt="Password: ").strip()
                self.client = Client(
                    host=args.host, username=username, password=password
                )
                break
            except Exception as e:
                print(e)

    def do_EOF(self, _):
        "Exit the shell"
        self.close()
        return True

    def do_shell(self, _):
        "Interactive remote ssh"
        if not self.client:
            print("login to a remote host first. For more info please type help or ?")
        else:
            try:
                self.client.invoke_shell()
            except OSError as e:
                if e == "Socket is closed":
                    pass
                else:
                    print(e)

    def do_quit(self, _):
        "Exit the shell"
        self.close()
        return True

    def do_exit(self, _):
        "Exit the shell"
        self.close()
        return True
