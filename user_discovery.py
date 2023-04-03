"""Module to find new users to interact with"""
import db_connector as dbc

def update_discovery():
    """Updates ip address of client in Discovery DB"""
    result = dbc.query_db("UPDATE discovery SET ipv4 = currentip WHERE user = test", False)
    return 0

def find_user():
    """Finds a user in the discovery DB"""
    result = dbc.query_db("SELECT discovery WHERE user = test2", False)
    return result

def add_new_user():
    """Adds current user to discovery DB"""
    result = dbc.query_db("INSERT username, ipv4, port INTO discovery", False)
    return result