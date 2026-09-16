import argparse
import sys

from connection import Connection
from consts import ENCODING

from card import Card

###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip: str, server_port: int, data: bytes) -> None:
    """
    Send data to server in address (server_ip, servr_port).
    """
    with Connection.connect(server_ip, server_port) as conn:
        conn.send_message(data)


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description="Send card to server.")

    parser.add_argument("server_ip", type=str, help="the servers ip")
    parser.add_argument("server_port", type=int, help="the servers port")

    parser.add_argument("name", type=str, help="the name of the card")
    parser.add_argument("creator", type=str, help="the name of the creator of the card")
    parser.add_argument("riddle", type=str, help="the riddle")
    parser.add_argument("solution", type=str, help="the solution")
    parser.add_argument("path", type=str, help="path to the secret image")

    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()

    data = (
        Card.create_from_path(
            args.name, args.creator, args.riddle, args.solution, args.path
        )
        .encrypt()
        .serialize()
    )

    try:
        send_data(args.server_ip, args.server_port, data)
        print("Done.")

    except Exception as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
