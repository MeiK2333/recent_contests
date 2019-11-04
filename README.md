# recent_contests

Recent Contests from frequently used OJs.

WEB API 配置了允许跨域访问，您可以直接引用本数据源，但请注明数据来源。

## 本地部署

```bash
$ docker-compose up -d
```

服务将在 `8001` 端口以 WEB 的方式启动。如果想要使用自定义的端口，请修改 `docker-compose.yml` 中的相关设置。

爬虫将每小时运行一次，如果想要主动执行，可以 `exec` 至 `spider` 中执行 `python spider.sh`。

## Contests.json

返回**还未结束**的比赛列表，其中**至少**包含：

- `source`: 比赛平台
- `name`: 比赛名
- `link`: 跳转到比赛的链接
- `start_time`: 比赛开始时间（UTC+0）
- `end_time`: 比赛结束时间（UTC+0）
- `hash`: `source + name + link + start_time + end_time` 的 MD5 哈希值

注意：比赛的开始时间与结束时间均为 **UTC+0**。

### 参数

**include**

指定包含某 OJ，不提供此参数时返回所有可用数据

```
/contests.json?include=Codeforces&include=LOJ
/contests.json?include[]=Codeforces&include[]=LOJ
```

**exclude**

指定不包含某 OJ

```
/contests.json?exclude=CodeChef&exclude=CS%20Academy
/contests.json?exclude[]=CodeChef&exclude[]=CS%20Academy
```

`include` 与 `exclude` 可以同时使用，但不保证效果。

## 已经支持的 OJ

- [Codeforces](https://codeforces.com/)
- [CodeChef](https://www.codechef.com/)
- [Kattis](https://open.kattis.com/)
- [AtCoder](https://atcoder.jp/)
- [计蒜客](https://www.jisuanke.com/)
- [牛客网](https://www.nowcoder.com/)
- [LOJ](https://loj.ac/)
- [CS Academy](https://csacademy.com/)
- [hihoCoder](https://hihocoder.com/)
- [LeetCode](https://leetcode.com/)
- [洛谷](https://www.luogu.org/)
- [51nod](https://www.51nod.com/)

## 还未支持的 OJ

因为无数据等原因，有些 OJ 暂时没能添加：

- [UOJ](http://uoj.ac/)
- [HackerRank](https://www.hackerrank.com)

## 支持新的 OJ / 新功能建议 / Bug 反馈

请创建一个 [Issues](https://github.com/MeiK2333/recent_contests/issues) 来反馈您的意见。
