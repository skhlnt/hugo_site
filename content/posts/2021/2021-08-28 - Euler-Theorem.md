---
title: "欧拉定理（数论） 及其拓展 - Extended Euler Theorem"
date: 2021-08-28 19:47:47
draft: false
slug: b8ca3bb8

author: "Kenshin2438"
description: "欧拉定理及拓展欧拉定理，主要为证明。"
keywords:
  - 数论
  - 欧拉定理
  - 拓展欧拉定理
  - Extended Euler Theorem
categories:
  - Number Theory
tags:
  - (Extended)Euler's Theorem

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

$\forall a<m,(a, m)=1$，均有$a^{\varphi(m)}\equiv1\pmod{m}$，于是就有欧拉定理：

$$a^n\equiv a^{n \mod \varphi(m)} \pmod{m}$$

对于$n$取值较大的情况（比如$10^{30000}\mod 13$），欧拉降幂的作用不可忽视，但局限的是必须满足$(a,m)=1$才能有上式恒成立。

由于上述形式流传甚广，读者大抵早已熟记于心，这里便不再赘述。本文的最终目的是介绍另一个适用范围更广的版本，即所谓拓展欧拉定理。

$$a^n\equiv a^{n \mod \varphi(m) + \varphi(m)} \pmod{m} \quad \textrm{if }n \geq \varphi(m)$$

<!--more-->

## 证明 - 欧拉定理

证明方法来自《初等数论》柯召

---

考虑这样一组数$r_1,r_2,\dots,r_{\varphi(m)}$，满足$\forall r_i\in \set{r_1,r_2,\dots,r_{\varphi(m)}},\mathrm{s.t.}(r_i,m)=1$，同时$\forall i\ne j,(r_i,r_j)=1$。

当$(a,m)=1$，我们可以得到:
$$
\begin{aligned}
(ar_1)(ar_2)\dots(ar_{\varphi(m)}) & \equiv & r_1r_2\dots r_{\varphi(m)}\pmod{m}\newline
(r_1r_2\dots r_{\varphi(m)})\times (a^{\varphi(m)} - 1) & \equiv & 0\pmod{m}
\end{aligned}
$$

由于$(r_i,m)=1$，可知$(r_1r_2\dots r_{\varphi(m)},m)=1$，故$a^{\varphi(m)}\equiv1\pmod{m}$。

## 拓展情况

这里的讨论是基于$(a,m)\ne1$的情况来的，因为当$(a,m)=1$成立时直接用欧拉定理就能推知上式成立。

由于$n=\lfloor\frac{n}{\varphi(m)}\rfloor\times\varphi(m) + \langle n \rangle_{\varphi(m)}\geq\varphi(m)$，不妨令$n=\lambda\varphi(m) + \langle n\rangle_{\varphi(m)},\lambda\in\mathbb{Z}^+$。

问题转换为证明$a^{\lambda\varphi(m)}\equiv a^{\varphi(m)}\pmod m$，这可以从$\lambda=2$的情况递推过去，下面证明$\lambda=2$时同余式成立。

---

> 将$a$因式分解，其中与$m$互素的部分可以直接使用欧拉定理消去，剩余的素数幂乘积分开后的情况和原问题同一结构，所以只考虑单个素数情况即可。原问题等价为证明：$p^{2\times\varphi(m)}\equiv p^{\varphi(m)}\pmod m,p\in Prime$。

+ 当$p\nmid m$时显然成立。

+ 否则，令$p^s \mid\mid m, m=k\times p^s$，显然有$p^{\varphi(m)}\equiv 1\pmod k$，不妨令$p^{\varphi(m)}=kq+1,q\in\mathbb{Z}$。

  + 问题进一步转换为证明$(kq+1)^2\equiv(kq+1)\pmod m$，即证明$kp^s \mid kq\times(kq+1)$
  + 代入$kq+1=p^{\varphi(m)}$，即证明$p^s\mid q\times p^{\varphi(m)}$
  + 由于$\varphi(m)\geq\varphi(p^s)$，只需要证明$\varphi(p^s)=p^{s-1}(p-1)\geq s$

下面是证明：

由**Bernoulli's Inequality**对左式放缩：$p^{s-1}(p-1)\geq(p-1)\times\left[1+(s-1)\times(p-1)\right]$

即证：$(p-1)\times\left[1+(s-1)\times(p-1)\right]-s\geq0$，

$$
\begin{aligned}
LHS &=s(p-2)p-(p^2-3p+2)\newline
&\geq s(p-2)p-(p^2-3p+p)\newline
&=(s-1)(p-2)p\newline
&\geq0=RHS
\end{aligned}
$$

（高考之后就很少碰不等式证明了，手生了2333。其实有更短的证明：$\varphi(p^s)\geq 2^s>s$，上面的证明纯粹是写着好玩。）

## 应用示例

> **链接：https://ac.nowcoder.com/acm/problem/17190 来源：牛客网**
>
> **题目描述**
>
> 给一个长为$n$的序列，$m$次操作，每次操作：
>
> 1. 区间$[l,r]$加$x$
>
> 2. 对于区间$[l,r]$，查询$a[l]^{a[l+1]^{a[l+2]\dots}}\mod p$，一直到$a[r]$  
>
>   请注意每次的模数不同。
>
> **数据范围**
>
> $n , m <= 500000$
>
> 序列中每个数在 $[1,2e9]$ 内，$x <= 2e9 , p <= 2e7$

容易知道，每次考虑取模$\varphi(m)$，接近$\log m$次就能到$1$，也就是说用拓展欧拉定理直接暴力递归即可。

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

const int maxn = 2e7 + 10;

bitset<maxn> ok;
int pr[maxn], cnt;
int phi[maxn];

void init(int n) {
	phi[1] = 1;
	for (int i = 2; i <= n; ++i) {
		if (!ok[i]) phi[pr[++ cnt] = i] = i - 1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; ++j) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) {
				phi[pr[j] * i] = phi[i] * pr[j];
				break;
			} phi[pr[j] * i] = phi[i] * (pr[j] - 1);
		}
	} return ;
}

int n, m, x;
ll d[maxn];
inline void add(int p, ll v) {
	for (; p <= n; p += p & -p) d[p] += v;
}
inline ll query(int p, ll res = 0LL) {
	for (; p; p &= p - 1) res += d[p];
	return res;
}

inline ll qpow(ll x, ll n, ll mod, ll res = 1, ll tag = 0) {
	if (x >= mod) x %= mod, tag = 1;
	while (n) {
		if (n & 1) {
			res = res * x;
			if (res > mod) res = res % mod, tag = 1;
		} n >>= 1;
		x = x * x;
		if (x > mod) x = x % mod, tag = 1;
	} return res + mod * tag;
}

inline ll slove(int l, int r, ll p) {
	ll v = query(l);
	if (l == r || p == 1LL) return (v > p) ? (v % p + p) : (v);
	return qpow(v, slove(l + 1, r, (ll)phi[p]), (ll)p);
}

int main() {
	init(2e7);
	scanf("%d%d", &n, &m);
	for (int i = 1; i <= n; ++i)
		scanf("%d", &x), add(i, x), add(i + 1, -x);
	while (m--) {
		int op, l, r;
		scanf("%d%d%d%d", &op, &l, &r, &x);
		if (op == 1) {
			add(l, x), add(r + 1, -x);
		} else {
			printf("%lld\n", slove(l, r, x) % x);
		}
	}
	return 0;
}
```
