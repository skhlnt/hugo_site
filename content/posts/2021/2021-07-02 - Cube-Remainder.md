---
title: "三次剩余 - Peralta Method Extension"
date: 2021-07-02 13:07:26
slug: 8c520df7

author: "Kenshin2438"
description: "三次剩余，以及一个可以继续推广至k次剩余的随机算法"
keywords: 
  - 三次剩余
  - k次剩余
  - 随机算法
  - "LiBreOJ #175. 模立方根"
  - "51Nod - 1039"
  - "Peralta Method"
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

{{< admonition info "Changelog" true >}}
update at 2022/06/10: 更新代码，并且新增范例(51Nod-1039)，用于展示**如何求得所有解**。
{{< /admonition >}}

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

>The Peralta method is a fast way of computing square roots for a prime of form $p=2^eq+1$ $(q \not\equiv0\mod 2)$ for large $e$. 


考虑这样一个环：
$$R=\frac{\mathbb{Z}_p[x]}{x^3-a}=\\{ \alpha+\beta Y+\gamma Y^2 | \alpha,\beta,\gamma\in\mathbb{Z}_p,Y^3=a\\}$$

对于$z\in R$，即$z=\alpha+\beta Y+\gamma Y^2$，有$z^{p-1}\equiv 1\pmod{p}$

如果$z^{\frac{p-1}{3}}=\beta_0 Y$，则有$(\beta_0 Y)^3\equiv\beta_0^3a\equiv1\pmod{p}$，即$\sqrt[3]{a}\equiv\beta_0^{-1}\pmod{p}$

**算法流程**[^1]

> For a prime $p\equiv 1 \mod 3$:
> 
> * Choose $z\in R^*$ at random.
> * Compute $z^(\frac{p-1}{s})=\alpha + \beta Y + \gamma Y^2$.
> * If $\alpha=\gamma=0$, then write($\beta^{-1}\mod p$) otherwise go to Step 1.

随机结果符合条件的概率为$\frac{1}{9}$，所以这个算法的时间复杂度全在快速幂上了。

### Code

```cpp Peralta.cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

mt19937 rng(__builtin_ia32_rdtsc());
inline ll randint(ll l, ll r) {
  return uniform_int_distribution<ll>(l, r)(rng);
}

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0LL; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

struct R {
  ll a, p, x, y, z;

  R(ll _a, ll _p) : a(_a), p(_p) { x = 1LL, y = 0LL, z = 0LL; }
  void rand() {
    x = randint(0, p - 1);
    y = randint(0, p - 1);
    z = randint(0, p - 1);
  }
  R &operator*=(const R &rhs) {
    ll _x = (x * rhs.x + y * rhs.z % p * a + z * rhs.y % p * a) % p;
    ll _y = (x * rhs.y + y * rhs.x + z * rhs.z % p * a) % p;
    ll _z = (x * rhs.z + y * rhs.y + z * rhs.x) % p;
    x = _x, y = _y, z = _z;
    return *this;
  }

  void pow(ll n) {
    R res(a, p), b = *this;
    for (; n; n >>= 1, b *= b) {
      if (n & 1LL) res *= b;
    }
    x = res.x, y = res.y, z = res.z;
  }
};

ll Peralta_Method_Extension(ll a, ll p) {
  a = (a % p + p) % p;
  if (a == 0) return 0LL;

  if (p % 3 == 2) return qpow(a, (p * 2 - 1) / 3, p);
  
  if (qpow(a, (p - 1) / 3, p) != 1LL) return 0LL;
  // No Solution

  R t(a, p);
  while (true) {
    t.rand(), t.pow((p - 1) / 3);
    if (t.x == 0 && t.y != 0 && t.z == 0) {
      return qpow(t.y, p - 2, p);
    }
  }

  assert(false);
  return -1;
}

int main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int T;
  cin >> T;

  while (T--) {
    ll p, a;
    cin >> a >> p;

    cout << Peralta_Method_Extension(a, p) << '\n';
  }

  return 0;
}
```

---

## 51Nod - 1039

问题一致，但需要求得所有可行解。

