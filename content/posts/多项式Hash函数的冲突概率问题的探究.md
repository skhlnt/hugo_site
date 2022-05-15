---
title: "多项式Hash函数冲突概率的探究"
date: 2022-03-22T00:45:24+08:00
draft: true
slug: 6751dc4c

author: "Kenshin2438"
description: "最近做题碰到了Hash，学习时对Hash冲突的概率产生了一点兴趣。"
categories: 
  - 多项式
  - 数论
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

注意到，我们的 Hash 函数中的$\mathrm{base},M$均为自定义的值，显然影响冲突概率的正好是这两数。如果固定模数$M$来讨论这个问题，则只要看$\mathrm{base}\in[1,M)$有多少为该同余式的解。

## $M$ 为素数

### $\textrm{Lagrange}$定理

$$
f(x)=\sum_{i=0}^{n}a_i\times x^i \equiv 0 \pmod{M}
$$

满足$n>0,a_n \not\equiv 0 \pmod{M},M\in \mathrm{Prime}$，则上同余式最多$n$个解。

**证明：**

1. 当$n=1$时，一次同余式$a_1x+a_0\equiv 0\pmod{M},a_1\nmid M$显然恰好一个解。
2. 假设定理对于$n-1\geq 1$同余式成立，下面证定理对$n$次同余式也成立。


## $M$ 为合数

### CRT/孙子剩余定理
