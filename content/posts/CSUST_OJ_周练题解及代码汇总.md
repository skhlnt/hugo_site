---
title: "CSUST - OJ周练题解及代码汇总"
date: 2022-05-09T20:43:10+08:00
draft: true
slug: 527e3034

author: "Kenshin2438"
description: ""
summary: ""
categories: 
  - CSUST
tags: 
  - Contest

weight: false
math: true
comments: true
TocOpen: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

{{< admonition warning "Warning" true >}}
代码都是重新写的，所以更新得比较慢，还有部分代码之后再拉上来（最近我考试比较多），如果你们现在需要的话直接私聊我也行。

如果有任何问题，可以直接去群里或者私下找学长学姐问。

**代码可以参考，但不要直接照抄**，不然看起来是补了题，实则不懂的还是不懂！！！

---

编译参数：

```bash
"g++" -std=c++17 -Wall -Ofast -DLOCAL "ac.cpp" -o "ac.exe" 
```

代码缺省：

```cpp
#include <bits/stdc++.h>
using namespace std;

#ifdef LOCAL
#include "debug.hpp"
#else
#define debug(...) 42
#endif

#define PII pair<int, int>
#define vec vector
#define str string
#define fi first
#define se second
#define all(a) (a).begin(), (a).end()
#define SZ(x) static_cast<int>((x).size())

using db = double;
using ll = long long;

void SingleTest(int TestCase) {
  
}

void init() {}

int main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  // cout << fixed << setprecision(10);
  int T = 1, TestCase = 0;
  // cin >> T;
  for (init(); T--;) SingleTest(++TestCase);
  return 0;
}
```
{{< /admonition >}}

<!-- more -->

## 4.10

### A 数论king

**勒让德定理**

我们知道$\lfloor \frac{n}{k} \rfloor$表示区间$[1,n]$中包含因子$k$的数的个数。

题目所求的即为：包含因子$5^1,5^2,5^3,\dots$的数的个数。

```cpp
ll pot(ll n, ll p) { // 求 n! 中素数 p 的指数
  ll res = 0;
  while (n) res += n / p, n /= p;
  return res;
}

void SingleTest(int TestCase) {
  ll n; cin >> n;
  cout << pot(n, 5) << '\n';
}
```

### B 厂里数论王

**同余**

$$
\text{sum}_i - \text{sum}_j \equiv 0 \pmod{m} \Rightarrow \text{sum}_i \equiv \text{sum}_j \pmod{m}
$$

在循环时记录前缀和模$m$的值，再去看是否存在重复出现的情况即可。

```cpp
void SingleTest(int TestCase) {
  int n, m; cin >> n >> m;
  vec<ll> a(n);
  for (ll &x : a) cin >> x;

  set<ll> s{ 0 };
  ll sum = 0;
  for (const ll &x : a) {
    sum = (sum + x) % m;
    if (s.find(sum) != s.end()) return cout << "YES\n", void();
    s.insert(sum);
  }
  cout << "NO\n";
}
```

### C 暴力出奇迹

**排序不等式**

$$
\sum_{1\leq l\leq r\leq n}f(l,r)=\sum_{1\leq l\leq r\leq n}\sum_{i=l}^{r}a_i\times b_i=\sum_{i=1}^{n}i\times (n-i+1)\times a_i\times b_i
$$

对于两序列乘积和的最值问题，很容易联想到的是排序不等式，逆序和最小。（这里不做证明）

题目中，$i\times (n-i+1)\times a_i$确定，可以由它构造出一个新的数组，求它与$b$数组的逆序和。

```cpp
void SingleTest(int TestCase) {
  int n; cin >> n;
  vec<ll> a(n), b(n);
  for (int i = 0; i < n; i++) {
    cin >> a[i];
    // 注意此时还不能取模
    a[i] = a[i] * (n - i) * (i + 1);
  }
  sort(all(a));
  for (ll &x : b) cin >> x;
  sort(all(b), greater<ll>());
  const int mod = 998244353;
  ll ans = 0;
  for (int i = 0; i < n; i++) {
    ans = (ans + (a[i] % mod) * b[i] % mod) % mod;
  }
  cout << ans << '\n';
}
```

### D 打包商品

**并查集**

祖宗节点记录当前集合中的最大值和最小值。

