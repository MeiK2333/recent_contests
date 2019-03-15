from datetime import datetime, timedelta

import requests

from db import update_to_db


def main():
    url = 'https://www.51nod.com/Contest/ContestList?type=2'
    resp = requests.get(url)

    data = []

    convert_time = timedelta(hours=8)

    for contest in resp.json()['ContestViews']:
        contest_id = contest['Id']
        link = f'https://www.51nod.com/Contest/ContestDescription.html#contestId={contest_id}'
        desc = contest['Contest']['Description']
        name = contest['Contest']['Title']
        start_time = datetime.fromtimestamp(
            contest['Contest']['StartTime'] // 1000)
        end_time = datetime.fromtimestamp(
            contest['Contest']['EndTime'] // 1000)
        start_time -= convert_time
        end_time -= convert_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'link': link,
            'desc': desc
        })

    update_to_db('51nod', data)


if __name__ == '__main__':
    main()
