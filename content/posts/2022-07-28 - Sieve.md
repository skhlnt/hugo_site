---
title: "筛法 - Sieve"
date: 2021-07-28 17:36:43
draft: false
slug: bb62b52f

author: "Kenshin2438"
description: "本篇博客着重于介绍在算法竞赛中几种常见的筛法，默认读者有基本的数论知识。"
keywords: 
  - 筛法
  - 线性筛
  - Min25筛
  - Powerful Number筛
  - PN筛
  - 杜教筛
  - "P4213 【模板】杜教筛（Sum）"
  - "P3768 简单的数学题"
  - "gym 103306 Flipped Factorization"
  - "Luogu P5325 【模板】Min_25筛"
categories:
  - Number Theory
tags:
  - 线性筛
  - 杜教筛
  - Powerful Number Sieve
  - Min25

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

{{< admonition info "logs" true >}}
- Update 2021.10.03 增加PN筛

---

包含有: 线性筛，杜教筛，Min25筛，PN筛，州阁筛

本篇主要用于**入门**数论中的一些简单的筛法

虽然不是特别全面，但是后面会一步步完善的。

**注意：不会对用到的数论函数解释，默认读者对数论有基本认知。**
{{< /admonition >}}

<!--more-->

## 线性筛

从名字也可以看出，这种筛法为线性复杂度。

我们主要用它来得到某个**积性函数**函数值的表，（~~在线性的时间复杂度内得到~~）。

线性筛的基本思路，对于某个合数$n$，若它的最小质因子为$p$：

- 如果$(p,\frac{n}{p})\not = 1$，考虑函数本身，主要看质因子指数对函数值的影响。
- 如果$(p, \frac{n}{p})=1$，由积性函数的性质$f(n)=f(\frac{n}{p})f(p)$。

### 质数筛（顺便记录最小素因子）

按照合数的定义就知道了。

```cpp
int lpf[LIM];
vector<int> sieve() {
  vector<int> pr;
  for (int i = 2; i < LIM; i++) {
    if (lpf[i] == 0) {
      lpf[i] = i, pr.push_back(i);
    }
    for (const int &p : pr) {
      ll j = p * 1LL * i;
      if (j >= LIM) break;
      lpf[j] = p;
      if (i % p == 0) break;
    }
  }
  return pr;
}
```

### 欧拉函数筛

设$(n,m)=d$，则有

$$\varphi(nm)=\varphi(n)\varphi(m)\frac{d}{\varphi(d)}$$

### 莫比乌斯函数筛

质因子指数大于1，直接为０就行。（太简单就不写了，代码也是高度类似，~~其实全部都差不多~~）


### 约数个数函数筛

设$n=\prod_{i=1}^{s}p_i^{\alpha_i}$，则

$$d(n)=\prod_{i=1}^{s}{(\alpha_i+1)}$$

### 约数和函数筛

设$n=\prod_{i=1}^{s}p_i^{\alpha_i}$，则

$$\sigma(n)=\sum_{d \mid n}{d}=\prod_{i=1}^{s}\sum_{k=0}^{\alpha_i}{p_i^k}$$

---

## 杜教筛
杜教筛适用于求解积性函数的前缀和问题，其复杂度为$O(n^\frac{3}{4})$，经过优化可以降到$O(n^\frac{2}{3})$。

但是，受限颇多。

令$f(x)$为一个积性函数，求$S(n)=\sum_{i=1}^{n}f(i)$

我们考虑引入另一个积性函数$g(n)$，它们的**迪利克雷乘积**为$h(n)$

下面开始推表达式：
$$
\begin{aligned}
\sum_{i=1}^{n}{h(i)}
&= \sum_{i=1}^{n}\sum_{d \mid i}{g(d)f(\frac{i}{d})}\newline
&= \sum_{d=1}^{n}{g(d)}\sum_{i=1}^{\lfloor \frac{n}{d} \rfloor}{f(i)}\newline
&= \sum_{d=1}^{n}{g(d)S(\lfloor \frac{n}{d} \rfloor)}
\end{aligned}
$$

所以有
$$g(1)S(n)=\sum_{i=1}^{n}{h(i)}-\sum_{i=2}^{n}{g(i)S(\lfloor \frac{n}{i} \rfloor)}$$

