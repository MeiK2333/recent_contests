from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }
    resp = requests.get('https://www.luogu.org/contest/lists', headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    divs = soup.find(class_='lg-content-table-left')

    data = []

    convert_time = timedelta(hours=8)

    for div in divs.find_all(class_='lg-table-row'):
        left = div.find(class_='am-u-md-7')
        if left.find('strong').string.strip() != '未开始':
            continue
        name = left.find('a').string.strip()
        link = 'https://www.luogu.org' + left.find('a')['href']
        mid = div.find(class_='am-u-md-2')
        temp = mid.text.split()
        raw_start_time = f'{temp[0]} {temp[1]}'
        raw_end_time = f'{temp[2]} {temp[3]}'
        start_time = datetime.strptime(raw_start_time, '%Y-%m-%d %H:%M')
        start_time -= convert_time
        end_time = datetime.strptime(raw_end_time, '%Y-%m-%d %H:%M')
        end_time -= convert_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'name': name,
            'link': link,
            'start_time': str_start_time,
            'end_time': str_end_time,
        })

    update_to_db('luogu', data)


if __name__ == '__main__':
    main()
