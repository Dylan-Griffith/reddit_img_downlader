from os import path
import urllib.request
from urllib.parse import urlparse
from scrape import load_csv_file, user_lst
import requests

ext_lst = ['.mp4', '.jpg', '.gif']
CSV_FILENAME = 'scrape.csv'

file_path = path.join(path.dirname(__file__), 'img')


def download_img(url, name):
    name = file_path + '/' + name
    urllib.request.urlretrieve(url, name)
    print('Download Completed')


def main():
    load_csv_file()
    for user in user_lst:
        ext = '.' + user.url.split('.')[-1]
        name = user.id_num + ext
        new_path = path.join(file_path, name)
        if not path.isfile(new_path):
            if ext in ext_lst:
                try:
                    download_img(user.url, name)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    main()
