# Dataset source: https://www.kaggle.com/colinmorris/reddit-usernames

import pandas as pd
import sys

SAMPLE_SIZE = 10000

try:
    SAMPLE_SIZE = int(sys.argv[1])
except:
    print("Sample size not inputted. Defaulting to 10 000.")

dataset = pd.read_csv('users.csv', header=0, usecols=['author'])
sample_users = dataset.sample(SAMPLE_SIZE)

with open('non_bot_accounts.txt', 'w') as f:
    for i, row in sample_users.iterrows():
        print('u/' + row['author'], file=f)