```cpp
void SingleTest(int TestCase) {
  int n, m, k;
  cin >> n >> m >> k;
  vec<int> p(n + 1);
  iota(all(p), 0);
  vec<PII> val(n + 1); // max, min
  for (int i = 1; i <= n; i++) {
    cin >> val[i].fi;
    val[i].se = val[i].fi;
  }
  const function<int (int)> f = [&](int x) -> int {
    return x == p[x] ? x : p[x] = f(p[x]);
  };
  for (int u, v; m--; ) {
    cin >> u >> v;
    u = f(u), v = f(v);
    if (u == v || (val[u].fi - val[v].se > k) || (val[v].fi - val[u].se > k)) {
      continue;
    }
    if (u > v) swap(u, v);
    p[v] = u;
    val[u].fi = max(val[u].fi, val[v].fi);
    val[u].se = min(val[u].se, val[v].se);
  }
  for (int i = 1; i <= n; i++) {
    int fa = f(i);
    cout << fa << ' ' << val[fa].fi - val[fa].se << '\n';
  }
}
```

### E 他们说要我出一道签到题

Catalan数

**可以参考：https://zhuanlan.zhihu.com/p/31050581**

题目可以转换成格路问题，要求的实际是安排$n$次入栈和出栈的时间（放在格路问题中就是向左和向上的时间）

但由于出栈时栈中必须还有数字存在，所以要求出栈时刻的位置不能越过$n\times n$方格的对角线。

最后计算的方式有很多中，递推和通项计算都能通过本题。

```cpp
const int mod = (int) 1e9 + 7;

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

ll inv(ll x, ll p) { return qpow(x, mod - 2, mod); }

void SingleTest(int TestCase) {
  int n; cin >> n;
  vec<ll> catlan(n + 1);
  catlan[0] = 1LL;
  for (int i = 1; i <= n; i++) {
    catlan[i] = (4 * i - 2) * inv(i + 1, mod) % mod * catlan[i - 1] % mod;
  }
  cout << catlan[n] << '\n';
}
```

--- 

## 4.12

### A. 简单博弈

Catalan数 +（勒让德定理 / 因式分解）

$$
C_n=\frac{(2n)!}{(n+1)!n!}
$$

本题模数为$1e9$，无法通过求逆元解决计算问题，但是真的要求逆元吗？

可以知道Catalan数是一个整数，考虑将通项的分子分母分解因式，则因子的指数可以确定，最终只要快速幂即可。

#### 勒让德定理（阶乘的因式分解）

对于某个素数$p$，$n!$的分解中$p$的指数就为上面这题的$F(n)$。

素数筛之后，枚举素数同时直接求其指数，然后快速幂。

#### 直接因式分解

不利用勒让德定理，直接因式分解也可以，提供一种卡常数的思路：

处理素数表时记录每个数的**最小素因子 $\text{LPF}$**，然后分解的时候直接除以它的$\text{LPF}$，直到为$1$。

对于数$n$的分解，时间复杂度约为$\mathcal{O}(\frac{\sqrt{n}}{\log{\sqrt{n}}})$。

```cpp
const int mod = (int) 1e9;

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

void SingleTest(int TestCase) {
  int n; cin >> n;
  int m = n << 1;
  vec<int> lpf(m + 1), p, pos(m + 1);
  for (int i = 2; i <= m; i++) {
    if (lpf[i] == 0) {
      lpf[i] = i;
      pos[i] = SZ(p);
      p.push_back(i);
    }
    for (int x : p) {
      if ((ll) x * i > m) break;
      lpf[i * x] = x;
      if (i % x == 0) break;
    }
  }
  vec<ll> pw(SZ(p), 0);
  for (int i = 1; i <= m; i++) {
    int x = i;
    while (x != 1) {
      pw[ pos[lpf[x]] ]++;
      x /= lpf[x];
    }
  }
  for (int i = 1; i <= n; i++) {
    {
      int x = i;
      while (x != 1) {
        pw[ pos[lpf[x]] ]--;
        x /= lpf[x];
      }
    }
    {
      int x = i + 1;
      while (x != 1) {
        pw[ pos[lpf[x]] ]--;
        x /= lpf[x];
      }
    }
  }
  ll ans = 1;
  for (int i = 0; i < SZ(p); i++) {
    ans = ans * qpow(p[i], pw[i], mod) % mod;
  }
  cout << ans << '\n';
}
```

### B. 一步两步

动态规划（注意空间限制）

用$dp[i][j]$表示$i$步之后到达$j$点的方案，第一维只会用到上一层的结果，因此第一维空间开到2就行。

