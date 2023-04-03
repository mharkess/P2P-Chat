"""Client-side portion of the p2p application"""
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
        print("Comms")
