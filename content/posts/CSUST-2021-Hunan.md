---
title: "CSUST - 2021 湖南省赛选拔赛"
date: 2021-09-15 00:13:08
draft: false
slug: 233f4181

author: "Kenshin2438"
description: ""
categories:
  - Contest
tags:
  - CSUST

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

[比赛链接](http://acm.csust.edu.cn/contest/158/problems)

（ps: 写题请到`Problems`页面）

可能算详解？代码部分随缘写。

<!-- more -->

# 题解

## A. NO GAMES NO LIFE
> **题目描述**
>
> 共有$n$（偶数）堆棋子，第$i$堆初始为$1 \leq a_i \leq 100$，玩家每次必须选$\frac{n}{2}$堆棋子并使之减少**正整数**个，每次每堆减少的值可以不同。
> `Bai`先手，`Kong`后手。玩家无法选择时失败。

基准思路：

- 谁先导致场上出现被取完的堆必定输掉游戏
- 如果选了`1`则必须减少到`0`

考虑数字`1`的数量，令$cnt[i]$为数字$i$的个数。

- $cnt[1] > \frac{n}{2}$时玩家必选到`1`，必输
- $1 \leq cnt[1] \leq \frac{n}{2}$可以增加`1`的数量使下家面临第一个局面，必胜
- $cnt[1] = 0$时考虑`2`的数量
  - $cnt[2] > \frac{n}{2}$玩家必选到`2`，必然产生`1`，且个数不大于$\frac{n}{2}$，必输
  - $1 \leq cnt[2] \leq \frac{n}{2}$可以增加`2`的数量使下家面临上一个局面，必胜
  - $cnt[2] = 0$时考虑`3`的数量
    - $\dots$

显然，问题只与最小值的数量有关。

## B. 整除数
> **题目描述**
>
> 找到最小的$n$位能被$m$整除的**自然数**

- $n=1$时，直接输出`0`
- 找到最小的$n$位整数$10^{n-1}$，求最少还需多少使得其能被$m$整除，即$(m - 10^{n-1} \% m) \mod m$，如果加上后位数不变则为答案，否则无解。

## C. 网格图
> **题目描述**
> 
> 从$(0,0)$，每次你只可以往正东走，或者往正北走(即x，y坐标增大的方向)。但是你每次走的长度可以是任意**正实数**。这个网格上有$\mathit n$个景点，你可以经过任意个景点，问：以每个景点为终点时，分别能走出多少条不同路线。(当且仅当经过的景点不同时才被视为不同路线) 取模$1e9+7$.

由于是走正实数，某点左下方的所有景点都可以直接到达该点。

比较特殊的是与之处在同一行列的点，这里就只需加上到最近的那个点的方案数。

思路，按照$(x,y)$从小到大排序，只要保证到某点时，所有处于其左下方的点都已经更新答案，那么该点的方案就是它们求和再+1（从$(0,0)$直达）。

同时要维护行列点数目，每次更新答案后再更新即可。

## D. 修机器
> **题目描述**
> 
> $n$个机器，总时间为$T$，修理某机器的时间为$y_i$，收益为$\textrm{修完后剩余时间} \times x_i$，求可能的最大收益。

首先可以明确本题是一个01背包问题，关键在于怎样安排顺序会影响物品价值。

先考虑一个子问题：在恰好能修完的条件下选择$k$个机器，求如何安排其顺序，使之收益最大？

- $k=0,1$收益为$0$。
- $k=2$时，为$\max{x_a \times y_b}$，即取$\frac{x}{y}$更大的在前。
- $k>2$时，每次只考虑最后一个位置，情况可以递推过去，即最后一定是比值最小的。

按照比值$\frac{x}{y}$排序，然后按照背包的基本思路去写就好了。

## E. squares
> **题目描述**
>
> 找出坐标$(0,0)$到$(n,m)$之间由整点构成的正方形的数量，取模$1e9+7$。

简单的思维题，推导在下面的图片上，懒得制图就手写了。

![squares](/images/CSUST-2021-Hunan-squares.png)

## F. 拍照
> **题目描述**
>
> 给定一个$n\times m$的矩阵和一个长$s$的序列$h$，所有元素在$0$到$9$。在矩阵中找连续的长为$s$的连续数组其元素与$h$对应元素的和均不超过$9$。

数字都很小，考虑枚举所有可能的对应序列，使用`hash`或者`kmp`查询数量。

## G. 递增数组2
> **题目描述**
> 
> 给出一个长度为$N$的**严格递增**的数组$A$，一共$K$次操作，每次选择$[L,R]$区间，加上$C$，询问否存在某个$A_i=i(1\leq i \leq n)$。
> 
> **数据范围**
> 
> $1\leq N\leq 10^7,1\leq K\leq 500$

我们把加上相同值的最长连续区间称为**一段操作**，由于$K$极小，所以最终并不会产生很多的段。

又因为初始的数组是有序的，我们只要二分查询每一段中是否有$A_i+C=i$即可。

```cpp
#include <algorithm>
#include <iostream>
#include <cstdio>
#include <set>
#define PII pair<int, int>
#define fi first
#define se second
using namespace std;
typedef long long ll;

const int N = 1e7 + 100;

int n, q;
ll a[N];

struct node {
  int l, r;
  mutable ll v;
  node(int _l, int _r, ll _v) : l(_l), r(_r), v(_v) {}
  bool operator < (const node &o) const {return l < o.l;}
};
set<node> st;
#define si set<node>::iterator

si split(int p) {
    si it = st.lower_bound( node(p, p, 0) );
    if (it != st.end() && it->l == p) return it;
    --it;
    int L = it->l, R = it->r, V = it->v;
    st.erase(it);
    st.insert( node(L, p - 1, V) );
    return st.insert( node(p, R, V) ).fi;
}
void assign(int L, int R, int V) {
    si ed = split(R + 1), be = split(L);
    for (si it = be; it != ed; ++it) it->v += V;
}
bool bs(int l, int r, ll v) {
  bool res = false;
  while (l <= r) {
    int m = (l + r) >> 1;
    if (a[m] + v == 0LL) {res = true; break;}
    if (a[m] + v < 0) l = m + 1;
    else r = m - 1;
  }
  return res;
}
int main() {
  scanf("%d%d", &n, &q);
  for (int i = 1; i <= n; i++)
    scanf("%lld", &a[i]), a[i] -= i;
  st.insert( node(1, n, 0LL) );
  while (q--) {
    int L, R, c;
    scanf("%d%d%d", &L, &R, &c);
    assign(L, R, c);
    bool ans = false;
    for (node x : st)
      if ( bs(x.l, x.r, x.v) ) {ans = true; break;}
    puts(ans ? "YES" : "NO");
  }
  return 0;
}
```

## H. function
> **题目描述**
> 
> 令$F(x)$为数字$x$的数位和，给定$n$，求满足$F(x)+x=n$的所有$n$，升序输出。

由于数位和最大为$9\times \textrm{位数}$，所以可以知道满足条件的$x$很少，直接暴力枚举即可。

## I. 数字游戏
> **题目描述**
>
> 给定两个由数字$0~9$构成的序列$s,t$，每次选定$s$的一个连续区间并将其转成升序，在有限步（可以为$0$）后是否能使得$s,t$相同

将一个连续区间变成升序后是不可逆的，那么每次就只选择两个相邻的数字变成升序以减少影响。

考虑去模拟这个过程，**注意不要真的去移动实际值**，那样的复杂度是不可接受的。

由于数字的种类有限，直接记录每个数字所在的位置，就可以判断当前位置上的所需要的数字是否可以移动到该位置上。

判断方式也很简单，两位置之间没有比它更小的数存在即可移动到所需位置。

所以每次只需要知道该位置（包含在内）之后的每个数字第一次出现的位置，就可以了，考虑使用栈去维护。

```cpp
#include <iostream>
#include <string>
#define str string
using namespace std;

const int N = 1e5 + 10;

str s, t;
int cnt[15], p[15][N];

int main() {
  ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);
  cin >> s >> t;
  int n = s.length();
  for (int i = n - 1; i >= 0; i--) {
    int d = s[i] & 15;
    p[d][++cnt[d]] = i;
  }
  bool ans = true;
  for (char x : t) {
    int d = x & 15;
    if (cnt[d] == 0) {ans = false; break;}
    bool tmp = false;
    for (int i = 0; i < d; i++)
      if (cnt[i] && p[i][cnt[i]] < p[d][cnt[d]]) {
        tmp = true; break;
      }
    if (tmp) {ans = false; break;}
    --cnt[d];
  }
  cout << (ans ? "True" : "False");
  return 0;
}
```

## J. lazy tree
> **题目描述**
>  
> 给出数列${a_n}$，有两种操作
> 
> 1. 选定区间$[l,r]$所有元素加上$v$
> 2. 区间$[l,r]$询问$\sum_{i=l}^{r}\sum_{j=i+1}^{r}a_i\times a_j$，取模$1e9+7$

所求为区间中不重复的两个位置的数对的乘积之和。

$$Query=\frac{(\sum_{i=l}^{r}a_i)^2-\sum_{i=l}^{r}a_i^2}{2}$$

线段树直接维护即可。

```cpp
#include <algorithm>
#include <iostream>
#include <cstdio>
#include <cstring>
#define il inline
using namespace std;
typedef long long ll;

const int N = 1e5 + 100;
const int mod = 1e9 + 7;
const int inv2 = 500000004;

int T;

int n, q;

#define ld nd << 1
#define rd nd << 1 | 1
#define st int s, int t, int nd

struct node {
  ll s1, s2, lz;
} tr[N << 2];

void merge(int nd) {
  tr[nd].s1 = (tr[ld].s1 + tr[rd].s1) % mod;
  tr[nd].s2 = (tr[ld].s2 + tr[rd].s2) % mod;
}
void build(st) {
  tr[nd].lz = 0LL;
  if (s == t) {
    scanf("%lld", &tr[nd].s1);
    tr[nd].s2 = tr[nd].s1 * tr[nd].s1 % mod;
    return ;
  }
  int m = (s + t) >> 1;
  build(s, m, ld), build(m + 1, t, rd), merge(nd);
}
void pushlz(st, ll v) {
  int len = t - s + 1;
  tr[nd].s2 = (tr[nd].s2 + v * v % mod * len % mod) % mod;
  tr[nd].s2 = (tr[nd].s2 + 2LL * tr[nd].s1 % mod * v % mod) % mod;
  tr[nd].s1 = (tr[nd].s1 + v * len % mod) % mod;
  tr[nd].lz = (tr[nd].lz + v) % mod;
}
void downlz(st) {
  int m = (s + t) >> 1;
  pushlz(s, m, ld, tr[nd].lz), pushlz(m + 1, t, rd, tr[nd].lz);
  tr[nd].lz = 0LL;
}
void update(st, int L, int R, ll v) {
  if (L <= s && t <= R) return pushlz(s, t, nd, v);
  if (tr[nd].lz) downlz(s, t, nd);
  int m = (s + t) >> 1;
  if (L <= m) update(s, m, ld, L, R, v);
  if (R > m) update(m + 1, t, rd, L, R, v);
  merge(nd);
}
ll q1(st, int L, int R) {
  if (L <= s && t <= R) return tr[nd].s1;
  if (tr[nd].lz) downlz(s, t, nd);
  int m = (s + t) >> 1;
  ll res = 0LL;
  if (L <= m) res = (res + q1(s, m, ld, L, R)) % mod;
  if (R > m) res = (res + q1(m + 1, t, rd, L, R)) % mod;
  return res;
}
ll q2(st, int L, int R) {
  if (L <= s && t <= R) return tr[nd].s2;
  if (tr[nd].lz) downlz(s, t, nd);
  int m = (s + t) >> 1;
  ll res = 0LL;
  if (L <= m) res = (res + q2(s, m, ld, L, R)) % mod;
  if (R > m) res = (res + q2(m + 1, t, rd, L, R)) % mod;
  return res;
}
ll query(int L, int R) {
  ll s1 = q1(1, n, 1, L, R);
  ll s2 = q2(1, n, 1, L, R);
  return (s1 * s1 % mod - s2 + mod) % mod * inv2 % mod;
}
int main() {
  for (scanf("%d", &T); T--; ) {
    scanf("%d%d", &n, &q);
    build(1, n, 1);
    while (q--) {
      int op, l, r, v;
      scanf("%d", &op);
      if (op == 1) {
        scanf("%d%d%d", &l, &r, &v);
        update(1, n, 1, l, r, v);
      } else {
        scanf("%d%d", &l, &r);
        printf("%lld\n", query(l, r));
      }
    }
  }
  return 0;
}
```

---

# 总结

![Rank](/images/CSUST-2021-Hunan-Rank.png)

虽然侥幸拿了Rank-2，但是鉴于运气成分有点多，还是得加油。

个人认为自己赛中暴露出的问题：

- `心态不稳`。前面一段时间一直发懵（30min才交第一发），结束前修机器那题应该能过的，但后面有点自暴自弃最后一小时基本放弃思考了。
- `动态规划`和`贪心`这块太薄弱了。
- 手速太慢了。。。
