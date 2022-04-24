---
title: "组合数取模 - Lucas/exLucas"
date: 2021-07-24 22:03:03
slug: e874bcb3
lastmod: 2022-01-19 10:22:32

author: "Kenshin2438"
description: ""
categories:
  - Number Theory
tags:
  - Lucas/exLucas

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

{{< admonition info "info" true >}}
Update at 2022.1.19 修正`FastMod`代码来源。
{{< /admonition >}}

证明和代码分开，可以根据自己的需要跳转。

<!--more-->

## Lucas定理

$${n \choose m} \mod p = {\lfloor \frac{n}{p} \rfloor \choose \lfloor \frac{m}{p} \rfloor} {\langle n \rangle _p \choose \langle m \rangle _p} \mod p$$

上式当$p$为素数时成立。

此时，若$p$为一个较小的素数，而$n,m$为一个较大的数（指不能直接通过预处理阶乘及其逆元的大数，比如$1e18$），那么我们就可以递归地求解该结果。

```cpp Lucas
inline ll func(ll n, ll m, ll p, ll res = 1LL) {
	if (n < m) return 0;
	while (m) res = res * C(n % p, m % p) % p, n /= p, m /= p;
	return res;
}
```

根据上述代码，我们只要预处理出$p$以内的阶乘及其逆元即可，时间复杂度$O(p+\log{m})$。

## 证明

> 其实在上面的递归过程已经提示了一件事：$p$进制分解。

考虑$n,m$在$p$进制的表达式

$$n=\sum_{i=0}^{k}{a_kp^k},m=\sum_{i=0}^{k}{b_kp^k}$$

那么`Lucas`定理实际就是：

$${n \choose m}\equiv{a_0 \choose b_0}{a_1 \choose b_1}\dots{a_k \choose b_k}\pmod{p}$$

现在先来看一个简单的式子：

$$(a+b)^p=\sum_{i=0}^{p}{p \choose i}a^ib^{p-i}\equiv{a^p+b^p}\pmod{p}$$

因为其余的部分都有因子$p$

那么我们可以得到：

$$(1+x)^n\equiv(1+x)^{\sum a_ip^i}\equiv\prod(1+x^{p^i})^{a_i}\pmod{p}$$

现在考虑$x^m$的系数，左边是${n \choose m}$，右边是$\prod{a_i \choose b_i}$，已经是`Lucas`的表达式啦。

## 拓展问题
如果上式中$p$为合数，同时$n,m$依旧很大，怎么求解呢？

由**中国剩余定理**可以知道，

如果合数$p$的唯一分解为$\prod_{i=1}^{s}{p_i}^{\alpha_i}$，则有：
$$x \equiv {n \choose m} \pmod{p} \Rightarrow
\begin{cases}
x & \equiv & {n \choose m} \pmod{p_1^{\alpha_1}} \\\\
x & \equiv & {n \choose m} \pmod{p_2^{\alpha_2}} \\\\
  & \vdots & \\\\
x & \equiv & {n \choose m} \pmod{p_s^{\alpha_s}} \\\\
\end{cases}$$

所以只要求出$p$的**唯一分解**，再分别解出各个同余式，通过**CRT**合并答案就能完成全部解答。

现在的问题就转变为，如何求出${n \choose m} \mod {p_i}^{\alpha_i}$。

我们知道${n \choose m}=\frac{n!}{m!(n-m)!}$，如果$m!$与$p^{\alpha}$互素，那么只要拓展欧几里得求出阶乘逆元就能直接算出结果。但是，先不论$n,m$的大小是否支持我们直接求出阶乘。它们是否互素呢？显然是否定的。

不过，如果能分离出不互素的部分和互素的部分，我们可以就求逆元得到答案了。

