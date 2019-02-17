from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://codeforces.com/contests')
    soup = BeautifulSoup(resp.text, 'html.parser')
    tables = soup.find_all('table')
    trs = tables[0].find_all('tr')

    data = []

    for tr in trs[1:]:
        contest_id = tr['data-contestid']
        tds = tr.find_all('td')
        name = tds[0].string.strip()

        raw_start_time = tds[2].find('span').string.strip()
        start_time = datetime.strptime(raw_start_time, '%b/%d/%Y %H:%M')
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        length = tds[3].string.strip()
        if length.count(':') == 1:
            hours, minutes = length.split(':')
            length_time = timedelta(hours=int(hours), minutes=int(minutes))
        elif length.count(':') == 2:
            days, hours, minutes = length.split(':')
            length_time = timedelta(
                days=int(days), hours=int(hours), minutes=int(minutes))
        else:
            length_time = timedelta()
        end_time = start_time + length_time
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        register_a = tds[5].find_all('a')
        if register_a:
            register_link = 'https://codeforces.com' + register_a[0]['href']
        else:
            register_link = 'https://codeforces.com/contests'
        data.append({
            'id': contest_id,
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'length': length,
            'link': register_link
        })
    update_to_db('Codeforces', data)


if __name__ == '__main__':
    main()
