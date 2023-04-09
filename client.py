"""Client-side portion of the p2p application"""
import threading
import os
import sys
import db_connector as dbc
import message_transmit as mt
import user_discovery as ud

def first_time_setup():
    """Generates local db during initial setup"""
    dbc.generate_local_db()
    while True:
        username =  input('\nEnter a username you would like to use: ')
        confirm = input ('\nAre you sure you want that username? (y/n): ')
        if confirm == 'y':
            ud.add_new_user(username)
            return username
            

def client_send():
    """Main function to be ran on client-side"""
    user_lock = False
    while True:
        if not user_lock:
            while True:
                user = input('\nEnter the user you want to chat with: ')
                s_connection = mt.message_connection(user)
                if s_connection != 0:
                    user_lock = True
                    break
                print("\nThis user is currently offline.")
        message = input('\n >>User: ')
        if message == 'QChat':  # Will quit the program
            print("Client stopped")
            sys.exit()
        if message == 'SChat':  # Will switch user to chat to
            user_lock = False
            s_connection.close()
        else:
            s_connection.send(message.encode('ascii'))
            #print('\n >> %s: %s', user, str(msg_recv.decode('ascii')))

def client_recieve():
    """Local server to recieve incoming messages"""
    server_socket = mt.start_message_server()
    while True:
        client_socket, addr = server_socket.accept()
        msg_recv = server_socket.recv(1024)
        #print("\n"+ "sender: " + msg[0].decode())
        
# Using threading to send/recieve simultaneously
send = threading.Thread(target=client_send)
send.daemon = True
receive = threading.Thread(target=client_recieve)
receive.daemon = True
while True:
    first_time = input('\n Are you using this program for the first time? (y/n): ')
    if first_time == 'y':
        user = first_time_setup()
        break
    else:
        username = input('\n Enter your username: ')
        ud.update_discovery(username)
        break
send.start()
receive.start()
send.join()
print("Program terminated")
sys.exit()

