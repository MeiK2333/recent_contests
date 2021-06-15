from datetime import datetime, timedelta, timezone

import requests

from schemas import Contest
from spider.utils import update_platform


def main():
    resp = requests.get(
        "https://www.codechef.com/api/list/contests/all?sort_by=END&sorting_order=desc&offset=0"
    )
    present_contests = resp.json()["present_contests"] + resp.json()["future_contests"]
    data = []

    tz = timezone(timedelta(hours=5, minutes=30))

    for item in present_contests:
        start_time = datetime.strptime(
            item["contest_start_date_iso"], "%Y-%m-%dT%H:%M:%S+05:30"
        ).replace(tzinfo=tz)
        end_time = datetime.strptime(
            item["contest_end_date_iso"], "%Y-%m-%dT%H:%M:%S+05:30"
        ).replace(tzinfo=tz)
        code = item["contest_code"]
        data.append(
            Contest(
                contest_id=code,
                link=f"https://www.codechef.com/{code}",
                name=item["contest_name"],
                start_time=start_time,
                end_time=end_time,
            )
        )
    update_platform("CodeChef", data)


if __name__ == "__main__":
    main()
