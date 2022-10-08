---
title: "Bell数的Touchard同余 - Touchard's Congruence"
date: 2022-09-12T18:42:02+08:00
draft: true
slug: af868eb0

author: "Kenshin2438"
description: "Bell数的Touchard同余，使用上一篇文中介绍的Stirling数的模小素数的结论来证明。"
keywords: 
  - Bell数
  - Touchard同余
summary: ""
categories: 
  - Number Theory
tags: 
  - Bell number
  - Touchard's Congruence

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

贝尔数 $B_n$ 的含义是**基数为 $n$ 的集合划分成非空集合的划分数**。它满足Touchard同余，对于素数$p$有：

$$
\begin{aligned}
B_{n+p}   & \equiv B_{n+1}+B_{n}\pmod{p} \newline
B_{n+p^m} & \equiv B_{n+1}+mB_{n}\pmod{p} \newline
\end{aligned}
$$

<!--more-->

## 证明思路

联想到第二类斯特林数的定义，我们可知：

$$
B_n = \sum_{k=0}^{n}S(n,k)
$$

不同于其它通过构建**Bell多项式**(`Bell polynomial`)的证明方法，此处，我们将关注点转向另一个式子：

$$
S(n+p,k) \equiv S(n+1,k)+S(n,k-p) \pmod{p}
$$

显然，若该式子成立，则必然能够推导出$B_{n+p}\equiv B_{n+1}+B_{n}\pmod{p}$。

---

令$n=p\times n_1+n_0,k=p\times k_1+k_0,(0\leq n_0,k_0 \leq p-1)$。

利用之前的结论 [斯特林数取模小素数 - Congruence for Stirling Number](https://kenshin2438.top/archives/16b0c7ac.html/)，后续最大的工作量或许是分类讨论。

~~或许可行，但是听我说，今天只能写到这了~~

## 参考

+ [AN ELEMENTARY (NUMBER THEORY) PROOF OF TOUCHARD’S CONGRUENCE](https://arxiv.org/pdf/0906.0696.pdf)
+ [Some congruences concerning the Bell numbers](https://www.emis.de/journals/BBMS/Bulletin/bul964/Robert-Gertsch.pdf)
+ [The Arithmetic of Bell and Stirling Numbers - H. W. Becker and John Riordan](https://www.jstor.org/stable/2372336)