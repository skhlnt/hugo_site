---
title: "一类同余方程(DLP)的解法 - BSGS"
date: 2021-09-05 11:02:17
draft: true
slug: 4fd858f9

author: "Kenshin2438"
description: "DLP同余方程的解法，以及使用小步大步（BSGS）算法解决离散对数问题。"
keywords:
  - DLP同余方程
  - 离散对数
  - BSGS
  - exBSGS
  - Baby Step/Giant Step Algorithm
  - 小步大步算法
  - "51nod 1038 X^A mod P"
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

$\text{Baby Step/Giant Step Algorithm}$ 用于解决这样一类同余方程的方法

$$a^x \equiv b\pmod c$$

结合原根的知识还能解决模数有原根的$N$次剩余问题

$$x^n \equiv b\pmod c$$

<!--more-->

## 基础问题 $a^x\equiv b\pmod c$

具体来说，`BSGS`的思路就是`分块预处理`+`hash`。

下面分情况讨论：

### 一、$(a,c)=1$

由**欧拉定理**可知$x$的取值范围不会大于$\varphi(c)$，我们直接取$x<c$即可。

$a,c$互素时，存在$a$在模$c$意义下的逆元。

令分块的大小为$\lceil\sqrt c\rceil$，即我们将解的形式限定为$x=A\times\lceil\sqrt c\rceil - B,A,B\in[0,\lceil\sqrt c\rceil]$，直接将$a^B$的部分放到同余式右侧。

现在需要解决的问题变成：

$$a^{A\times\lceil\sqrt c\rceil}\equiv b\times a^{B}\pmod c$$

+ 首先预处理，枚举$b\times a^B$的取值，并将其存下来(`hash`)
+ 枚举$A$的取值，并查看是否存在对应的$B$是得两侧相等。
+ 得到结果，或者无解。

### 二、$(a,c)\neq 1$

一个比较好的想法是，我们将其转换成互素的情况。

由于$ax\equiv b\pmod c, g=\gcd(a, b, c)$可以转化成
$$\frac{a}{g}x\equiv \frac{b}{g}\pmod{\frac{c}{g}}$$

同样的，我们也可以不断去消去$c$中与$a$不互素的部分，从而达到目的

具体步骤为：

+ $a\times a^{x-1}\equiv b\pmod c$
+ $g=(a,c)$，若$g\nmid b$则无解
+ $\frac{a}{g}\times a^{x-1}\equiv \frac{b}{g}\pmod{\frac{c}{g}}$
+ 循环操作直到$(a,c)=1$或$\frac{a^k}{G}=\frac{b}{G}$

### 代码模板

```cpp
ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0LL; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

// a^x EQUIV n (MOD mod), and gcd(a, mod) = 1
ll BSGS(ll a, ll n, ll mod) {
  a %= mod, n %= mod;
  if (n == 1LL || mod == 1LL) return 0LL;

  unordered_map<ll, ll> bs;
  ll S = sqrt(mod) + 1;

  ll base = n;
  for (ll k = 0, val = base; k <= S; k++) {
    bs[val] = k, val = val * a % mod;
  }
  base = qpow(a, S, mod);
  for (ll x = 1, val = base; x <= S; x++) {
    if (bs.count(val)) return x * S - bs[val];
    val = val * base % mod;
  }
  return -1;  // No solution
}

pair<ll, ll> exgcd(ll a, ll b) {
  bool neg_a = (a < 0), neg_b = (b < 0);
  ll x = 1, y = 0, r = 0, s = 1;
  while (b != 0LL) {
    ll t = a / b;
    r ^= x ^= r ^= x -= t * r;
    s ^= y ^= s ^= y -= t * s;
    b ^= a ^= b ^= a %= b;
  }
  return {neg_a ? -x : x, neg_b ? -y : y};
}

ll inv(ll a, ll mod) {
  auto [res, _] = exgcd(a, mod);
  return (res % mod + mod) % mod;
}

// a^x EQUIV n (MOD mod), and gcd(a, mod) != 1
ll exBSGS(ll a, ll n, ll mod) {
  a %= mod, n %= mod;
  if (n == 1LL || mod == 1LL) return 0LL;

  ll k = 0, val = 1;
  for (ll g = __gcd(a, mod); g != 1LL; g = __gcd(a, mod)) {
    if (n % g != 0LL) return -1;  // No solution
    mod /= g, n /= g;
    val = val * (a / g) % mod, k++;
    if (val == n) return k;
  }
  ll res = BSGS(a, n * inv(val, mod) % mod, mod);
  return ~res ? res + k : res;
}
```

