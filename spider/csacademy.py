from datetime import datetime

import requests

from db import update_to_db


def main():
    headers = {
        'x-requested-with': 'XMLHttpRequest',
    }
    resp = requests.get('https://csacademy.com/contests/', headers=headers)
    json_data = resp.json()

    data = []

    convert_time = 60 * 60 * 8

    for item in json_data['state']['Contest']:
        if item.get('baseContestId'):
            continue
        contest_id = item['id']
        name = item['longName']
        link = 'https://csacademy.com/contest/' + item['name']
        if isinstance(item.get('startTime', None), float):
            start_time = datetime.fromtimestamp(
                item['startTime'] - convert_time)
        else:
            continue
        if isinstance(item.get('endTime', None), float):
            end_time = datetime.fromtimestamp(item['endTime'] - convert_time)
        else:
            continue

        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
        data.append({
            'id': contest_id,
            'name': name,
            'link': link,
            'start_time': str_start_time,
            'end_time': str_end_time,
        })

    update_to_db('CS Academy', data)


if __name__ == '__main__':
    main()
