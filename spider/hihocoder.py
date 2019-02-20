from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://hihocoder.com/contests')
    soup = BeautifulSoup(resp.text, 'html.parser')

    data = []

    convert_time = timedelta(hours=8)

    # 正在进行
    ol1 = soup.find(class_='ongoing')
    # 即将到来
    ol2 = soup.find(class_='upcoming')
    for li in ol1.find_all('li') + ol2.find_all('li'):
        name = li.find(class_='md-summary-cnt').find('a').string.strip()
        link = 'https://hihocoder.com' + \
            li.find(class_='md-summary-cnt').find('a')['href']
        description = li.find(class_='md-summary-cnt').find('p').text.strip()
        times = li.find_all(class_='htzc')
        raw_start_time, raw_end_time = [item.string.strip() for item in times]
        start_time = datetime.strptime(
            raw_start_time, '%Y-%m-%d %H:%M (+0800)')
        end_time = datetime.strptime(raw_end_time, '%Y-%m-%d %H:%M (+0800)')
        start_time -= convert_time
        end_time -= convert_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'name': name,
            'link': link,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'description': description,
        })

    update_to_db('hihoCoder', data)


if __name__ == '__main__':
    main()
