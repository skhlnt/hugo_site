---
title: "吉老师线段树 - Segment tree Beats"
draft: true
date: 2021-09-07 23:43:34
slug: ef1abe7a

author: "Kenshin2438"
description: ""
categories:
  - Data Structure
tags:
  - 吉老师线段树

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

很抱歉的是，关于吉老师线段树历史最值问题本文**尚**并未涉及。

（~~开个新坑~~）

只是最近写题时觉得它让我对线段树的使用有了新的理解，故做记录。

<!--more-->
# 我的理解
吉老师线段树不同于朴素线段树的地方在其维护方式，在维护**区间最大（小）值**的同时维护了**严格次大（小）值**。

这使其对某些问题有着几近玄学的复杂度。。。

一部分使用标记，另一部分使用暴力修改，单次修改变成了$O(\log^2 n)$。

初次看到时，我是真的无法接受，~~并且将其作为假算法略过了~~（顺带一提，我当时在写下面贴的模板题时考虑维护**最大，最小值**TLE了）

然后上次ccpc压力测试赛上**又**碰见了[Lowbit](http://acm.hdu.edu.cn/showproblem.php?pid=7116)，写的时候突然发觉这其实是个很朴素的想法，一部分考虑暴力从而减少整体的复杂度（算是均摊？）。

线段树维护值时怎么就不能用呢？

# 题目
> [HDU5306 Gorgeous Sequence](http://acm.hdu.edu.cn/showproblem.php?pid=5306)
>
> **题目描述**
>
> 0. x y t: For every $x≤i≤y$, we use min(ai,t) to replace the original ai's value.
> 1. x y: Print the maximum value of ai that $x≤i≤y$.
> 2. x y: Print the sum of ai that $x≤i≤y$.

知道思路后，题目就太板子了，懒得重写了（将就看，不会真有人看吧，不会吧，不会吧）

```cpp
#include <cstdio>
typedef long long i64;
#define gc() (p1 == p2 ? (p2 = buf + fread(p1 = buf, 1, 1 << 20, stdin), p1 == p2 ? EOF : *p1++) : *p1++)
#define read() ({ register int x = 0, f = 1; register char c = gc(); while(c < '0' || c > '9') { if (c == '-') f = -1; c = gc();} while(c >= '0' && c <= '9') x = x * 10 + (c & 15), c = gc(); f * x; })
#define pc(x) (p - puf == 1 << 20 ? (fwrite(puf, 1, 1 << 20, stdout), p = puf) : 0, *p++ = x)
#define print(x, b) ({ pt(x), pc(b); })
char buf[1 << 20], *p1, *p2, puf[1 << 20], *p = puf;
int pt(i64 x) { return x <= 9 ? pc(x + '0') : (pt(x / 10), pc(x % 10 + '0')); }

const int N = 1e6 + 10;

int T;
inline void down(int s, int t, int nd);

inline i64 min(i64 a, i64 b) { return a < b ? a : b; }
inline i64 max(i64 a, i64 b) { return a > b ? a : b; }
inline void swap(int & a, int & b) { a ^= b ^= a ^= b; }

#define ld nd << 1
#define rd nd << 1 | 1

struct node {
	i64 mx, sm, lz, mxx, num;
	void set(i64 x) { sm = mx = x, num = 1, mxx = -1; }
} tr[N << 2];

inline void merge(int nd) {
	int l = ld, r = rd;
	tr[nd].sm = tr[l].sm + tr[r].sm;
	if (tr[l].mx == tr[r].mx) {
		tr[nd].mx = tr[l].mx, tr[nd].num = tr[l].num + tr[r].num;
		tr[nd].mxx = max(tr[l].mxx, tr[r].mxx);
	} else {
		if (tr[l].mx < tr[r].mx) swap(l, r);
		tr[nd].mx = tr[l].mx, tr[nd].num = tr[l].num;
		tr[nd].mxx = max(tr[r].mx, tr[l].mxx);
	}
}
inline void build(int s, int t, int nd) {
	tr[nd].lz = -1;
	if (s == t) { tr[nd].set( read() ); return; }
	int m = s + t >> 1;
	build(s, m, ld), build(m + 1, t, rd), merge(nd);
}
inline void pushlz(int s, int t, int nd, i64 v) {
	if (~tr[nd].lz && tr[nd].lz <= v) return ;
	if (tr[nd].mx <= v) return ;

	tr[nd].lz = v;
	if (tr[nd].mxx < v) {
		tr[nd].sm -= tr[nd].num * (tr[nd].mx - v), tr[nd].mx = v;
	} else down(s, t, nd), merge(nd);
}
inline void down(int s, int t, int nd) {
	int m = s + t >> 1;
	pushlz(s, m, ld, tr[nd].lz), pushlz(m + 1, t, rd, tr[nd].lz);
	tr[nd].lz = -1;
}
inline void update(int s, int t, int nd, i64 v, int R, int L) {
	if (R < s || t < L) return ;
	if (L <= s && t <= R) return pushlz(s, t, nd, v);

	if (~tr[nd].lz) down(s, t, nd);

	int m = s + t >> 1;
	if (L <= m) update(s, m, ld, v, R, L);
	if (R >  m) update(m + 1, t, rd, v, R, L);
	merge(nd);
}
inline i64 S(int s, int t, int nd, int R, int L) {
	if (L <= s && t <= R) return tr[nd].sm;

	if (~tr[nd].lz) down(s, t, nd);

	int m = s + t >> 1;
	i64 res = 0;
	if (L <= m) res += S(s, m, ld, R, L);
	if (R >  m) res += S(m + 1, t, rd, R, L);
	return res;
}
inline i64 M(int s, int t, int nd, int R, int L) {
	if (L <= s && t <= R) return tr[nd].mx;

	if (~tr[nd].lz) down(s, t, nd);

	int m = s + t >> 1;
	i64 res = 0LL;
	if (L <= m) res = max(res, M(s, m, ld, R, L));
	if (R >  m) res = max(res, M(m + 1, t, rd, R, L));
	return res;
}

int main() {
	T = read();
	while (T--) {
		int n = read(), q = read();
		build(1, n, 1);
		while (q--) {
			switch (read()) {
				case 0: update(1, n, 1, read(), read(), read()); break;
				case 1: print(M(1, n, 1, read(), read()), '\n'); break;
				case 2: print(S(1, n, 1, read(), read()), '\n'); break;
			}
		}
	} fwrite(puf, 1, p - puf, stdout);
	return 0;
}
```

> [HDU7116 Lowbit](http://acm.hdu.edu.cn/showproblem.php?pid=7116)
>
> **题目描述**
>
> + 1 L R, add lowbit(ai) to each ai in the interval [L,R].
> + 2 L R, query the sum of the numbers in the interval [L,R].

考虑加上`lowbit`时的效果，数字最低位的`bit-1`不断左移，事实上最终将变成`2^k`的形式。

那么之后的情况就十分简单了，只需要将值左移一位。

思路：大胆暴力处理前面的部分直至其变成`2^k`，如果整个区间均为`2^k`那么只要将整体乘2即可。

```cpp
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <queue>
#include <stack>
#include <vector>
using namespace std;

typedef long long i64;

const int mod = 998244353;
const int N = 1e5 + 10;

int n, q, T;

i64 tr[N << 2], tg[N << 2];
int l[N << 2], r[N << 2];
bool is[N << 2];

#define ld nd << 1
#define rd nd << 1 | 1

inline i64 low(i64 x) { return x & -x; }
inline void merge(int nd) {
	tr[nd] = (tr[ld] + tr[rd]) % mod;
	is[nd] = is[ld] && is[rd];
}
inline void build(int s, int t, int nd) {
	l[nd] = s, r[nd] = t, tg[nd] = 1LL;
	if (s == t) {
		cin >> tr[nd];
		is[nd] = tr[nd] == low(tr[nd]);
		return;
	}
	int m = (s + t) >> 1;
	build(s, m, ld), build(m + 1, t, rd), merge(nd);
}
inline void downlz(int nd) {
	tr[ld] *= tg[nd], tr[ld] %= mod;
	tr[rd] *= tg[nd], tr[rd] %= mod;

	tg[ld] *= tg[nd], tg[ld] %= mod;
	tg[rd] *= tg[nd], tg[rd] %= mod;

	tg[nd] = 1LL;
}
inline void update(int nd, int L, int R) {
	if (L > r[nd] || R < l[nd]) return;
	if (L <= l[nd] && r[nd] <= R && is[nd]) {
		tr[nd] <<= 1, tr[nd] %= mod;
		tg[nd] <<= 1, tg[nd] %= mod;
		return;
	}
	if (l[nd] == r[nd]) {
		tr[nd] += low(tr[nd]);
		is[nd] = tr[nd] == low(tr[nd]);
		return;
	}
	if (tg[nd] ^ 1LL) downlz(nd);
	update(ld, L, R), update(rd, L, R), merge(nd);
}
inline i64 S(int nd, int L, int R) {
	if (L > r[nd] || R < l[nd]) return 0;
	if (L <= l[nd] && r[nd] <= R) return tr[nd];
	if (tg[nd] ^ 1LL) downlz(nd);
	return ( S(ld, L, R) + S(rd, L, R) ) % mod;
}
int main() {
	ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);
	for (cin >> T; T--;) {
		cin >> n;
		build(1, n, 1);
		for (cin >> q; q--;) {
			int op, L, R;
			cin >> op >> L >> R;
			if (op == 1)
				update(1, L, R);
			else
				cout << S(1, L, R) << '\n';
		}
	}
	return 0;
}
```

# 参考资料

+ CSDN上有人传了吉老师的课件
+ [OI-Wiki](https://oi-wiki.org/ds/seg-beats/)
