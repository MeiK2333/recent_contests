from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    resp = requests.get('https://www.luogu.org/contest/list?page=1&_contentOnly=1', headers=headers)
    contests = resp.json()['currentData']['contests']['result']

    data = []

    convert_time = 60 * 60 * 8

    for contest in contests:
        link = f'https://www.luogu.org/contest/{contest["id"]}'
        start_time = datetime.fromtimestamp(contest['startTime'] - convert_time)
        end_time = datetime.fromtimestamp(contest['endTime'] - convert_time)
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'name': contest['name'],
            'link': link,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'host_name': contest['host']['name'],
            'problem_count': contest['problemCount']
        })

    update_to_db('洛谷', data)


if __name__ == '__main__':
    main()
