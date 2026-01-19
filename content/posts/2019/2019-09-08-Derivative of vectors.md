---
title: Derivative of vectors
date: 2019-09-08T19:50:33-05:00
draft: false
slug: ea69281f
author: "miralem"
summary: 就是一个简单的note，有比没有好

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
就是一个简单的note，有比没有好  

考虑向量对向量求导$\frac{\partial \vec{y}}{\partial \vec{x}}$。现在，这个记号的意义有两种可能：  
$$  
\left(\begin{array}{ccc}{\frac{\partial y_{1}}{\partial x_{1}}} & {\cdots} & {\frac{\partial y_{1}}{\partial x_{n}}} \\ {\vdots} & {} & {} \\ {\frac{\partial y_{m}}{\partial x_{1}}} & {\cdots} & {\frac{\partial y_{n}}{\partial x_{n}}}\end{array}\right)  
$$  
或者  
$$  
\left(\begin{array}{ccc}{\frac{\partial y_{1}}{\partial x_{1}}} & {\cdots} & {\frac{\partial y_{m}}{\partial x_{1}}}  \\ {\vdots} & {} & {} \\ {\frac{\partial y_{1}}{\partial x_{n}}} & {\cdots} & {\frac{\partial y_{n}}{\partial x_{n}}}\end{array}\right)  
$$  
前者是numerator layout，即分子的y保持为列向量的样子；后者是denominator layout，即分母的x保持为列向量的样子。我们使用numerator layout。  

现在考虑式子$\frac{\partial \vec{u}^{\top} \vec{v}}{\partial \vec{x}}$。从直觉上说，我们至少希望结果保持为行向量的样子。如果不是向量，我们会写$u\partial_x v+v\partial_xu$。但是这回对应的$v\partial_xu^\top$dimension对不上。为了对上，我们改写为  
$$  
\frac{\partial \vec{u}^{\top} \vec{v}}{\partial \vec{x}}=\vec{u}^{\top} \frac{\partial \vec{v}}{\partial \vec{x}}+\vec{v}^{\top} \frac{\partial \vec{u}}{\partial \vec{x}}  
$$  
这个思路可以解决基本上所有的情况。例子：我们有矩阵D，向量a,v，令$E=(Da-v)^\top(Da-v)$，那么  
$$  
\partial_aE=\partial_a(a^\top D^\top Da-a^\top D^\top v-v^\top Da+v^\top v)=2a^\top D^\top D-2v^\top D  
$$  
如果我们使用denominator layout，那么所有的结果就要取转置。注意，使用chain rule得到的结果在顺序上也要反过来。例如，$\partial f(g(u))/\partial x$，其中u和x都是向量，就变成了$\partial_xu\cdot\partial_ug\cdot\partial_gf$，而在numerator layout下是我们习惯的$\partial_gf\cdot\partial_ug\cdot\partial_xu$。这也是我们偏好后者的缘由之一。  
