---
title: "珂朵莉树 - Chtholly Tree"
date: 2021-09-04 23:54:50
draft: true
slug: f799d70a

author: "Kenshin2438"
description: ""
categories:
  - Data Structure
tags:
  - 珂朵莉树

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

<!-- more -->

# 基础操作
思路十分清晰简单（暴力），维护一个有序的区间段的集合，每段区间带上其属性。

拆分前用`lower_bound`找到对应的位置，删去中间原来所有的后，再加入新的那段。

注意，`set.erase(begin, end)`为前闭后开，所以在找右端点时应该找`R + 1`。

```cpp
struct node {
	int l, r;
	mutable int v;
	node(int _l, int _r, int _v) : l(_l), r(_r), v(_v) {}
	bool operator < (const node & o) const { return l < o.l; }
};

set<node> tr;
#define si set<node>::iterator

si split(int p) {
	si it = tr.lower_bound(node(p, p, '\0'));
	if (it != tr.end() && it->l == p) return it;
	--it;
	int L = it->l, R = it->r, V = it->v;
	tr.erase(it);
	tr.insert(node(L, p - 1, V));
	return tr.insert(node(p, R, V)).fi;
}

void assign(int L, int R, int V) {
	si ed = split(R + 1), be = split(L);

	// do something

	tr.erase(be, ed);
	tr.insert(node(L, R, V));
}
```

# 例题
> [Physical Education Lessons](https://codeforces.com/problemset/problem/915/E)
>
> 多次区间赋值（全变成`0`或`1`），再加上求总和。

```cpp
#include <bits/stdc++.h>
#define PII pair<int, int>
#define PLL pair<i64, i64>
#define il inline
#define pc putchar
#define gc getchar
#define vec vector
#define eb emplace_back
#define pb push_back
#define ps push
#define fi first
#define se second
#define mp make_pair
#define ld nd << 1
#define rd nd << 1 | 1
#define fin freopen("_.in", "r", stdin), freopen("_.out", "w", stdout)
#define fast ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0)
using namespace std;

typedef long long i64;
typedef unsigned long long u64;

const int N = 2e5 + 10;
const int M = 3e5 + 10;
const int mod = 1e9 + 7;

int T;

int n, q, sum;

struct node {
	int l, r;
	mutable int v;
	node(int _l, int _r, int _v) : l(_l), r(_r), v(_v) {}
	bool operator < (const node & o) const { return l < o.l; }
};

set<node> tr;
#define si set<node>::iterator

si split(int p) {
	si it = tr.lower_bound(node(p, p, '\0'));
	if (it != tr.end() && it->l == p) return it;
	--it;
	int L = it->l, R = it->r, V = it->v;
	tr.erase(it);
	tr.insert(node(L, p - 1, V));
	return tr.insert(node(p, R, V)).fi;
}

void assign(int L, int R, int V) {
	si ed = split(R + 1), be = split(L);

	int tmp = 0;
	for (si it = be; it != ed; ++it)
		tmp += it->v * (it->r - it->l + 1);
	sum = sum - tmp + (R - L + 1) * V;

	tr.erase(be, ed);
	tr.insert(node(L, R, V));
}

int main() {
	scanf("%d%d", &n, &q);
	tr.insert(node(1, sum = n, 1));
	while (q--) {
		int l, r, op;
		scanf("%d%d%d", &l, &r, &op);
		assign(l, r, op == 1 ? 0 : 1);
		printf("%d\n", sum);
	}
	return 0;
}
```
