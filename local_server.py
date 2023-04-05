"""Local server that recieves multiple incoming messages"""
import message_transmit as mt
import threading

def main():
    server_socket = mt.start_message_server()
    while True:
        (client_socket, client_ip) = server_socket.accept()
        