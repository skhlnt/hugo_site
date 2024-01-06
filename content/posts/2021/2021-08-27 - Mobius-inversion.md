---
title: "莫比乌斯反演问题记录 - Mobius Inversion"
date: 2021-08-27 19:24:52
slug: e7791216

author: "Kenshin2438"
description: "莫比乌斯反演问题记录，每一题都代表了一种典型，实在不好取舍便都记录下来了。"
keywords:
  - 莫比乌斯反演
  - 问题记录
  - "P3172 [CQOI2015]选数"
  - "P3312 [SDOI2014]数表"
  - "P3911 最小公倍数之和"
  - "P1829 [国家集训队]Crash的数字表格 / JZPTAB"
  - "P2398 GCD SUM"
  - "P2257 YY的GCD"
  - "「SDOI2015」约数个数和"
  - "LCMSUM"
  - "HDU 6134 Battlestation Operational"
categories:
  - Number Theory
tags:
  - Mobius Inversion

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

题外话：好像文章有点长，本地调的时候加载目录都掉帧了。虽然一度想删点题目，但思前想后还是一题没删，总感觉每一题都代表了一种典型，实在不好取舍，或许只写推导会好一点，但还是有点怕代码的实现未有较好交代。。。

好了，闲言少叙。
本篇是平时刷的反演题目的解题记录，个人认为这方面的知识点和写题目是有点脱节的，题目要么是纯套路，要么就是有些不太友好的小技巧。

题目来源：`Luogu`, `LibreOJ`, `HDU`等。


---

## P3312 [SDOI2014]数表

> **题目描述**
>
> 有一张 $n\times m$ 的数表，其第 $i$行第 $j$ 列（$1\le i\le n$，$1\le j\le m$）的数值为能同时整除 $i$ 和 $j$ 的所有自然数之和。给定 $a$，计算数表中不大于 $a$ 的数之和。
>
> **输入包含多组数据。**
>
> 输入的第一行一个整数 $Q$ 表示测试点内的数据组数
>
> 接下来 $Q$ 行，每行三个整数 $n$，$m$，$a$（$|a|\le 10^9$）描述一组数据。
>
> 答案模$2^{31}$。

显然有答案为：

$$Ans=\sum_{i=1}^{n}\sum_{j=1}^{m}\sigma(\gcd(i,j))[\gcd(i,j)\leq a] \newline$$

先不考虑大小限制，之后将其转换成离线求值+动态加入贡献的问题。

$$
\begin{aligned}
\sum_{i=1}^{n}\sum_{j=1}^{m}\sigma(\gcd(i,j))&=\sum_{d=1}^{n}\sigma(d)\sum_{i=1}^{[\frac{n}{d}]}\sum_{j=1}^{[\frac{m}{d}]}[\gcd(i,j)=1]\newline
&=\sum_{d=1}^{n}\sigma(d)\sum_{k=1}^{[\frac{n}{d}]}\mu(k)\sum_{i=1}^{[\frac{n}{d}]}\sum_{j=1}^{[\frac{m}{d}]}\newline
&=\sum_{d=1}^{n}\sigma(d)\sum_{k=1}^{[\frac{n}{d}]}\mu(k)[\frac{n}{dk}]\times[\frac{m}{dk}]\newline
&=\sum_{T=1}^{n}[\frac{n}{T}][\frac{m}{T}]\sum_{d\mid T}\sigma(d)\mu(\frac{T}{d})
\end{aligned}
$$

只有当$\sigma(n)\leq a_i$，才将$\sigma(n)$的贡献计入，那么我们可以离线处理，用树状数组维护，$O(Q\sqrt{n}\log{n})$。

取模$2^{31}$标志着需要$32$位整型自然溢出，当然最终还是要变成无符号整数，这里可以写成`ans & 2^{31}-1`。

