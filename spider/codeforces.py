from datetime import datetime

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

        raw_time = tds[2].find('span').string.strip()
        time = datetime.strptime(raw_time, '%b/%d/%Y %H:%M')
        str_time = time.strftime('%Y-%m-%d %H:%M:%S')
        length = tds[3].string.strip()
        register_a = tds[5].find_all('a')
        if register_a:
            register_link = 'https://codeforces.com' + register_a[0]['href']
        else:
            register_link = 'https://codeforces.com/contests'
        data.append({
            'id': contest_id,
            'name': name,
            'start_time': str_time,
            'length': length,
            'link': register_link
        })
    update_to_db('Codeforces', data)


if __name__ == '__main__':
    main()
