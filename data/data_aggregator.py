import praw
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pymongo import MongoClient

import attributes
from redditor import Redditor

PUSHSHIFT_API_BASE_URL = 'http://api.pushshift.io/reddit/search'
DATABASE_NAME = 'botternaught'
COLLECTION_NAME = 'redditors'
REDDIT = praw.Reddit('botternaught')
MONGO_CLIENT = MongoClient('localhost', 27017)

def construct_params(user, fields):
    return {
        'author': user,
        'fields': fields
    }

def get_collection():
    db = MONGO_CLIENT[DATABASE_NAME]
    return db[COLLECTION_NAME]

def request(retries=5, backoff_factor=1, status_forcelist=(429, 500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_comments_for_account(username):
    endpoint = '{}/comment'.format(PUSHSHIFT_API_BASE_URL)
    try:
        r = request().get(url=endpoint, params=construct_params(username, attributes.COMMENT_FIELDS))
        return r.json()
    except:
        print('Error {} {}: failed to get comment data for user {}'.format(r.status_code, r.reason, username))
        return None

def get_submissions_for_account(username):
    endpoint = '{}/submission'.format(PUSHSHIFT_API_BASE_URL)
    try:
        r = request().get(url=endpoint, params=construct_params(username, attributes.SUBMISSION_FIELDS))
        return r.json()
    except:
        print('Error {} {}: failed to get submission data for user {}'.format(r.status_code, r.reason, username))
        return None

def scrape_account(username, is_bot):
    redditor = Redditor()
    try:
        user = REDDIT.redditor(username)

        redditor.username = username
        redditor.post_karma = user.link_karma
        redditor.comment_karma = user.comment_karma
        redditor.created_utc = user.created_utc
        redditor.has_verified_email = user.has_verified_email
        redditor.is_default_icon = True if 'avatar_default' in user.icon_img else False
        redditor.is_mod = user.is_mod
        redditor.is_gold = user.is_gold

        redditor.is_bot = is_bot
    except Exception as e:
        print('{}: failed to get info for user {}'.format(e, user))
        return None

    redditor.comments = get_comments_for_account(username)['data']
    redditor.submissions = get_submissions_for_account(username)['data']
    return redditor

def get_accounts_from_file(filename):
    f = open(filename, 'r')
    # parse text file (ie. "u/user_name" => "user_name")
    accounts = [line.split('u/')[1].split('\n')[0] for line in f.readlines()]
    f.close()
    return accounts

def add_account_to_db(redditor):
    collection = get_collection()
    collection.insert_one(redditor.__dict__)

def scrape_all_accounts():
    bot_accounts = get_accounts_from_file('bot_accounts.txt')
    for i, account in enumerate(bot_accounts):
        redditor = scrape_account(account, is_bot=True)
        if redditor is not None:
            print('Successfully scraped user {:<30} | {}/{} bot accounts done.'.format(
                account, i + 1, len(bot_accounts)
            ))
            add_account_to_db(redditor)

    non_bot_accounts = get_accounts_from_file('non_bot_accounts.txt')
    for i, account in enumerate(non_bot_accounts):
        redditor = scrape_account(account, is_bot=False)
        if redditor is not None:
            print('Successfully scraped user {:<30} | {}/{} non bot accounts done.'.format(
                account, i + 1, len(non_bot_accounts)
            ))
            add_account_to_db(redditor)

def main():
    scrape_all_accounts()

if __name__ == '__main__':
    main()
