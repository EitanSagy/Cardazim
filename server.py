import argparse
import socket
import sys

from consts import ENCODING


def run_server(ip: str, port: int) -> None:
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port))
            s.listen()
            conn, _ = s.accept()
            with conn:
                print(conn.recv(1024)[:-4].decode(ENCODING))


def get_args():
    parser = argparse.ArgumentParser(description="Open server listener.")
    parser.add_argument("ip", type=str, help="the servers ip")
    parser.add_argument("port", type=int, help="the servers port")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        run_server(args.ip, args.port)
        print("Done.")
    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
