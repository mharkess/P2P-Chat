"""Module to transmit messages between users"""
import socket

def message_connection(user):
    """Establishes connection to another user"""
    s_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 3452
    s_local.connect((host,port))
    return s_local

def start_message_server():
    """Creates a socket server to recieve messages from users"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 3452))
    return server


def send_message(message, user):
    """Sends a message to another user"""
    s_local = message_connection(user)
    s_local.send(message)
