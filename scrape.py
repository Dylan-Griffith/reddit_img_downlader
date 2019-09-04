import praw
import config
import os
import csv
import datetime as dt
import pandas as pd

"""
Scrapes through subreddits to get submission data
Creates CSV of data
"""

user_lst = []
SUBREDDIT = 'art'
LIMIT = 100


class User:

    def __init__(self, author, score, title, url, id_num, created, utc_created, subreddit):
        self.author = author
        self.score = score
        self.title = title
        self.url = url
        self.id_num = id_num
        self.created = created
        self.utc_created = utc_created
        self.subreddit = subreddit

    def __repr__(self):
        return self.author


def authenticate():
    print('Authenticating User....')
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=config.user_agent,
                         username=config.username,
                         password=config.password)
    print("User '{user}' Authenticated".format(user=reddit.user.me()))
    return reddit


def load_csv_file():
    try:
        with open('scrape.csv', 'r') as fin:
            csv_file_reader = csv.reader(fin)
            lst = (list(csv_file_reader))

        for row in range(1, len(lst)):
            user = User(author=lst[row][0],
                        score=lst[row][1],
                        title=lst[row][2],
                        subreddit=lst[3],
                        url=lst[row][4],
                        created=lst[row][5],
                        id_num=lst[row][6],
                        utc_created=lst[row][7])
            user_lst.append(user)
    except FileNotFoundError:
        return


def main():
    reddit = authenticate()
    subreddit = reddit.subreddit(SUBREDDIT)
    load_csv_file()
    submission_id_lst = [user.id_num for user in user_lst]
    suicide_dct = scrape_data(subreddit, submission_id_lst)
    data_frame = pd.DataFrame(suicide_dct, columns=['author', 'score', 'title', 'subreddit',
                                                    'url', 'created', 'id_num', 'utc_created'])
    data_frame = data_frame.sort_values(by=['score'], ascending=False)
    save_data(data_frame)


def save_data(data_frame):
    if os.path.exists('./scrape.csv'):
        with open('scrape.csv', 'a') as fout:
            data_frame.to_csv(fout, index=False, header=False)
    else:
        print('Creating File...')
        data_frame.to_csv('scrape.csv', index=False)


def scrape_data(subreddit, submission_id_lst):

    def get_date(created):
        return dt.datetime.fromtimestamp(created)

    submission_dct = {
                   "author": [],
                   "score": [],
                   "title": [],
                   "subreddit": [],
                   "url": [],
                   "created": [],
                   'id_num': [],
                   'utc_created': []
                   }

    for submission in subreddit.hot(limit=LIMIT):
        if submission.id not in submission_id_lst and not submission.stickied:
            print('Found new post!')
            submission_dct['author'].append(submission.author)
            submission_dct['score'].append(submission.score)
            submission_dct['title'].append(submission.title)
            submission_dct['subreddit'].append(SUBREDDIT)
            submission_dct['url'].append(submission.url)
            submission_dct["created"].append(get_date(submission.created))
            submission_dct['id_num'].append(submission.id)
            submission_dct["utc_created"].append(submission.created_utc)
            submission_id_lst.append(submission.id)

    return submission_dct


if __name__ == '__main__':
    main()