```cpp
void SingleTest(int TestCase) {
  const vec<array<int, 3>> from = {
    {1, 3, 4},
    {0, 2, 5},
    {1, 3, 6},
    {0, 2, 7},
    {0, 5, 7},
    {1, 4, 6},
    {2, 5, 7},
    {3, 4, 6}
  };
  const int mod = (int) 1e9 + 7;

  int n; cin >> n;
  vec<ll> dp(8, 0); dp[0] = 1;
  for (int i = 1; i <= n; i++) {
    vec<ll> ndp(8, 0);
    for (int dot = 0; dot < 8; dot++) {
      auto [a, b, c] = from[dot];
      ndp[dot] = (dp[a] + dp[b] + dp[c]) % mod;
    }
    dp = move(ndp);
  }
  cout << dp[0] << '\n';
}
```

### C. 点击就送

签到

$$
Ans=\sum_{i=1}^{n}\sum_{j=i}^{n}(a_i\times b_j)=\sum_{i=1}^{n}\left(a_i\times\sum_{j=i}^{n}b_j\right)
$$

```cpp
void SingleTest(int TestCase) {
  int n; cin >> n;
  vec<ll> a(n + 1), b(n + 1, 0);
  for (int i = 1; i <= n; i++) cin >> a[i];
  for (int i = 1; i <= n; i++) {
    cin >> b[i];
    b[i] += b[i - 1];
  }
  ll ans = 0;
  for (int i = 1; i <= n; i++) {
    ans += a[i] * (b[n] - b[i - 1]);
  }
  cout << ans << '\n';
}
```

### D. 区间异或

打表

实际上，等差数组的异或存在一定规律。

```cpp
void SingleTest(int TestCase) {
  ll l, r, ans; cin >> l >> r;
  ll len = r - l + 1;
  switch (len % 8) {
    case 0: ans = len; break;
    case 1: ans = len; break;
    case 2: ans = 2; break;
    case 3: ans = 2; break;
    case 4: ans = len + 2; break;
    case 5: ans = len + 2; break;
    case 6: ans = 0; break;
    case 7: ans = 0; break;
  }
  cout << ans << '\n';
}
```

### 直线重合

STL（`set` 或者`map` + `tuple`（可选））

直线方程$Ax+By+C=0$，考虑Hash（直接使用STL）

但是为了确保相同直线不被重复计算，你需要处理一下使得参数满足某个确定的规则，比如：

+ $A,B,C$互素
+ $C$非负

如此$\{A,B,C\}$唯一确定了一条直线，某条直线也唯一对应了一组$\{A,B,C\}$。

表示$\{A, B, C\}$，可以使用`tuple`，也可以放在结构体中重载。

```cpp
void SingleTest(int TestCase) {
  int n; cin >> n;
  set<tuple<ll, ll, ll>> line;
  for (ll x1, x2, y1, y2; n--; ) {
    cin >> x1 >> y1 >> x2 >> y2;
    ll A = x2 - x1;
    ll B = y2 - y1;
    ll C = x1 * y2 - y1 * x2;
    ll g = __gcd(__gcd(A, B), C);
    A /= g, B /= g, C /= g;
    if (C < 0) A *= -1, B *= -1, C *= -1;
    line.insert({A, B, C});
  }
  cout << (int) line.size() << '\n';
}
```

---

## 4.19

这是一个dp场，题解会比较接近代码，但我不希望你们直接抄题解。

个人建议，你们可以从集合的角度来考虑dp的状态划分和转移。

---

### A pph的篮球考试

我们用 `dp[k][n]` 表示第 `n` 轮，有 `k` 个球不中的概率，那么转移方程是很明显的:
```
dp[k][n] = dp[k][n-1] * 1/a[k] + dp[k-1][n-1] * (1 - 1/a[k]);
```
由于结果只与上次和这次决定，开个 2 * 6 的数组保存结果就可以了。

```cpp
const int mod = 998244353;

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

ll inv(ll x, ll p) { return qpow(x, mod - 2, mod); }

void SingleTest(int TestCase) {
  int n; cin >> n;
  vec<ll> dp(6, 0); dp[0] = 1;
  for (int _ = 0; _ < n; _++) {
    ll x; cin >> x;
    x = inv(x, mod);
    vec<ll> ndp(6, 0);
    for (int i = 0; i < 6; i++) {
      if (i == 0) {
        ndp[i] = dp[i] * x % mod;
      } else {
        ndp[i] = dp[i] * x % mod + dp[i - 1] * (1 - x) % mod;
        ndp[i] = (mod + ndp[i] % mod) % mod;
      }
    }
    dp = move(ndp);
  }
  for (int i = 0; i < 6; i++) {
    cout << dp[i] << " \n"[i == 5];
  }
}
```

### B 摸鱼的tomjobs

把相同作业量的作业相加作为一种物品，每种物品都有两种选择 `做` 和 `不做` 。

枚举作业量，`dp[i]`表示前`i`种作业的最佳答案，按照作业量为`i`的物品是否选来分类。