注意到，$p^{\alpha}$只有一种质因子$p$，那么阶乘中与之不互素的部分显然都是与$p$不互素的。这种不互素的数的个数也可以轻松算出，即${pot_p(n!)}={\sum_{i=1}^{\infty}{\lfloor \frac{n}{p^i} \rfloor}}$。然后在模$p^{\alpha}$意义下所有数在$Z_{p^{\alpha}}$中，（**注意$p^{\alpha}$比较小**）也就是说大于$p^{\alpha}$的数通过取模必然在$[0,p-1]$中，且很容易知道这样的数是循环出现的。

所以现在的思路就是，预处理$p^{\alpha}$内所有与$p$互素的数的乘积（令为$base$），那么$n!$中必然有$\lfloor \frac{n}{p^{\alpha}} \rfloor$个这样的乘积，剩余部分为$n\%p^{\alpha}$内与$p$互素的数的乘积。

$$
fac(n)=base^\frac{n}{p^{\alpha}} fac(n \\% p^{\alpha})
$$

总结一下就是，现在我们把阶乘在$O({p^{\alpha}}+\log_{p}{n})$时间上，分成了互素数乘积`fac(n)`和不互素的`p^pot`两部分。

所以，上代码了。
```cpp exLucas  
inline ll pot(ll n, ll p, ll res = 0) {
	while (n) 
		res += n / p, n /= p;
	return res;
}

inline ll fac(ll n, ll p, ll mod, ll res = 1LL) {
	if (n == 0) return 1LL;
	ll base = 1LL;
	for (ll i = 2; i < mod; i++) 
		if (i % p) base = mul(base, i, mod);
	while (n) {
		ll tmp = qpow(base, n / mod, mod), sz = n % mod;
		for (ll i = 2; i <= sz; i++) 
			if (i % p) tmp = mul(tmp, i, mod); 
		res = mul(res, tmp, mod), n /= p;
	} 
	return res;
}
```
那么，现在我们就能得到：
$${n \choose m} \equiv fac(n) \times inv(fac(m)) \times inv(fac(n-m)) \times p^{pot_p(n)-pot_p(m)-pot_p(n-m)} \pmod{p^{\alpha}}$$

之后就是简单的**CRT**啦，这个就不单独上代码了。

