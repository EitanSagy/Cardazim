import socket


class Connection:
    def __init__(self, connection: socket.socket):
        self.conn = connection

    def __repr__(self):
        return f"Connection(ip={self.conn.getpeername()[0]},port={self.conn.getpeername()[1]})"

    def send_message(self, message: bytes):
        size_bytes = len(message).to_bytes(4, "little")
        to_send = size_bytes + message

        self.conn.sendall(to_send)

    def receive_message(self) -> bytes:
        b = self.conn.recv(4)
        message_size = int.from_bytes(b, "little")
        return self.conn.recv(message_size)

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
