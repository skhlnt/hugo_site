---
title: "$V+F-E=2$ 平面图欧拉示性数公式"
draft: false
date: 2021-09-23 13:01:24
slug: c9c1bd29

author: "Kenshin2438"
description: "简单介绍一下平面图的欧拉示性数公式，该问题该能拓展到更高维的情况，是拓扑学中的一个经典问题。"
keywords:
  - 平面图欧拉示性数公式
  - 欧拉示性数公式
  - V+F-E=2
tags:
  - 图论
  - 欧拉示性数公式
categories:
  - Math

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

一直没啥想写的，不过最近又看见一道和欧拉示性数公式相关的思维题，所以萌生出了写这篇博客的想法。

首先是关于**平面图**欧拉示性数公式的定义：

> 设$G$是一个连通的平面图，顶点的数目为$V$，边的数目为$E$，面的数目为$F$，则有$$V+F-E=2$$

下面使用数学归纳法进行证明：

1. 当$E=0$时，有$V=1,F=1$，等式显然成立。
2. 假设当$E=k$时等式成立，下面考虑$E=k+1$的情形。
   1. 当图中无环时易知$V=k+2,F=1$，等式显然成立。
   2. 反之，我们设$e$为环中的一条边，那么对于图$G\setminus\set{e}$由假定知等式成立（即为$E=k$的情形，令其$V=v_0,F=f_0$，则$v_0+k-f_0=2$）。那么对于图$G$我们有$V=v_0,E=k+1,F=f_0+1$，因此等式也成立。

综上，由数学归纳法可知等式对于$E\geq0$的情形皆成立。

## 具体使用

{{< admonition warning "声明" true >}}
下面这种方法只在本人太闲了弄出来玩的，实际体验并不一定好。

简单来说就是固定了边数，在使点数尽可能小，从而使之面的数目最大化。
{{< /admonition >}}

> [CSUST OJ 1066 被打脸的潇洒哥](http://acm.csust.edu.cn/problem/1066)
> 
> **题目描述**
> 
> 平面上有n个圆，求使这n个圆两两相交（即每两个圆之间恰好有两个交点）后最多能把平面划分成多少个区域。

对于圆这样的图形，我们不方便计算它的各项参数，可以直接将其边无限细分，即假定点数为$m$，则边也为$m$。由于$m$无穷大，两圆相交时并不会产生新的边，但是会减去重叠的两个点。

所以，当一共有$n$个圆时，图上的各项参数为
$$E=n\times m,V=n\times m-2\times {n \choose 2},F=2+E-V=2+n\times(n-1)$$

```cpp
int main() {
  ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);
  for (cin >> T; T--; ) {
    cin >> n;
    if (n == 0) {cout << 1 << '\n'; continue;}
    cout << 2 + (n - 1) * n << '\n';
  }
  return 0;
}
```

> [HDU 2050 折线分割平面](http://acm.hdu.edu.cn/showproblem.php?pid=2050)
> 
> 我觉得不需要题目描述了，标题即描述。

由于折线比较特殊，不方便定义端点，我们可以先直接划定边界，例如放一个圆$V=n_0,E=n_0$，但此时圆外的区域不能算作一块平面。同时，折线就可以改成两条共端点的线段。

然后就按常规的来，无穷细分一条线段为$V=k,E=k-1$。则当共有$n$条折线时，图的各项参数（使$F$最大的情况，由于边数确定即交点尽可能多）为

$$E=n_0+n\times2(k-1),V=n_0+n\times(2k-1)-2n-4\times{n \choose 2}$$

所以$F=1+E-V=1+n+2n(n-1)$

```cpp
int main() {
  ios_base::sync_with_stdio(false), cin.tie(0), cout.tie(0);
  for (cin >> T; T--; ) {
    cin >> n;
    cout << 1 + n + 2 * n * (n - 1) << '\n';
  }
  return 0;
}
```
