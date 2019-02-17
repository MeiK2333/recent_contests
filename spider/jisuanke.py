from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://nanti.jisuanke.com/contest')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')

    data = []

    convert_time = timedelta(hours=8)

    for tr in table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        status = tds[6].text.strip()
        if status == '已结束':
            continue
        contest_type = tds[0].string.strip()
        name = tds[1].find('a').string.strip()
        link = 'https:' + tds[1].find('a')['href']
        raw_start_time = tds[3].string.strip()
        length = tds[4].string.strip()
        hours, minutes = length.split('\n')
        hours = hours.strip().split()[0]
        minutes = minutes.strip().split()[0]
        length_time = timedelta(hours=int(hours), minutes=int(minutes))
        start_time = datetime.strptime(raw_start_time, '%Y-%m-%d %H:%M')
        start_time -= convert_time
        end_time = start_time + length_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'type': contest_type,
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'link': link
        })

    update_to_db('jisuanke', data)


if __name__ == '__main__':
    main()
