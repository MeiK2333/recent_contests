import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost/recent_contests")
platforms = [
    {"source": "51nod", "link": "https://www.51nod.com/"},
    {"source": "AtCoder", "link": "https://atcoder.jp/"},
    {"source": "CodeChef", "link": "https://www.codechef.com/"},
    {"source": "Codeforces", "link": "http://codeforces.com/"},
    {"source": "CSAcademy", "link": "https://csacademy.com/"},
    {"source": "hihoCoder", "link": "https://hihocoder.com/"},
    {"source": "计蒜客", "link": "https://www.jisuanke.com/"},
    {"source": "Kattis", "link": "https://open.kattis.com//"},
    {"source": "LeetCode", "link": "https://leetcode.com/"},
    {"source": "力扣", "link": "https://leetcode-cn.com/"},
    {"source": "LibreOJ", "link": "https://loj.ac/"},
    {"source": "洛谷", "link": "https://www.luogu.com.cn/"},
    {"source": "牛客竞赛", "link": "https://ac.nowcoder.com/"},
]
