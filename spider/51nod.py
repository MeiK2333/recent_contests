from datetime import datetime, timedelta, timezone

import requests

from schemas import Contest
from spider.utils import update_platform


def main():
    url = "https://www.51nod.com/Contest/ContestList"
    resp = requests.get(url)

    # 51nod 所在时区 utc+8
    tz = timezone(timedelta(hours=8))

    data = []
    for item in resp.json()["ContestViews"]:
        contest_id = str(item["Id"])
        link = f"https://www.51nod.com/Contest/ContestDescription.html#contestId={contest_id}"
        desc = item["Contest"]["Description"]
        name = item["Contest"]["Title"]
        start_time = datetime.fromtimestamp(item["Contest"]["StartTime"] // 1000, tz=tz)
        end_time = datetime.fromtimestamp(item["Contest"]["EndTime"] // 1000, tz=tz)
        data.append(
            Contest(
                contest_id=contest_id,
                name=name,
                link=link,
                start_time=start_time,
                end_time=end_time,
            )
        )
    update_platform("51nod", data)


if __name__ == "__main__":
    main()
