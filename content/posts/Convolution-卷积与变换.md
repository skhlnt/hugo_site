---
title: "Convolution 卷积与变换"
date: 2022-03-12T20:39:10+08:00
draft: true
slug: d7959a4b.html

author: "Kenshin2438"
description: "记录一下我见过的奇奇怪怪的卷积以及用于高效计算的变换"
tag: ["卷积"]
categories: [""]

weight: false
math: true
comments: true

cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
---

## 卷积积分/离散卷积

## 多项式卷积

一般来说，多项式卷积表示的就是多项式乘法对应项的系数

$$
c[k] = \sum_{i+j=k}(a[i] \times b[j])
$$

### FFT

+ FFT 三次变两次

由于复数平方满足下式：
$$
z = a + bj \rightarrow z^2=(a^2 + b^2) + 2abj
$$
我们在所用的复数数组，其实部和虚部分别为两多项式的系数，然后平方取虚部的一半即可得到答案，此时只要一次`DFT`和一次`IDFT`。

### NTT

$$
c[k] = \sum_{i+j=k}(a[i] \times b[j]) \bmod P
$$

$P=r\times 2^k+1$为一个素数，$g$为模$P$的原根。

### MTT

任意模数`NTT`，考虑的是没有原根的情况。

## 异或卷积

$$
c[k] = \sum_{i \oplus j = k}(a[i] \times b[j])
$$

### FWT


## 或卷积/与卷积

+ `OR`
$$
c[k] = \sum_{i \| j = k}(a[i] \times b[j])
$$

+ `AND`
$$
c[k] = \sum_{i \& j = k}(a[i] \times b[j])
$$

### SOSDP/高维前缀和

先枚举每个元素，再枚举集合，然后就有转移$S \setminus \{i\} \rightarrow S$。

```cpp
void SOSDP(int *a, int n) { 
    for (int i = 0; i < n; i++) 
        for (int s = 0; s < (1 << n); j++) 
            if (s >> i & 1) a[s] += a[s ^ (1 << i)];
}
```

### FMT

## 子集卷积

$$
c[k] = \sum_{i \& j=0,i | j=k}(a[i] \times b[j])
$$

## gcd/lcm卷积

+ `gcd`
$$
c[k] = \sum_{\gcd(i, j) = k}(a[i] \times b[j])
$$

+ `lcm`
$$
c[k] = \sum_{\mathrm{lcm}(i, j) = k}(a[i] \times b[j])
$$

## 区间卷积

其实是一类线段树问题，来源[BZOJ 2962. 序列操作](https://hydro.ac/d/bzoj/p/2962)

> 有一个长度为n的序列，有三个操作
> 1.I a b c表示将[a,b]这一段区间的元素集体增加c
> 2.R a b表示将[a,b]区间内所有元素变成相反数
> 3.Q a b c表示询问[a,b]这一段区间中选择c个数相乘的所有方案的和mod 19940417的值。(此处1<=c<=20)

