---
title: "CSUST - 2022 ACM个人排位赛"
date: 2022-08-05T20:50:36+08:00
draft: false
slug: eca83592

author: "Kenshin2438"
description: ""
summary: "出了一堆水题，结果榜歪得离谱？！害，人都麻了。"
categories: 
  - CSUST
tags: 
  - Contest

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

## 写点题外话

出题的时候：

“大水题，大铁牌题” “别出太难了，到时候大家都不会写，跟没出一样。”</br>
“这场是不是太简单了点，**感觉难度都没选拔赛高啊**？”</br>
“预计rank1在8题左右，其他人写个4，5题的样子。”</br>
“20的应该都见过这些题（指字典树和线段树这两题），**感觉要被过穿啊**！”</br>
**“简单点好啊，大家多过点题，开心一点。”**</br>

然后……

“怎么有人搁那挂机啊？” “为什么不关同步流？你在干什么啊？！”</br>
“看不懂。” **“训练了啥？”** “我麻了。” “这个榜是不是有点惨啊。”</br>
“快看看其它题，快看看其它题……” **“hy，你的茶颜没了”**</br>

---

太惨了，不过前面的几位同学打得还可以，在我预期的范围内。其他人要好好加油啊，你们那刷题量也太可怜了，ACM又不是纯理论，是要求代码实现的！暑训没刷个3，4百题，感觉也没什么意义。

给个查刷题数目的网站，都去看看自己。**还有一点就是，为了冲题量而去刷水题没有任何意义。**

+ [OJ Analyzer](https://ojhunt.com/)
+ [CF 刷题类型分析](https://cfviz.netlify.app/)
---

+ 编译参数

```bash
-std=c++17 -Wall -O2 -DLOCAL -ID:\Document\repos\Code-of-ACM\template\debug\
```

如需运行以下代码，编译环境**至少需要c++14，最好是c++17**。

以下代码均为**个人验题**使用的代码，不代表出题人的`std`写法。在语法上，除了**结构化声明和结构化绑定**为`c++17`标准、**复数字面量1i**从`c++14`才开始有[定义](https://en.cppreference.com/w/cpp/numeric/complex/operator%22%22i)，其它用到的语法和函数均在`c++11`标准内。另，使用了`GCC`的`built-in`函数，不保证其它编译器能通过编译。

+ 代码缺省

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
#define all(a) begin(a), end(a)

#ifdef LOCAL
#include "debug.hpp"
#else
#define debug(...) 42
#endif

void solve() {

}

int main() {
  cin.tie(nullptr)->sync_with_stdio(false);

  int T = 1;
  cin >> T;
  while (T--) solve();

  return 0;
}
```

---

## A	小贺爱数学

### 1. 预处理

+ 时间复杂度 $\mathcal{O}(n^2)$

$$
\begin{aligned}
ans 
&= \sum_{i=1}^{n}\sum_{j=1}^{n}\sum_{k=1}^{n}(a[i]\times a[j]\times a[k])\times(i+j+k)!\newline
&= \sum_{k=1}^{n}\sum_{t=2}^{2n}a[k]\times \left(\sum_{i+j=t}a[i]\times a[j]\right)\times(t+k)!\newline
\end{aligned}
$$

```cpp
void solve() {
  const int mod = 1e9 + 7;

  int n; cin >> n;
  vector<ll> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];

  vector<ll> pre(2 * n + 1);
  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
      pre[i + j] = (pre[i + j] + a[i] * a[j]) % mod;
    }
  }

  vector<ll> fac(n * 3 + 1);
  for (int i = fac[0] = 1; i <= n * 3; i++) {
    fac[i] = fac[i - 1] * i % mod;
  }

  ll ans = 0;
  for (int k = 1; k <= n; k++) {
    for (int t = 2; t <= n * 2; t++) {
      ans = (ans + (a[k] * pre[t] % mod) * fac[t + k]) % mod;
    }
  }
  cout << ans << '\n';
}
```

### 2. 多项式写法 (当然，在这个数据范围下是没必要的)

+ 时间复杂度 $\mathcal{O}(n\log{n})$

构造多项式（其实是数列$a_n$的**生成函数**）

$$F(x)=\sum_{i=0}^{\infty}a_i\times x^i$$

然后答案变成 

$$
ans = \sum_{t=3}^{3n}[x^t]F^{3}(x)\times t!
$$

$[x^t]f(x)$表示多项式$f(x)$中$x^t$项的系数。

由于模数$1e9+7$不方便使用$NTT$，下面提供一份使用**拆系数FFT**的代码。（实现任意模数NTT的还有三模数NTT，也称MTT。前置知识大概是，NTT和中国剩余定理）
```cpp
#define sz(x) static_cast<int>((x).size())
using C = complex<double>;
void FFT(vector<C> &a) {
  int n = sz(a), L = 31 - __builtin_clz(n);
  static vector<complex<long double>> R(2, 1);
  static vector<C> rt(2, 1);
  for (static int k = 2; k < n; k <<= 1) {
    R.resize(n), rt.resize(n);
    auto x = polar(1.0L, acos(-1.0L) / k);
    for (int i = k; i < 2 * k; i++) {
      rt[i] = R[i] = i & 1 ? R[i >> 1] * x : R[i >> 1];
    }
  }
  vector<int> rev(n);
  for (int i = 0; i < n; i++) {
    rev[i] = rev[i >> 1] >> 1 | (i & 1) << (L - 1);
  }
  for (int i = 0; i < n; i++) {
    if (i < rev[i]) swap(a[i], a[rev[i]]);
  }
  for (int k = 1; k < n; k <<= 1) {
    for (int i = 0; i < n; i += k * 2) {
      for (int j = 0; j < k; j++) {
        C z = rt[j + k] * a[i + j + k];
        a[i + j + k] = a[i + j] - z, a[i + j] += z;
      }
    }
  }
}

