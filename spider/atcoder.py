from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://atcoder.jp/contests/')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find_all('table')[1]

    data = []

    convert_time = timedelta(hours=9)

    for tr in table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        raw_start_time = tds[0].find('time').string
        start_time = datetime.strptime(raw_start_time, '%Y-%m-%d %H:%M:%S+0900')
        start_time -= convert_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        name = tds[1].find('a').string
        link = 'https://atcoder.jp' + tds[1].find('a')['href']
        length = tds[2].string.strip()
        hours, minutes = length.split(':')
        length_time = timedelta(hours=int(hours), minutes=int(minutes))
        end_time = start_time + length_time
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        data.append({
            'name': name,
            'link': link,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'length': length,
        })

    update_to_db('AtCoder', data)


if __name__ == '__main__':
    main()