```cpp
#include <bits/stdc++.h>
#define PII pair<int, int>
#define fi first
#define se second
using namespace std;

typedef long long i64;

const int N = 1e5;
const int mod = 0x7fffffff;

int T;
struct Query {
	int n, m, a, id;
	bool operator < (const Query &b) const {
		return a < b.a;
	}
} Q[N + 10];
int ans[N + 10];
PII  s[N + 10];
int mu[N + 10];

bitset<N + 10> ok;
int pr[N], cnt;
int sig[N + 10], pw[N + 10];

void init(int n) {
	mu[1] = sig[1] = 1;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) mu[pr[++cnt] = i] = -1, sig[i] = i + 1, pw[i] = i;
		for (int j = 1; j <= cnt && pr[j] <= n / i; ++j) {
			int t = pr[j] * i; ok[t] = 1;
			if (i % pr[j] == 0) {
				pw[t] = pw[i] * pr[j];
				sig[t] = 1LL * sig[i] * (pw[t] * pr[j] - 1) / (pw[t] - 1);
				break;
			}
			mu[t] = -mu[i], sig[t] = sig[i] * (pr[j] + 1), pw[t] = pr[j];
		}
	}
	for (int i = 1; i <= n; i++) s[i].fi = sig[i], s[i].se = i;
	sort(s + 1, s + 1 + n);
}

int tr[N + 10];
inline void ins(int p, int v) {
	for (; p <= N; p += p & -p) tr[p] += v;
}
inline int que(int p, int r = 0) {
	for (; p; p &= p - 1) r += tr[p];
	return r;
}

inline int slove(int n, int m, int res = 0) {
	if (n > m) n ^= m ^= n ^= m;
	for (int l = 1, r; l <= n; l = r + 1) {
		int fn = n / l, fm = m / l;
		r = min(n / fn, m / fm);
		res += fn * fm * (que(r) - que(l-1));
	} return res;
}

int main() {
	init(N);

	scanf("%d", &T);
	for (int i = 1; i <= T; i++)
		scanf("%d%d%d", &Q[i].n, &Q[i].m, &Q[i].a), Q[i].id = i;
	sort(Q + 1, Q + 1 + T);
	for (int o = 1, k = 1; o <= T; o++) {
		while (k <= N && s[k].fi <= Q[o].a) {
			for (int d = s[k].se, sg = s[k].fi, i = d, t = 1; i <= N; i += d, ++t)
				ins(i, sg * mu[t]);
			k++;
		} ans[Q[o].id] = slove(Q[o].n, Q[o].m);
	}
	for (int i = 1; i <= T; i++) printf("%d\n", ans[i] & mod);
	return 0;
}
```

---

## P3172 [CQOI2015]选数

> **题目大意**
>
> 在$[L,H]$中依次选择$N$个数（可以重复），求使得这$N$个数的$gcd$为$K$的选法取模$1e9+7$。
>
> 对于 $100\%$ 的数据，$1\le N,K\le 10^9$，$1\le L\le H\le 10^9$，$H-L\le 10^5$。

$$
\begin{aligned}
Ans&=\sum_{a_1=L}^{H}\sum_{a_2=L}^{H}\dots\sum_{a_N=L}^{H}\left[ (a_1,a_2,\dots,a_N)=K \right] \newline
&=\sum_{a_1=\lceil \frac{L}{K} \rceil}^{\lfloor\frac{H}{K} \rfloor}\sum_{a_2=\lceil \frac{L}{K} \rceil}^{\lfloor \frac{H}{K} \rfloor}\dots\sum_{a_N=\lceil \frac{L}{K} \rceil}^{\lfloor \frac{H}{K} \rfloor}\left[ (a_1,a_2,\dots,a_N)=1\right] \newline
&=\sum_{a_1=\lceil \frac{L}{K} \rceil}^{\lfloor\frac{H}{K} \rfloor}\sum_{a_2=\lceil \frac{L}{K} \rceil}^{\lfloor \frac{H}{K} \rfloor}\dots\sum_{a_N=\lceil \frac{L}{K} \rceil}^{\lfloor \frac{H}{K} \rfloor}\sum_{d\mid(a_1,a_2,\dots,a_N)}{\mu(d)} \newline
&=\sum_{d=1}^{\lfloor \frac{H}{K} \rfloor}{\mu(d)\times(\lfloor\frac{\lfloor\frac{H}{K} \rfloor}{d}\rfloor-\lceil\frac{\lceil\frac{L}{K}\rceil}{d}\rceil+1)^N}\newline
\end{aligned}
$$
前者求$\sum\mu(n)$用杜教筛就可以了，$O(n^{\frac{2}{3}})$。

