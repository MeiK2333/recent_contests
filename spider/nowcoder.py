import html
import json
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

from schemas import Contest
from spider.utils import update_platform

def get_divs(url: str):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    divs = (
        soup.find(class_="nk-main")
            .find(class_="platform-mod")
            .find_all(class_="platform-item")
    )
    return divs

def main():
    divs = []
    # 牛客系列赛
    divs += get_divs("https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=13")
    # 高校校赛
    divs += get_divs("https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14")

    data = []

    tz = timezone.utc

    for div in divs:
        json_data = json.loads(html.unescape(div["data-json"]))
        name = json_data["contestName"]
        start_time = datetime.fromtimestamp(json_data["contestStartTime"] / 1000, tz=tz)
        end_time = datetime.fromtimestamp(json_data["contestEndTime"] / 1000, tz=tz)
        contest_id = div["data-id"]
        link = f"https://ac.nowcoder.com/acm/contest/{contest_id}"

        data.append(
            Contest(
                name=name,
                link=link,
                start_time=start_time,
                end_time=end_time,
                contest_id=contest_id,
            )
        )

    update_platform("牛客竞赛", data)


if __name__ == "__main__":
    main()