+ 如果$p \bmod 3 = 2$，则有**唯一解**。
+ 反之，若有解则必定有三个不同值。

上面的代码可求得其中之一，不妨令其为$s$。那么，如何求出其他值呢？对于一般的3次方程$x^3=a$，如果已知一个可行解$s$，那么剩余的解可以用$s$分别乘以单位复根的一次和平方得到。

单位根为$\frac{-1+\sqrt{-3}}{2}$，在模意义下，需要用二次剩余去求解$x^2\equiv-3\pmod{p}$，在下面的代码中，使用了$\text{Tonelli Shanks}$算法计算二次剩余。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

mt19937 rng(__builtin_ia32_rdtsc());
inline ll randint(ll l, ll r) {
  return uniform_int_distribution<ll>(l, r)(rng);
}

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0LL; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

struct R {
  ll a, p, x, y, z;

  R(ll _a, ll _p) : a(_a), p(_p) { x = 1LL, y = 0LL; }
  void rand() {
    x = randint(0, p - 1);
    y = randint(0, p - 1);
    z = randint(0, p - 1);
  }
  R &operator*=(const R &rhs) {
    ll _x = (x * rhs.x + y * rhs.z % p * a + z * rhs.y % p * a) % p;
    ll _y = (x * rhs.y + y * rhs.x + z * rhs.z % p * a) % p;
    ll _z = (x * rhs.z + y * rhs.y + z * rhs.x) % p;
    x = _x, y = _y, z = _z;
    return *this;
  }

  void pow(ll n) {
    R res(a, p), b = *this;
    for (; n; n >>= 1, b *= b) {
      if (n & 1LL) res *= b;
    }
    x = res.x, y = res.y, z = res.z;
  }
};

ll Peralta_Method_Extension(ll a, ll p) {
  a = (a % p + p) % p;
  if (a == 0) return 0LL;

  if (p % 3 == 2) return qpow(a, (p * 2 - 1) / 3, p);
  
  if (qpow(a, (p - 1) / 3, p) != 1LL) return -1LL;
  // No Solution

  R t(a, p);
  while (true) {
    t.rand(), t.pow((p - 1) / 3);
    if (t.x == 0 && t.y != 0 && t.z == 0) {
      return qpow(t.y, p - 2, p);
    }
  }

  assert(false);
  return -1;
}

ll Tonelli_Shanks(ll a, ll p) {
  a = (a % p + p) % p;
  if (a == 0) return 0LL;

  if (qpow(a, (p - 1) / 2, p) != 1LL) return -1LL;
  // No Solution

  if (p % 4 == 3) return qpow(a, (p + 1) / 4, p);

  ll k = __builtin_ctzll(p - 1), h = p >> k, N = 2;
  // p = 1 + h * 2^k
  while (qpow(N, (p - 1) / 2, p) == 1) N++;
  // find a non-square mod p

  ll x = qpow(a, (h + 1) / 2, p);
  ll g = qpow(N, h, p);
  ll b = qpow(a, h, p);

  for (ll m = 0;; k = m) {
    ll t = b;
    for (m = 0; m < k && t != 1LL; m++) {
      t = t * t % p;
    }

    if (m == 0) return x;
    ll gs = qpow(g, 1 << (k - m - 1), p);

    g = gs * gs % p;
    b = b * g % p;
    x = x * gs % p;
  }

  assert(false);
  return -1;
}

int main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  int T;
  cin >> T;

  while (T--) {
    ll p, a;
    cin >> p >> a;

    ll ans = Peralta_Method_Extension(a, p);
    if (~ans) {
      if (p % 3 == 2) {
        cout << ans << '\n';
      } else {
        ll u = qpow(2, p - 2, p) * (Tonelli_Shanks(p - 3, p) - 1) % p;

        vector<ll> out{ans, ans * u % p, ans * u % p * u % p};
        sort(begin(out), end(out));

        cout << out[0] << ' ' << out[1] << ' ' << out[2] << '\n';
      }
    } else {
      cout << "No Solution\n";
    }
  }

  return 0;
}
```

## 参考资料
[^1]: https://www.sciencedirect.com/science/article/pii/S0893965902000319