后者明显是分块+快速幂，但是里面存在一个`向上取整`的部分。想了很久怎样找向上取整的区间，然后突然记起向上取整可以转化为向下取整，即$\lceil \frac{L}{K} \rceil=\lfloor \frac{L-1}{K} \rfloor + 1$。
$$Ans=\sum_{d=1}^{\lfloor \frac{H}{K} \rfloor}{\mu(d)\times(\lfloor\frac{\lfloor\frac{H}{K} \rfloor}{d}\rfloor-\lfloor\frac{\lfloor\frac{L-1}{K}\rfloor}{d}\rfloor)^N}\newline$$

然后就和常规的整除分块一样啦。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N   = 1e6;
const int mod = 1e9 + 7;

int pr[N], cnt;
bitset<N + 10> ok;
int mu[N + 10];

void init(int n) {
	mu[1] = 1;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) mu[pr[++cnt] = i] = mod - 1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; ++j) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) break;
			mu[pr[j] * i] = mod - mu[i];
		}
	}
	for (int i = 1; i <= n; i++)
		mu[i] = (mu[i] + mu[i-1]) % mod;
	return ;
}

inline int qpow(int x, int n, int r = 1) {
	for (; n; n >>= 1, x = 1LL * x * x % mod)
		if (n & 1) r = 1LL * r * x % mod;
	return r;
}

unordered_map<int, int> sm;

inline int sieve(int n) {
	if (n <= N) return mu[n];
	if (sm.count(n)) return sm[n];
	int res = 1;
	for (int l = 2, r; l <= n; l = r + 1) {
		int fl = n / l; r = n / fl;
		res = (res - 1LL * sieve(fl) * (r - l + 1) % mod + mod) % mod;
	} return sm[n] = res;
}

int main() {
	init(N);

	int n, k, L, H;
	scanf("%d%d%d%d", &n, &k, &L, &H);
	H = H / k, L = (L - 1) / k;

	int ans = 0;
	for (int l = 1, r; l <= H; l = r + 1) {
		int fl = L / l, fh = H / l;
		fl ? r = min(H / fh, L / fl) : r = H / fh;
		ans = (ans + 1LL * (sieve(r) - sieve(l-1) + mod) * qpow(fh - fl, n) % mod) % mod;
	} printf("%d", ans);
	return 0;
}
```

---

## P3911 最小公倍数之和

> **题目描述**
>
> 对于$A_1,A_2,\cdots,A_N$，求 $\sum_{i=1}^N\sum_{j=1}^N lcm(A_i,A_j)$。
>
> **数据范围**
>
> **$1\le N \le 50000;1 \le A_i \le 50000。$**

随机数组的形式没办法直接快速求值，注意到，$A_i$的取值范围很小，我们可以定义一个**贡献**，将未出现的数剔除掉，只统计数组中元素的贡献。显然，这里应该用**出现次数**作为贡献（出现多少次就会被计算多少次）。
$$
\begin{aligned}
Ans&=\sum_{i=1}^{M}\sum_{j=1}^{M}lcm(i,j)\times c[i]\times c[j]\newline
&=\sum_{g=1}^{M}\sum_{i=1}^{[\frac{M}{g}]}\sum_{j=1}^{[\frac{M}{g}]}{g\times i\times j}\times[(i,j)=1]\times c[ig]\times c[jg]\newline
&=\sum_{g=1}^{M}\sum_{k=1}^{[\frac{M}{g}]}\mu(k)\sum_{i=1}^{[\frac{M}{gk}]}\sum_{j=1}^{[\frac{M}{gk}]}{g\times ik\times jk}\times c[igk]\times c[jgk]\newline
&=\sum_{T=1}^{M}T(\sum_{i=1}^{[\frac{M}{T}]}i\times c[iT])^2\sum_{k \mid T}{k\times\mu(k)}\newline
\end{aligned}
$$
后面一项可以预处理，中间项只能暴力去做，正好$M$不大，时间复杂度$O(M\log M)$能过。

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long i64;

const int N = 5e4;

int n;

bitset<N + 10> ok;
int mu[N + 10], pr[N], cnt;
i64 s[N + 10], c[N + 10];

void init() {
	mu[1] = 1;
	for (int i = 2; i <= N; i++) {
		if (!ok[i]) mu[pr[++cnt] = i] = -1;
		for (int j = 1; j <= cnt && pr[j] <= N / i; ++j) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) break;
			mu[pr[j] * i] = -mu[i];
		}
	}
	for (int i = 1; i <= N; i++) {
		i64 t = (i64)i * mu[i];
		for (int j = i; j <= N; j += i) s[j] += t;
	} return ;
}

int main() {
	init();

	scanf("%d", &n);
	for (int a, i = 1; i <= n; i++)
		scanf("%d", &a), ++c[a];
	i64 ans = 0;
	for (int i = 1; i <= N; i++) {
		i64 t = 0;
		for (int j = 1, m = N / i; j <= m; j++)
			t += (i64)j * c[i * j];
		ans = ans + (i64)i * t * t * s[i];
	} printf("%lld", ans);
	return 0;
}
```

