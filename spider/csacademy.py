from datetime import datetime, timezone

import requests

from schemas import Contest
from spider.utils import update_platform


def main():
    headers = {"x-requested-with": "XMLHttpRequest"}
    resp = requests.get("https://csacademy.com/contests/", headers=headers)
    json_data = resp.json()

    data = []

    tz = timezone.utc

    for item in json_data["state"]["Contest"]:
        if item.get("baseContestId"):
            continue
        contest_id = item["id"]
        name = item["longName"]
        link = "https://csacademy.com/contest/" + item["name"]
        if isinstance(item.get("startTime", None), float):
            start_time = datetime.fromtimestamp(item["startTime"], tz=tz)
        else:
            continue
        if isinstance(item.get("endTime", None), float):
            end_time = datetime.fromtimestamp(item["endTime"], tz=tz)
        else:
            continue

        data.append(
            Contest(
                contest_id=contest_id,
                name=name,
                link=link,
                start_time=start_time,
                end_time=end_time,
            )
        )

    update_platform("CSAcademy", data)


if __name__ == "__main__":
    main()