```
dp[i] = max(dp[i-1], dp[i] + dp[i-2] + a[i]);
```

### C 万能代码

**区间dp**

`dp[i][j]` 表示 `s[i..j]` 的最短长度，枚举分界点`k`，按照 `s[i..k]` 是否为 `s[k+1..j]` 的重复串来分类。

```
dp[i][j] = min(dp[i][j], 单个串的长度 + 重复串的个数(R) + 可能要加的(M));
```

否则：

```
dp[i][j] = dp[i][k] + dp[k+1][j];
```

### D 序列变换

观察一下 `00`，`01`，`10`，`11` 在经过迭代后会产生的新的子串，很容易得到其数目的表达式

### E 种花

枚举所有相邻的组合，分别计算期望再求和。

|   获得的钱    |                     0                      |  2000   |
| :-----------: | :-------------------------------------------: | :--: |
| $\mathcal{P}$ | $\mathcal{P}(\text{两人选的数均不含因子p})$ | 其他 |

---

## 4.24 

### A 红黑树

思维

最终串有两种可能的结果 `rbrbrbr...` 和 `brbrbrb...` ，答案为其中操作次数最小的。

对于每一种可能，记录 `b->r` 和 `r->b` 的次数，考虑使用**交换**去减少操作次数。

（**交换**意味着 `b->r` 与 `r->b` 同时增加一次）

### B 摆蔬菜2

滑动窗口

> 滑动窗口的基本思路：
> 使用双指针，分别指向区间的左右两端。首先固定左侧指针，右指针后移，当窗口元素不满足条件时，更新答案 并 移动左侧指针到合适位置。
> 
> 由于左右指针最多移动n次，所以找窗口的复杂度为$\mathcal{O}(n)$。

对于本题，对于每个右端点，其所能选取的剩余子集即为当前合法窗口`[l, r-1]`的所有子集。

```cpp
const int mod = (int) 1e9 + 7;

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x %= mod; n > 0; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

void SingleTest(int TestCase) {
  int n, m; cin >> n >> m;
  vec<ll> a(n);
  for (ll &x : a) cin >> x;
  sort(all(a));
  ll ans = 0;
  for (int l = 0, r = 0; r < n; r++) {
    while (a[r] - a[l] > m) l++;
    // 2的幂可以提前预处理
    ans = (ans + qpow(2, r - l, mod)) % mod;
  }
  cout << ans << '\n';
}
```

### C 摆蔬菜1

滑动窗口 + 单调队列（使用`deque`实现） + 前缀和

单调队列用于维护**后缀最值**，在本题中可以用于维护窗口元素的最值。

具体来说，使用两个单调队列来分别维护当前窗口的最大值和最小值（队首元素为最值），如果此时窗口不满足最值之差小于$m$，则将左指针右移，移动的时候注意更新单调队列。

对于所有合法区间，取区间和的最大值为答案。时间复杂度为$\mathcal{O}(n)$。

```cpp
void SingleTest(int TestCase) {
  int n, m; cin >> n >> m;
  vec<ll> a(n + 1), sum(n + 1, 0);
  for (int i = 1; i <= n; i++) {
    cin >> a[i];
    sum[i] = sum[i - 1] + a[i];
  }
  ll ans = 0;
  deque<ll> Max, Min;
  for (int l = 1, r = 1; r <= n; r++) {
    while (!Max.empty() && a[Max.back()] < a[r]) Max.pop_back();
    Max.push_back(r);
    while (!Min.empty() && a[Min.back()] > a[r]) Min.pop_back();
    Min.push_back(r);
    while (a[Max.front()] - a[Min.front()] > m) {
      if (Max.front() == l) Max.pop_front();
      if (Min.front() == l) Min.pop_front();
      l++;
    }
    ans = max(ans, sum[r] - sum[l - 1]);
  }
  cout << ans << '\n';
}
```

### D zhrt的数据结构课2

线段树（懒标记 区间修改）

线段树在数据结构中十分重要，如何维护和转移是考虑此类题目的一个重点。

考虑对与一个数$X$加 $1$，其权值的变化：

$$
\frac{X(X-1)}{2} \Rightarrow \frac{X(X+1)}{2}
$$

恰好增加了$X$，也就是说区间加 $1$ 时，其中每个数的权值都增加了$X$。

所以，用线段树维护权值和的时候还需要维护$X$的和。

