"""Module to connect client to local DB"""
# Library imports
import cProfile
import pstats
import logging
import sqlite3
import mysql.connector
from decouple import config

# Setup logging for feed ingester module
logger = logging.getLogger('db_connector_logger')
logger.setLevel(logging.DEBUG)

# Logging handler and setting logging level to DEBUG
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# format for log entries
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# adding format to handler
ch.setFormatter(formatter)

# adding handling to logger
logger.addHandler(ch)


def generate_local_db():
    """Generates SQLite3 DB for local use"""
    #database_ip = config('local_chat_db', default='')
    try:
        db_connection = sqlite3.connect("local_storage.db")
    except sqlite3.Error:
        logging.error("Unable to generate a local db")
        return 1

def connect_to_db(isLocal):
    """Establishes conenction to a database"""
    if isLocal:
        database_ip = config('local_chat_db', default='')
        try:
            db_connection = sqlite3.connect(database_ip)
            db_cursor = db_connection.cursor()
            logging.info("Successful Connection")
            return db_connection, db_cursor
        except sqlite3.Error:
            logging.error("ERROR 140: Cannot connect to database")
            return 1, 1
    else:
        database_ip = config('user_discovery_db', default='')
        database_user = config('user_discovery_db_user', default='')
        database_pass = config('user_discovery_db_pass', default='')
        try:
            db_connection = mysql.connector.connect(
                host = database_ip,
                user = database_user,
                password = database_pass
            )
            db_cursor = db_connection.cursor()
            logging.info("Successful Connection")
            return db_connection, db_cursor
        except sqlite3.Error:
            logging.error("ERROR 140: Cannot connect to database")
            return 1, 1
        
def sanatize_params(params,islocal):
    """Sanatizes parameters before running SQL query"""
    if islocal:
        illegal_characters = ('"', '!', '@', '#', '$', '%', '^', '*', '+', '=', '-', '\'','|' )
    else:
        illegal_characters = ('"', '!', '@', '#', '$', '%', '^', '*', '+', '=', '-', '\'','|', '.', '&', '?', '/' )
    for current_param in params:
        if any(i in current_param for i in illegal_characters):
            return 1
    return 0


def query_db(query, islocal, **kwargs):
    """Executes query on database that are sent by the other API endpoints"""
    query_params = kwargs.get('query_params', None)
    if islocal:
        db_connection, db_cursor = connect_to_db(True)
        if db_cursor == 1:
            logging.error("ERROR 400: Cannot connect to database")
        else:
            try:
                if query_params is not None:
                    if sanatize_params(query_params, islocal) > 0:
                        return 1
                    db_cursor.execute(query, query_params)
                else:
                    db_cursor.execute(query)
                db_connection.commit()
                logging.info("Successful Query")
                db_connection.close()
            except sqlite3.Error:
                logging.error("ERROR 141: Invalid Query")
                db_connection.close()
    else:
        db_connection, db_cursor = connect_to_db(False)
        if db_cursor == 1:
            logging.error("ERROR 400: Cannot connect to database")
        else:
            db_cursor.execute(query)
            db_connection.commit()
            query_result = db_cursor.fetchall()
            db_cursor.close()
            db_connection.close()
            logging.info("Successful Discovery Query")
            return query_result


def db_connector_profiler():
    """Runs a profile on db_connector and prints results to the console"""
    profiler = cProfile.Profile()
    profiler.enable()
    query_db("TEST query",True)
    print('Query Successful')
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.print_stats()
    return 0