using Poly = vector<ll>;
template <int M> Poly convMod(const Poly &a, const Poly &b) {
  if (a.empty() || b.empty()) return {};
  Poly res(sz(a) + sz(b) - 1);
  int B = 32 - __builtin_clz(sz(res));
  int n = 1 << B, S = sqrt(M);
  vector<C> L(n), R(n), outs(n), outl(n);
  for (int i = 0; i < sz(a); i++) {
    L[i] = C(int(a[i] / S), int(a[i] % S));
  }
  for (int i = 0; i < sz(b); i++) {
    R[i] = C(int(b[i] / S), int(b[i] % S));
  }
  FFT(L), FFT(R);
  for (int i = 0; i < n; i++) {
    int j = (n - i) & (n - 1);
    outl[j] = (L[i] + conj(L[j])) * R[i] / (2.0 * n);
    outs[j] = (L[i] - conj(L[j])) * R[i] / (2.0 * n) / 1i;
  }
  FFT(outl), FFT(outs);
  for (int i = 0; i < sz(res); i++) {
    ll A = ll(imag(outs[i]) + 0.5) % M;
    ll B = (ll(imag(outl[i]) + 0.5) + ll(real(outs[i]) + 0.5)) % M * S % M;
    ll C = ll(real(outl[i]) + 0.5) % M * (S * S % M) % M;
    res[i] = (A + B + C) % M;
  }
  return res;
}

void solve() {
  const int mod = 1e9 + 7;

  int n; cin >> n;
  vector<ll> a(n + 1);
  for (int i = 1; i <= n; i++) cin >> a[i];

  vector<ll> fac(n * 3 + 1);
  for (int i = fac[0] = 1; i <= n * 3; i++) {
    fac[i] = fac[i - 1] * i % mod;
  }
  Poly P = convMod<mod>(convMod<mod>(a, a), a);
  ll ans = 0;
  for (int i = 3; i <= n * 3; i++) {
    ans = (ans + P[i] * fac[i] % mod) % mod;
  }
  cout << ans << '\n';
}
```

## B/C	小刘爱下井字棋

写个$hard-version$，使用$alpha-beta$剪枝优化后的$Minimax$搜索。

[学习这玩意时参考过的博客](https://orchidany.gitee.io/2019/12/28/%E5%AF%B9%E6%8A%97%E6%90%9C%E7%B4%A2/)

```cpp
using board = array<array<int, 3>, 3>;
board g; // tictactoe board

bool win(const int &p) {
  if (g[0][0] == g[0][1] && g[0][1] == g[0][2] && g[0][0] == p) return true;
  if (g[1][0] == g[1][1] && g[1][1] == g[1][2] && g[1][0] == p) return true;
  if (g[2][0] == g[2][1] && g[2][1] == g[2][2] && g[2][0] == p) return true;

  if (g[0][0] == g[1][0] && g[1][0] == g[2][0] && g[0][0] == p) return true;
  if (g[0][1] == g[1][1] && g[1][1] == g[2][1] && g[0][1] == p) return true;
  if (g[0][2] == g[1][2] && g[1][2] == g[2][2] && g[0][2] == p) return true;

  if (g[0][0] == g[1][1] && g[1][1] == g[2][2] && g[0][0] == p) return true;
  if (g[0][2] == g[1][1] && g[1][1] == g[2][0] && g[0][2] == p) return true;

  return false;
}
const int X = +1;
const int O = -1;

