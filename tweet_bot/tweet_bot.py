from ShiningArmor import twitter
from db import db


def tweet_bot(args):
    # Get the message
    (db_conn, message, record_id) = db.get_message(args)

    if args['hash_tag']:
        # create a thread tweet, both should have hash-tag
        message["padyam"] = f'{message["padyam"]}\n' \
                            f'{args["hash_tag"]}'
        message["meaning"] = f'{message["meaning"]}\n' \
                             f'{args["hash_tag"]}'

        # convert dict values as list type to tweet
        message = list(message.values())
    try:
        tokens = twitter.tokens(args['twitter_tokens_file'])
        api = twitter.auth(tokens)

        if twitter.tweet(api, message) == 0:
            print(f'Tweet posted ... Hurray!')

        if args['testing'] is False:
            db.update_db_record(db_conn, record_id, args['mode'])
    except Exception as err:
        print(f'Exception occurred: {err}')
    finally:
        db.close_db_connection(db_conn)
