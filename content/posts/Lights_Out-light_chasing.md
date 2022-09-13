---
title: "关灯问题(Lights Out) - Light chasing"
date: 2022-08-29T17:32:04+08:00
draft: false
slug: a8d49aaf

author: "Kenshin2438"
description: "关于(n * n)的Lights Out问题，使用光追逐(Light chasing)在O(n^3)时间复杂度下解决。"
summary: ""
categories: 
  - Data Structure
tags: 
  - Lights Out(Light chasing)
  - Linear Basis

weight: false
math: true
comments: true

cover:
  image: "/images/lights_out.png" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

有一个$n \times n$的方阵，每个位置上都有一盏灯。每次可以选择一个格子，选定后**它与它相邻**(有公共边)的格子的亮暗状态都会发生改变。现给定初始方阵中每盏灯的亮暗情况，请输出一个**使所有灯都熄灭的方案**。

<!--more-->

+ 该问题在wikipedia上的词条 [Lights Out(game)](https://en.wikipedia.org/wiki/Lights_Out_(game))，尚未有中文页。
+ 如有读者想验证自己的程序，可在LibreOJ提交，[LibreOJ #6243. 关灯问题](https://loj.ac/p/6243) 。

---

## 初探

如果你有线性代数的相关知识储备，相信你此时已经意识到，该问题可以做如下的转换：

**有$n^2$个开关，一共控制了$n^2$盏灯。同时，我们也已知每个开关所控制的灯集合。所以，只要将方程（一共$n^2$个，变量为每个开关的状态）列出，解决这个线性方程组便解决了这道题。**

至于代码实现，不过是一个Gaussian elimination，写成记录异或路径的线性基也可，这个应该不是问题。~~甚至，对于某些原题自动机，可能已经找到了原题。~~

问题到这似乎已经解决，**但是时间复杂度呢？** 无论选择以上哪种实现，时间复杂度都在妥妥的$\mathcal{O}(\frac{n^6}{\omega})$。

$n$很小时，或许能够在$1s$内解决。例如这题，[gym102920 J](https://codeforces.com/gym/102920/problem/J)。

## 一个或许可行的方案

怎么办呢？无脑冲高斯消元似乎是不可能的了，那么，可以优化吗？于是，你开始注意到，这个系数矩阵似乎有点意思啊！（以$n=5$为例）

$$
\left(
\begin{matrix}
  C & I & O & O & O \newline
  I & C & I & O & O \newline
  O & I & C & I & O \newline
  O & O & I & C & I \newline
  O & O & O & I & C \newline
\end{matrix}
\right)
$$

其中，$O$为零矩阵，$I$为单位矩阵，且均为$n \times n$的方阵。而矩阵$C$的为：

$$
C = \left(
\begin{matrix}
  1 & 1 & 0 & 0 & 0 \newline
  1 & 1 & 1 & 0 & 0 \newline
  0 & 1 & 1 & 1 & 0 \newline
  0 & 0 & 1 & 1 & 1 \newline
  0 & 0 & 0 & 1 & 1 \newline
\end{matrix}
\right)
$$

通过优化消元的过程，应该是能够做到在$\mathcal{O}(n^3)$时间复杂度下解决该问题。（每一位上的`1`，所在位置是很有规律的）

但是，笔者不才，并未有深入下去探索。

## Light chasing（光追逐）

### Q: 什么是 "光追逐" 呢？

{{< admonition quote "Light chasing - wikipedia" false >}}
"Light chasing" is a method similar to Gaussian elimination which always solves the puzzle (if a solution exists), although with the possibility of many redundant steps. In this approach, rows are manipulated one at a time starting with the top row. All the lights are disabled in the row by toggling the adjacent lights in the row directly below. The same method is then used on the consecutive rows up to the last one. The last row is solved separately, depending on its active lights. Corresponding lights (see table below) in the top row are toggled and the initial algorithm is run again, resulting in a solution.
{{< /admonition >}}

上面的是Wikipedia中的介绍（未翻译）。

简单来说就是：确定好一行的状态之后，便不会再次对此行做任何修改。于是，第一行的开关状态一旦确定，为了使得剩下行的灯熄灭（同时不会再次点亮之前行的灯），我们**不得不**做出固定的操作！最后，只要验证最后一行是否均熄灭即可（**此行没有下一行来帮助熄灭灯**）。

~~太好了，问题的规模一下子从$O(n^6)$变成了$O(2^n)$，只要枚举第一行的操作集合就能完成啦！~~ 对于POJ上的某题，这样写枚举肯定是可行的，但是本题的$n$有$1000$呐！

### Q: 如何进行 "光追逐"

1. 首先，我们已知第一行的操作集合，直接施行即可。
2. 到了某一行，比如第$i$行。
   + 我们需要处理的**其实不是当前行的状态，而是上一行**。
   + 根据上一行的**灯状态**，和开关的**操作状态**。上一行($i-1$行)依旧亮着的灯，在本行($i$行)对应位置的开关需要操作，以使其处在关闭状态。
   + 根据操作，得到本行的灯状态（留到下一行处理，**且只能够留到下一行处理，因为此时再操作第$i$行必然导致$i-1$行中的灯亮起。**）。
3. 然后不断递归操作，直到到最后一行。

时间复杂度：$\mathcal{O}(\frac{n^2}{\omega})$

### 优化 "枚举" 第一行的状态的方式

下面给出的是笔者代码的逻辑，或许不是最"正宗的"光追逐的写法。

首先，我们可以轻松解决这样一些问题：

+ 当第一行不操作时，使用光追逐，最后一行会是怎样？
+ 初始灯全灭，此时操作第一行的状态为**只有第$k$个开关打开**。使用光追逐，最后一行会是怎样？
+ 对于第一行的各个灯，如果按照上一问的操作方式，每个开关的开启事件是否正交？（或者应该叫线性无关？）

所以，问题到此已经解决啦！

时间复杂度：$\mathcal{O}(\frac{n^3}{\omega})$

## 代码

应该算是完全依照上述思路编写。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
#define all(a) begin(a), end(a)
#define sz(x) (int)((x).size())

#ifdef LOCAL
#include "debug.hpp"
#else
#define debug(...) 42
#endif

const int N = 1024;
bitset<N> g[N], ans[N], final;

template <size_t N> struct Basis {
  vector<bitset<N>> B, path;
  int sz = 0;

  Basis(int n) : B(n), path(n) {};

  void insert(bitset<N> v, int id) {
    bitset<N> cur; cur.set(id);
    for (int i = B.size() - 1; i >= 0; i--) {
      if (v.test(i) == false) continue;
      if (B[i].test(i)) {
        v ^= B[i], cur ^= path[i];
      } else {
        for (int j = i - 1; j >= 0; j--)
          if (v.test(j)) v ^= B[j], cur ^= path[j];
        for (int j = i + 1; j < (int) B.size(); j++)
          if (B[j].test(i)) B[j] ^= v, path[j] ^= cur;
        B[i] = v, path[i] = cur, sz += 1;
        return;
      }
    }
  }
  int size() { return sz; }
  pair<bool, bitset<N>> solver(bitset<N> x) {
    bitset<N> res;
    for (int i = B.size() - 1; i >= 0; i--) {
      if (x.test(i)) {
        if (B[i].test(i)) {
          x ^= B[i];
          res ^= path[i];
        } else {
          return {false, res};
        }
      }
    }
    return {true, res};
  }
};

void solve() {
  int n; cin >> n;
  for (int i = 1; i <= n; i++) {
    string s; cin >> s;
    for (int j = 0; j < n; j++) {
      if (s[j] == '#') g[i].set(j);
    }
  }

  { // Light chasing
    bitset<N> light = g[1], ops;

    for (int i = 2; i <= n; i++) {
      auto cur_ops   = light;
      auto cur_light = (cur_ops << 1) ^ cur_ops ^ (cur_ops >> 1) ^ ops ^ g[i];
      cur_light.reset(n);

      ops   = move(cur_ops);
      light = move(cur_light);
    }

    final = move(light);
  }

  static const auto getVec = [n](int id) {
    bitset<N> light, ops;
    ops.set(id);
    light = (ops << 1) ^ ops ^ (ops >> 1);
    light.reset(n);

    for (int i = 2; i <= n; i++) {
      auto cur_ops   = light;
      auto cur_light = (cur_ops << 1) ^ cur_ops ^ (cur_ops >> 1) ^ ops;
      cur_light.reset(n);

      ops   = move(cur_ops);
      light = move(cur_light);
    }
    
    return light;
  };

  Basis<N> B(n);
  for (int i = 0; i < n; i++) {
    auto x = getVec(i);
    B.insert(x, i);
  }

  bool ok = false;
  tie(ok, ans[1]) = B.solver(final);
  if (ok == false) return cout << "No solution\n", void();

  for (int i = 1; i < n; i++) {
    ans[i + 1] = (ans[i] << 1) ^ ans[i] ^ (ans[i] >> 1) ^ ans[i - 1] ^ g[i];
    ans[i + 1].reset(n);
  }

  for (int i = 1; i <= n; i++) {
    for (int j = 0; j < n; j++) {
      cout << (ans[i].test(j) ? '#' : '.');
    }
    cout << '\n';
  }
}

int main() {
  cin.tie(nullptr)->sync_with_stdio(false);

  int T = 1;
  // cin >> T;
  while (T--) solve();

  return 0;
}
```