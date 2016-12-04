import logging
import MySQLdb

def get_db_connection(db_config):
    try:

        db_connection = MySQLdb.connect(**db_config)

    except MySQLdb.Error as err:

        logging.error("MySQLdb.Error: " + err.message)
        raise err  # Re-raise the exception

    logging.info("Created database connection.")
    return db_connection

