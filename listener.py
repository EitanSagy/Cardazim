import socket
from connection import Connection


class Listener:
    def __init__(self, host: str, port: int, backlog: int = 1000):
        self.host = host
        self.port = port
        self.backlog = backlog

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))

    def __repr__(self):
        return f"Listener(port={self.port}, host={self.host}, backlog={self.backlog})"

    def start(self):
        self.socket.listen()

    def stop(self):
        self.socket.__exit__()

    def accept(self):
        conn, _ = self.socket.accept()
        return Connection(conn)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *unused):
        self.stop()
        return False

    @classmethod
    def listen(cls, host: str, port: int, backlog: int | None = None):
        return Listener(host, port, backlog)