---

## P1829 [国家集训队]Crash的数字表格 / JZPTAB

> **题目描述**
>
> 求$\sum_{i=1}^{n}\sum_{j=1}^{m}lcm(i,j)\mod 20101009$，其中$1<n,m\leq10^7$。

上面推过了，只要将贡献设置为$1$，得到答案：
$$Ans=\sum_{T=1}^{n}T(\sum_{i=1}^{[\frac{n}{T}]}i)(\sum_{j=1}^{[\frac{m}{T}]}j)\sum_{k \mid T}{k\times\mu(k)}\newline$$
看起来最终求值可以$O(\sqrt n)$解决，但是预处理的复杂度$O(n\log n)$太大了，需要优化。

首先，由于$\sum_{d\mid n}f(d)\mu(d)=\prod\limits_{p\mid n,p\in Prime}\left(1-f(p)\right)$，我们得到：

$$\sum_{k \mid T}{k\times\mu(k)}=\prod\limits_{p\mid n,p\in Prime}(1-p)$$

整体妥妥的积性，线性筛预处理就好了，我们将其令为$f(T)$，有
$$Ans=\sum_{T=1}^{n}T\times f(T)\times (\sum_{i=1}^{[\frac{n}{T}]}i)(\sum_{j=1}^{[\frac{m}{T}]}j)$$
分块求值，$O(n+\sqrt n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long i64;

const int mod = 20101009;
const int N = 1e7;

int pr[664579 + 10], cnt;
bitset<N + 10> ok;
int f[N + 10];

void init(int n) {
	f[1] = 1;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) f[pr[++cnt] = i] = mod + 1 - i;
		for (int j = 1; j <= cnt && pr[j] <= n / i; ++j) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) {f[pr[j] * i] = f[i]; break;}
			f[pr[j] * i] = 1LL * f[i] * f[pr[j]] % mod;
		}
	} 
	for (int i = 1; i <= n; i++) f[i] = (f[i-1] + 1LL * f[i] * i % mod) % mod;
}

int main() {
	int n, m;
	scanf("%d%d", &n, &m);
	if (n > m) n ^= m ^= n ^= m;
	init(n); //
	int ans = 0;
	for (int l = 1, r; l <= n; l = r + 1) {
		int fn = n / l, fm = m / l;
		r = min(n / fn, m / fm);
		fn = (1LL * fn * (fn + 1) >> 1LL) % mod;
		fm = (1LL * fm * (fm + 1) >> 1LL) % mod;
		ans = (ans + 1LL * fn * fm % mod * (f[r] - f[l-1] + mod) % mod) % mod;
	} printf("%d", ans);
	return 0;
}
```

当然，如果你推到之前一步就停下来开始码也能写，只是会慢大概`150ms`。
$$Ans=\sum_{g=1}^{n}g\sum_{k=1}^{[\frac{n}{g}]}k^2\mu(k)\sum_{i=1}^{[\frac{n}{gk}]}\sum_{j=1}^{[\frac{m}{gk}]}i\times j$$

现在，能两次整除分块解决啦。

```cpp
typedef long long ll;
typedef unsigned long long ull;

const int maxn = 1e7 + 10;
const int mod  = 20101009;

int T, R;

int pr[664579 + 10], cnt;
bitset<maxn> ok;
int mu[maxn], f[maxn];

void init(int n) {
	mu[1] = 1;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) pr[++ cnt] = i, mu[i] = -1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; j++) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) break;
			mu[pr[j] * i] = -mu[i];
		}
	}
	for (int i = 1; i <= n; i++) {
		f[i] = (f[i-1] + 1LL * i * i * mu[i] % mod + mod) % mod;
	}
}

il int func(ll be, ll ed) { return (1LL * (be + ed) * (ed - be + 1) >> 1LL) % mod; }