inline int doMin(int step, int alpha, int beta);
inline int doMax(int step, int alpha, int beta);

int doMax(int step, int alpha, int beta) {
  if (win(O)) return -1;
  if (win(X)) return +1;
  if (step == 9) return 0;
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      if (g[i][j] == 0) {
        g[i][j] = X;
        int now = doMin(step + 1, alpha, beta);
        g[i][j] = 0;

        if (now > alpha) alpha = now;
        if (alpha >= beta) return alpha;
      }
    }
  }
  return alpha;
}
int doMin(int step, int alpha, int beta) {
  if (win(O)) return -1;
  if (win(X)) return +1;
  if (step == 9) return 0;
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      if (g[i][j] == 0) {
        g[i][j] = O;
        int now = doMax(step + 1, alpha, beta);
        g[i][j] = 0;

        if (now < beta) beta = now;
        if (alpha >= beta) return beta;
      }
    }
  }
  return beta;
}
int battle(int step, int alpha, int beta) {
  // player = (step & 1 ? O : X);
  return (step & 1 ? doMin(step, alpha, beta) : doMax(step, alpha, beta));
}

void solve() {
  int n; cin >> n;
  for (int i = 0; i < 3; i++) {
    string s; cin >> s;
    for (int j = 0; j < 3; j++) {
      g[i][j] = s[j] == 'P' ? 0 : s[j] == 'X' ? X : O;
    }
  }
  cout << battle(n, -1, 1) << '\n';
}
```

## D	达哥想变强

+ Trie 模板题

[OI-wiki](https://oi-wiki.org/string/trie/#_5) 不会写的去点链接，顺带学点其它用法。

```cpp
using u32 = unsigned;
template <u32 BitLength> struct binary_trie {
  struct node {  // 4-ary trie
    u32 val;
    u32 hgt;
    array<node *, 4> child;
  };

  explicit binary_trie() { _root = new node{0, inner_len, {}}; };
  void insert(u32 x) {
    x ^= _xor_val;
    node *v = _root;
    node **parent;
    size_t topbits = x >> (v->hgt - 2) & 3;
    if (!v->child[topbits]) {
      v->child[topbits] = new node{x, 0, {}};
      return;
    }
    parent = &v->child[topbits];
    v = v->child[topbits];
    while (true) {
      if (static_cast<int>(v->hgt) > bsr(x ^ v->val)) {
        if (!v->hgt) return;
        topbits = x >> (v->hgt - 2) & 3;
        if (v->child[topbits]) {
          parent = &v->child[topbits];
          v = v->child[topbits];
        } else {
          v->child[topbits] = new node{x, 0, {}};
          return;
        }
      } else {
        node *split_node = new node{v->val, (bsr(v->val ^ x) | 1) + 1u, {}};
        (split_node->val >>= split_node->hgt) <<= split_node->hgt;
        *parent = split_node;
        split_node->child[v->val >> (split_node->hgt - 2) & 3] = v;
        split_node->child[x >> (split_node->hgt - 2) & 3] = new node{x, 0, {}};
        return;
      }
    }
  }
  u32 max() const {
    node *v = _root;
    size_t topbits;
    while (v->hgt != 0) {
      topbits = (_xor_val >> (v->hgt - 2) & 3) ^ 3;
      for (size_t ind = 0; ind < 4; ind++) {
        if (v->child[ind ^ topbits]) {
          v = v->child[ind ^ topbits];
          break;
        }
      }
    }
    return v->val ^ _xor_val;
  }

  void xor_all(u32 xor_val) noexcept { _xor_val ^= xor_val; }

 private:
  u32 inner_len = (BitLength + 1u) & ~1u;
  node *_root;
  u32 _xor_val = 0;
  static constexpr int bsr(u32 t) {
    return (t == 0 ? -1 : 63 - __builtin_clzll(t));
  }
};