```cpp
const int N = (int) 1e6 + 10;

ll sum[N << 2][2], laz[N << 2];

#define ld nd << 1 | 0
#define rd nd << 1 | 1

void merge(int nd) {
  sum[nd][0] = sum[ld][0] + sum[rd][0];
  sum[nd][1] = sum[ld][1] + sum[rd][1];
}

void apply(int s, int t, int nd, ll val) {
  sum[nd][0] += sum[nd][1] * val + (val - 1) * val / 2 * (t - s + 1);
  sum[nd][1] += val * (t - s + 1);
  laz[nd] += val;
}

void push(int s, int t, int nd) {
  int m = (s + t) >> 1;
  apply(s, m, ld, laz[nd]);
  apply(m + 1, t, rd, laz[nd]);
  laz[nd] = 0;
}

void update(int s, int t, int nd, int L, int R, ll val) {
  if (s > R || t < L) return;
  if (s >= L && t <= R) return apply(s, t, nd, val);
  if (laz[nd]) push(s, t, nd);
  int m = (s + t) >> 1;
  update(s, m, ld, L, R, val);
  update(m + 1, t, rd, L, R, val);
  merge(nd);
}

ll query(int s, int t, int nd, int L, int R) {
  if (s > R || t < L) return 0LL;
  if (s >= L && t <= R) return sum[nd][0];
  if (laz[nd]) push(s, t, nd);
  int m = (s + t) >> 1;
  return query(s, m, ld, L, R) + query(m + 1, t, rd, L, R);
}

void SingleTest(int TestCase) {
  int n, q; cin >> n >> q;
  while (q--) {
    int l, r; char op;
    cin >> op >> l >> r;
    if (op == 'U') update(1, n, 1, l, r, 1);
    else cout << query(1, n, 1, l, r) << '\n';
  }
}
```

上面代码是重新写的，要板子的话可以从下面代码直接扒。

```cpp
template<typename T, typename E, T (*ut)(), E (*ue)(),
  T (*f)(T, T), T (*g)(T, E), E (*h)(E, E)>
struct LazySegTree {
 private:
  int n, _log;
  vec<T> val;
  vec<E> laz;
  void _push(int t) {
    if (laz[t] == ue()) return ;
    val[t << 1 | 0] = g(val[t << 1 | 0], laz[t]);
    val[t << 1 | 1] = g(val[t << 1 | 1], laz[t]);
    if ((t << 1) < n) {
      laz[t << 1 | 0] = h(laz[t << 1 | 0], laz[t]);
      laz[t << 1 | 1] = h(laz[t << 1 | 1], laz[t]);
    }
    return laz[t] = ue(), void();
  }
  void _update(int t) { val[t] = f(val[t << 1 | 0], val[t << 1 | 1]); }
  void _apply(int t, const E &dif) {
    if (dif == ue()) return ;
    val[t] = g(val[t], dif);
    if (t < n) laz[t] = h(laz[t], dif);
  }
 public:
  LazySegTree(const vec<T> &v) {
    n = 1, _log = 0;
    while (n < (int) v.size()) n <<= 1, _log++;
    T ti = ut(); E ei = ue();
    val.resize(n << 1, ti), laz.resize(n, ei);
    for (int i = 0; i < (int) v.size(); i++) val[i + n] = v[i];
    for (int i = n - 1; i > 0; i--) _update(i);
  }
  void update(int l, int r, const E &dif) {
    if (l == r) return ; // update [l, r)
    l += n, r += n;
    for (int i = _log; i >= 1; i--) {
      if (((l >> i) << i) != l) _push(l >> i);
      if (((r >> i) << i) != r) _push((r - 1) >> i);
    }
    for (int a = l, b = r; a < b; a >>= 1, b >>= 1) {
      if (a & 1) _apply(a++, dif);
      if (b & 1) _apply(--b, dif);
    }
    for (int i = 1; i <= _log; i++) {
      if (((l >> i) << i) != l) _update(l >> i);
      if (((r >> i) << i) != r) _update((r - 1) >> i);
    }
  }
  void set(int p, const T& dif) {
    p += n;
    for (int i = _log; i >= 1; i--) _push(p >> i);
    val[p] = dif;
    for (int i = 1; i <= _log; i++) _update(p >> i);
  }
  T get(int p) {
    p += n;
    for (int i = _log; i >= 1; i--) _push(p >> i);
    return val[p];
  }
  T query(int l, int r) {
    if (l == r) return ut();
    l += n, r += n;
    for (int i = _log; i >= 1; i--) {
      if (((l >> i) << i) != l) _push(l >> i);
      if (((r >> i) << i) != r) _push((r - 1) >> i);
    }
    T L = ut(), R = ut();
    for (int a = l, b = r; a < b; a >>= 1, b >>= 1) {
      if (a & 1) L = f(L, val[a++]);
      if (b & 1) R = f(R, val[--b]);
    }
    return f(L, R);
  }
};

namespace SegTreeUtil { // Utilization
template <typename T> T Merge_T(T a, T b) {
  a._ += b._;
  a.sum += b.sum;
  a.len += b.len;
  return a;
}
template <typename T, typename E> T Modify(T a, E b) {
  a.sum += b * a._ + b * (b - 1) / 2 * a.len;
  a._ += b * a.len;
  return a;
}
template <typename E> E Merge_E(E a, E b) {
  return a + b;
}
template <typename T> T Init_T() {
  return T();
}
template <typename E> E Init_E() {
  return E();
}
template <typename T, typename E> struct Tree
  : LazySegTree<T, E, Init_T<T>, Init_E<E>,
  Merge_T<T>, Modify<T, E>, Merge_E<E>> {
  using base =
    LazySegTree<T, E, Init_T<T>, Init_E<E>,
  Merge_T<T>, Modify<T, E>, Merge_E<E>>;

  Tree(const vec<T> &v) : base(v) {}
};
} using SegTreeUtil::Tree;

struct node {
  ll _, sum, len;
  node() : _(0), sum(0), len(1) {}
};

void SingleTest(int TestCase) {
  int n, q; cin >> n >> q;
  vec<node> v(n);
  Tree<node, ll> tr(v);
  while (q--) {
    int l, r; char op;
    cin >> op >> l >> r;
    if (op == 'U') tr.update(l - 1, r, 1);
    else cout << tr.query(l - 1, r).sum << '\n';
  }
}
```

