from time import time, ctime, sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from db import db


def wa_bot(args):
    # Main WhatsApp Bot Logic
    t = time()

    # Get the message
    (db_conn, message, record_id) = db.get_message(args)

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
            db.update_db_record(db_conn, record_id, args['mode'])

        # Close DB connection
        db.close_db_connection(db_conn)

        print(f'{ctime(t)} - WhatsApp message sent!')

    except NoSuchElementException as err:
        print(f'{ctime(t)} - Exception: NoSuchElementException')
        print(err)

    except TimeoutException as err:
        print(f'{ctime(t)} - Exception: Timeout')
        print(err)

    except Exception as err:
        print(f'{ctime(t)} - Un-know Exception:\n\n{err}')
        pass

    return 0