> [洛谷 P4720 【模板】扩展卢卡斯定理/exLucas](https://www.luogu.com.cn/problem/P4720)

直接给出全部代码吧：

> 因为最近沉迷压行，可能看起来有点不舒服，~~但是我舒服就行~~但是可以复制到本地去格式化，所以我就不改啦。

```cpp Luogu-P4720.cpp
// #pragma GCC optimize("Ofast")
// #pragma GCC target("avx,avx2,fma")

#include <bits/stdc++.h>
using namespace std;
#define fast ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0)
#define fin freopen("input.txt", "r", stdin), freopen("output.txt", "w", stdout)
#define PII pair<int, int>
#define PLL pair<ll, ll>
#define pb push_back
#define mp make_pair
#define fi first
#define se second
#define ld nd << 1
#define rd nd << 1 | 1

typedef long double lld;
typedef long long ll;
typedef unsigned long long ull;
// typedef __int128_t i128;
typedef vector<ll> vec;

// const int mod = 1e9 + 7;
// const int mod = 998244353;
const int maxn = 1e6 + 50;
const int inf = 0x3f3f3f3f;			// 1e9;
const ll INF = 0x3f3f3f3f3f3f3f3f;	// 1e18;

int T;

inline ll mul(ll a, ll b, ll p) { return (a * b - (ll)((lld)a / p * b) * p + p) % p; } 

inline ll qpow(ll x, ll m, ll mod, ll res = 1) {
	for ( ; m; m >>= 1, x = mul(x, x, mod)) if (m & 1) res = mul(res, x, mod);
	return res;
}

inline void exgcd(ll a, ll b, ll &g, ll &x, ll &y) {
	if (b) exgcd(b, a % b, g, y, x), y -= a / b * x;
	else x = 1, y = 0, g = a;
}

inline ll inv(ll x, ll m) {
	ll a, b, g; 
	exgcd(x, m, g, a, b);
	return (a % m + m) % m;
}

ll r[maxn], m[maxn], tot = 1;
inline ll CRT() {
	ll M = 1LL, ans = 0LL;
	for (int i = 1; i < tot; i++) M *= m[i];
	for (int i = 1; i < tot; i++) { // combine
		ll Mi = M / m[i], Mi_inv = inv(Mi, m[i]);
		ans = (ans + mul(mul(r[i], Mi, M), Mi_inv, M)) % M;
	} return ans;
}

inline ll pot(ll n, ll p, ll res = 0) {
	while (n) res += n / p, n /= p;
	return res;
}

inline ll fac(ll n, ll p, ll mod, ll res = 1LL) {
	if (n == 0) return 1LL;
	ll base = 1LL;
	for (ll i = 2; i < mod; i++) if (i % p) base = mul(base, i, mod);
	while (n) {
		ll tmp = qpow(base, n / mod, mod), sz = n % mod;
		for (ll i = 2; i <= sz; i++) if (i % p) tmp = mul(tmp, i, mod); 
		res = mul(res, tmp, mod), n /= p;
	} return res;
}

inline ll exLucas(ll a, ll b, ll p) {
	for (ll i = 2; i * i <= p; i ++) {
		if (p % i == 0) {
			ll t = 1LL;
			while (p % i == 0) p /= i, t *= i;
			ll fa = fac(a, i, t), fb = fac(b, i, t), fc = fac(a - b, i, t);
			ll pk = qpow(i, pot(a, i) - pot(b, i) - pot(a - b, i), t);
			m[tot] = t, r[tot ++] = mul(pk, mul(fa, mul(inv(fb, t), inv(fc, t), t), t), t);
		}
	} 
	if (p ^ 1LL) {
		ll fa = fac(a, p, p), fb = fac(b, p, p), fc = fac(a - b, p, p);
		ll pk = qpow(p, pot(a, p) - pot(b, p) - pot(a - b, p), p);
		m[tot] = p, r[tot ++] = mul(pk, mul(fa, mul(inv(fb, p), inv(fc, p), p), p), p);
	}
	return CRT();
}

ll a, b, p, ans;

int main() {
	scanf("%lld%lld%lld", &a, &b, &p);
	ans = exLucas(a, b, p);
	printf("%lld", ans);
	return 0;
}
```

## 一些优化（LibreOJ #181. 二项式系数）

> 上面给的代码只能过一些数据比较水的单组测试样例，因为是板子题所以没有优化。

要过一些其它的题比如[LibreOJ #181. 二项式系数](https://loj.ac/p/181)，这种数据比较毒瘤的是肯定不行的。

以下优化基于`模数确定，多组输入`的情况。

### 预处理部分

在求分离阶乘的时候，我们其实可以通过前缀和预处理出，前k个数中与$p^{\alpha}$互素的数的乘积$sum[k]$，以及$base$的$\lambda$次幂$base_{sum}[\lambda]$。

由于$base$与$p^{\alpha}$互素，通过**欧拉定理**可知$base^{\varphi(p^{\alpha})}\equiv 1\pmod{p^{\alpha}}$。

> $\varphi(p^k)=p^{k-1}\varphi(p)=p^{k-1}(p-1)$

所以预处理时，$sum$预处理到$p^{\alpha}$，$base_{sum}$预处理到$p^{k-1}(p-1)$即可。

---

再一个是**CRT**函数。

> 设$m_1,m_2,\dots,m_k$为$k$个两两互素的正整数，$m=\prod{m_i}$。
>
> 令$m=m_iM_i$，则同余方程组
> $$\begin{cases}x &\equiv & b_1 \pmod{m_1} \\\\ x &\equiv & b_2 \pmod{m_2} \\\\ & \vdots & \\\\ x &\equiv & b_k \pmod{m_k} \end{cases}$$
> 
> 有唯一解
> $$x\equiv {\sum_{i=1}^{k}{b_iM_iM_i^{-1}}}\pmod{m},M_iM_i^{-1}\equiv1\pmod{m_i}$$

由于需要多次调用**CRT**，我们可以直接预处理$M_iM_i^{-1}$这一部分。

---

再预处理完这些之后，我们就来改写`fac`函数，使之同时求出`pot`。

```cpp
inline int fac(long long x, long long & pot) {
	int res = pot = 0;
	while (x) {
		res = res * base_sum[x / pk % phi] * sum[x % pk];
		pot += x / p, x /= p; 
	} 
	return res;
}
```
然后是`exLucas`函数

```cpp
inline int exLucas(long long n, long long m) {
	long long pa, pb, pc;
	int fa = fac(n, pa);
	int fb = fac(m, pb);
	int fc = fac(n - m, pc);
	return fa * inv(fb) * inv(fc) * qpow(p, pa - pb - pc);
}
```
### 复杂度分析

我们来算算复杂度

+ 唯一分解加上预处理
  $$\log{P}\sum(\varphi(p^k)+p^k+\log{p^k})$$
+ 查询
  $$T\log{P}(\log_p{(n)}+\log_p{(m)}+\log_p{(n-m)}+\log(pot))$$

总共大概$1e8$和一个不太大（实际很大）的常数，然后本地跑了3.6秒，一直`TLE`。。。

感觉太玄学了就去看了大佬提交的代码，然后就看到了一个很玄学的优化（取模）。

### 大佬的玄学优化（取模）

{{< admonition success "代码来源" true >}}
```cpp
/**
 * Author: Simon Lindholm
 * Date: 2020-05-30
 * License: CC0
 * Source: https://en.wikipedia.org/wiki/Barrett_reduction
 * Description: Compute $a \% b$ about 5 times faster than usual, where $b$ is constant but not known at compile time.
 * Returns a value congruent to $a \pmod b$ in the range $[0, 2b)$.
 * Status: proven correct, stress-tested
 * Measured as having 4 times lower latency, and 8 times higher throughput, see stress-test.
 * Details:
 * More precisely, it can be proven that the result equals 0 only if $a = 0$,
 * and otherwise lies in $[1, (1 + a/2^64) * b)$.
 */
#pragma once

typedef unsigned long long ull;
struct FastMod {
	ull b, m;
	FastMod(ull b) : b(b), m(-1ULL / b) {}
	ull reduce(ull a) { // a % b + (0 or b)
		return a - (ull)((__uint128_t(m) * a) >> 64) * b;
	}
};
```
{{< /admonition >}}

[实际使用代码，内容有修改](https://loj.ac/s/1188125)

```cpp
#define u64 unsigned long long
#define u128 __uint128_t

struct FastMod {
	u64 b, m;
	void in(u64 x) {
		b = x, m = (u64)((u128(1) << 64) / x);
	}
	int operator()(u64 a) {
		u64 q = (u64)((u128(m) * a) >> 64), r = a - q * b;
		return r >= b ? r - b : r;
	} 
};
```
> 个人理解：除法的效率很低，用位运算代替除法提高效率的优化（？）

这个是我自己一直在用的，比较常规。
```cpp
return (a * b - (ll)((ld)a / p * b) * p + p) % p;
```

我搜索了一下`c++`中各种运算的效率

[来源：CSDN博客](https://blog.csdn.net/luolaihua2018/article/details/115042119?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522162702345116780255258303%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=162702345116780255258303&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~baidu_landing_v2~default-1-115042119.first_rank_v2_pc_rank_v29&utm_term=c%2B%2B+%E4%B9%98%E6%B3%95%E5%92%8C%E9%99%A4%E6%B3%95%E7%9A%84%E6%95%88%E7%8E%87&spm=1018.2226.3001.4187)，不保证正误，但是至少知道除法很慢就对了。

> 移位 > 赋值 > 大小比较 > 加法 > 减法 > 乘法 > 取模 > 除法。

由于模数确定，我们处理一下再用位运算右移代替除法会比正常取模快。

### AC代码

> [LibreOJ 提交链接](https://loj.ac/s/1196902) 加了快读，以及压行，所以有点丑，但应该不影响阅读。

```cpp LiberOJ-181.cpp
#include <cstdio>
#include <algorithm>
#include <vector>
#define gc() (p1 == p2 ? (p2 = buf + fread(p1 = buf, 1, 1 << 20, stdin), p1 == p2 ? EOF : *p1++) : *p1++)
#define read() ({ register long long x = 0, f = 1; register char c = gc(); while(c < '0' || c > '9') { if (c == '-') f = -1; c = gc();} while(c >= '0' && c <= '9') x = x * 10 + (c & 15), c = gc(); f * x; })
#define pc(x) (p - puf == 1 << 20 ? (fwrite(puf, 1, 1 << 20, stdout), p = puf) : 0, *p++ = x)
#define print(x, b) ({ pt(x), pc(b); })
char buf[1 << 20], *p1, *p2, puf[1 << 20], *p = puf;
int pt(int x) { return x <= 9 ? pc(x + '0') : (pt(x / 10), pc(x % 10 + '0')); }

int P;

struct FastMod {
	unsigned long long b, m;
	void in(unsigned long long x) {
		b = x, m = (unsigned long long)((__uint128_t(1) << 64) / x);
	}
	int operator()(unsigned long long a) {
		unsigned long long q = (unsigned long long)((__uint128_t(m) * a) >> 64), r = a - q * b;
		return r >= b ? r - b : r;
	} 
} M;

struct node {
	int p, pk, o, phi; 
	FastMod f;
	std::vector<int> sum, base_sum;
	void exgcd(int a, int b, int & x, int & y) { b ? (exgcd(b, a % b, y, x), y -= a / b * x) : (x = 1, y = 0); } 
	int inv(int a) { int x, y; exgcd(a, pk, x, y); return f(x + pk); }
	int qpow(int x, int n, int res = 1) { for ( ; n; n >>= 1, x = f(1ll * x * x)) if (n & 1) res = f(1ll * res * x); return res; }
	void set(int _p, int _pk) {
		f.in(_pk), p = _p, pk = _pk, phi = _pk - _pk / _p, o = M(P / _pk * 1ll * inv(P / _pk));
		sum.resize(pk), base_sum.resize(phi), sum[0] = base_sum[0] = 1;
		for (register int i = 1; i < pk; i++) sum[i] = i % p ? f(1ll * sum[i-1] * i) : sum[i-1];
		for (register int i = 1; i < phi; i++) base_sum[i] = f(1ll * base_sum[i-1] * sum[pk-1]);
	}
	int fac(long long x, long long & pot, int res = 1) {
		pot = 0;
		while (x) res = f(f(base_sum[x / pk % phi] * 1ll * res) * 1ll * sum[x % pk]), pot += x / p, x /= p;
		return res;
	}
	int get(long long a, long long b) {
		long long pa, pb, pc; int fa = fac(a, pa), fb = fac(b, pb), fc = fac(a - b, pc);
		return f(f(f(1ll * qpow(p, pa - pb - pc) * fa) * 1ll * inv(fb)) * 1ll * inv(fc));
	}
} pr[11];

long long n, m;

int main() {
	register int T = read(), t = P = read(), tot = 0, ans; M.in(P);
	for (register int i = 2; i <= t / i; i++) // Factorization
		if (t % i == 0) {
			for (ans = 1; t % i == 0; ans *= i, t /= i) continue;
			pr[++ tot].set(i, ans);
		}
	if (t ^ 1) pr[++ tot].set(t, t);

	while (T -- ) {
		n = read(), m = read(), ans = 0;
		for (register int i = 1; i <= tot; i++)
			ans = M(ans + M(pr[i].get(n, m) * 1ll * pr[i].o));
		print(ans, '\n');
	}
	fwrite(puf, 1, p - puf, stdout);
}
```
