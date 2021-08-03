from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException

from time import time, ctime, sleep

from db import db


# Main WhatsApp Bot Logic
def wa_bot(args):
    (wa_message, rc) = ('', 0)
    t = time()

    # Get the message to be sent
    (db_conn, message, record_id) = db.get_message(args)

    if message is None:
        print(f'{ctime(t)} | No messages to be sent!')
        return rc

    wa_contact = f'{args["wa_contact"]}'
    print(f'{ctime(t)} | Sending message to contact: {wa_contact}\n')

    # Build the message
    if args['caption']:
        wa_message = f'{args["caption"]}'

    if message['padyam']:
        # bold the padyam
        t_padyam = message["padyam"]
        t_padyam_li = t_padyam.split('\n')
        t_padyam_bold = ''

        for i in t_padyam_li:
            if i:
                # ensure its not empty line
                t_padyam_bold = f'{t_padyam_bold}\n*{i}*'

        message["padyam"] = t_padyam_bold

        wa_message = f'{wa_message}' \
                     f'\n' \
                     f'{message["padyam"]}' \
                     f'\n'

    if message['meaning']:
        # highlight the keywords
        for i in ("తాత్పర్యం:", "తాత్పర్యం :", "భావం:", "భావం :"):
            message['meaning'] = message["meaning"].replace(i, f'*{i}*')

        wa_message = f'{wa_message}' \
                     f'\n' \
                     f'{message["meaning"]}' \
                     f'\n'

    # Convert string message into list
    wa_message_li = wa_message.split('\n')

    print(f'{ctime(t)} | {wa_message_li}')

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("user-data-dir=" + "cookies")

    try:
        display = Display(visible=0)
        display.start()

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get('https://web.whatsapp.com')
        sleep(20)

        driver.find_element_by_xpath('//*[@title = "{}"]'.format(wa_contact)).click()
        sleep(10)

        # Date: 1-Aug-2021
        # ElementNotInteractableException occurred started from 11-July-2021
        # same code that worked previously stopped only got resolved post the below change
        # not sure if it was due to the browser/driver updates
        # driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        # changed to
        # driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[1]')
        # Note: the last "div[2]" was updated to "div[1]"
        # Spent lot of hours to solve this error

        wa_msg = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[1]')

        # Put the message in one-block
        for i in wa_message_li:
            wa_msg.send_keys(i + Keys.SHIFT + Keys.RETURN)

        wa_msg.send_keys(Keys.ENTER)
        sleep(15)

        driver.quit()
        display.stop()

        if args['testing'] is False:
            # Update the DB record
            db.update_db_record(db_conn, record_id, args['mode'])

        # Close DB connection
        db.close_db_connection(db_conn)

        print(f'{ctime(t)} | WhatsApp message successfully sent!')

    except NoSuchElementException as err:
        print(f'{ctime(t)} | NoSuchElementException occurred')
        print(err)
        rc = 1
    except TimeoutException as err:
        print(f'{ctime(t)} | TimeoutException occurred')
        print(err)
        rc = 1
    except ElementNotInteractableException as err:
        print(f'{ctime(t)} | ElementNotInteractableException occurred')
        print(err)
        rc = 1
    except Exception as err:
        print(f'{ctime(t)} | An unknown/unhandled exception occurred')
        print(err)
        rc = 1

    return rc
