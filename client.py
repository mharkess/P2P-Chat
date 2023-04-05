"""Client-side portion of the p2p application"""
import threading
import db_connector as dbc
import message_transmit as mt
import user_discovery as ud

def first_time_setup():
    """Generates local db during initial setup"""
    dbc.generate_local_db()
    return 0

def main():
    """Main function to be ran on client-side"""
    first_time_setup()
    ud.update_discovery()
    while True:
        if not user_lock:
            user = input('\nEnter the user you want to chat with: ')
            s_connection = mt.message_connection(user)
            user_lock = True
        message = input('\n >>User: ')
        if message == 'QChat':  # Will quit the program
            break
        if message == 'SChat':  # Will switch user to chat to
            user_lock = False
        else:
            s_connection.send(message.encode('ascii'))
            msg_recv = s_connection.recv(1024)
            print('\n >> %s: %s', user, str(msg_recv.decode('ascii')))
