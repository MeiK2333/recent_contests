from datetime import datetime, timezone

import requests

from schemas import Contest
from spider.utils import update_platform


def main():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 "
        "Safari/537.36 "
    }
    resp = requests.get(
        "https://www.luogu.org/contest/list?page=1&_contentOnly=1", headers=headers
    )
    contests = resp.json()["currentData"]["contests"]["result"]

    data = []

    tz = timezone.utc

    for contest in contests:
        link = f'https://www.luogu.org/contest/{contest["id"]}'
        start_time = datetime.fromtimestamp(contest["startTime"], tz=tz)
        end_time = datetime.fromtimestamp(contest["endTime"], tz=tz)

        data.append(
            Contest(
                name=contest["name"],
                link=link,
                start_time=start_time,
                end_time=end_time,
                contest_id=link.split("/")[-1],
            )
        )

    update_platform("洛谷", data)


if __name__ == "__main__":
    main()
