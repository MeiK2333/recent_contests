from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://loj.ac/contests')
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')

    data = []

    convert_time = timedelta(hours=8)

    for tr in table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        name = tds[0].find('a').text.strip()
        link = 'https://loj.ac' + tds[0].find('a')['href']
        raw_start_time = tds[1].string.strip()
        raw_end_time = tds[2].string.strip()
        start_time = datetime.strptime(raw_start_time, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(raw_end_time, '%Y-%m-%d %H:%M:%S')
        start_time -= convert_time
        end_time -= convert_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        description = tds[3].text.strip()

        data.append({
            'name': name,
            'link': link,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'description': description,
        })

    update_to_db('LOJ', data)


if __name__ == "__main__":
    main()
