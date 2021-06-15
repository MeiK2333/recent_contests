from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

from schemas import Contest
from spider.utils import update_platform


def main():
    resp = requests.get("https://contest-archive.loj.ac/contests/")
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")

    data = []

    tz = timezone(timedelta(hours=8))

    for tr in table.find("tbody").find_all("tr"):
        tds = tr.find_all("td")
        name = tds[0].find("a").text.strip()
        link = "https://contest-archive.loj.ac" + tds[0].find("a")["href"]
        raw_start_time = tds[1].string.strip()
        raw_end_time = tds[2].string.strip()
        start_time = datetime.strptime(raw_start_time, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=tz
        )
        end_time = datetime.strptime(raw_end_time, "%Y-%m-%d %H:%M:%S").replace(
            tzinfo=tz
        )

        description = tds[3].text.strip()

        data.append(
            Contest(
                name=name,
                link=link,
                start_time=start_time,
                end_time=end_time,
                contest_id=link.split("/")[-1],
            )
        )
    update_platform("LibreOJ", data)


if __name__ == "__main__":
    main()
