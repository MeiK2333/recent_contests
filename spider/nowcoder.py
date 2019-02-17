import json
from datetime import datetime, timedelta
from html.parser import HTMLParser

import requests
from bs4 import BeautifulSoup

from db import update_to_db


def main():
    resp = requests.get('https://ac.nowcoder.com/acm/contest/vip-index')
    soup = BeautifulSoup(resp.text, 'html.parser')
    divs = soup.find(
        class_='nk-main').find(class_='platform-mod').find_all(class_='platform-item')

    data = []

    convert_time = 60 * 60 * 8

    for div in divs:
        json_data = json.loads(HTMLParser().unescape(div['data-json']))
        name = json_data['contestName']
        start_time = datetime.fromtimestamp(
            json_data['contestStartTime'] / 1000 - convert_time)
        end_time = datetime.fromtimestamp(
            json_data['contestEndTime'] / 1000 - convert_time)
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        register_start_time = datetime.fromtimestamp(
            json_data['contestSignUpStartTime'] / 1000 - convert_time)
        register_end_time = datetime.fromtimestamp(
            json_data['contestSignUpEndTime'] / 1000 - convert_time)
        str_register_start_time = register_start_time.strftime(
            '%Y-%m-%d %H:%M:%S')
        str_register_end_time = register_end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'name': name,
            'link': 'https://ac.nowcoder.com/acm/contest/vip-index',
            'start_time': str_start_time,
            'end_time': str_end_time,
            'register_start_time': str_register_start_time,
            'register_end_time': str_register_end_time,
        })

    update_to_db('nowcoder', data)


if __name__ == "__main__":
    main()
