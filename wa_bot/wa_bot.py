from time import time, ctime, sleep

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from db import db


def wa_bot(args):
    # Main WhatsApp Bot Logic
    t = time()
    wa_message = ''
    rc = 0

    # Get the message
    (db_conn, message, record_id) = db.get_message(args)

    # No messages to be sent
    if message is None:
        print(f'{ctime(t)} - NO MESSAGES TO BE SENT')
        return 1

    wa_contact = f'{args["wa_contact"]}'
    print(f'Sending message to contact: {wa_contact}')

    # Build the message
    if args['caption']:
        wa_message = f'{args["caption"]}'

    if message['padyam']:
        #
        # bold the padyam
        #
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
        message['meaning'] = message["meaning"].replace("తాత్పర్యం:", "*తాత్పర్యం:*")
        message['meaning'] = message["meaning"].replace("భావం: ", "*భావం:* ")
        wa_message = f'{wa_message}' \
                     f'\n' \
                     f'{message["meaning"]}' \
                     f'\n'

    # Convert string message into list
    wa_message_li = wa_message.split('\n')

    print(f'{ctime(t)} - \n{wa_message_li}')

    options = Options()

    options.add_argument("--no-sandbox")
    options.add_argument("user-data-dir=" + "cookies")

    try:
        display = Display(visible=0, size=(1360, 768))
        display.start()

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get('https://web.whatsapp.com')
        sleep(20)

        driver.find_element_by_xpath('//*[@title = "{}"]'.format(wa_contact)).click()
        sleep(15)

        wa_msg = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        # Put the message in one-block
        for i in wa_message_li:
            wa_msg.send_keys(i + Keys.SHIFT + Keys.RETURN)

        wa_msg.send_keys(Keys.ENTER)

        sleep(5)

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
        rc = 1

    except TimeoutException as err:
        print(f'{ctime(t)} - Exception: Timeout')
        print(err)
        rc = 1

    except Exception as err:
        print(f'{ctime(t)} - Un-know Exception:\n\n{err}')
        rc = 1

    return rc
