"""Module to find new users to interact with"""
import db_connector as dbc
import message_transmit as mt

def update_discovery(username):
    """Updates ip address of client in Discovery DB"""
    local_ip = mt.get_localIP()
    query = "UPDATE discovery.users SET ipaddress = '{}' WHERE username = '{}'".format(local_ip, username)
    result = dbc.query_db(query, False)
    return 0

def find_user(username):
    """Finds a user in the discovery DB"""
    query = "Select discovery.users WHERE username = {}".format(username)
    result = dbc.query_db(query, False)
    return result

def add_new_user(username):
    """Adds current user to discovery DB"""
    local_ip = mt.get_localIP()
    port = 3452
    query = "INSERT INTO discovery.users (username, ipaddress, port) VALUES ('{}','{}','{}')".format(username, local_ip,port)
    dbc.query_db(query, False)
    return 0