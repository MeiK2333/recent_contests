from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://acm.ecnu.edu.cn/contest/')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')

    data = []

    convert_time = timedelta(hours=8)

    for tr in table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        # 排除非公开比赛和已结束的比赛
        if tds[4].find(class_='green') is None or tds[5].text.strip() == '已结束':
            continue

        link = 'https://acm.ecnu.edu.cn' + tds[0].find('a')['href']
        name = tds[0].find('a').string.strip()
        raw_start_time = tds[1].string.strip()
        length = tds[2].string.strip()
        hours, minutes = length.split(':')
        length_time = timedelta(hours=int(hours), minutes=int(minutes))
        authors = [a.text.strip() for a in tds[3].find_all('a')]
        start_time = datetime.strptime(raw_start_time, '%Y-%m-%d %H:%M')
        start_time -= convert_time
        end_time = start_time + length_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'link': link,
            'authors': authors
        })

    update_to_db('ecnu', data)


if __name__ == '__main__':
    main()