void solve() {
  int n; cin >> n;
  vector<vector<pair<int, int>>> tree(n);
  for (int i = 1; i < n; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    --u, --v;
    tree[v].emplace_back(u, w);
    tree[u].emplace_back(v, w);
  }

  vector<int> S(n);
  const function<void(int, int)> dfs = [&](int u, int fa) {
    for (const auto &[v, w] : tree[u]) {
      if (v == fa) continue;
      S[v] = S[u] ^ w;
      dfs(v, u);
    }
  };
  dfs(0, 0);

  binary_trie<29> bt; bt.insert(0);

  u32 ans = 0;
  for (const int &x : S) {
    bt.xor_all(x), ans = max(ans, bt.max()), bt.xor_all(x);
    bt.insert(x);
  }

  cout << ans << '\n';
}
```

## E	最小值

$$
|a_i-b_j|+|b_j-c_k|+|c_k-a_i|=2\times\left(\max(a_i, b_j, c_k)-\min(a_i, b_j, c_k)\right)
$$

原时间限制下，二分次数过多会$TLE$。不过，可以观察到，二分的操作可以被指针优化掉。

这里提供的代码为本人验题用的代码，出题人的`std`代码用的是3个指针的写法。
```cpp
void solve() {
  int n; cin >> n;
  assert(1 <= n && n <= 1e6);
  vector<vector<int>> a(3, vector<int>(n));
  for (auto &&v : a) {
    for (auto &&x : v) cin >> x, assert(1 <= x && x <= 1e9);
    sort(all(v));
  }
  int ans = 2e9 + 10;
  vector<int> p = {0, 1, 2};
  do {
    int p1 = 0, p2 = 0;
    for (const auto &x : a[p[0]]) {
      if (x > a[p[2]].back()) break;
      if (x < a[p[1]].front()) continue;
      while (a[p[2]][p2] < x) p2++;
      while (p1 + 1 < n && a[p[1]][p1 + 1] <= x) p1++;
      ans = min(ans, 2 * (a[p[2]][p2] - a[p[1]][p1]));
    }
  } while (next_permutation(all(p)));
  cout << ans << '\n';
}
```

## F	function

二分结果。

```cpp
void solve() {
  ll n, m, k; cin >> n >> m >> k;
  k = n * m - k + 1;
  ll l = 1, r = n * m, ans = -1;
  while (l <= r) {
    ll mid = (l + r) >> 1;
    if ([&](ll x) -> bool {
      ll cnt = 0;
      for (int i = 1; i <= n; i++) cnt += min(m, x / i);
      return cnt >= k;
    }(mid)) r = mid - 1, ans = mid;
    else l = mid + 1;
  }
  cout << ans << '\n';
}
```

## G	train

最短路。

```cpp
const int N = 1e5;
vector<int> dis(N + 1, 1e9);

void init() {
  priority_queue<pair<int, int>> pq;
  pq.emplace(dis[0] = 0, 0);
  while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();
    if (-d > dis[u]) continue;
    for (int i = 1; i * 1LL * i + u <= N; i++) {
      const int v = u + i * i;
      if (dis[v] > dis[u] + 1) {
        dis[v] = dis[u] + 1;
        pq.emplace(-dis[v], v);
      }
    }
    for (int i = 1; u - i * 1LL * i >= 1; i++) {
      const int v = u - i * i;
      if (dis[v] > dis[u] + 1) {
        dis[v] = dis[u] + 1;
        pq.emplace(-dis[v], v);
      }
    }
  }
}

void solve() {
  int c; cin >> c;
  assert(1 <= c && c <= 1e5);
  cout << dis[c] << '\n';
}
```

## H	爱背单词的队长

KMP + 前缀和优化

这题没什么好讲的，唯一需要注意的点是，**查询的区间必须完全包含单词**。

```cpp
vector<int> KMP(const string &s, const string &pat) {
  string t = pat + '\0' + s;
#define sz(x) static_cast<int>((x).size())
  vector<int> lps(sz(t), 0);
  for (int i = 1; i < sz(t); i++) {
    int g = lps[i - 1];
    while (g && t[i] != t[g]) g = lps[g - 1];
    lps[i] = g + (t[i] == t[g]);
  }
  vector<int> match;
  for (int i = sz(t) - sz(s); i < sz(t); i++) {
    if (lps[i] == sz(pat)) {
      match.push_back(i - 2 * sz(pat));
    }
  }
#undef sz
  return match;
}

