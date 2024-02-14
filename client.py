#! /usr/bin/python

import socket


def send_data(image_url, title, text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("192.168.10.25", 65432))
        message = f"{image_url};{title};{text}"
        s.sendall(message.encode("utf-8"))


# Example usage
send_data("http://192.168.10.26:8123/local/128.png", "Example", "Hello, World!")
