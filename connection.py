import socket


class Connection:
    def __init__(self, connection: socket.socket):
        self.conn = connection

    def __repr__(self):
        return self.conn.__repr__()

    def send_message(self, message: bytes):
        size_bytes = len(message).to_bytes(8, "little")
        to_send = size_bytes + message

        self.conn.sendall(to_send)

    def receive_message(self) -> bytes:
        b = self.conn.recv(4)
        print(b)
        message_size = int.from_bytes(b, "little")
        print(message_size)
        return self.conn.recv(message_size + 4)[4:]

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