### E 战域

贪心 + 优先队列（结构体重载）

每件物品从使用$x-1$次到使用$x$次降低的能力可以求得。只要在每一轮中，选择降低最少的即可。

$$
\begin{aligned}
\sum_{i=l}^{r}(x_i+1)^2
&=\sum_{i=l}^{r}(x_i^2+2\times x_i+1)\newline
&=\sum_{i=l}^{r}x_i^2+2\times\sum_{i=l}^{r}x_i+\sum_{i=l}^{r}1
\end{aligned}
$$

---

## 4.26

### A 对决

**逆序对**

所求即为，满足$x_a \geq x_b, y_a \leq y_b$，如果按照$x$排序，以$y$作为权值，则满足条件的对决就是逆序对。

逆序对计数使用**树状数组**、**线段树**或者**归并排序**均可。

### B Rap男孩

**DP**

注意到数据范围很小，我们可以通过**DP**去找到第$i$首歌时音量的所有的可能取值。

最后一轮结束后，最大的可能取值为答案；如果所有的数都不可能则为`-1`。

### C 创造创造

**思维**

容易知道，矩形的面积为：

$$
S=(\max{x}-\min{x})\times(\max{y}-\min{y})
$$

由于$x,y$可以任意交换，我们将其放在同一个数组中考虑，容易发现，最大的$n$个数作为$x$坐标，剩下的作为$y$坐标，此时取到面积最小值（再交换$x,y$会带来$S$的增大）。

### D 喝可乐

**二分**

~~本题数据很水，直接模拟能过~~，$k,a_i$的取值实测只到$5e5$。

二分最终的最大值和最小值。

检验时如何判断$\text{mid}$值？以最大值为例，所有比$\text{mid}$大的数都要减到$\text{mid}$，判断此时需要的步数是否超过$k$。同时还需要满足的是，小于$\text{mid}$的部分不会加到比$\text{mid}$还大（这一步可以通过限制二分区间大于等于总和的平均值省略）。

### E 这才是真的冰阔落

**Catalan数（拓展问题）**

首先，使用银行卡的部分可以任意放置，假设有$k$个人使用银行卡。那么，问题就变成：

> $n−k$ 个人排队，他们只有面值为 $50$ 或 $100$ 的钱币，问最终剩余 $50$ 的张数在 $[L,R]$ 的合理方案的数目。

对于这个问题，假设有$a$张$50$和$b$张$100$的钱币（$a \geq b$），则最终剩余的$50$为$a-b$张。且合法方案数为 **不越过对角线的格路问题** 的解。

