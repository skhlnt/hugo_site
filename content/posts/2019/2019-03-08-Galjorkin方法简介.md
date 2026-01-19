---
title: Galjorkin方法简介
date: 2019-03-08T17:41:27-05:00
draft: false
slug: 03502af9
author: "miralem"
summary: 昨天查文献的时候，某一篇文献在和我干的事情毫无关系的部分提到了这个方法。我想到暑研的时候，一位博后给我科普的有限元分析和这看起来很像，所以决定看一眼。看上去，这确实是一个适合“工业化”的求微分方程数值解的办法。这东西在英文里头叫做 Galerkin method，但是显然有一个 e 的转写丢失了关于发音的信息。

tags: 
  - /理学
  - 有限元
  - /笔记

weight: false
math: true
comments: true
ShowToc: true
TocOpen: true
---
昨天查文献的时候，某一篇文献在和我干的事情毫无关系的部分提到了这个方法。我想到暑研的时候，一位博后给我科普的有限元分析和这看起来很像，所以决定看一眼。看上去，这确实是一个适合“工业化”的求微分方程数值解的办法。这东西在英文里头叫做 Galerkin method，但是显然有一个 e 的转写丢失了关于发音的信息。  

以一个例子来说明：泊松方程写作  

$$-\nabla^2\tilde{u}=f\ on \ \Omega$$  

$\tilde{u} = 0\ on\ \partial \Omega$   

为了 解它，我们取定一个N维的空间$X_0^N$，其基底是一些函数$\left\{\phi_i\right\}$，其中任意的函数$v ,w$满足（具体的缘由我没有细究。这里并不是非常简单。）$\int_\Omega v^2dV<\infty, v=0 \ on\ \partial\Omega$ 和 $\int_\Omega \nabla v\nabla wdV<\infty$ （这是最为常见的一种）。  

这样的目的是用这些基底表示出解来。N取得越大，就越能够逼近正确的解。显然，对于解$u$来说，一个本来应当是0的东西肯定需要和所有的基底函数垂直：  

$\int_\Omega (-\nabla^2 u-f)vdV=0\ for\ \forall v\ in\ X_0^N$  

分部积分之后，考虑到v在边界上是0这个性质，可以得到  

$\int_\Omega \nabla u\nabla vdV=\int_\Omega vfdV$  

（值得注意的是，使用一种内积$a(r, s)=\int_\Omega\nabla r\nabla sdV$，会发现误差$\tilde{u}-u$是和空间$X_0^N$垂直的。这侧面说明了这个方法的合理性。）  

然后将$u, v$表示出来，写成  

$\int_\Omega \nabla(\sum\phi_iu_i)\nabla(\sum\phi_jv_j)dV=\int_\Omega\sum\phi_iv_i\cdot fdV$  

或者说  

$\sum\sum\int_{\Omega}u_i\nabla \phi_i\nabla\phi_jv_jdV=\int_\Omega\sum\phi_iv_i\cdot fdV$  

记矩阵$A_{ij}=\int_\Omega\nabla\phi_i\nabla\phi_jdV$， 向量$b_i=\int_\Omega\phi_ifdV$  

上式就是  

$v^TAu=v^Tb$或$Au=b$  

实际操作中，有两种选取$\phi$的方式，叫nodal和modal，顾名思义，（格）点和（波）模。前者就是把空间划分为格点$\left\{x_i\right\}$并令$u(x_i)=u_i$或者说$\phi_j(x_i)=\delta_{ij}$。这种东西一看就很容易满足在边界处为0的条件。一般来说，有Lagrangian Polynomial这样全局都有值的做法，也有有限元中使用格点附近的线性函数（而在其他地方都是0）的做法。波模的例子比如一维正弦波。  
