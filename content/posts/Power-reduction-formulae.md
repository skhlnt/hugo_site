---
title: "三角函数降幂公式 - Power-reduction formulae"
date: 2021-08-01 14:29:35
slug: ce81e1da

author: "Kenshin2438"
description: ""
categories:
  - Math
tags:
  - Power-reduction formulae

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

先给出全部公式：

$$\begin{aligned}
& \sin^{2n}{x}=\frac{1}{2^{2n-1}}\left[ \sum_{k=0}^{n-1}{2n \choose k}(-1)^{n-k}\cos{2(n-k)x} + \frac{1}{2}{2n \choose n} \right] \\\\ 
& \sin^{2n+1}{x}=\frac{1}{2^{2n}}\sum_{k=0}^{n}{2n+1 \choose k}(-1)^{n-k}\sin{(2n-2k+1)x}  \\\\ 
& \cos^{2n}{x}=\frac{1}{2^{2n-1}}\left[ \sum_{k=0}^{n-1}{2n \choose k}\cos{2(n-k)x}+\frac{1}{2}{2n \choose n} \right] \\\\
& \cos^{2n+1}{x}=\frac{1}{2^{2n}}\sum_{k=0}^{n}{2n+1 \choose k}\cos{(2n-2k+1)x} \\\\
\end{aligned}$$

<!--more-->

虽然看起来原本简单的式子被极大地复杂化了，但其实在很多命题中，它们起着十分不错的化简作用。

---

$\mathrm{Proof:}$ 

由欧拉恒等式$e^{ix}=\cos{x}+i\sin{x}$有

$$\begin{cases} 
\sin x &=& \frac{e^{ix}-e^{-ix}}{2i} \\\\ 
\cos x &=& \frac{e^{ix}+e^{-ix}}{2}
\end{cases}$$ 

可以得到
$$\begin{aligned} 
\sin^{2n}{x} & = \left(\frac{e^{ix}-e^{-ix}}{2i}\right)^{2n} \\\\ 
& = \frac{1}{(-1)^{n}2^{2n}}\sum_{k=0}^{2n}{2n \choose k}{(-1)^{2n-k}e^{ixk-ix(2n-k)}} \\\\
& = \frac{1}{2^{2n}}\sum_{k=0}^{2n}{2n \choose k}(-1)^{(n-k)}e^{i2(n-k)x} \\\\
& = \frac{1}{2^{2n}}{2n \choose n}+\frac{1}{2^{2n-1}}\sum_{k=0}^{n-1}{2n \choose k}(-1)^{n-k}\cos{2(n-k)x}\\\\
\\\\
\cos^{2n}{x} & = \left(\frac{e^{ix}+e^{-ix}}{2}\right)^{2n} \\\\
& = \frac{1}{2^{n}}\sum_{k=0}^{2n}{2n \choose k}{e^{i2(k-n)x}} \\\\
& = \frac{1}{2^{2n}}\left[\sum_{k=0}^{n-1}{2n \choose k}{e^{i2(k-n)x}}+\sum_{k=0}^{n-1}{2n \choose k}{e^{i2(n-k)x}}\right] + \frac{1}{2^{2n}}{2n \choose n} \\\\
& = \frac{1}{2^{2n}}{2n \choose n}+\frac{1}{2^{2n-1}}\sum_{k=0}^{n-1}{2n \choose k}{\cos2(n-k)x}
\end{aligned}$$

同理可证其它几个，~~这里懒得写了~~读者自证不难。

> 简单来说，证明思路就是:
> 1. 先用欧拉恒等式和二项式定理，将其展开。
> 2. 找到可以合并的项，再用欧拉恒等式转化回去。

## 拓展链接

> [Wiki上关于三角恒等式的条目](https://en.wikipedia.org/wiki/List_of_trigonometric_identities)
> 
> [某知名音乐生Aries的博文](https://zhuanlan.zhihu.com/p/161360664)

上面有很多有趣的恒等式，一些看起来毫不相干的式子被紧密地联系起来……

~~有时间写点~~(有时间也不想（不会）写。)