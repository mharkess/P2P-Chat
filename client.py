"""Client-side portion of the p2p application"""
import threading
import os
import sys
import db_connector as dbc
import message_transmit as mt
import user_discovery as ud

current_user = ''

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
                if s_connection != 1:
                    user_lock = True
                    break
                print("\nNote: This user is currently offline.")
        current_user = user
        message = input('\n >> You: ')
        if message == 'QChat':  # Will quit the program
            print("Client stopped")
            sys.exit()
        if message == 'SChat':  # Will switch user to chat to
            user_lock = False
            s_connection.close()
        else:
            message = username + "%" + message
            s_connection.send(message.encode('ascii'))
            #print('\n >> %s: %s', user, str(msg_recv.decode('ascii')))

def client_recieve():
    """Local server to recieve incoming messages"""
    server_socket = mt.start_message_server()
    while True:
        client_socket, addr = server_socket.accept()
        msg_recv = server_socket.recv(1024)
        message = msg_recv[0].decode()
        user_send = message.split("%")
        query = "INSERT INTO local_storage.texthistory (username, contents) VALUES ('{}','{}')".format(user_send[0], user_send[1])
        if user_send[0] == current_user:
            print(" >> %s: %s",user_send[0], user_send[1])
        dbc.query_db(query,True)
        #print("\n"+ "sender: " + msg[0].decode())
        
# Using threading to send/recieve simultaneously
send = threading.Thread(target=client_send)
send.daemon = True
receive = threading.Thread(target=client_recieve)
receive.daemon = True
while True:
    first_time = input('\n Are you using this program for the first time? (y/n): ')
    if first_time == 'y':
        username = first_time_setup()
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