void solve() {
  int n, m, q; cin >> n >> m >> q;
  string s; cin >> s;
  vector<pair<int, vector<int>>> cnt(m);
  for (auto &&[len, v] : cnt) {
    string t; cin >> t;
    len = t.length(), v.resize(n + 1, 0);
    auto match = KMP(s, t);
    for (const int &pos : match) v[pos + 1] += 1;
    partial_sum(all(v), begin(v));
  }
  for (int l, r; q--;) {
    cin >> l >> r;
    ll ans = 0;
    for (const auto &[len, v] : cnt) {
      if (r - len + 1 >= l) ans += v[r - len + 1] - v[l - 1];
    }
    cout << ans << '\n';
  }
}
```

## I	多项式

DFS/二进制枚举

我的写法其实有SoSDP那味，，，怕你们看不懂特意加了注释（**不会SoSDP的也该去学学了，这玩意放现在的比赛都只能当签到了！**）。

```cpp
void solve() {
  int n; cin >> n;

  vector<ll> r(1 << n); // r[01101110] -> 表示集合内元素的乘积
  for (int i = 0; i < n; i++) cin >> r[1 << i];

  r[0] = 1; // 特殊处理空集
  vector<ll> F(n + 1);
  for (int mask = 0; mask < (1 << n); mask++) {
    r[mask] = r[mask ^ (mask & -mask)] * r[mask & -mask];
    // 如果 mask           = 01101110
    // 那么 (mask & -mask) = 00000010
    // (mask & -mask) 在树状数组中也出现过，又称 lowbit
    // 在这里用的是因为 (mask - lowbit) & lowbit == mask
    F[__builtin_popcount(mask)] += r[mask];
  }
  for (int i = 1; i <= n; i++) {
    cout << F[i] << " \n"[i == n];
  }
}
```

## J	非降数组

裸一个DP，`dp[i][j]`表示，前面`i`个数满足`c[i] = j`的合法方案。

$$
dp[i][j] = \sum_{k=1}^{j}dp[i-1][k]
$$

不能直接暴力$j,k$，但是可以通过前缀和优化掉一层枚举。对于被卡内存的同学，这里表示十分抱歉，设置`256MB`确实不合理。

```cpp
void solve() {
  const int mod = 1e9 + 7, N = 1005;

  int n; cin >> n;
  vector<int> a(n), b(n);
  for (int &x : a) cin >> x;
  for (int &x : b) cin >> x;

  vector<ll> dp(N);
  fill(next(begin(dp), a[0]), next(begin(dp), b[0] + 1), 1);
  for (int i = 1; i < n; i++) {
    vector<ll> ndp(N);
    partial_sum(all(dp), begin(dp));
    for (int c = a[i]; c <= b[i]; c++) ndp[c] = dp[c] % mod;
    dp = move(ndp);
  }
  cout << accumulate(all(dp), 0LL) % mod << '\n';
}
```

## L	反转

括号序列必须满足两个点（如果视`(`为`+1`，同时`)`为`-1`）

+ 所有前缀和非负
+ 整体上，总和为0

板子太长了，所以拿数组重写了。
```cpp
const int N = 2e5 + 10;
char str[N];
int n, q, sum[N];

#define ld nd << 1 | 0
#define rd nd << 1 | 1
int laz[N << 2], mi[N << 2];
void merge(int nd) { mi[nd] = min(mi[rd], mi[ld]); }
void build(int s, int t, int nd) {
  if (s == t) return mi[nd] = sum[s], void();
  int m = (s + t) >> 1;
  build(s, m, ld), build(m + 1, t, rd), merge(nd);
}
void pushlz(int nd, int v) { mi[nd] += v, laz[nd] += v; }
void downlz(int nd) {
  if (laz[nd] == 0) return;
  pushlz(ld, laz[nd]), pushlz(rd, laz[nd]), laz[nd] = 0;
}
void update(int s, int t, int nd, int l, int r, int v) {
  if (l <= s && t <= r) return pushlz(nd, v);
  downlz(nd);
  int m = (s + t) >> 1;
  if (l <= m) update(s, m, ld, l, r, v);
  if (r > m) update(m + 1, t, rd, l, r, v);
  merge(nd);
}
void solve() {
  cin >> n >> q >> (str + 1);
  for (int i = 1; i <= n; i++) {
    sum[i] = sum[i - 1] + (str[i] == '(' ? 1 : -1);
  }
  build(1, n, 1);
  for (int p; q--;) {
    cin >> p;
    if (str[p] == '(') {
      update(1, n, 1, p, n, -2);
      sum[n] -= 2;
    } else {
      update(1, n, 1, p, n, +2);
      sum[n] += 2;
    }
    str[p] ^= '(' ^ ')';
    cout << ((sum[n] == 0 && mi[1] == 0) ? "YES" : "NO") << '\n';
  }
}
```