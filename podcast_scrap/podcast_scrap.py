import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Setting Paths
HOME_PATH = os.environ['HOME']
SAVE_PATH = f'{HOME_PATH}/Downloads/podcasts'

# Get URL
start = date(2005, 10, 10)
end = date(2015, 1, 1)
cur = start

# 2013-03-22 and before are in the format 032213_podcast.mp3
while cur <= date(2019, 3, 22):
    cur_str = cur.strftime("%m%d%y")
    url = f'https://traffic.libsyn.com/therelevantpodcast/{cur_str}_podcast.mp3'
    r = requests.get(url)
    if r.status_code == 200:
        # Send GET requests to see if episode exists
        filename = url.split('/')[-1]
        print(f'Beginning file download for file {filename}...')
        urllib.request.urlretrieve(url, f'{SAVE_PATH}/{filename}')
        # If episode exists, then download
    elif r.status_code == 404:
        print('File DNE.')
        cur += relativedelta(days=1)
        continue
    print(f'Download Complete for {filename}.')
    cur += relativedelta(days=1)
    
# 2013-03-29 first episode file format in 20130329_podcast.mp3
while cur <= end:
    cur_str = cur.strftime("%Y%m%d")
    url = f'https://traffic.libsyn.com/therelevantpodcast/{cur_str}_podcast.mp3'
    r = requests.get(url)
    if r.status_code == 200:
        # Send GET requests to see if episode exists
        filename = url.split('/')[-1]
        print(f'Beginning file download for file {filename}...')
        urllib.request.urlretrieve(url, f'{SAVE_PATH}/{filename}')
        # If episode exists, then download
    elif r.status_code == 404:
        print('File DNE.')
        cur += relativedelta(days=1)
        continue
    print(f'Download Complete for {filename}.')
    cur += relativedelta(days=1)
    