> 现在，如果我们想快速得到$S(n)$，就得很快知道$\sum{h(i)},\sum{g(i)}$

### 杜教筛的限制
+ 引入的积性函数$g(n)$的前缀和容易计算
+ $h(n)$的前缀和容易计算

### 优化方式
预处理出$n^{\frac{2}{3}}$以内的前缀和，使得递归的出口更快得到。

### 洛谷 P4213 【模板】杜教筛（Sum）

> [洛谷 P4213 【模板】杜教筛（Sum）](https://www.luogu.com.cn/problem/P4213)
>
> **题目描述：**
>
> 给定一个正整数，求
> $$ans_1=\sum_{i=1}^{n}{\varphi(i)},ans_2=\sum_{i=1}^{n}{\mu(i)}$$

+ **1.欧拉函数的前缀和**

考虑积性函数$g(n)=1(n)=1$，则

$$h(n)=\sum_{d \mid n}{\varphi(d)}=n$$

由我们上面的结论得到：

$$S(n)=\sum_{i=1}^{n}{i}-\sum_{i=2}^{n}{S(\lfloor \frac{n}{i} \rfloor)}$$

+ **2.麦比乌斯函数的前缀和**

依旧考虑积性函数$g(n)=1(n)=1$，则

$$h(n)=\sum_{d \mid n}{\mu(d)}=\lfloor \frac{1}{n} \rfloor$$

$$S(n)=\sum_{i=1}^{n}{\lfloor \frac{1}{i} \rfloor}-\sum_{i=2}^{n}{S(\lfloor \frac{n}{i} \rfloor)}$$

```cpp P4213.cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

const int maxn = 5e6;

int pr[maxn], cnt;
bitset<maxn + 5> ok;
ll phi[maxn + 5];
int mu[maxn + 5];

unordered_map<int, pair<ll, ll> > spm;

void func(int n) {
	mu[1] = phi[1] = 1;
	for (int i = 2; i <= n; i ++) {
		if (!ok[i]) pr[++ cnt] = i, phi[i] = i - 1, mu[i] = -1;
		for (int j = 1; j <= cnt && pr[j] <= n / i; j ++) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) {
				phi[pr[j] * i] = phi[i] * pr[j];
				break;
			} else {
				phi[pr[j] * i] = phi[pr[j]] * phi[i];
				mu[pr[j] * i] = -mu[i];
			}
		}
	}
	for (int i = 1; i <= n; i++) phi[i] += phi[i-1], mu[i] += mu[i-1];
}

inline void slove(ll n, ll & ans1, ll & ans2) {
	if (n <= maxn) {
		ans1 = phi[n], ans2 = mu[n];
		return ;
	}
	if (spm.count(n)) {
		ans1 = spm[n].first, ans2 = spm[n].second;
		return ;
	}
	ans1 = 1LL * n * (n + 1) >> 1LL, ans2 = 1LL;
	for (ll l = 2, r; l <= n; l = r + 1) {
		r = n / (n / l);
		ll a, b;
		slove(n / l, a, b);
		ans1 -= a * (r - l + 1), ans2 -= b * (r - l + 1);
	}
	spm[n] = { ans1, ans2 };
}

int main() {
	func(maxn);
	int T; scanf("%d", &T);
	while (T -- ) {
		ll n, ans1, ans2;
		scanf("%lld", &n);
		slove(n, ans1, ans2);
		printf("%lld %lld\n", ans1, ans2);
	}
	return 0;
}
```

### 洛谷 P3768 简单的数学题

> [洛谷 P3768 简单的数学题](https://www.luogu.com.cn/problem/P3768)
>
> **题目描述**
>
> 由于出题人懒得写背景了，题目还是简单一点好。
>
> 输入一个整数 $n$ 和一个整数 $p$ ，你需要求出：
> $$\left(\sum_{i=1}^n\sum_{j=1}^n ij \gcd(i,j)\right) \bmod p$$

**由于这是一篇讲筛法的博客，这里略去莫反的部分应该理所应当吧（~~读者自证不难~~）**

简单套路莫比乌斯反演得到答案形式：

$$ANS=\sum_{i=1}^{n}{F^2(i)}\times i^2\varphi(i),F(i)=\sum_{i=1}^{\lfloor\frac{n}{i}\rfloor}{i}$$

前者分块，后者杜教筛。

现在我们待求的$S(n)=\sum_{i=1}^{n}i^2\varphi(i)$，令$f(n)=n^2\varphi(n)$。

有了上面的经验，我们自然想要得到$\sum_{d\mid n}{\varphi(d)}=n$

所以，要是能把$f(n)$前面的$n^2$消去就好了

回忆一下迪利克雷乘积$h(n)=\sum_{d\mid n}{f(d)g(\frac{n}{d})}$，代入$f(n)$的表达式：

$$h(n)=\sum_{d\mid n}{d^2\varphi(d)g(\frac{n}{d})}$$

所以$g(n)$的构造就很明显啦，$g(n)=n^2$完全积性

此时

$$h(n)=\sum_{d\mid n}d^2\varphi(d)(\frac{n}{d})^2=n^2\sum_{d\mid n}\varphi(d)=n^3$$

最终，代回最初的结论就好了

$$S(n)=\sum_{i=1}^{n}{i^3}-\sum_{i=2}^{n}{i^2S(\lfloor \frac{n}{i} \rfloor)}$$

```cpp P3768.cpp
#include <bits/stdc++.h>
#define PII pair<int, int>
#define PLL pair<ll, ll>
#define re #define il inline
#define pb push_back
#define ps push
#define fi first
#define se second
#define mp make_pair
#define ld nd << 1
#define rd nd << 1 | 1
#define fin freopen("_.in", "r", stdin), freopen("output.out", "w", stdout)
#define fast ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0)
using namespace std;

typedef long long ll;
typedef unsigned long long ull;

const int maxn = 5e6;


int pr[maxn], cnt;
bitset<maxn + 10> ok;
ll phi[maxn + 10];

ll n, p, inv;

unordered_map<ll, ll> sp;

il ll qpow(ll x, ll n, ll res = 1LL) {
	for ( ; n; n >>= 1, x = x * x % p) if (n & 1) res = res * x % p;
	return res;
}

il ll sum2(ll n) { return n %= p, (n * n + n >> 1LL) % p * (n << 1 | 1) % p * inv % p; }

il ll sum3(ll n) { return n %= p, qpow((n * n + n >> 1LL) % p, 2); }

void init(int n) {
	inv = qpow(3, p - 2);
	phi[1] = 1;
	for (re int i = 2; i <= n; i++) {
		if (!ok[i]) pr[++ cnt] = i, phi[i] = i - 1LL;
		for (re int j = 1; j <= cnt && pr[j] <= n / i; j++) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) {
				phi[pr[j] * i] = phi[i] * pr[j];
				break;
			} else {
				phi[pr[j] * i] = phi[pr[j]] * phi[i];
			}
		}
	}
	for (re int i = 1; i <= n; i++) phi[i] = (phi[i-1] + 1LL * i * i % p * phi[i]) % p;
}

il ll slove(ll n) {
	if (n <= maxn) return phi[n];
	if (sp.count(n)) return sp[n];
	ll res = sum3(n);
	for (re ll l = 2, r; l <= n; l = r + 1) {
		r = n / (n / l);
		res = (res - (sum2(r) - sum2(l-1) + p) % p * slove(n / l) % p + p) % p;
        res = (res - (sum2(r) - sum2(l-1) + p) % p * slove(n / l) % p + p) % p;
		res = (res - (sum2(r) - sum2(l-1) + p) % p * slove(n / l) % p + p) % p;
	} return sp[n] = res;
}

int main() {
	scanf("%lld%lld", &p, &n);
	init(maxn);
	ll ans = 0;
	for (re ll l = 1, r; l <= n; l = r + 1) {
		r = n / (n / l);
		ans = (ans + sum3(n / l) * (slove(r) - slove(l-1) + p) % p) % p;
	}
	printf("%lld\n", ans);
	return 0;
}
```

---

## PN筛
这是对杜教筛的进一步拓展。

不一定比Min_25好用，但是如果能优化，会很优秀。

### 前置知识
{{< admonition tip "Tip" true >}}
有**迪利克雷乘积**，**迪利克雷逆函数**，**积性函数**知识的可以选择跳过。
{{< /admonition >}}

+ 如果$g,h=f*g$均为积性函数，则$f$也为积性函数。

反证法，如果$f(n)$不是积性函数，则

$$\exists n,m\in Z^+,(n, m)=1,\mathrm{s.t. }f(nm) \neq f(n)f(m)$$

我们取这样一对$n,m$使得$nm$最小。

1. $mn = 1$

   则有$f(1)\neq f(1)f(1)$，即$f(1)\neq 1$，但是$h(1)=1=f(1)g(1)=f(1)$，矛盾。
2. $nm > 1$

   则对于所有$a,b\in Z^+,(a,b)=1,ab<nm$有$f(ab)=f(a)f(b)$成立。
   $$
	 \begin{aligned}
   h(nm)
	 &= \sum_{a\mid n}\sum_{b\mid m}f(ab)g(\frac{nm}{ab})\newline
   &= f(nm)g(1) + \sum_{a\mid n, b\mid m, ab<nm}f(ab)g(\frac{n}{a}\times\frac{m}{b}) \newline
   &= f(nm)g(1) + \sum_{a\mid n, b\mid m, ab<nm}f(a)f(b)g(\frac{n}{a})g(\frac{m}{b}) \newline
   &= f(nm) - f(n)f(m) + \sum_{a\mid n}f(a)g(\frac{n}{a})\sum_{b\mid m}f(b)g(\frac{m}{b}) \newline
   &= h(n)h(m) + \left(f(nm) - f(n)f(m)\right)
   \end{aligned}
	 $$
   与$h$为积性函数矛盾。

综上得证。

---

+ 若数论函数$f(n)$满足$f(1)\neq0$，则存在唯一的$f^{-1}(n)$为$f(n)$的**迪利克雷逆函数**，使得$f*f^{-1}=I$，其中$I(n)=[\frac{1}{n}]$。

使用数学归纳法证明：

1. $f^{-1}(1)*f(1)=f^{-1}(1)f(1)=1$，即$f^{-1}(1)=\frac{1}{f(1)}$。
2. 设$\forall i < k(k\geq2), f^{-1}(i)$唯一确定。

   由于$\sum_{d\mid k}f^{-1}(d)f(\frac{k}{d})=0$，我们得到

   $$f(1)f^{-1}(k)+\sum_{d\mid k, d<k}f^{-1}(d)f(\frac{k}{d})=0$$

   显然$f^{-1}(k)$也被唯一确定。

综上得证。

---

### PN筛的推导

首先我们考虑引入一个**拟合函数**$g(x)$，满足$g(p)=f(p)$，且$g(x)$为**积性**函数、**前缀和易求**。

令$h=f*g^{-1}$，

$$f(p)=g(1)h(p)+h(1)g(p) \Rightarrow h(p)=0$$

所求的前缀和为:

$$
\begin{aligned}
S(n) 
&= \sum_{i=1}^{n}f(i)\newline
&= \sum_{i=1}^{n}\sum_{d\mid i}h(d)g(\frac{i}{d})\newline
&= \sum_{d=1}^{n}h(d)\sum_{i=1}^{\lfloor\frac{n}{d}\rfloor}g(i)
\end{aligned}
$$

> **Powerful Number**:
> 由于$h(p)=0$，且$h$为积性函数，则仅当$n$满足下面的条件时，$h(n)$才有贡献。
> $$n=\prod_{i=1}^{s} p_i^{t_i},\forall i \in [1, s],t_i>1$$
> **关于PN的数目**，从莫比乌斯函数的角度考虑，应该为$n-\sum_{i=1}^{n}\mu^2(i)$，但是这样并不能很好的计算值。
>
> 这里用PN的一个性质，$n\in PN,\exists a,b, \mathrm{s.t. } n=a^2b^3$，则结果为$\sum_{a=1}^{\sqrt n}\sqrt[3]{\frac{n}{a^2}}$，用积分可以简单求值为$O(\sqrt n)$。

现在需要做的是：

1. 处理$g(n)$的前缀和
2. 预处理$h(p^k)$的值`h[p][k]`
3. 在`dfs`时加上PN的贡献

$$f(p^k)=\sum_{i=0}^{k}h(p^i)g(p^{k-i})$$

如果可以计算得到$h(p^k)$的表达式，则可以大大降低复杂度（很容易卡`h[p][k]`）。

### PN筛的示例
> [gym 103306 Flipped Factorization](https://codeforces.com/gym/103306/problem/F)
>
> $$n=\prod p_i^{e_i}(p_i\in Prime), f(n)=\prod e_i^{p_i},f(1)=1$$
> 求前缀和，取模`1e9+7`

令$g=1,f=h*g$，易推知：

$$f(p^k)=\sum_{i=0}^{k}h(p^i)g(p^{k-i})=\sum_{i=0}^{k}h(p^i)\rightarrow h(p^k)=f(p^k)-f(p^{k-1})$$

前缀和为：

$$\begin{aligned} Ans&=\sum_{i=1}^{n}f(i)\newline &=\sum_{i=1}^{n}\sum_{d\mid i}h(d)\newline &=\sum_{d=1}^{n}h(d)\times\lfloor\frac{n}{d}\rfloor \end{aligned}$$

`dfs`去寻找PN时，带上$d,h(d)$更新答案即可。

```cpp
#include <algorithm>
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <queue>
#include <vector>
#include <string>
#include <stack>
#include <set>
#include <map>
#include <bitset>
#define PII pair<int, int>
#define mp make_pair
#define fi first
#define se second
#define ps push
#define all(a) a.begin(), a.end()
#define pb push_back
#define vec vector
#define str string
using namespace std;
typedef long long ll;

const int N = 1e7 + 10;
const int mod = 1e9 + 7;

int cnt;

ll pr[N];
bitset<N> ok;

ll n, sq, ans;

ll qpow(ll x, ll n) {
  ll res = 1LL;
  for (x %= mod; n; n >>= 1, x = x * x % mod)
    if (n & 1LL) res = res * x % mod;
  return res;
}

void dfs(ll x, ll h, int num) {
  ll lim = n / x;
  ans = (ans + lim % mod * h % mod) % mod;
  for (int i = num + 1; i <= cnt; i++) {
    if (1LL * pr[i] * pr[i] > lim) break;
    ll cur = 1LL * x * pr[i] * pr[i], tmp = n / pr[i];
    for (int j = 2; cur <= n; j++, cur = cur * pr[i]) {
      dfs(cur, (qpow(j, pr[i]) - qpow(j-1, pr[i]) + mod) % mod * h % mod, i);
      if (cur > tmp) break;
    }
  }
}

int main() {
  scanf("%lld", &n), sq = sqrtl(n) + 1;
  for (int i = 2; i <= sq; i++) {
    if (!ok[i]) pr[++cnt] = i;
    for (int j = 1; j <= cnt && 1LL * i * pr[j] <= sq; j++) {
      ok[i * pr[j]] = 1;
      if (i % pr[j] == 0) break;
    }
  }
  dfs(1, 1, 0);
  printf("%lld", ans);
  return 0;
}
```

---

## 洲阁筛

~~州阁筛已经被杜教筛和Min25筛踩爆了（吧），要不就鸽了吧~~

~~之后必更新~~

---

## Min_25筛

设有积性函数$f(n)$，目标是求其前缀和$S(n),n\leq 1e10$

### 约定
+ $p\in\textrm{Prime Set}$.
+ $LPF(i)$ denotes the minimal prime factor divisor of $i$.

### 推导

$$
\begin{aligned}
\sum_{i=1}^{n}{f(i)}&=f(1)+\sum_{2\leq p\leq n}\sum_{2\leq i\leq n,LPF(i)=p}{f(i)}\newline
&=f(1)+\sum_{2\leq p\leq \sqrt n}\sum_{2\leq i\leq n,LPF(i)=p}{f(i)}+\sum_{\sqrt n < p\leq n}{f(p)}\newline
&=1+\sum_{2\leq p\leq \sqrt n}\sum_{e\geq 1, 2\leq p^e \leq n}{f(p^e)}\left(1 + \sum_{2\leq j\leq \lfloor \frac{n}{p^e} \rfloor,LPF(j)>p}{f(j)} \right)+\sum_{\sqrt n<p\leq n}{f(p)}\newline
\end{aligned}
$$

---

$$\textrm{let }G(n,m)=\sum_{2\leq i\leq n,LPF(i)>m}{f(i)},F(n)=\sum_{2\leq p\leq n}{f(p)}$$

$$
\begin{aligned}
G(n,m)&=\sum_{2\leq i\leq n,LPF(i)>m}{f(i)}\newline
&=\sum_{m<p\leq \sqrt n}\sum_{e\geq 1,2\leq p^e\leq n}f(p^e)\left(1+\sum_{2\leq j\leq \lfloor\frac{n}{p^e} \rfloor,LPF(j)>p}f(j) \right) +\sum_{\sqrt n < p\leq n}{f(p)} \newline
&=\sum_{m<p\leq\sqrt n}\sum_{e\geq 1,2\leq p^e\leq n}{f(p^e)}\left([e>1]+ \sum_{2\leq j\leq \lfloor\frac{n}{p^e} \rfloor,LPF(j)>p}{f(j)} \right)+\sum_{m<p\leq n}f(p)\newline
&=\sum_{m<p\leq\sqrt n}\sum_{e\geq 1,2\leq p^e\leq n}{f(p^e)}\left([e>1]+G(\lfloor \frac{n}{p^e} \rfloor,p) \right)+\left(F(n)-F(m)\right)\newline
\end{aligned}
$$

到目前为止，我们只要快速求出（预处理）$F(i)$，就能通过递推得到答案$S(n)=G(n,0)+1$。

这里，插空说一下Min25筛的要求：

+ $f(p)$为一个低阶多项式，即$\sum a_ip^{s_i}$的形式。（或者**表达式**是**完全积性**且易求前缀和的）
+ $f(p^s)$易求得。

---

怎么求$F(n)$呢？

**下面是Min25筛法最精髓的部分，也就是利用埃氏筛法的思想。**

我们先这样思考这样一个问题：筛去$n$以内的合数，需要多少个素数呢？

用最小的质因子去筛数，大于它且能被其整除的数都是合数。我们都知道$n$以内的合数的最小质因子不大于$\sqrt n$，所以我们只需要$\pi(\sqrt n)$个素数就能完成这一筛数过程。

同样的，我们待求的$F(n)$表示$n$以内的全部素数的贡献。

那么，如果能表示出埃氏筛每次筛数对结果的影响，那么就能通过递推得到筛完$+\infty$个素数后，所得的值就之后素数的贡献了。

> $+\infty$仅意味着确保只有质数的贡献，实际上只需要$\pi(\sqrt n)$就可以。

---

考虑这样一个函数

$$H(i,n)=\sum_{1\leq k\leq n,k\in Prime \lor k=1 \lor LPF(k)>p_i}{k^s}$$

这里的$p_i$表示第$i$大的素数。

$$
H(i,n)=
\begin{cases}
H(i-1,n)-p_i^s\left(H(i-1,\lfloor\frac{n}{p_i}\rfloor)-H(i-1,p_{i-1})\right) & \textrm{if } p_i\leq\sqrt{n} \newline
H(i-1,n)		& \textrm{otherwise}		\newline
\end{cases}
$$

根据$H(i,n)$与$F(n)$的关系$F(n)=H(+\infty,n)$，我们只需要$\sqrt n$以内的素数就能求出$F(n)$了。

---

好了，看着dalao的论文口嗨完了Min25筛，现在我们来实现一下

### 示例
> [Luogu P5325 【模板】Min_25筛](https://www.luogu.com.cn/problem/P5325)
>
> 设$f(x)$为积性函数，且$f(p^k)=p^k(p^k-1)$，求$\sum_{i=1}^{n}f(i)\bmod 1e9+7$.

显然$f(p^k)=(p^k)^2-(p^k)$，满足所需条件。

我们让$h1$对应一次项，$h2$对应二次项，则所求的函数就可以表示为

$$F(n)=h2(+\infty,n)-h1(+\infty,n)$$

再利用之前的递推式就可以预处理得到。

首先，处理$H(i-1,p_{i-1})$时，（也就是只有前$i-1$个素数的贡献）往往通过线性筛根据其积性函数的性质预处理出来。

其次，通过上述式子可以发现我们可以利用滚动数组来减少一维的开销，从而降低空间复杂度。再者，分块的值的数目也有限，我们通过离散化来降低空间的开销到$O(\sqrt n)$。具体来说，我们把分块值用$\sqrt n$来分治，小于的部分直接存下，大于的部分取$[\frac{n}{x}]$使得其值小于$\sqrt n$。当然，为了避免冲突，这两部分的值分别放在两个数组中记录。


```cpp P5325.cpp
#include <bits/stdc++.h>
#define PII pair<int, int>
#define PLL pair<ll, ll>
#define re #define il inline
#define vec vector
#define pc putchar
#define gc getchar
#define pb push_back
#define ps push
#define fi first
#define se second
#define mp make_pair
#define ld nd << 1
#define rd nd << 1 | 1
#define fin freopen("_.in", "r", stdin), freopen("output.out", "w", stdout)
#define fast ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0)
using namespace std;

typedef long long ll;
typedef unsigned long long ull;

const int maxn = 1e6 + 50;
const double eps = 1e-8;

const ll mod = 1e9 + 7;
const ll inv2 = 500000004;
const ll inv3 = 333333336;

ll pr[maxn]; int cnt = 0;
bitset<maxn> ok;

ll n, sq;
ll s1[maxn], s2[maxn];
ll h1[maxn], h2[maxn];
ll block[maxn]; int tot = 0;
ll idx1[maxn], idx2[maxn];

il ll sum1(ll x) { return x %= mod, x * (x + 1) % mod * inv2 % mod; }

il ll sum2(ll x) { return x %= mod, sum1(x) * (x << 1LL | 1LL) % mod * inv3 % mod; }

void init() {
	sq = sqrt(n);
	for (re int i = 2; i <= sq; i++) {
		if (!ok[i]) pr[++ cnt] = i;
		for (re int j = 1; j <= cnt && pr[j] * i <= sq; j++) {
			ok[pr[j] * i] = 1;
			if (i % pr[j] == 0) break;
		}
	}
	for (re int i = 1; i <= cnt; i++) {
		s1[i] = (s1[i-1] + pr[i]) % mod;
		s2[i] = (s2[i-1] + pr[i] * pr[i] % mod) % mod;
	}
	for (re ll l = 1, r; l <= n; l = r + 1) {
		r = n / (n / l); block[++ tot] = n / l;
		h1[tot] = (sum1(block[tot] % mod) - 1 + mod) % mod;
		h2[tot] = (sum2(block[tot] % mod) - 1 + mod) % mod;
		block[tot] <= sq ? idx1[block[tot]] = tot : idx2[n / block[tot]] = tot;
	}
	for (re int i = 1; i <= cnt; i++) {
		for (re int j = 1; j <= tot && pr[i] * pr[i] <= block[j]; j++) {
			ll tmp = block[j] / pr[i];
			int pos = tmp <= sq ? idx1[tmp] : idx2[n / tmp];
			h1[j] = (h1[j] - pr[i] * (h1[pos] - s1[i-1] + mod) % mod + mod) % mod;
			h2[j] = (h2[j] - pr[i] * pr[i] % mod * (h2[pos] - s2[i-1] + mod) % mod + mod) % mod;
		}
	}
}

il ll G(ll x, int i) {
	if (pr[i] >= x) return 0;
	int pos = x <= sq ? idx1[x] : idx2[n / x];
	ll res = ((h2[pos] - h1[pos] + mod) % mod - (s2[i] - s1[i] + mod) % mod + mod) % mod;
	for (re int k = i + 1; k <= cnt && pr[k] * pr[k] <= x; k++) {
		ll pe = pr[k];
		for (re int e = 1; pe <= x; e++, pe = pe * pr[k]) {
			ll t = pe % mod;
			res = (res + t * (t - 1) % mod * (G(x / pe, k) + (e > 1)) % mod) % mod;
		}
	} return res;
}

int main() {
	scanf("%lld", &n), init();
	printf("%lld\n", (1LL + G(n, 0)) % mod);
	return 0;
}
```
