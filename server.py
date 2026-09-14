import argparse
import socket
import sys

from consts import ENCODING
from listener import Listener


def run_server(ip: str, port: int) -> None:
    """
    Run a server on <ip>:<port>
    Every connection accepted gets its own thread for handling.
    """
    connections = []
    with Listener.listen(ip, port) as listener:
        while True:
            connections.append(listener.accept())
            print(connections[-1].receive_message())


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
