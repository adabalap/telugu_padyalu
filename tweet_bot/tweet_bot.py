from ShiningArmor import twitter
from db import db


def tweet_bot(args):
    # Get the message from DB
    (db_conn, message, record_id) = db.get_message(args)
    rc = 0

    if args['hash_tag']:
        # Append hash-tag to padyam
        message["padyam"] = f'{message["padyam"]}\n\n' \
                            f'{args["hash_tag"]}'

        # convert dict values as list type to tweet
        # message = list(message.values())
        message = message["padyam"]

    try:
        tokens = twitter.tokens(args['twitter_tokens_file'])
        api = twitter.auth(tokens)

        twitter.tweet(api, message)

        if args['testing'] is False:
            db.update_db_record(db_conn, record_id, args['mode'])

    except Exception as err:
        print(f'Exception occurred: {err}')
        rc = 1

    finally:
        db.close_db_connection(db_conn)

    return rc
