from datetime import datetime, timedelta, timezone

import requests

from schemas import Contest
from spider.utils import update_platform


def main():
    resp = requests.post(
        "https://leetcode-cn.com/graphql",
        json={
            "operationName": None,
            "variables": {},
            "query": "{\n  brightTitle\n  allContests {\n    containsPremium\n    title\n    cardImg\n    titleSlug\n "
            "description\n    startTime\n    duration\n    originStartTime\n    isVirtual\n    company {\n      "
            "watermark\n      __typename\n    }\n    __typename\n  }\n}\n ",
        },
    )

    contests = resp.json()["data"]["allContests"]

    data = []

    for contest in contests:
        if contest["isVirtual"]:
            continue
        start_time = datetime.utcfromtimestamp(contest["startTime"]).replace(tzinfo=timezone.utc)
        name = contest["title"]
        link = "https://leetcode-cn.com/contest/" + contest["titleSlug"]
        length_time = timedelta(seconds=contest["duration"])
        end_time = start_time + length_time
        data.append(
            Contest(
                name=name,
                start_time=start_time,
                end_time=end_time,
                link=link,
                contest_id=name,
            )
        )

    update_platform("力扣", data)


if __name__ == "__main__":
    main()