[参考链接 - 不能“穿越”对角线的格路问题](https://zhuanlan.zhihu.com/p/31050581)

$$
{a+b \choose a} - {a+b \choose a+1}
$$

又因为$a+b=n-k,L \leq a-b \leq R$，则$a$的范围是：

$$
\max(\lceil\frac{n-k+L}{2}\rceil, \lceil\frac{n-k}{2}\rceil) \text{到}\min(n-k, \lfloor\frac{n-k+R}{2}\rfloor)
$$

对于固定的$k$，该问题的答案为：

$$
\begin{aligned}
Ans 
&= \sum_{a=\lceil\frac{n-k+L}{2}\rceil}^{\min(n-k, \lfloor\frac{n-k+R}{2}\rfloor)}\Bigg[{n-k \choose a} - {n-k \choose a+1}\Bigg]\newline
&= {n-k \choose \lceil\frac{n-k+L}{2}\rceil} - {n-k \choose \min(n-k, \lfloor\frac{n-k+R}{2}\rfloor)+1}
\end{aligned}
$$

回到原问题，只要枚举$k$的取值同时计算就能得到答案。

$$
\begin{aligned}
Ans 
&= \sum_{k=0}^{n-L}{n \choose k}\Bigg[{n-k \choose \lceil\frac{n-k+L}{2}\rceil} - {n-k \choose \min(n-k, \lfloor\frac{n-k+R}{2}\rfloor)+1}\Bigg]
\end{aligned}
$$

现在剩下的问题就是取模了，同之前一样这次的模数依旧不是一个的素数。本题需要预处理**组合数**，4.12周练A题给的的方法在这里不太能过。

对于组合数${n \choose m}=\frac{n!}{m! \times (n-m)!}$，$m!$是否能直接求逆元呢？显然不行的，因为它之中可能包含有与$p$不互素的因子。

那么，我们考虑分离其中与$p$互素的部分，按照一般的方法直接求解"阶乘"，"逆元"（并非真正意义上的阶乘，而是去除了与$p$的公因子，剩余数的累乘），不互素的部分（即包含模数$p$的素因子）在求组合数的时候再计算。

时间复杂度 $\mathcal{O}(\sqrt{P} + n \log n \log P)$

+ 相关问题 [Luogu - P4720 【模板】扩展卢卡斯定理/exLucas](https://www.luogu.com.cn/problem/P4720)

```cpp
#include <bits/stdc++.h>
using namespace std;

#ifdef LOCAL
#include "debug.hpp"
#else
#define debug(...) 42
#endif

#define PII pair<int, int>
#define vec vector
#define str string
#define fi first
#define se second
#define all(a) (a).begin(), (a).end()
#define SZ(x) static_cast<int>((x).size())

using db = double;
using ll = long long;

ll qpow(ll x, ll n, ll mod) {
  ll res = 1LL;
  for (x = x % mod; n > 0; n >>= 1, x = x * x % mod) {
    if (n & 1LL) res = res * x % mod;
  }
  return (res + mod) % mod;
}

int n, P, L, R, phi;
vec<int> pr;

int Euler_phi(int n) {
  int phi = n;
  for (int i = 2; i <= n / i; i++) {
    if (n % i == 0) {
      pr.push_back(i);
      phi = phi / i * (i - 1);
      while (n % i == 0) n /= i;
    }
  }
  if (n != 1) {
    pr.push_back(n);
    phi = phi / n * (n - 1);
  }
  return phi;
}

ll fac[100005], inv[100005];
void get() {
  fac[0] = fac[1] = inv[0] = inv[1] = 1;
  for (int i = 2; i <= n; i++) {
    ll x = i;
    for (int p : pr) {
      while (x % p == 0) x /= p;
    } // 除去公因子
    fac[i] = fac[i - 1] * x % P;
    inv[i] = qpow(fac[i], phi - 1, P);
  }
}

ll pot(int n, int p) { // 求 n! 中素数 p 的指数
  ll res = 0;
  while (n) res += n / p, n /= p;
  return res;
}

ll binom(int n, int m) {
  if (n < 0 || n < m || m < 0) return 0LL;
  if (m == 0 || m == n) return 1LL;
  ll res = fac[n] * inv[m] % P * inv[n - m] % P;
  for (int p : pr) {
    ll pw = pot(n, p) - pot(m, p) - pot(n - m, p);
    res = res * qpow(p, pw, P) % P;
  }
  return res;
}

void SingleTest(int TestCase) {
  cin >> n >> P >> L >> R;
  // 处理欧拉函数，用于逆元的计算
  // 同时质因数分解 P
  phi = Euler_phi(P);
  get(); // 预处理互素的部分 fac, inv
  ll ans = 0;
  for (int k = 0; k <= n - L; k++) {
    ll C0 = binom(n, k);
    ll C1 = binom(n - k, (n - k + L + 2 - 1) / 2);
    ll C2 = binom(n - k, 1 + min(n - k, (n - k + R) / 2));
    ans = (ans + (C1 - C2 + 2LL * P) % P * C0 % P) % P;
  }
  cout << ans << '\n';
}

void init() {}

int main() {
  cin.tie(nullptr)->sync_with_stdio(false);
  // cout << fixed << setprecision(10);
  int T = 1, TestCase = 0;
  // cin >> T;
  for (init(); T--;) SingleTest(++TestCase);
  return 0;
}
```

---

## 5.3

### A 动漫明星大乱斗

**思维**

符合题意的人是不会被他人选中的。

### B 小明的数学作业

**DP + 离散化**

一个等差数列可由其中任意的一对相邻的数来确定。

$$
dp[a_i][a_j] = 1 + dp[a_j][a_j + a_j - a_i]
$$

其中$a_i < a_j$。

由于数据范围的问题，我们不可能直接将$a_i$作为下标，但是可以通过离散化将其映射成下标。

### C 还没想好题目的题

**最短路**

$n-1$次最短路，时间刚好卡满。

### D 欺负萌新的佳爷

**二分**

注意到题目的矩阵很特殊，我们可以单独对每一行分析单调性。

所以可以直接二分答案（第`k`大）。

```cpp
void SingleTest(int TestCase) {
  ll n, m, k;
  cin >> n >> m >> k;
  ll a, b, c;
  cin >> a >> b >> c;
  const auto f = [&](ll x, ll y) -> ll {
    return a * x * x + b * x + c * y;
  };
  auto check = [&](ll val) -> bool {
    ll num = 0;
    if (c == 0) {
      for (int x = 1; x <= n; x++) {
        if (f(x, 0) > val) num += m;
      }
    } else if (c > 0) {
      for (int x = 1; x <= n; x++) {
        if (f(x, 1) > val) {
          num += m;
        } else if (f(x, m) > val) {
          num += m - (val - f(x, 0)) / c;
        }
      }
    } else {
      for (int x = 1; x <= n; x++) {
        if (f(x, m) > val) {
          num += m;
        } else if (f(x, 1) > val) {
          ll tmp = val - f(x, 0);
          num += tmp / c - (tmp % c == 0);
        }
      }
    }
    return num < k;
  };
  ll r = 1e17, l = -r, ans;
  while (l <= r) {
    ll mid = (l + r) >> 1;
    if (check(mid)) {
      ans = mid, r = mid - 1;
    } else {
      l = mid + 1;
    }
  }
  cout << ans << '\n';
}
```

### E 这真是一个水题吗

~~<small>显然不是</small>~~

**Hash + 二分**

字符串匹配的算法中，除了喜闻乐见的`KMP`，还有字符串`Hash`。

通过`Hash`+二分我们还能找到当前串最远的匹配长度，利用这一性质就能解决本题。

即，只要在匹配时找最远的匹配位置，若是失配则跳过该位置的字符，继续向后找。

这样的“跳跃”最多只能有$k$次，时间复杂度为 $\mathcal{O}(k\times n\log{n})$。

```cpp
using ull = unsigned long long;

void SingleTest(int TestCase) {
  str a, b; int k;
  cin >> a >> b >> k;
  int n = a.length(), m = b.length();
  if (n < m) return cout << 0, void();
  a = "#" + a, b = "#" + b; // 1-indexed
  const ull base = 131ULL;
  vec<ull> ha(n + 1, 0), hb(m + 1, 0), pw(n + 1, 1);
  for (int i = 1; i <= n; i++) {
    ha[i] = ha[i - 1] * base + a[i];
    pw[i] = pw[i - 1] * base;
  }
  for (int i = 1; i <= m; i++) {
    hb[i] = hb[i - 1] * base + b[i];
  }
  auto check = [&](int pos) -> bool {
    auto same = [&](int l1, int r1, int l2, int r2) -> bool {
      ull HA = ha[r1] - ha[l1 - 1] * pw[r1 - l1 + 1];
      ull HB = hb[r2] - hb[l2 - 1] * pw[r2 - l2 + 1];
      return HA == HB;
    }; // Hash judge
    auto bina = [&](int pa, int pb) -> int {
      int l = 1, r = m - pb + 1, res = 0;
      while (l <= r) {
        int mid = (l + r) >> 1;
        if (same(pa, pa + mid - 1, pb, pb + mid - 1))
          l = mid + 1, res = mid;
        else
          r = mid - 1;
      }
      return res;
    }; // binary search
    int chance = k, pp = 1;
    if (chance == 0) return same(pos, pos + m - 1, pp, pp + m - 1);
    do {
      int d = bina(pos, pp);
      pos += d + (chance > 0), pp += d + (chance > 0);
      if (pp > m) return true;
    } while (chance-- && pos <= n);
    return false;
  };
  int ans = 0;
  for (int i = 1; i + m - 1 <= n; i++) ans += check(i);
  cout << ans << '\n';
}
```