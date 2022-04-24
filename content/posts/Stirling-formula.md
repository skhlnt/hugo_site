---
title: "斯特灵公式 - Stirling formula"
date: 2021-06-03 00:00:00
slug: 5160a86b

author: "Kenshin2438"
description: ""
categories:
  - Math
tags:
  - Stirling formula

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

上次写题用到了斯特灵公式，然后就被老师喷了 $\dots$ 

u1s1活该被喷，虽然斯特灵公式我一直在用，但是从来没有证过

为了以后大胆地用斯特灵公式，这里简单写一个证明。

<!--more-->

#### $Proof$：

$$
Stirling \\\\ formula: \qquad n! \thickapprox \sqrt{2 \pi n} \left ( \frac{n}{e} \right )^{n}
$$

第一眼看见，真的被惊艳到了。

这是一个很好的对阶乘的渐进估计，事实上，就算是对广义阶乘函数（$\Gamma$）也很管用。
$$
\newcommand{\ud}{\mathrm{d}}
Gamma \ \ Function: \qquad \Gamma{(x)} = \int_{0}^{\infty} t^{x-1}e^{-t} \ \ud t
$$
为了更好地研究阶乘函数，我们将其写成如下形式：
$$
\newcommand{\ud}{\mathrm{d}}
x! = \Gamma (x+1) = \int_{0}^{\infty} {t^{x}e^{-t}} \ \ud t =  \int_{0}^{\infty} {e^{x \ln t - t}} \\\\ud t
$$
我们换一下元， $t = (s+1)x$ ,
$$
\newcommand{\ud}{\mathrm{d}}
\begin{eqnarray}
x! & = & \int_{-1}^{\infty} {e^{x \ln(s+1) + x \ln x - x(s+1)}} x \ \ud s \\\\
& = & \frac{x^{x+1}}{e^{x}} \int_{-1}^{\infty} {e^{x\left ( \ln(s+1) - s\right )}} \ \ud s \\\\
& = & \frac{x^{x+1}}{e^{x}} \int_{-1}^{\infty} {e^{x\left ( -s + \sum_{n=1}^{\infty}{\frac{(-1)^{n-1}}{n} s^{n}} \right )}} \ \ud s \\\\
& \thickapprox & \frac{x^{x+1}}{e^{x}} \int_{-\infty}^{+\infty} {e^{-x \frac{s^2}{2}}} \ \ud s \\\\
& = & \frac{x^{x+1}}{e^{x}} \sqrt{\frac{2}{x}} \int_{-\infty}^{+\infty} {e^{-u^2}} \ \ud u \\\\
& = & \frac{x^{x}}{e^{x}} \sqrt{2 \pi x}
\end{eqnarray}
$$

####  使用 Laplace's method

$Wiki$上关于斯特灵公式的证明用到了$Laplace's \\\\ method$
$$
\newcommand{\ud}{\mathrm{d}}
\int_{a}^{b} {e^{M \ f(x)}} \ud x \thickapprox e^{M f(x_0)} \sqrt{\frac{2\pi}{M|f''(x_0)|}} \quad as \quad M \rightarrow \infty
$$
这里不作介绍，请移步$Wiki$

#### 使用形式

一般用到的是更为精确一点的形式：

$$
n! = \sqrt{2 \pi n} \left ( \frac{n}{e} \right )^{n} (1 + \frac{1}{12n} + o(\frac{1}{n}))
$$