### 例题

**暂时** 看我在CSDN发的那篇吧。

[传送门](https://blog.csdn.net/qq_41743740/article/details/118946068)

## $N$次剩余问题（离散对数）

要求模数要有原根，令为$g$。

+ 两侧取离散对数得到$N\log x\equiv \log b\pmod{\varphi(c)}$
+ 求出右侧$\log b$，即求$g^y\equiv b\pmod c$
+ 现在转换为一次同余式的求解

### 例题代码

> **51nod 1038 X^A mod P**
> 
> [题目链接](http://www.51nod.com/Challenge/Problem.html#problemId=1038)
> 
> X^A mod P = B，其中P为**质数**。给出P和A B，求< P的所有X。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
#define all(a) begin(a), end(a)

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0LL; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

// a^x EQUIV n (MOD mod), and gcd(a, mod) = 1
ll BSGS(ll a, ll n, ll mod) {
  a %= mod, n %= mod;
  if (n == 1LL || mod == 1LL) return 0LL;

  unordered_map<ll, ll> bs;
  ll S = sqrt(mod) + 1;

  ll base = n;
  for (ll k = 0, val = base; k <= S; k++) {
    bs[val] = k, val = val * a % mod;
  }
  base = qpow(a, S, mod);
  for (ll x = 1, val = base; x <= S; x++) {
    if (bs.count(val)) return x * S - bs[val];
    val = val * base % mod;
  }
  return -1;  // No solution
}

tuple<ll, ll> exgcd(ll a, ll b) {
  ll x = 1, y = 0, r = 0, s = 1;
  while (b != 0LL) {
    ll t = a / b;
    r ^= x ^= r ^= x -= t * r;
    s ^= y ^= s ^= y -= t * s;
    b ^= a ^= b ^= a %= b;
  }
  return {a, x};
}

void solve() {
  ll a, b, p;
  cin >> p >> a >> b;

  ll phi = p - 1;  // p is a prime number

  b %= p, a %= phi;

  vector<int> fact = [](int n) {
    vector<int> res;
    for (int i = 2; i * i <= n; i++) {
      if (n % i == 0) {
        res.push_back(i);
        while (n % i == 0) n /= i;
      }
    }
    if (n != 1) res.push_back(n);
    return res;
  }(phi);

  ll root = [&fact, &phi](int p) {
    for (ll res = 2; res < p; res++) {
      bool ok = true;
      for (const ll &x : fact) {
        if (qpow(res, phi / x, p) != 1) continue;
        ok = false;
        break;
      }
      if (ok) return res;
    }
    return -1LL;
  }(p);

  ll L = BSGS(root, b, p);
  auto [g, inv] = exgcd(a, phi);
  /**
   * root^log(b) \equiv b (mod p)
   * 
   * a * log(ans) \equiv log(b) (mod phi)
   **/
  if (L % g != 0) return cout << "No Solution\n", void();

  a /= g, L /= g;
  ll mod = phi / g;

  L = (inv * L % mod + mod) % mod;

  vector<ll> ans;
  for (; L < phi; L += mod) {
    ans.push_back(qpow(root, L, p));
  }

  sort(all(ans));
  for (const ll &x : ans) cout << x << ' ';

  cout << '\n';
}

int main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int T;
  cin >> T;

  while (T--) solve();
  return 0;
}
```

## TODO

+ [x] 复习BSGS
+ [ ] 更新例题（luogu题单）
+ [ ] 原根
+ [x] k次剩余题目加代码（Nod51）