int main() {
	int n, m, ans = 0;
	scanf("%d%d", &n, &m);
	int o = n < m ? n : m;
	init(o);
	for (int l = 1, r; l <= o; l = r + 1) {
		int ta = n / (n / l), tb = m / (m / l);
		r = ta < tb ? ta : tb;
		int sum = 0;
		for (int i = 1, j; i <= o / l; i = j + 1) {
			ta = (n / l) / ((n / l) / i), tb = (m / l) / ((m / l) / i); 
			j = ta < tb ? ta : tb;
			sum = (sum + 1LL * (f[j] - f[i-1] + mod) * func(1, n / l / i) % mod * func(1, m / l / i) % mod) % mod;
		}
		ans = (ans + 1LL * sum * func(l, r) % mod) % mod;
	}
	printf("%d", ans);
	return 0;
}
```

---

## P2398 GCD SUM

> **题目描述**
>
> 给定$n,m$，求$\sum_{i=1}^{n}\sum_{j=1}^{m}\gcd(i,j)$.
>
> **数据范围**
>
> $n\leq1e5$

用一个之前没写过的欧拉反演，原理：$\sum_{d\mid n}\varphi(d)=n$。

$$
\begin{aligned}
Ans&=\sum_{i=1}^{n}\sum_{j=1}^{m}\gcd(i,j)\newline
&=\sum_{i=1}^{n}\sum_{j=1}^{m}\sum_{d\mid\gcd(i,j)}\varphi(d)\newline
&=\sum_{d=1}^{n}\varphi(d)\times[\frac{n}{d}]\times[\frac{m}{d}]
\end{aligned}
$$
总共$O(n+\sqrt{n})$，数据范围给得太小了。

用莫反推起来步骤一样，就略去了。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5;

bitset<N + 10> ok;
int pr[N], cnt;
long long phi[N + 10];
void init(int n) {
	phi[1] = 1;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) phi[pr[++cnt] = i] = i - 1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; j++) {
			int t = pr[j] * i; ok[t] = 1;
			if (i % pr[j] == 0) {phi[t] = phi[i] * pr[j]; break;}
			phi[t] = phi[i] * phi[ pr[j] ];
		}
	}
	for (int i = 1; i <= n; i++) phi[i] += phi[i-1];
}

int main() {
	int n; scanf("%d", &n); init(n);
	long long ans = 0;
	for (int l = 1, r; l <= n; l = r + 1) {
		int fn = n / l;
		r = n / fn;
		ans += ( phi[r] - phi[l-1] ) * fn * fn;
	}
	printf("%lld", ans);
	return 0;
}
```

---

## P2257 YY的GCD

> **题目描述**
>
> 给定正整数 $n$，求 $1\le x \leq N,1 \le y \le M$ 且 $\gcd(x,y)$ 为素数的数对 $(x,y)$ 有多少对。
>
> **数据范围**
>
> $T$组输入。（时间：`4.00s`）
>
> $T=1e4$，$N,M\leq1e7$。

$$
\begin{aligned}
Ans&=\sum_{x=1}^{N}\sum_{y=1}^{M}[(x,y)=p \land p\in Prime]\newline
&=\sum_{p\in Prime}\sum_{x=1}^{[\frac{N}{p}]}\sum_{y=1}^{[\frac{M}{p}]}[(x,y)=1]\newline
&=\sum_{p\in Prime}\sum_{k=1}^{[\frac{N}{p}]}\mu(k)\times[\frac{N}{pk}]\times[\frac{M}{pk}]\newline
&=\sum_{T=1}^{N}[\frac{N}{T}]\times[\frac{M}{T}]\sum_{p\mid T,p\in Prime}\mu(\frac{T}{p})
\end{aligned}
$$

$O(N+\pi(N)\log p)$预处理后面部分$F(n)=\sum\limits_{p\mid n,p\in Prime}\mu(\frac{n}{p})$。

> （用线性筛可以优化到$O(N)$预处理）
> $$F(n)=
> \begin{cases}
> 1 & \textrm{if } n\in Prime \newline
> \mu(\frac{n}{p}) - F(\frac{n}{p}) & \textrm{if } p\mid\mid n\newline
> \mu(\frac{n}{p}) & \textrm{otherwise}
> \end{cases}
> $$

然后$O(T\sqrt N)$求值。

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long i64;

const int N = 1e7;

int pr[N], cnt;
bitset<N + 10> ok;
i64 F[N + 10], mu[N + 10];

