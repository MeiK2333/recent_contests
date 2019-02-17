from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get(
        'https://open.kattis.com/contests?kattis_original=on&kattis_recycled=on&user_created=off')
    soup = BeautifulSoup(resp.text, 'html.parser')

    tables = soup.find_all('table')

    data = []

    ongoing_table = tables[0]
    upcoming_table = tables[1]

    for tr in ongoing_table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        name = tds[0].find('a').string.strip()
        link = 'https://open.kattis.com' + tds[0].find('a')['href']
        length = tds[2].string
        raw_start_time = tds[3].string
        if '-' in raw_start_time:
            start_time = datetime.strptime(
                raw_start_time, '%Y-%m-%d %H:%M:%S UTC')
        else:
            start_time = datetime.strptime(datetime.utcnow().strftime(
                '%Y-%m-%d') + ' ' + raw_start_time,  '%Y-%m-%d %H:%M:%S UTC')
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        hours, minutes, seconds = length.split(':')
        length_time = timedelta(
            hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        end_time = start_time + length_time
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'link': link,
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time
        })

    for tr in upcoming_table.find('tbody').find_all('tr'):
        tds = tr.find_all('td')
        name = tds[0].find('a').text.strip()
        link = 'https://open.kattis.com' + tds[0].find('a')['href']
        length = tds[1].string
        raw_start_time = tds[2].string
        if '-' in raw_start_time:
            start_time = datetime.strptime(
                raw_start_time, '%Y-%m-%d %H:%M:%S UTC')
        else:
            start_time = datetime.strptime(datetime.utcnow().strftime(
                '%Y-%m-%d') + ' ' + raw_start_time,  '%Y-%m-%d %H:%M:%S UTC')
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        hours, minutes, seconds = length.split(':')
        length_time = timedelta(
            hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        end_time = start_time + length_time
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'link': link,
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time
        })

    update_to_db('Kattis', data)


if __name__ == '__main__':
    main()
