from datetime import datetime, timedelta

import requests

from db import update_to_db


def main():
    resp = requests.get(
        "https://www.codechef.com/api/list/contests/all?sort_by=END&sorting_order=desc&offset=0"
    )
    present_contests = resp.json()["present_contests"]
    data = []

    convert_time = timedelta(hours=5, minutes=30)

    for item in present_contests:
        start_time = datetime.strptime(
            item["contest_start_date_iso"], "%Y-%m-%dT%H:%M:%S+05:30"
        )
        start_time -= convert_time
        end_time = datetime.strptime(
            item["contest_end_date_iso"], "%Y-%m-%dT%H:%M:%S+05:30"
        )
        end_time -= convert_time
        code = item["contest_code"]
        data.append(
            {
                "id": code,
                "link": f"https://www.codechef.com/{code}",
                "name": item["contest_name"],
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    update_to_db("CodeChef", data)


if __name__ == "__main__":
    main()
