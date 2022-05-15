---
title: "珂朵莉树 - Chtholly Tree"
date: 2021-09-04 23:54:50
draft: false
slug: f799d70a

author: "Kenshin2438"
description: ""
categories:
  - Data Structure
tags:
  - Chtholly-Tree(ODT)

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

随机数据下十分优秀的处理区间赋值操作的暴力数据结构。

本篇只给出`split`和`assgin`操作的代码，其它更暴力的就不提了，一般的能用的情况下有这两个应该就够了。

<!--more-->

# 基础操作
思路十分清晰简单（暴力），维护一个有序的区间段的集合，每段区间带上其属性。

拆分前用`lower_bound`找到对应的位置，删去中间原来所有的后，再加入新的那段。

注意，`set.erase(begin, end)`为前闭后开，所以在找右端点时应该找`R + 1`。

```cpp
struct ODT {
  map<ll, ll> mp;
  ODT(ll _, ll unit) { mp[_ - 1] = unit; }
  void split(ll x) { mp[x] = prev(mp.upper_bound(x))->se; }
  void assign(ll l, ll r, ll v) {
    split(l), split(r + 1);
    auto it = mp.find(l);
    while (it->fi != r + 1) it = mp.erase(it);
    mp[l] = v;
  }
  ll query(ll l, ll r) {
    split(l), split(r + 1);
    auto it = mp.find(l);
    ll res = 0;
    while (it->fi != r + 1) {
      auto nex = next(it);
      res += it->se * (nex->fi - it->fi);
      it = nex;
    }
    return res;
  }
};
```

# 例题

> [CF915 E. Physical Education Lessons](https://codeforces.com/problemset/problem/915/E)
>
> 多次区间赋值（全变成`0`或`1`），再加上求总和。

```cpp
struct ODT {
  map<ll, ll> mp;
  ll S;
  ODT(ll _, ll unit) { mp[_ - 1] = unit; }
  void split(ll x) { mp[x] = prev(mp.upper_bound(x))->se; }
  void assign(ll l, ll r, ll v) {
    split(l), split(r + 1);
    auto it = mp.find(l);
    while (it->fi != r + 1) {
      S += (next(it)->fi - it->fi) * (v - it->se);
      it = mp.erase(it);
    }
    mp[l] = v;
  }
};

void SingleTest(int TestCase) {
  int n, q; cin >> n >> q;
  ODT tree(1, 1); tree.S = n;
  for (int k, l, r; q--; ) {
    cin >> l >> r >> k;
    tree.assign(l, r, k == 2);
    cout << tree.S << '\n';
  }
}
```
