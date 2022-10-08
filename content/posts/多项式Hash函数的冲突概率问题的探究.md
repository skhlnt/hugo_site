---
title: "多项式Hash函数冲突概率的探究"
date: 2022-03-22T00:45:24+08:00
draft: false
slug: 6751dc4c

author: "Kenshin2438"
description: "最近做题碰到了Hash，学习时对Hash冲突的概率产生了一点兴趣。"
keywords:
  - Rolling Hash
  - 滚动hash
  - hash冲突
categories: 
  - Number Theory
tags: 
  - Hash
  - CRT

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

# Hash 简介

Hash 的思想很简单，通过某种映射将一个序列或者字符串对应到一个值域较小的值，自然，我们只希望这种映射关系是**单射**的。

常用的 Hash 函数是一个模意义下的整系数多项式（同余式），例如，对于字符串$S$，定义Hash函数：

$$
h(S)=\left(\sum_{i=1}^{|S|}\mathrm{base}^{|S| - i} \times S_i \right) \bmod M
$$

那么，何为 Hash 冲突呢？对于另一个**等长**的串$T$，满足$T \neq S, h(T)=h(T)$，即：

$$
h(T)-h(S) = \left(\sum_{i=1}^{n}\mathrm{base}^{n - i} \times (T_i - S_i) \right) \equiv 0 \pmod{M}
$$

---

注意到，我们的 Hash 函数中的$\mathrm{base},M$均为自定义的值，显然影响冲突概率的正好是这两数。如果**固定模数**$M$，**随机基数**$\mathrm{base}$来讨论这个问题，则只要看$\mathrm{base}\in[1,M)$有多少为该同余式的解。

## $M$ 为素数

### $\textrm{Lagrange}$定理

$$
f(x)=\sum_{i=0}^{n}a_i\times x^i \equiv 0 \pmod{M}
$$

满足$n>0,a_n \not\equiv 0 \pmod{M},M\in \mathrm{Prime}$，则上同余式最多$n$个解。

**证明：**

1. 当$n=1$时，一次同余式$a_1x+a_0\equiv 0\pmod{M}$，由于$M\nmid a_1$，显然恰好一个解。
2. 当$n\geq M$结论显然成立。
3. 当$2 \leq n \leq M - 1$时，我们进行**反证**。假设上式有多余$n$个解（不妨令为$x_0,x_1,\dots,x_k,(k \geq n+1)$，并且$\forall i\neq j, x_i \not\equiv x_j\pmod{M}$）

由于：
$$
f(x)-f(x_0)\equiv\sum_{i=0}^{k}a_i(x^i-x_0^i)=(x-x_0)g(x)\pmod{M}
$$
容易知道，此时的$g(x)$为一个$n-1$次多项式，且$[x^{n-1}]g(x)=a_n\not\equiv 0\pmod{M}$。

于是，由于$f(x_i)\equiv f(x_j)\pmod{M}$，我们可以知道：
$$
(x_i-x_0)g(x_i)\equiv 0\pmod{M}
$$
则$g(x)\equiv 0\pmod{M}$有超过$k-1\geq n$个解。由此归纳可知：一次同余式$a_nx+a_0\equiv 0\pmod{M}$应有超过$2$个解（这与上面的**结论矛盾**）。

## $M$ 为合数

[孙子剩余定理 - CRT/exCRT](https://kenshin2438.top/archives/72b0c59.html/)

