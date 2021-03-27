import argparse
import sqlite3
from sqlite3 import Error
from time import time, ctime, sleep
from ShiningArmor import twitter
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


def get_cmd_line_args():
    # Parse the command line arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-m", "--mode", required=True)  # mode: whatsapp, twitter
    ap.add_argument("-u", "--wa_contact", required=False)
    ap.add_argument("-d", "--db_file", required=True)
    ap.add_argument("-t", "--twitter_tokens_file", required=False)
    ap.add_argument("-ht", "--hash_tag", required=False)
    ap.add_argument("-T", "--testing", required=False)

    args = vars(ap.parse_args())

    if args['mode'] == 'whatsapp':
        if args['wa_contact'] is None:
            print(f'error: -u/--wa_contact is mandatory in whatsapp mode')
            exit(1)

    if args['mode'] == 'twitter':
        if args['twitter_tokens_file'] is None:
            print(f'error: -t/--twitter_tokens_file is mandatory in twitter mode')
            exit(1)

    args['testing'] = 'True' if args['testing'] else args['testing'] == 'False'

    return args


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


def get_telugu_padyalu(db_conn):
    # Initilize the return vairbales
    message = {}
    record_id = None

    # Query the table
    cur = db_conn.cursor()

    if args['mode'] == 'twitter':
        SQL = "SELECT rowid, * FROM telugu_padyalu WHERE tweet_status == 0"
    elif args['mode'] == 'whatsapp':
        SQL = "SELECT rowid, * FROM telugu_padyalu WHERE wa_status == 0"

    cur.execute(SQL)

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
    (message, record_id) = get_telugu_padyalu(db_conn)

    return db_conn, message, record_id


def wa_bot(args):
    # Main WhatsApp Bot Logic
    t = time()

    # Get the message
    (db_conn, message, record_id) = get_message(args)

    # No messages to be sent
    if message is None:
        print(f'{ctime(t)} - NO MESSAGES TO BE SENT')
        return 1

    message = f'*వేమన్న పద్యం* :\n{message}'
    print(f'{ctime(t)} - Sending message to: {args["wa_contact"]}\n')
    print(f'{ctime(t)} - {message}')

    options = Options()

    options.add_argument("--no-sandbox")
    options.add_argument("user-data-dir=" + "cookies")

    try:
        display = Display(visible=0, size=(1360, 768))
        display.start()

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get('https://web.whatsapp.com')
        sleep(25)

        driver.find_element_by_xpath('//*[@title = "{}"]'.format(args['wa_contact'])).click()
        sleep(30)

        wa_msg = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        wa_msg.send_keys(message)
        sleep(15)

        driver.quit()
        display.stop()

        if args['testing'] is False:
            # Update the DB record
            update_db_record(db_conn, record_id, args['mode'])

        # Close DB connection
        close_db_connection(db_conn)

        print(f'{ctime(t)} - WhatsApp message sent!')

    except NoSuchElementException as err:
        print(f'{ctime(t)} - Exception: NoSuchElementException')
        print(err)

    except TimeoutException as err:
        print(f'{ctime(t)} - Exception: Timeout')
        print(err)

    except Error as err:
        print(f'{ctime(t)} - Un-know Exception:\n\n{err}')
        pass

    return 0


def tweet_bot(args):
    # Get the message
    (db_conn, message, record_id) = get_message(args)

    if args['hash_tag']:
        message = f'{message["padyam"]} \n {args["hash_tag"]}'

    try:
        tokens = twitter.tokens(args['twitter_tokens_file'])
        api = twitter.auth(tokens)
        twitter.tweet(api, message)

        if args['testing'] is False:
            update_db_record(db_conn, record_id, args['mode'])
    except Error as err:
        print(f'Exception occurred: {err}')
    finally:
        close_db_connection(db_conn)

    print(f'Tweet posted ... Hurray!')

if __name__ == "__main__":
    # parse the command line arguments
    args = get_cmd_line_args()

    if args['mode'] == 'whatsapp':
        # put WhatsApp BOT to work
        wa_bot(args)
    elif args['mode'] == 'twitter':
        # put Twitter BOT to work
        tweet_bot(args)
    else:
        # un-know mode
        print('error: Current Valid Modes Allowed: [whatsapp, twitter]')
        exit(1)