void init(int n) {
	mu[1] = 1;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) mu[pr[++ cnt] = i] = -1, F[i] = 1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; j++) {
			int t = pr[j] * i; ok[t] = 1;
			if (i % pr[j] == 0) {F[t] = mu[i];break;}
			mu[t] = -mu[i], F[t] = mu[i] - F[i];
		}
	}
	for (int i = 1; i <= n; i++) F[i] += F[i-1];
}

inline i64 slove(int n, int m, i64 res = 0) {
	if (n > m) n ^= m ^= n ^= m;
	for (int l = 1, r; l <= n; l = r + 1) {
		int fn = n / l, fm = m / l;
		r = min(n / fn, m / fm);
		res += 1LL * fn * fm * (F[r] - F[l-1]);
	} return res;
}

int main() {
	init(N);

	int T, n, m;
	for (scanf("%d", &T); T--; ) {
		scanf("%d%d", &n, &m);
		printf("%lld\n", slove(n, m) );
	}
	return 0;
}
```

---

## 「SDOI2015」约数个数和

> **题目描述**
>
> 求$\sum_{i=1}^{N}\sum_{j=1}^{M}d(i,j)$
>
> **数据范围**
>
> 多组，$1\leq T\leq 5e4$，$1\leq N,M,\leq 5e4$。

$$
\begin{aligned}
Ans&=\sum_{i=1}^{N}\sum_{j=1}^{M}\sum_{x\mid i}\sum_{y\mid j}[\gcd(x,y)=1]\newline
&=\sum_{i=1}^{N}\sum_{j=1}^{M}\sum_{x\mid i}\sum_{y\mid j}\sum_{k\mid\gcd(x,y)}\mu(k)\newline
&=\sum_{k=1}^{N}\mu(k)\times\left( \sum_{x=1}^{[\frac{N}{k}]}\sum_{i=1}^{[\frac{N}{kx}]}1 \right)\times\left( \sum_{y=1}^{[\frac{M}{k}]}\sum_{j=1}^{[\frac{M}{ky}]}1 \right)\newline
&=\sum_{k=1}^{N}\mu(k)\times\left(\sum_{x=1}^{[\frac{N}{k}]}[\frac{N}{kx}]\right)\times\left(\sum_{y=1}^{[\frac{M}{k}]}[\frac{M}{ky}]\right)
\end{aligned}
$$

后面部分令为$F(\lfloor\frac{n}{k}\rfloor)=\sum_{x=1}^{\lfloor\frac{n}{k}\rfloor}\lfloor\frac{n}{kx}\rfloor=\sum_{x=1}^{\lfloor\frac{n}{k}\rfloor}\lfloor\frac{\lfloor\frac{n}{k}\rfloor}{x}\rfloor$。

明显的整除分块，$O(n\sqrt n)$预处理就完事了。

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long i64;

const int N = 5e4;

int pr[N], cnt;
bitset<N + 10> ok;
i64 F[N + 10], mu[N + 10];

void init(int n) {
	mu[1] = 1;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) mu[pr[++ cnt] = i] = -1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; j++) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) break;
			mu[pr[j] * i] = -mu[i];
		}
	}
	for (int i = 1; i <= n; i++) mu[i] += mu[i-1];
	for (int i = 1; i <= n; i++) {
		for (int l = 1, r; l <= i; l = r + 1) {
			int fn = i / l;
			r = i / fn;
			F[i] += 1LL * (r - l + 1) * fn;
		}
	}
}

inline i64 slove(int n, int m, i64 res = 0) {
	if (n > m) n ^= m ^= n ^= m;
	for (int l = 1, r; l <= n; l = r + 1) {
		int fn = n / l, fm = m / l;
		r = min(n / fn, m / fm);
		res += F[fn] * F[fm] * (mu[r] - mu[l-1]);
	} return res;
}

int main() {
	init(N);

	int T, n, m;
	for (scanf("%d", &T); T--; ) {
		scanf("%d%d", &n, &m);
		printf("%lld\n", slove(n, m) );
	}
	return 0;
}
```

---

## LCMSUM

> **题目描述**
>
> 求$\sum_{i=1}^{n}lcm(i,n)$
>
> **数据范围** 
>
> `500ms`
>
> 多组，$T\leq3e5,1\leq n\leq1e6$。

