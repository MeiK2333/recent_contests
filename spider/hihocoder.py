from datetime import datetime, timezone
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

from schemas import Contest
from spider.utils import update_platform


def main():
    resp = requests.get("https://hihocoder.com/contests")
    soup = BeautifulSoup(resp.text, "html.parser")

    data = []

    tz = timezone(timedelta(hours=8))

    # 正在进行
    ol1 = soup.find(class_="ongoing")
    # 即将到来
    ol2 = soup.find(class_="upcoming")
    for li in ol1.find_all("li") + ol2.find_all("li"):
        name = li.find(class_="md-summary-cnt").find("a").string.strip()
        link = (
            "https://hihocoder.com" + li.find(class_="md-summary-cnt").find("a")["href"]
        )
        description = li.find(class_="md-summary-cnt").find("p").text.strip()
        times = li.find_all(class_="htzc")
        raw_start_time, raw_end_time = [item.string.strip() for item in times]
        start_time = datetime.strptime(
            raw_start_time, "%Y-%m-%d %H:%M (+0800)"
        ).replace(tzinfo=tz)
        end_time = datetime.strptime(raw_end_time, "%Y-%m-%d %H:%M (+0800)").replace(
            tzinfo=tz
        )

        data.append(
            Contest(
                contest_id=link.split("/")[-1],
                name=name,
                link=link,
                start_time=start_time,
                end_time=end_time,
            )
        )

    update_platform("hihoCoder", data)


if __name__ == "__main__":
    main()
