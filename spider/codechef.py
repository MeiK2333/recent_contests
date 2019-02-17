from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://www.codechef.com/contests')
    soup = BeautifulSoup(resp.text, 'html.parser')
    tables = soup.find_all('table')

    data = []
    present_table = tables[1]
    trs = present_table.find('tbody').find_all('tr')
    future_table = tables[2]
    trs.extend(future_table.find('tbody').find_all('tr'))

    convert_time = timedelta(hours=5, minutes=30)

    for tr in trs:
        tds = tr.find_all('td')
        code = tds[0].string.strip()
        name = tds[1].string.strip()
        link = 'https://www.codechef.com' + tds[1].find('a')['href']
        raw_start_time = tds[2]['data-starttime'].strip()
        raw_end_time = tds[3]['data-endtime'].strip()
        start_time = datetime.strptime(
            raw_start_time, '%Y-%m-%dT%H:%M:%S+05:30')
        # 转换时区到 UTC
        start_time -= convert_time
        end_time = datetime.strptime(raw_end_time, '%Y-%m-%dT%H:%M:%S+05:30')
        end_time -= convert_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'id': code,
            'link': link,
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time,
        })

    update_to_db('CodeChef', data)


if __name__ == '__main__':
    main()
