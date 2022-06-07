---
title: "一类同余方程(DLP)的解法 - BSGS"
date: 2021-09-05 11:02:17
draft: true
slug: 4fd858f9

author: "Kenshin2438"
description: ""
categories:
  - Number Theory
tags:
  - BSGS

weight: 2
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
    
    map<ll, ll> bs;
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
    return -1; // No solution
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
        if (n % g != 0LL) return -1; // No solution
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

### 例题代码(TODO)

最小原根的大小会比较小，暴力去枚举求就可以。

暂时口嗨一下算法，等碰见了再来更新。

---

## TODO

+ [x] 复习BSGS
+ [ ] 更新例题（luogu题单）
+ [ ] 原根
+ [ ] k次剩余题目加代码（Nod51）