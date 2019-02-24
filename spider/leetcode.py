from datetime import datetime, timedelta

import requests

from db import update_to_db


def main():
    resp = requests.post('https://leetcode.com/graphql', json={
        "operationName": None,
        "variables": {},
        "query": "{\n  brightTitle\n  allContests {\n    containsPremium\n    title\n    cardImg\n    titleSlug\n    description\n    startTime\n    duration\n    originStartTime\n    isVirtual\n    company {\n      watermark\n      __typename\n    }\n    __typename\n  }\n}\n"
    })

    contests = resp.json()['data']['allContests']

    data = []

    convert_time = timedelta(hours=8)

    for contest in contests:
        if contest['isVirtual']:
            continue
        start_time = datetime.fromtimestamp(contest['startTime'])
        start_time -= convert_time
        name = contest['title']
        link = 'https://leetcode.com/contest/' + contest['titleSlug']
        length_time = timedelta(seconds=contest['duration'])
        end_time = start_time + length_time
        str_start_time = start_time.strftime('%Y-%m-%d %H:%M:%S')
        str_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data.append({
            'name': name,
            'start_time': str_start_time,
            'end_time': str_end_time,
            'link': link
        })

    update_to_db('LeetCode', data)


if __name__ == '__main__':
    main()
