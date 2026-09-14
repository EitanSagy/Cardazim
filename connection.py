import socket
from threading import Thread


class Connection(Thread):
    def __init__(self, connection: socket.socket):
        self.conn = connection

    def __repr__(self):
        return self.conn.__repr__()

    def send_message(self, message: bytes):
        size_bytes = len(message).to_bytes(4, "little")
        to_send = message + size_bytes

        self.conn.sendall(to_send)

    def receive_message(self) -> bytes:
        return self.conn.recv(1024)[:-4]  # remove the size argument

    def close(self):
        self.conn.__exit__()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        self.close()
        return False

    @classmethod
    def connect(cls, host: str, port: int):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return Connection(s)
