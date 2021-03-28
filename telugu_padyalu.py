import argparse

from wa_bot import wa_bot
from tweet_bot import tweet_bot


def get_cmd_line_args():
    # Parse the command line arguments
    ap = argparse.ArgumentParser()
    valid_args = True

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
            valid_args = False

    if args['mode'] == 'twitter':
        if args['twitter_tokens_file'] is None:
            print(f'error: -t/--twitter_tokens_file is mandatory in twitter mode')
            valid_args = False

    args['testing'] = 'True' if args['testing'] else args['testing'] == 'False'

    if valid_args:
        return args
    else:
        exit(1)


if __name__ == "__main__":
    # parse the command line arguments
    args = get_cmd_line_args()

    if args['mode'] == 'whatsapp':
        # put WhatsApp BOT to work
        wa_bot.wa_bot(args)
    elif args['mode'] == 'twitter':
        # put Twitter BOT to work
        tweet_bot.tweet_bot(args)
    else:
        # un-know mode
        print('error: Current Valid Modes Allowed: [whatsapp, twitter]')
        exit(1)
