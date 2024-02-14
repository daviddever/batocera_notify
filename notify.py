#! /usr/bin/python

import socket
import subprocess


def listen_for_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 65432))  # Adjust as necessary
        s.listen()
        print("Listening for incoming connections...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode("utf-8")
                if data:
                    # Launch the display script with the received data
                    subprocess.run(["python", "display_script.py", data])


if __name__ == "__main__":
    listen_for_data()
