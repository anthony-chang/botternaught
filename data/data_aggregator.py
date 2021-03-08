import requests
import json
import attributes

PUSHSHIFT_API_BASE_URL = 'http://api.pushshift.io/reddit/search'

def construct_params(user, fields):
    return {
        'author': user,
        'fields': fields
    }

def get_comments_for_account(user):
    endpoint = '{}/comment'.format(PUSHSHIFT_API_BASE_URL)
    try:
        r = requests.get(url=endpoint, params=construct_params(user, attributes.COMMENT_FIELDS))
        return r.json()
    except:
        print('Failed to get comment data for user {}'.format(user))
        return None


def get_submissions_for_account(user):
    endpoint = '{}/submission'.format(PUSHSHIFT_API_BASE_URL)
    try:
        r = requests.get(url=endpoint, params=construct_params(user, attributes.SUBMISSION_FIELDS))
        return r.json()
    except:
        print('Failed to get submission data for user {}'.format(user))
        return None

def get_accounts():
    f = open('bot_accounts.txt', 'r+')
    # sanitize text file (ie. "u/user_name 1094" => "user_name")
    accounts = [line.split('/', 1)[1].split('\t')[0] for line in f.readlines()]
    f.close
    return accounts

def main():
    # Placeholder
    bot_accounts = get_accounts()
    for user in bot_accounts:
        comment_data = get_comments_for_account(user)
        submission_data = get_submissions_for_account(user)


if __name__ == '__main__':
    main()
