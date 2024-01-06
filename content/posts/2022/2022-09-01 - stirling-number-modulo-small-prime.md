---
title: "斯特林数取模小素数 - Congruence for Stirling Number"
date: 2022-09-01T08:53:21+08:00
draft: false
slug: 16b0c7ac

author: "Kenshin2438"
description: "斯特林数取模小素数，在和它相关的为数不多的论文中，有人将其称为Stirling数的Lucas同余。"
keywords:
  - 斯特林数
  - Stirling数
  - 斯特林数取模
  - 斯特林数取模小素数
  - 斯特林数同余
  - Lucas同余
summary: ""
categories: 
  - Number Theory
tags: 
  - Stirling Number
  - Lucas Congruence

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

笔者在此并不想涉及过多的组合内容，其一，诸如此类的介绍文章在zhihu和csdn已经大量存在；其二，笔者并无自信将斯特林数的知识点吃透，也不觉得自己能够在这种理解程度下，提供什么特别的内容。

但是，本人在Google检索的过程中却鲜少见**Stirling数取模小素数**的内容，所以在基本明白之后，在此记录。

+ 关于Stirling数的组合性质，推荐繁凡的[《小学生都能看懂的三类斯特林数从入门到升天教程 》（含性质完整证明、斯特林反演、拉赫数）](https://zhuanlan.zhihu.com/p/350774728)
+ 关于斯特林数取模，只检索到 [《第一类Stirling数的Lucas定理》](https://www.bilibili.com/read/cv7038105/) （不知道为啥是B站，好迷，公式排版不太能看懂）

## 定义 以及 前置知识

将 $n$ 个元素分成 $k$ 组，每组内部进行环排列，这样的方案数称为**无符号第一类斯特林数**，记作 $c(n, k)$。

可以发现，$c(n, k)$ 存在如下的递推关系：

$$c(n, k) = (n − 1)c(n − 1, k) + c(n − 1, k − 1)$$

定义**有符号第一类斯特林数** $s(n, k) = (−1)^{n−k}c(n, k)$，则有

$$(x)_ {n} = x(x − 1) \dots(x − n + 1) = \sum_{k=0}^{n} s(n,k) x^k$$

---

将 $n$ 个元素分成 $k$ 个非空集合，集合之间不计顺序，这样的方案数称为**第二类斯特林数**，记作 $S(n, k)$。

可以发现，$S(n, k)$ 存在如下的递推关系：

$$S(n, k) = S(n − 1, k − 1) + kS(n − 1, k)$$

我们有

$$\sum_{k=0}^{n} S(n, k)(x)_k = x^n$$

> 以上内容来自ppt **如何优雅的数数 - 11Dimensions**，未找到原始出处。

---

+ 本人的笔记 [组合数取模 - Lucas/exLucas](https://kenshin2438.top/archives/e874bcb3.html/)

接下来的推导与对与Lucas定理推导有共通之处，建议先阅读。

同时，在此补充几个容易混淆的知识点。主要摘自潘承洞先生的《数论基础》以及下方贴出的链接。

0. 关于符号 $\equiv$

该符号使用Markdown语法写出，格式为`\equiv`。实际来源于 `equivalent` ，中文翻译 `等价` 。虽然我们一般在同余理论中使用到它，但是，`同余` 的单词其实为 `congruent` 。

**为什么要提及这一区别？** 因为在多项式同余理论(`polynomial congruence`)中，`equivalent` 和 `congruent` 实际代表着完全不同的含义。当然，国内的各种教材对此的确会做提醒（但在名词翻译问题上着实混乱），但是对于算法竞赛的圈子——并不是所有人都会从理论学起——很可能根本不会有人在意这一点。

1. $F_p$上多项式的等价。`equivalent`

设 $p$ 为素数, $f(x), g(x)$ 为整数多项式, 若多项式 $f(x),g(x)$ 对所有的 $t \in Z/(p)$都有 $f(t) \equiv g(t) \pmod{p}$，则称 $f(x)$ 对模 $p$ 等价于 $g(x)$。记作

$$f \equiv g \pmod{p}$$

2. 多项式的（恒等）同余。 `congruent`

设 $p$ 为素数, $f(x), g(x)$ 为整数多项式, 若多项式 $f(x) − g(x)$ 的**所有系数**均被 $p$ 整除, 则称 $f(x)$ 对模 $p$ 恒等同余于 $g(x)$, 记作（本人使用的电子版存在格式错误，下面的符号参考外文论文）

$$f \sim g \pmod{p}$$

**要注意的是, 对所有 $x$ 均有 $f(x) \equiv g(x) \pmod{p}$, 并不一定能推出$f \sim g \pmod{p}$。**

例如，$x^p \equiv x \pmod{p}$ 但是 **并不满足** $x^p \sim x \pmod{p}$。

3. `Lagrange’s theorem` 的一个拓展。

如果 $f$ 和 $g$ 满足 $\deg(f),\deg(g)\leq p-1$ 且 $f \equiv g$, 则可以得到 $f \sim g$。

证明参阅：[LECTURE 6: POLYNOMIAL CONGRUENCES MODULO PRIMES](https://www.math.uzh.ch/gorodnik/nt/lecture6.pdf)。

---

下面若无特殊说明，都默认$p$为素数，且在有限域$\mathrm{GF}(p)$。

## 第一类Stirling数 $s(n,k) \bmod p$

令有$n=p\times n_1 + n_0, (0\leq n_0 < p)$。

同Lucas定理的证明一致，我们先考虑其生成函数（大概算是？）下降幂 $(x)_n \bmod p$。

$$(x)_ p=\prod_{k=0}^{p-1}(x-k) \sim x^p-x \pmod{p}$$ 

在$\mathrm{GF}(p)$，由费马小定理，这是显然的（我们有恒等式$X^p-X=\prod_{a\in\mathrm{GF(p)}}(X-a)$）。

所以，显然有推论：

$$(x)_ n \sim (x^p-x)^{n_1}(x)_{n_0} \pmod{p}$$

又由于，我们已知$s(n,k)=[x^k]\left(x\right)_n$，可以得到：

$$
\begin{aligned}
s(n,k)
& \equiv [x^k]\left(x^p-x\right)^{n_1}(x)_ {n_0} \newline
& \equiv [x^{k-n_1}]\left(x^{p-1}-1\right)^{n_1}(x)_ {n_0} \newline
& \equiv [x^{k-n_1}]\sum_{i=0}^{n_1}{n_1 \choose i}x^{(p-1)i}(-1)^{n_1-i}\sum_{j=0}^{n_0}s(n_0,j)x^j \newline
& \equiv [x^{k-n_1}]\sum_{i=0}^{n_1}\sum_{j=0}^{n_0}{n_1 \choose i}(-1)^{n_1-i}s(n_0,j)x^{(p-1)i+j}
\end{aligned}
$$

现在的目标转向解决不定方程，

$$
k-n_1=(p-1)\times i+j,(0 \leq i \leq n_1, 0 \leq j \leq n_0 \leq p-1)
$$

+ 当$n_0=p-1,(p-1)\mid (k-n_1)$时，显然$j$有两种取值$0,p-1$，但$s(n_0,0)=0(n_0>0)$可以忽略。
+ 其它情况下，该不定方程有唯一解。

综上，$s(n,k) \equiv {n_1 \choose i}(-1)^{n_1-i}s(n_0,j)$，其中数对$(i,j)$唯一。

## 第二类Stirling数 $S(n,k) \bmod p$

我们已知，对于第二类斯特林数有如下的关系：

$$\sum_{t=0}^{n} S(n, t)(x)_ t = x^n$$

对于等式的左边进行展开：

$$
\begin{aligned}
\sum_{t=0}^{n}S(n,t)(x)_ t
& \equiv \sum_{t_1=0}^{\infty}\sum_{t_0=0}^{p-1}S(n,t_1\times p + t_0)(x^p-x)^{t_1}(x)_ {t_0} \newline
& \equiv \sum_{t_1=0}^{\infty}\left(x^p-x\right)^{t_1}\left(\sum_{t_0=0}^{p-1}S(n,t_1\times p + t_0)(x)_ {t_0} \right)\newline
\end{aligned}
$$

显然，$\sum_{t_0=0}^{p-1}S(n,t_1\times p+t_0)(x)_ {t_0}$ 为一个低于 $p$ 次的多项式。同之前一样，我们需要找到对应的系数（为了满足同余关系，我们只能使用满足$\sim$的代换，**禁用$x^p \equiv x$**）。

对于待求的 $S(n,k)$，令 $k=p\times k_1+k_0,(0\leq k_0 \leq p-1)$，则需要知道 $(x^p-x)^{k_1} (x)_ {k_0}$ 的系数（显然这样的展开是唯一的，类似于分解）。

我们这次寻找 $x^n$ 对 $(x^p - x)$ 的展开式，容易想到 $x^p=(x^p-x)+x$。

+ 尝试 $n=p\times n_1+n_0,(0\leq n_0\leq p-1)$

容易得到：$x^n=\sum_{t=0}^{\infty}(x^p-x)^t{n_1\choose t}x^{n_1-t+n_0}$。由于$n_1+n_0-t$极有可能超过$p$，后项的$x^{n_1+n_0-t}$显然能够通过同样的方式继续分解，无法保证算法的时间复杂度。

+ 尝试 $n-k_1=(p-1)\times i+j,(0< j\leq p-1)$

可得到：

$$
x^n=\sum_{t=0}^{\infty}(x^p-x)^t{i \choose t}x^{k_1+j-t}
$$

1. 当$t \geq k_1 + 1$，无需考虑。
2. 当$t = k_1$，易知${i \choose k_1}x^{j}$符合不超过$p-1$次多项式的要求。

   $${i \choose k_1}x^{j}={i \choose k_1}\sum_{t_0=0}^{j}S(j,t_0)(x)_{t_0}$$
3. 当$t \leq k_1 - 1$，对应项为$(x^p-x)^t\times x^{k_1+j-t}$，配凑后变为
   
   $$(x^p-x)^t[(x^p-x)+x]^{k_1-t}\times x^{j-(p-1)\times(k_1-t)}$$
   此处含$(x^p-x)^{k_1}$的项为$(x^p-x)^{k_1}x^{j-(p-1)\times(k_1-t)}$，而$k_1-t\geq 1,j\leq p-1$，仅当$t=k_1-1,j=p-1$，存在一个常系数多项式${i \choose k_1-1}$符合。

## 代码

```cpp
struct StirlingNumber {
  const int P; // P is a small prime
  vector<vector<int>> C, S1, S2;

  StirlingNumber(int _P = 2) : P(_P) {
    C.resize(P, vector<int>(P, 0)), S1 = S2 = C;
    for (int i = 0; i < P; i++) {
      C[i][0] = 1, C[i][i] = 1;
      for (int j = 1; j < i; j++) {
        C[i][j] = (C[i - 1][j] + C[i - 1][j - 1]) % P;
      }
    }
    for (int i = 0; i < P; i++) {
      S2[i][0] = 0, S2[i][i] = 1;
      for (int j = 1; j < i; j++) {
        S2[i][j] = (S2[i - 1][j] * j + S2[i - 1][j - 1]) % P;
      }
    }
    for (int i = 0; i < P; i++) { // signed
      S1[i][0] = 0, S1[i][i] = 1;
      for (int j = 1; j < i; j++) {
        S1[i][j] = (S1[i - 1][j] * (P - i + 1) + S1[i - 1][j - 1]) % P;
      }
    }
  }

  int getC(ll n, ll k) const {
    if (k < 0 || k > n) return 0;
    int res = 1;
    for (; n; n /= P, k /= P) {
      res = res * C[n % P][k % P] % P;
    }
    return res;
  }
  int getS1(ll n, ll k) const {
    if (k < 0 || k > n) return 0;
    if (n == 0) return 1;
    ll n1 = n / P, n0 = n % P;
    if (k < n1) return 0;
    ll i = (k - n1) / (P - 1), j = (k - n1) % (P - 1);
    if (j == 0 && n0 == P - 1) j = P - 1, i -= 1;
    if (i < 0 || i > n1 || j > n0) return 0;
    int res = S1[n0][j] * getC(n1, i) % P;
    if ((n1 ^ i) & 1) res = (P - res) % P;
    return res;
  }
  int getS2(ll n, ll k) const {
    if (k < 0 || k > n) return 0;
    if (n == 0) return 1;
    ll k1 = k / P, k0 = k % P;
    if (n < k1) return 0;
    ll i = (n - k1) / (P - 1), j = (n - k1) % (P - 1);
    if (j == 0) j = P - 1, i -= 1;
    if (j == P - 1 && k0 == 0) return getC(i, k1 - 1);
    else return getC(i, k1) * S2[j][k0] % P;
  }
};
```

## 参考

+ [LECTURE 6: POLYNOMIAL CONGRUENCES MODULO PRIMES](https://www.math.uzh.ch/gorodnik/nt/lecture6.pdf)
+ [maspyのHP - Stirling 数を p で割った余りの計算](https://maspypy.com/stirling-%e6%95%b0%e3%82%92-p-%e3%81%a7%e5%89%b2%e3%81%a3%e3%81%9f%e4%bd%99%e3%82%8a%e3%81%ae%e8%a8%88%e7%ae%97)
+ [CONGRUENCE PROBLEMS INVOLVING STIRLING NUMBERS OF THE FIRST KIND](https://www.fq.math.ca/Scanned/31-1/peele.pdf)
+ [The Lucas congruence for Stirling numbers of the second kind](http://matwbn.icm.edu.pl/ksiazki/aa/aa94/aa9413.pdf)