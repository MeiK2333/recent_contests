from datetime import datetime, timezone
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

from schemas import Contest
from spider.utils import update_platform


def main():
    resp = requests.get("https://nanti.jisuanke.com/contest")
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table")

    data = []

    tz = timezone(timedelta(hours=8))

    for tr in table.find("tbody").find_all("tr"):
        tds = tr.find_all("td")
        status = tds[6].text.strip()
        contest_type = tds[0].string.strip()
        name = tds[1].find("a").attrs['title']
        link = "https:" + tds[1].find("a")["href"]
        raw_start_time = tds[3].string.strip()
        length = tds[4].string.strip()
        hours, minutes = length.split("\n")
        hours = hours.strip().split()[0]
        minutes = minutes.strip().split()[0]
        length_time = timedelta(hours=int(hours), minutes=int(minutes))
        start_time = datetime.strptime(raw_start_time, "%Y-%m-%d %H:%M").replace(
            tzinfo=tz
        )
        end_time = start_time + length_time

        data.append(
            Contest(
                name=name,
                start_time=start_time,
                end_time=end_time,
                link=link,
                contest_id=link.split("/")[-1],
            )
        )

    update_platform("计蒜客", data)


if __name__ == "__main__":
    main()
