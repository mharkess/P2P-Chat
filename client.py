"""Client-side portion of the p2p application"""
import db_connector as dbc

def first_time_setup():
    dbc.generate_local_db()
    return 0