$$
\begin{aligned}
Ans&=\sum_{g\mid n}\sum_{i=1}^{\frac{n}{g}}i\times n\times[(i, \frac{n}{g})=1]\newline
&=n\sum_{g\mid n}\sum_{i=1}^{\frac{n}{g}}i\times[(i,\frac{n}{g})=1]\newline
&=n\sum_{g\mid n}\frac{\frac{n}{g}\times\varphi(\frac{n}{g})}{2}
\end{aligned}
$$

直接预处理就完事$O(n\ln n)$。

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long i64;

const int N = 1e6;

int n, m;
int pr[N], cnt;
bitset<N + 10> ok;
i64 f[N + 1], phi[N + 1];

void init(int n) {
	phi[1] = 2LL;
	for (int i = 2; i <= n; i++) {
		if (!ok[i]) phi[pr[++cnt] = i] = i - 1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; ++j) {
			int t = pr[j] * i; ok[t] = 1;
			if (i % pr[j] == 0) {phi[t] = phi[i] * pr[j];break;}
			phi[t] = phi[i] * (pr[j] - 1);
		}
	}
	for (int i = 1; i <= n; i++) {
		i64 t = phi[i] * i;
		for (int j = i; j <= n; j += i) f[j] += t;
	}
}

int main() {
	init(N);

	int T; scanf("%d", &T);
	while (T--) {
		int n; scanf("%d", &n);
		printf("%lld\n", f[n] * n >> 1LL);
	}
	return 0;
}
```

---

## [HDU 6134] Battlestation Operational

> **题目描述**
> 求$\sum_{i=1}^{n}\sum_{j=1}^{i}\lceil\frac{i}{j}\rceil\times[(i,j)=1] \mod 1e9+7$。
>
> **数据范围**
>
> $1\leq n\leq 1e6$，多组（不超过$1e4$）

先考虑一个子问题，$g(n)=\sum_{i=1}^{n}\lceil\frac{n}{i}\rceil\times[(n,i)=1]$。
$$
\begin{aligned}
g(n)
&=\sum_{i=1}^{n}\lceil\frac{n}{i}\rceil\times[(n,i)=1]\newline
&=\sum_{d\mid n}\mu(d)\sum_{i=1}^{\frac{n}{d}}\lceil\frac{\frac{n}{d}}{i}\rceil\newline
&=\sum_{d\mid n}\mu(d)\left(\frac{n}{d}-\sigma_0(\frac{n}{d})+\sum_{i=1}^{\frac{n}{d}}\lfloor\frac{\frac{n}{d}}{i}\rfloor\right)\newline
&=\sum_{d\mid n}\mu(d)\left(\frac{n}{d}+\sum_{i=1}^{\frac{n}{d}-1}\sigma_0(i)\right)
\end{aligned}
$$

> 中间一步稍作解释吧，
> $$\sum_{i=1}^{n}\sigma_0(i)=\sum_{i=1}^{n}\sum_{d\mid i}1=\sum_{d=1}^{n}\sum_{i=1}^{\lfloor\frac{n}{d}\rfloor}1=\sum_{d=1}^{n}\lfloor\frac{n}{d}\rfloor$$。

其实现在已经能写了，初始化$\mu(n),\sigma_0(n)$就可以，这个方法比较常规就不写了。

我们可以继续使用莫比乌斯反演优化，$g(n)=\sum_{d\mid n}\mu(d)f(\frac{n}{d})$，得到$f(n)=\sum_{d\mid n}g(d)$。

也就是$g(n)=f(n)-\sum_{d\mid n,d<n}g(d)$，直接推就好了也是$O(n\ln n)$，但是这样就不用预处理$\mu$了，借助滚动数组的思想我们还能进一步优化空间。

```cpp
#include <cstdio>
typedef long long i64;

const int N = 1e6;
const int mod = 1e9 + 7;

i64 g[N + 10], d[N + 10];

int main() {
	for (int i = 1; i <= N; i++) 
		for (int j = i; j <= N; j += i) 
			d[j]++;
	for (int i = 1; i <= N; i++) d[i] += d[i-1], d[i] %= mod;
	for (int i = 1; i <= N; i++) g[i] = (i + d[i-1]) % mod;
	for (int i = 1; i <= N; i++)
		for (int j = i << 1; j <= N; j += i)
			g[j] = (g[j] - g[i] + mod) % mod;
	for (int i = 1; i <= N; i++) g[i] += g[i-1], g[i] %= mod;
	int n; 
	while (~scanf("%d", &n)) printf("%lld\n", g[n]);
	return 0;
}
```
