---
title: "三次剩余 - Peralta Method Extension"
date: 2021-07-02 13:07:26
slug: 8c520df7

author: "Kenshin2438"
description: ""
categories:
  - Number Theory
tags:
  - Peralta Method Extension

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

三次剩余，以及一个可以继续推广至k次剩余的随机算法

<!-- more -->
## LiBreOJ #175. 模立方根

> [题目链接](https://loj.ac/p/175)
> 
> **题目描述**
>
> $T$组输入，每组给出$a,p$，求同余方程$x^3 \equiv a \pmod{p}$的任一可行解，若无解则返回`0`。
>
> **数据范围**
>
> $T=10^5$，$p$为奇素数，$p<2^{30},a \in \mathbb{F}_p\setminus \\{0\\}$

## 分析

题目显然是让我们求，若$a$在$p$的3次剩余系中，求出原数。

* 设$k\mid p-1,p-1=kq$，则$a$是模奇素数$p$的一个$k$次剩余的充分必要条件

$$a^q\equiv 1\pmod{p}$$

$\textrm{Proof:}$

必要性：若$a$是$p$的一个$k$次剩余，则存在整数$x$，$(x,p)=1$，满足$x^k\equiv a \pmod{p}$，则$a^q \equiv x^{kq}=x^{p-1} \equiv 1 \pmod{p}$。

充分性：若$a^q\equiv 1\pmod{p}$，$g$是$p$的一个原根，则有$q\,ind_{g}a\equiv 0 \pmod{p-1}$，即有$ind_{g}a\equiv0\pmod{\frac{p-1}{q}}$，得到$k\mid ind_ga$，即$a$是模$p$的一个$k$次剩余。

### 对素数形式的分析

1. $p$为$3n+2$形式的素数：

	由费马小定理：$a^{p}\equiv a\pmod{p}$，即$a^{3n+2}\equiv a\pmod{p}$；同时也有$a^{p-1}\equiv 1\pmod{p}$，即$a^{3n+1}\equiv 1\pmod{p}$。两者相乘得到${(a^{2n+1})}^{3} \equiv a \pmod{p}$。

2. $p$为$3n+1$形式的素数时，解的存在性上面已经讨论了。若有解，我们虽然没有上述那么漂亮的解的形式，但这里有一个绝妙的算法可以解决该问题。

### Peralta Method Extension
[参考资料](https://www.sciencedirect.com/science/article/pii/S0893965902000319)

>The Peralta method is a fast way of computing square roots for a prime of form $p=2^eq+1$ $(q \not\equiv0\mod 2)$ for large $e$.

考虑这样一个环：
$$R=\frac{\mathbb{Z}_p[x]}{x^3-a}=\\{ \alpha+\beta Y+\gamma Y^2 | \alpha,\beta,\gamma\in\mathbb{Z}_p,Y^3=a\\}$$
可知，

对于$z\in R$，即$z=\alpha+\beta Y+\gamma Y^2$，有$z^{p-1}\equiv 1\pmod{p}$

如果$z^{\frac{p-1}{3}}=\beta_0 Y$，则有$(\beta_0 Y)^3\equiv\beta_0^3a\equiv1\pmod{p}$，即$\sqrt[3]{a}\equiv\beta_0^{-1}\pmod{p}$

**算法流程**

> For a prime $p\equiv 1 \mod 3$:
> 
> * Choose $z\in R^*$ at random.
> * Compute $z^(\frac{p-1}{s})=\alpha + \beta Y + \gamma Y^2$.
> * If $\alpha=\gamma=0$, then write($\beta^{-1}\mod p$) otherwise go to Step 1.

随机结果符合条件的概率为$\frac{1}{9}$，所以这个算法的时间复杂度全在快速幂上了。

## Code

```cpp Peralta.cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

inline ll qpow(ll x, ll n, ll mod, ll res = 1) {
	while (n) {
		if (n & 1) res = res * x % mod;
		x = x * x % mod, n >>= 1;
	}
	return res;
}

ll m;
struct F {
	ll s[3];
	F() { s[0] = 1, s[1] = s[2] = 0; }
	F(ll a, ll b, ll c) { s[0] = a, s[1] = b, s[2] = c; }
	void set(ll a, ll b, ll c) { s[0] = a, s[1] = b, s[2] = c; }
} f;

inline F mul(F a, F b, ll mod) {
	ll k[3] = {0, 0, 0};
	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			if (i + j < 3) k[i+j] += a.s[i] * b.s[j] % mod;
			else k[i+j-3] += a.s[i] * b.s[j] % mod * m % mod;
		}
	}
	for (int i = 0; i < 3; i++) k[i] %= mod;
	return F(k[0], k[1], k[2]);
}

inline F qp(F x, ll n, ll mod, F res = {}) {
	while (n) {
		if (n & 1) res = mul(res, x, mod);
		x = mul(x, x, mod), n >>= 1;
	}
	return res;
}

inline ll slove(ll a, ll p) {
	if (a == 0) return p;
	if (a == 1) return 1;
	if (p == 3) return 2;
	if (p % 3 == 2) return qpow(a, 1 + ((p / 3) << 1), p);
	if (qpow(a, (p - 1) / 3, p) ^ 1LL) return 0;

	ll x, t = (p - 1) / 3; 
	m = a;
	while (true) {
		f.set(rand() % p, rand() % p, rand() % p);
		f = qp(f, t, p);
		if (!f.s[0] && !f.s[2] && f.s[1]) return x = qpow(f.s[1], p - 2, p);
	}
	return 0;
}

int main() {
	srand((unsigned)time(nullptr));
	
	int t;
	scanf("%d", &t);
	while (t--) {
		ll a, p;
		scanf("%lld %lld", &a, &p);
		printf("%lld\n", slove((a % p + p) % p, p));
	}
	return 0;
}
```
