---
title: "一类同余方程的解法 - BSGS"
date: 2021-09-05 11:02:17
draft: true
slug: 4fd858f9

author: "Kenshin2438"
description: ""
categories:
  - Number Theory
tags:
  - BSGS

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

> Baby Step, Giant Step

解决这样一类同余方程的方法

$$a^x \equiv b\pmod c$$

结合原根的知识还能解决模数有原根的$N$次剩余问题

$$x^n \equiv b\pmod c$$

<!-- more -->

# 基础问题 $a^x\equiv b\pmod c$
具体来说，`BSGS`的思路就是`分块预处理`+`hash`。

下面分情况讨论：

## 一、$(a,c)=1$
由欧拉定理可知$x$的取值范围不会大于$\varphi(c)$，我们直接取$x<c$即可。

$a,c$互素时，存在$a$模$c$意义下的逆元。

令分块的大小为$\lceil\sqrt c\rceil$，即我们将解的形式限定为$x=A\times\lceil\sqrt c\rceil - B,A,B\in[0,\lceil\sqrt c\rceil]$，直接将$a^B$的部分放到同余式右侧。

现在需要解决的问题变成：

$$a^{A\times\lceil\sqrt c\rceil}\equiv b\times a^{B}\pmod c$$

+ 首先预处理，枚举$b\times a^B$的取值，并将其存下来(`hash`)
+ 枚举$A$的取值，并查看是否存在对应的$B$是得两侧相等。
+ 得到结果，或者无解。

## 二、$(a,c)\neq 1$
一个比较好的想法是，我们将其转换成互素的情况。

由于$ax\equiv b\pmod c, g=\gcd(a, b, c)$可以转化成
$$\frac{a}{g}x\equiv \frac{b}{g}\pmod{\frac{c}{g}}$$

同样的，我们也可以不断去消去$c$中与$a$不互素的部分，从而达到目的

具体步骤为：

+ $a\times a^{x-1}\equiv b\pmod c$
+ $g=(a,c)$，若$g\nmid b$则无解
+ $\frac{a}{g}\times a^{x-1}\equiv \frac{b}{g}\pmod{\frac{c}{g}}$
+ 循环操作直到$(a,c)=1$或$\frac{a^k}{G}=\frac{b}{G}$

## 代码模板
```cpp
map<ll, ll> bs;
inline ll BSGS(ll a, ll b, ll p) { // (a, p) = 1
	if (b == 1 || p == 1) return 0;
	ll m = sqrt(p) + 1; bs.clear();
	for (ll k = 0, t = b; k <= m; k ++, t = mul(t, a, p)) bs[t] = k;
	for (ll x = 1, t = qpow(a, m, p), base = t; x <= m; x ++, t = mul(t, base, p)) 
		if (bs.count(t)) return ((x * m - bs[t]) % p + p) % p;
	return -1;
}

inline ll exBSGS(ll a, ll b, ll c) {
	a %= c, b %= c;
	if (b == 1 || c == 1) return 0;
	ll g = __gcd(a, c), k = 0, t = 1, res;
	while (g ^ 1LL) {
		if (b % g) return -1;
		c /= g, b /= g, t = mul(t, (a / g), c), k ++;
		if (t == b) return k;
		g = __gcd(a, c);
	}
	b = b * inv(t, c) % c, res = BSGS(a, b, c);
	return ~res ? res + k : res;
}
```

## 例题

看我在CSDN发的那篇吧。

[传送门](https://blog.csdn.net/qq_41743740/article/details/118946068)

# $N$次剩余问题（离散对数）

要求模数要有原根，令为$g$。

+ 两侧取离散对数得到$N\log x\equiv \log b\pmod{\varphi(c)}$
+ 求出右侧$\log b$，即求$g^y\equiv b\pmod c$
+ 现在转换为一次同余式的求解

## 例题代码(TODO)

最小原根的大小会比较小，暴力去枚举求就可以。

暂时口嗨一下算法，等碰见了再来更新。

TODO: 原根，k次剩余题目加代码