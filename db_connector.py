"""Module to connect client to local DB"""
# Library imports
import cProfile
import pstats
import logging
import sqlite3
import MySQLdb
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


def connect_to_db(isLocal):
    """Establishes conenction to database"""
    if (isLocal):
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
        try:
            db_connection = sqlite3.connect(database_ip)
            db_cursor = db_connection.cursor()
            logging.info("Successful Connection")
            return db_connection, db_cursor
        except sqlite3.Error:
            logging.error("ERROR 140: Cannot connect to database")
            return 1, 1


def query_db(query):
    """Executes query on database that are sent by the other API endpoints"""
    db_connection, db_cursor = connect_to_db()
    if db_cursor == 1:
        logging.error("ERROR 400: Cannot connect to database")
    else:
        try:
            db_cursor.execute(query)
            db_connection.commit()
            logging.info("Successful Query")
            db_connection.close()
        except sqlite3.Error:
            logging.error("ERROR 141: Invalid Query")
            db_connection.close()


def db_connector_profiler():
    """Runs a profile on db_connector and prints results to the console"""
    profiler = cProfile.Profile()
    profiler.enable()
    query_db("TEST query")
    print('File Upload Successful')
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.print_stats()
    return 0