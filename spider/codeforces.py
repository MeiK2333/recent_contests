from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

from schemas import Contest
from spider.utils import update_platform


def main():
    resp = requests.get("https://codeforces.com/contests")
    soup = BeautifulSoup(resp.text, "html.parser")
    tables = soup.find_all("table")
    trs = tables[0].find_all("tr")

    data = []
    tz = timezone(timedelta(hours=3))

    for tr in trs[1:]:
        contest_id = tr["data-contestid"]
        tds = tr.find_all("td")
        name = tds[0].text.split("\n")[1].strip()

        raw_start_time = tds[2].find("span").string.strip()
        start_time = datetime.strptime(raw_start_time, "%b/%d/%Y %H:%M").replace(
            tzinfo=tz
        )
        length = tds[3].string.strip()
        if length.count(":") == 1:
            hours, minutes = length.split(":")
            length_time = timedelta(hours=int(hours), minutes=int(minutes))
        elif length.count(":") == 2:
            days, hours, minutes = length.split(":")
            length_time = timedelta(
                days=int(days), hours=int(hours), minutes=int(minutes)
            )
        else:
            length_time = timedelta()
        end_time = start_time + length_time
        register_a = tds[5].find_all("a")
        if register_a:
            register_link = "https://codeforces.com" + register_a[0]["href"]
        else:
            register_link = "https://codeforces.com/contests"
        data.append(
            Contest(
                contest_id=contest_id,
                name=name,
                start_time=start_time,
                end_time=end_time,
                link=register_link,
            )
        )
    update_platform("Codeforces", data)


if __name__ == "__main__":
    main()
