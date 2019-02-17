# recent_contests

Recent Contests from frequently used OJs

## Contests.json

返回**还未结束**的比赛列表，其中**至少**包含：

- `name`: 比赛名
- `link`: 跳转到比赛的链接
- `start_time`: 比赛开始时间（UTC+0）
- `end_time`: 比赛结束时间（UTC+0）

注意：比赛的开始时间与结束时间均为 **UTC+0**。

### 参数

**include**

指定包含某 OJ，不提供此参数时返回所有可用数据

```
/contests.json?include=Codeforces&include=LOJ
```

**exclude**

指定不包含某 OJ

```
/contests.json?exclude=CodeChef&exclude=CS%20Academy
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

## 还未支持的 OJ

因为暂时无数据等原因，有些 OJ 暂时没能添加：

- [hihoCoder](https://hihocoder.com/)
- [51nod](https://www.51nod.com/)
- [e-olymp](https://www.e-olymp.com/)
- [UOJ](http://uoj.ac/)

