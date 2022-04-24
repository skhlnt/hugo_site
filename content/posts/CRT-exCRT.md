---
title: "孙子剩余定理 - CRT/exCRT"
date: 2021-07-25 15:04:43
draft: true
slug: 72b0c59

author: "Kenshin2438"
description: ""
categories:
  - Number Theory
tags:
  - CRT/exCRT

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

之前介绍`Lucas`定理时，内容涉及到了中国剩余定理，以及欧拉定理。

后者应该是广为人知的定理（之后也会写拓展欧拉定理的~~吧~~），然而前者的名气似乎远有不如。

本篇以证明为主，（~~不喜欢证明的可以关了~~）当然也会遵循传统给出板子。

<!--more-->

> 设$m_1,m_2,\dots,m_k$为$k$个两两互素的正整数，$m=\prod{m_i}$。
>
> 令$m=m_iM_i$，则同余方程组
> $$\begin{cases}x &\equiv & b_1 \pmod{m_1} \\\\ x &\equiv & b_2 \pmod{m_2} \\\\ & \vdots & \\\\ x &\equiv & b_k \pmod{m_k} \end{cases}$$
> 
> 有唯一解
> $$x\equiv {\sum_{i=1}^{k}{b_iM_iM_i^{-1}}}\pmod{m},M_iM_i^{-1}\equiv1\pmod{m_i}$$

我们从基础解和基础解系的角度出发，构造这样一组**基础解**：
$$\begin{cases}
x_1 & \equiv & 1 \pmod{m_1} \quad \\\\
x_1 & \equiv & 0 \pmod{m_2} \quad \\\\
& \vdots & \\\\
x_1 & \equiv & 0 \pmod{m_k} \quad 
\end{cases}
\quad \dots \quad
\begin{cases}
x_k & \equiv & 0 \pmod{m_1} \quad \\\\
x_k & \equiv & 0 \pmod{m_2} \quad \\\\
& \vdots & \\\\
x_k & \equiv & 1 \pmod{m_k} \quad 
\end{cases}$$

由于$m_i$两两之间互素，我们很容易得到**最初**给的同余方程组的解，为：$\sum{b_ix_i}\mod m$.

### 单独考虑其中一个基础解

可以知道$x_i\mid [\{m_1,m_2,\dots,m_k\} \setminus \{ m_i\}]$，即$x_i$应该为$\frac{m}{m_i}t$的形式，同时又由于$x_i\equiv 1\pmod{m_i}$，$x_i$同时也为$sm_i+1$的形式，其中($s,t\in \mathbb{Z}$)。

综合来看就是

$$\exists s,t \in \mathbb{Z}, \frac{m}{m_i}t=m_is+1=x_i$$

结果至此已经很明显了，即：

$$x_i\equiv\frac{m}{m_i}\times (\frac{m}{m_i})^{-1} \equiv 1\pmod{m_i}$$

> 没看出来的请自行百度**拓展欧几里得**，这里就不给详解了。

逆元的存在性可由$(\frac{m}{m_i}, m_i)=1$得到，又由于$m_i$两两互素，结果直接合并即可得到我们上面待证明的结论。

## 拓展问题
这里使我们的一个条件失效，即$m_i$**两两互素**。

### 再思考 - 合并同余式
从两个式子的情况开始:

$$\begin{cases}
x \equiv b_1 \pmod{m_1} \\\\
x \equiv b_2 \pmod{m_2}
\end{cases}$$

我们令$(m_1, m_2)=d$，且两同余式有公共解$x_0$.

则有$\begin{cases}x_0\equiv b_1 \pmod{d} \\\\ x_0 \equiv b_2 \pmod{d} \end{cases}$，得到$d\mid(b_1-b_2)$。

> 这也是该方程组的有解的必要条件，充分性也很好证明。

我们把第一个同余方程的解表示为$x=b_1+m_1y$，代入第二个同余式有:

$$m_1y\equiv b_2-b_1\pmod{m_2}$$

要使上面的一次同余方程有解，则$(m_1,m_2)\mid (b_2-b_1)$，**充分性get**。

若已满足条件，则该方程对模数$\frac{m_2}{d}$有唯一解$y\equiv y_0\pmod{\frac{m_2}{d}}$

所以，

$$x=b_1+m_1y_0+\frac{m_1m_2}{d}t,(t=0,\pm1,\pm2,\dots)$$

观察最后的解，可以知道同余式组的解$x$对模数$[m_1,m_2]$唯一。

也就是，`合并`两个同余式为

$$x\equiv x_t\pmod{[m_1,m_2]}$$

## 代码

原理应该讲清楚了，代码一次给出吧。


```cpp CRT/exCRT
inline ll CRT(ll r[], ll m[], int n) {
	ll M = 1LL, ans = 0LL;
	for (int i = 1; i <= n; i++) M *= m[i];
	for (int i = 1; i <= n; i++) { 
		ll Mi = M / m[i], Mi_inv = inv(Mi, m[i]);
		ans = (ans + mul(mul(r[i], Mi, M), Mi_inv, M)) % M;
	} return ans;
}

inline ll exCRT(ll r[], ll m[], int n) {
	ll M = m[1], ans = r[1];
	for (int i = 2; i <= n; i++) {
		ll g, x, y, rhs = ((r[i] - ans) % m[i] + m[i]) % m[i];
		exgcd(M, m[i], g, x ,y);
		if (rhs % g) return -1;
		ll t = m / g * M[i]; // m = lcm(m, M[i]);
		ans += mul(mul((x % M[i] + M[i]) % M[i], rhs / g, M[i]), m, t); 
		m = t;
		ans = (ans % M + M) % M;
	} return ans;
}
```

## 相关定理

> 若$m_1,m_2,\dots,m_k$为$k$个两两互素的正整数，$m=\prod{m_i}$。
> 
> 则同余式$f(x)\equiv0\pmod{m}$有解的充分必要条件是
> $$f(x)\equiv0\pmod{m_i}(i=1,2,\dots,k)$$
> 对每一个$i$均有解。
> 
> 若用$T_i$表示第$i$个方程的`解数`，则$f(x)\equiv0\pmod{m}$的解数$T=\prod{T_i}$。

证明从略。

~~咕咕咕~~