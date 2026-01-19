---
title: Vector Calculus, Matthews
date: 2019-05-02T02:09:45-05:00
draft: false
slug: afc1570c
author: "miralem"
summary: 我现在越来越感到自己有一些基础的不牢固，比如向量微积分，积分变换和与格林函数相关的一些知识。所以我首先找来一本小册子来复习最简单的第一部分。这是 Matthews 的《向量微积分》，应该是面向大一的物理系学生的，我应当早些看到这本书。有些东西，我之前没有意识到，每次做计算都走弯路。

tags: 
  - /理学
  - /笔记
  - 向量微积分

weight: false
math: true
comments: true
ShowToc: true
TocOpen: true
---
我现在越来越感到自己有一些基础的不牢固，比如向量微积分，积分变换和与格林函数相关的一些知识。所以我首先找来一本小册子来复习最简单的第一部分。这是 Matthews 的《向量微积分》，应该是面向大一的物理系学生的，我应当早些看到这本书。有些东西，我之前没有意识到，每次做计算都走弯路。  

第一章介绍向量的概念，以及点积与叉积。介绍了场的概念。  

第二章教人怎样做积分。  

第三章介绍了散度、梯度和旋度。用$\nabla f\cdot\mathbf{r}=df$来定义梯度。  

第四章介绍了下标写法。引入 Levi-Civita 符号和 Kronecker 符号后，用下标写法计算带有$\nabla$的式子变得比较方便，前提是记住  

$$(\mathbf{a}\times\mathbf{b})_i=\epsilon_{ijk}a_jb_k$$  

$$\epsilon_{ijk}\epsilon_{klm}=\delta_{il}\delta_{jm}-\delta_{im}\delta_{jl}$$  

以前我记不住诸如  

$$\nabla\times(\nabla\times\mathbf{u})=\nabla(\nabla\cdot\mathbf{u})-\nabla^2\mathbf{u}$$  

这样的式子，手算经常出问题。我知道下标写法很晚，所以以前没有意识到它可以这样简化相关的运算。  

第五章介绍了一些“Integral Theorems”但是没有提到广义斯托克斯公式。  

第六章讲非 Cartesian 的（正交）坐标系并给出了 grad Div Curl Laplcaian 的做法。  

第七章讲 Cartesian 张量。  

第八章讲了一些物理应用。在（三维的）连续介质中，存在量纲为压强的应力$P_{ij}$，可以写出 $\delta F_i=P_{ij}n_j\delta S$，由力和力矩平衡，得到约束  

$$\frac{\partial P_{ij}}{\partial x_j}=0$$  

$$P_{ij}=P_{ji}$$  

在固体中存在无量纲的应变，定义为$E_{ij}=\frac{1}{2}(\frac{\partial v_i}{\partial x_j}+\frac{\partial v_j}{\partial x_i})$，小形变下有胡克定律  

$$P_{ij}=c_{ijkl}E_{kl}$$  

由张量$c$的各向同性，最终可以写为  

$$P_{ij}=\lambda\delta_{ij}E_{kk}+2\mu E_{ij}$$  

$\lambda$和$\mu$就是叫做$Lam\'{e}$ 常量的。  

在流体当中，径向的应力由压强$p$决定，可在$P_{ij}$中消去径向的$\lambda$，即  

$$P_{ij}=-p\delta_{ij}+2\mu e_{ij}-\frac{2}{3}\mu\delta_{ij}e_{kk}$$  

$\mu$就是粘度。就此，得到运动方程即N-S方程：  

$$\rho\mathrm{D}\mathbf{u}=\mathbf{b}-\nabla p+\mu\nabla^2\mathbf{u}+\frac{1}{3}\mu\nabla\nabla\cdot\mathbf{u}$$  

$\mathrm{D}$为物质导数，$\mathbf{b}$为外力。如果外力是保守力（$b=-\nabla\Phi$）且流体不可压缩（$\nabla\cdot\mathbf{u}=0$），且是 steady fluid 忽略$\mu$的影响，则可以将$(\mathbf{u}\cdot\nabla)\mathbf{u}=\nabla(u^2/2)-\mathbf{u}\times(\nabla\times\mathbf{u})$代入上式，并与$\mathbf{u}$点乘，得到 Bernoulli 方程：  

$$\nabla(\rho u^2/2+p+\Phi)=0$$  

 这个守恒量为一些定性分析提供方便。  
