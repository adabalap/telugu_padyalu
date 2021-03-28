import sqlite3
from sqlite3 import Error


def create_db_connection(db_file):
    # Create a database connection to the SQLite database
    db_conn = None
    try:
        db_conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return db_conn


def close_db_connection(db_conn):
    # Close the DB connection
    db_conn.close()


def get_telugu_padyalu(db_conn, args):
    # Initialize the return variables
    message = {}
    record_id = None
    sql = ''

    # Query the table
    cur = db_conn.cursor()

    if args['mode'] == 'twitter':
        sql = "SELECT rowid, * FROM telugu_padyalu WHERE tweet_status == 0"
    elif args['mode'] == 'whatsapp':
        sql = "SELECT rowid, * FROM telugu_padyalu WHERE wa_status == 0"

    cur.execute(sql)

    try:
        row = cur.fetchone()

        if row:
            record_id = row[0]
            message['padyam'] = row[2]
            message['meaning'] = row[3]

    except Error as err:
        print(err)

    return message, record_id


def update_db_record(db_conn, record_id, mode):
    # Update the DB record as tweet has been published
    sql = ''
    cur = db_conn.cursor()

    if mode == 'twitter':
        sql = f'UPDATE telugu_padyalu SET tweet_status = 1 WHERE rowid == {record_id}'
    elif mode == 'whatsapp':
        sql = f'UPDATE telugu_padyalu SET wa_status = 1 WHERE rowid == {record_id}'

    # execute the query
    cur.execute(sql)

    # Commit the changes
    db_conn.commit()


def get_message(args):
    # Create a database connection
    db_conn = create_db_connection(args['db_file'])

    # Get message
    (message, record_id) = get_telugu_padyalu(db_conn, args)

    return db_conn, message, record_id
