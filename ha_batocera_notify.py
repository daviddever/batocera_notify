#! /usr/bin/env python3

import socket
import sys


def send_data(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(message.encode("utf-8"))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        send_data(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print("Usage: ha_batocera_notify.py <host> <port> <message>")
