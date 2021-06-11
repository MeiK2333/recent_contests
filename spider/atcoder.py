from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

from schemas import Contest
from spider.utils import update_platform


def main():
    resp = requests.get("https://atcoder.jp/contests/")
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find_all("table")[1]

    data = []

    tz = timezone(timedelta(hours=9))

    for tr in table.find("tbody").find_all("tr"):
        tds = tr.find_all("td")
        raw_start_time = tds[0].find("time").string
        start_time = datetime.strptime(
            raw_start_time, "%Y-%m-%d %H:%M:%S+0900"
        ).replace(tzinfo=tz)
        name = tds[1].find("a").string
        link = "https://atcoder.jp" + tds[1].find("a")["href"]
        length = tds[2].string.strip()
        hours, minutes = length.split(":")
        length_time = timedelta(hours=int(hours), minutes=int(minutes))
        end_time = start_time + length_time
        contest_id = link.split("/")[-1]

        data.append(
            Contest(
                name=name,
                link=link,
                start_time=start_time,
                end_time=end_time,
                contest_id=contest_id,
            )
        )

    update_platform("AtCoder", data)


if __name__ == "__main__":
    main()
