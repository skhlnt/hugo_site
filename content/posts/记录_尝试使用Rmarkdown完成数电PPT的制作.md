---
title: "R - 尝试使用Rmarkdown完成数电PPT的制作"
date: 2022-05-30T13:29:09+08:00
draft: true
slug: bd6e8d4c

author: "Kenshin2438"
description: "实际上为Beamer(PDF)输出, R语言用得不太熟练还不如直接用LaTex..."
summary: "实际上为Beamer(PDF)输出, R语言用得不太熟练还不如直接用LaTex..."
keywords:
  - Rmarkdown
  - R语言制作Beamer
categories: 
  - R
tags: 
  - Rmarkdown

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

暂时只作代码记录，后面复盘。

顺带记录一个东西：使用 ```` 包裹 `markdown`源码可以防止代码块的转义。

---

````Rmarkdown
---
title: "数字逻辑与数字系统"
subtitle: "第三章 - 门电路"
author: 
  - 
date: "`r Sys.Date()`"
fontsize: 10pt
output: 
  beamer_presentation: 
    toc: yes
    slide_level: 2
    fonttheme: professionalfonts
---

## 0x00 概述

本章将系统地讲述数字集成电路中的基本逻辑单元电路——门电路，为后续使用门电路器件打下基础。

主要介绍二极管和三极管在开关状态下的工作特性，`CMOS`门电路和`TTL`门电路的工作原理和逻辑功能等。

重点内容为`CMOS`门电路和`TTL`门电路。

## 0x00.1 基本概念

1. 门电路: 实现基本逻辑运算和复合逻辑运算的单元电路。
2. 电子电路中用高、低电平分别表示二值逻辑的1和0两种逻辑
状态
3. 常用的门电路: 与门、或门、非门、与非门、或非门、
与或非门和异或门
4. `TTL`逻辑门: 由若干半导体三极管和电阻组成
5. `CMOS`逻辑门: 由若干场效应管和电阻组成

## 0x00.2 获得高、低电平的基本开关电路

高低电平在一定的范围波动

（一般电路中，`2-5V`为高电平；`0-0.8V`为低电平）

```{r, echo=FALSE, fig.align='center', out.width='80%'}
knitr::include_graphics("images/基本开关电路.png")
```

开关元件`S`由半导体二极管、半导体三极管、场效应管构成。

## 0x00.3 正逻辑与负逻辑

+ 正逻辑: 高电平表示逻辑1, 低电平表示逻辑0
+ 负逻辑: 高电平表示逻辑0, 低电平表示逻辑1

```{r, echo=FALSE, fig.cap="正负逻辑-示意图", fig.align='center'}
knitr::include_graphics("images/正负逻辑-示意图.png")
```

## 0x00.4 门电路的分类

按开关管的类型可以将常见的逻辑门电路分为：

```{r, echo=FALSE, fig.align='center', out.width='100%'}
knitr::include_graphics("images/门电路分类.png")
```

## 0x01 半导体二极管门电路

利用半导体二极管的单向导电性

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='40%'}
img <- c("images/二极管开关电路.png", "images/二极管伏安特性曲线.png")
knitr::include_graphics(img)
```

工作原理：

- 当$V_I=V_{IH}=V_{CC}$, `D`截止, $V_O=V_{OH}=V_{CC}$;
- 当$V_I=V_{IL}=0$, `D`导通, $V_O=V_{OL}=0$。

## 0x01.1 二极管伏安特性的近似

- (a). 当外电路的等效电源$V_{CC}$和等效电阻$R_L$都很小时，二极管的正向导通压降和正向电阻都不能忽略。
- (b). 当二极管的正向导通压降和外加电源电压相比不能忽略，而与外接电阻相比二极管的正向电阻可以忽略。
- (c). 当二极管的正向导通压降和正向电阻与电源电压和外接电阻相比均可忽略时，可以将二极管看作理想开关。

PN结方程: $i = I_S\left(e^\frac{v}{V_T} - 1 \right)$

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='80%'}
knitr::include_graphics("images/二极管近似.png")
```

## 0x01.2 二极管门电路


设$V_{CC} = 5V, V_{IH}=3V, V_{IL}=0V$, 二极管的正向导通压降$V_{DF}=0.7V$

通过对电路的分析，容易验证电路功能。

### 二极管或门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/二极管或门.png")
```

---

### 二极管与门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/二极管与门.png")
```

---

### 二极管构成的门电路的缺点

1. 电平有偏移
2. 带负载能力差

## 0x02 TTL 门电路

三极管-三极管逻辑门电路（`TTL`），是指输入端和输出端都用三极管的电路，属于双极型数字集成电路。

回顾一下三极管的输出特性（以`NPN`为例）

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='80%'}
knitr::include_graphics("images/NPN输出特性.png")
```

1. 放大区：$v_{BE} > V_{ON}, v_{CE} > v_{BE}$; $\Delta i_C = \beta \Delta i_B$
2. 饱和区：$v_{BE} > V_{ON}, v_{CE} > v_{BE}$; $\Delta i_C$随$\Delta i_B$增加变缓，趋于饱和
3. 截止区：$v_{BE} < V_{ON}, v_{CE} > v_{BE}$; $i_B = i_C = 0$

## 0x02.1 双极型三极管的基本开关电路（三极管反相器）

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='45%'}
knitr::include_graphics("images/三极管开关电路.png")
```

1. $v_I=V_{IL}=0$, 则$v_{BE}<V_{ON}$

三极管截止, $i_B=i_C=0, v_O=V_{OH}=V_{CC}$

2. $v_I>V_{ON}$, 则三极管开始进入放大区

$$
i_B = \frac{v_I-V_{ON}}{R_B} \quad v_O=v_{CE}=V_{CC}-i_C R_C=V_{CC}-\beta i_B R_C
$$

---

3. 若$v_I$继续升高，$i_B$增加，$v_O$下降。当$R_C$上压降接近于$V_{CC}$时，$v_O \approx 0$。三极管工作在深度饱和状态 $v_O=V_{OL}\approx 0$。

双极型晶体管工作状态的判断：

$$
I_{BS}=\frac{V_{CC} - V_{CE(sat)}}{\beta\left(R_C + R_{CE(sat)}\right)}\approx\frac{V_{CC}-V_{CE(sat)}}{\beta R_C}\approx\frac{V_{CC}}{\beta R_C}
$$

若$i_B>I_{BS}$，则三极管工作在饱和状态。

## 0x02.2 TTL 反相器（非门）

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='50%'}
knitr::include_graphics("images/TTL反相器.png")
```

1. 当$v_I=V_{IL}$，T1发射结导通，T2发射结不导通，使T4导通、T5截止，输出为高电平$V_{OH}$；
2. 当$v_I=V_{IH}$，T2发射结导通使T4截止、T5导通，输出为低电平$V_{OL}$。

输出和输入是反相关系：$Y=A^\prime$。

---

**值得注意几个点**:

- T2的输出$v_{C2}$和$v_{E2}$变化方向相反，故称**倒相级**；
- 输出级在稳态下，T4和T5总有一个导通、一个截止。既能降低功耗又提高了带负载能力，称推拉式；
- D2保证T5导通时T4截止；D1抑制负向干扰；

对`TTL`电路而言，**输入端的悬空状态和接逻辑高电平等效**。输入端经过电阻（通常取几十千欧以内）接电源电压时，与接逻辑高电平等效。输入端经过电阻接地时，输入端的电平与电阻阻值的大小有关，当电阻阻值很小时（例如只有几十欧姆），输入端相当于接逻辑低电平；当电阻阻值大到一定程度以后，输入端电压将升高到逻辑高电平。

---

### 电压传输特性

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/TTL电压传输特性.png")
```

+ `AB`段：截止区 $v_I<0.6V$, 故$v_{B1}<1.3V$。
T2,T5截止，T4导通 $V_{OH}=V_{CC}-v_{R2}-v_{BE4}-v_{D2}\approx 3.4V$

+ `BC`段：线性区 $0.6V<v_I<1.3V$。
T2导通并且工作在放大区，T5截止，$v_I\uparrow\Rightarrow v_O\downarrow$

+ `CD`段：转折区 $v_I=V_{TH}\approx 1.4V$，故$v_{B1}\approx 2.1V$。
T2,T5导通，T4截止，$v_O$迅速减小 故$V_{OL}\approx 0$

+ `DE`段：饱和区 $v_I\uparrow$而$v_O$不变，为$v_O=V_{OL}$

---

### 输入端噪声容限

在输出高、低电平变化允许范围内，允许输入高、低电平的波动范围称为输入端噪声容限。

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/噪声容限.png")
```

## 0x02.3 `OC`门 （集电极开路门）

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='80%'}
knitr::include_graphics("images/OC门.png")
```

- 普通的`TTL`电路不能将输出端连在一起。输出端连在一起，可能使电路形成低阻通道，使电路因电流过大而烧毁；
- 由于`OC`门的集电极是开路的，所以若要实现正常的逻辑功能，需外加上拉电阻$R_L$并且外接电源$V_{CC}$。

---

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='45%'}
knitr::include_graphics("images/OC门上拉电阻.png")
```

上拉电阻$R_L$的选取： 

$$
R_{L \max} = \frac{V_{CC} - V_{OH \min}}{nI_{OH}+mI_{IH}}, R_{L \min} = \frac{V_{CC} - V_{OL \max}}{I_{OL \max}+PL_{IL}}
$$

$n$为`OC`门输出端并接的个数，$m$为负载门的输入端总数，$P$为负载门的总数。

## 0x02.4 其他类型的TTL门电路

+ `TSL`三态门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/TSL三态门.png")
```

---

+ `TTL`与非门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='50%'}
knitr::include_graphics("images/TTL与非.png")
```

1. 当$A, B$之中有一个接低电平，T1必有一个发射结导通，T2和T5都不导通，输出为高电平$V_{OH}$
2. 当$A, B$均接高电平，T2和T5同时导通，输出为低电平$V_{OL}$

- 输出满足$Y=(A \cdot B)^\prime$

---

+ `TTL`或非门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='50%'}
knitr::include_graphics("images/TTL或非.png")
```

1. 当$A$接高电平，T2和T5同时导通，T4截止，输出$Y$为低电平
2. 当$B$接高电平，T2'和T5'同时导通，T4截止，输出$Y$为低电平
3. 当$A,B$均为低电平，T2和T2'同时截止，T5截止，T4导通，于是输出$Y$为高电平

- 输出满足$Y=(A + B)^\prime$

---

+ `TTL`与或非门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='60%'}
knitr::include_graphics("images/TTL与或非.png")
```

---

+ `TTL`异或门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='60%'}
knitr::include_graphics("images/TTL异或门.png")
```

## 0x03 `CMOS`门电路

`MOS`门电路有制造工艺简单、集成度高、功耗低、体积小、成品率高等优点，特别适用于中、大规模集成电路的制造，在目前数字集成电路产品中占据了相当大的比例。

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='90%'}
knitr::include_graphics("images/常见MOS管.png")
```

## 0x03.1 `CMOS`开关电路

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/CMOS开关电路.png")
```

## 0x03.2 `CMOS`反相器

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/CMOS反相器.png")
```

---

### 电压传输特性

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/CMOS电压传输特性.png")
```

---

### 电流传输特性

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/CMOS电流传输特性.png")
```

---

### 输入端噪声容限

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/CMOS输入端噪声容限.png")
```

---

### 传输时延

传输延迟时间：输出电压变化落后于输入电压变化的时间。

+ $t_{PHL}$: 输出由高电平跳变为低电平时的传输延迟时间
+ $t_{PLH}$: 输出由低电平跳变为高电平时的传输延迟时间
+ $t_{pd}$ : 平均传输延迟时间, $t_{pd}=\frac{t_{PHL} + t_{PLH}}{2}$

---

## 0x03.3 `CMOS`与非门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='60%'}
knitr::include_graphics("images/CMOS与非门.png")
```

$A$ $B$ $T_{N1}$ $T_{N1}$ $T_{N1}$ $T_{N1}$ $L$
--  -- --------  -----   --------  -------- ---
0   0    截止     导通      截止       导通   1
0   1    截止     导通      导通       截止   1
1   0    导通     截止      截止       导通   1
1   1    导通     截止      导通       截止   0

---

## 0x03.4 `CMOS`或非门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='60%'}
knitr::include_graphics("images/CMOS或非门.png")
```

$A$ $B$ $T_{N1}$ $T_{N1}$ $T_{N1}$ $T_{N1}$ $L$
--  -- --------  -----   --------  -------- ---
0   0    截止     导通      截止       导通   1
0   1    截止     导通      导通       截止   0
1   0    导通     截止      截止       导通   0
1   1    导通     截止      导通       截止   0

## 0x03.5 `CMOS`传输门 (`TG`门)

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='100%'}
knitr::include_graphics("images/TG门.png")
```
+ 工作原理：设两管开启电压的绝对值为$2V, V_{DD}=5V$, 输入信号在$0-5V$内连续变化。
  1. $C = 0V, \bar{C}=5V$时，传输门截止（均截止）
  2. $C = 5V, \bar{C}=0V$时，传输门导通（至少一个导通）

## 0x03.6 其它`CMOS`门电路

### `OD`门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='80%'}
knitr::include_graphics("images/OD门.png")
```

目的同`TTL`的`OC`门，都是为了实现线与。

---

### `CMOS`三态门

```{r, echo=FALSE, fig.show='hold', fig.align='center', out.width='35%'}
knitr::include_graphics("images/CMOS三态门.png")
```

$$
\begin{cases}
\bar{EN}=0, & F=\bar{A} \\
\bar{EN}=1, & F\text{对外高阻态}
\end{cases}
$$

---

## 0x04 感谢

`Thanks!`

## 0x05 参考

1. 高等教育出版社《数字电子技术基础（第6版）》阎石
2. 2019《蜂考系统课 - 数电》
3. [中国科技大学课件 - 03门电路.pdf](http://staff.ustc.edu.cn/~huxw/%CA%FD%D7%D6%C2%DF%BC%AD%B5%E7%C2%B7/03%C3%C5%B5%E7%C2%B7.pdf)
4. 以及一份不知出处的数电笔记

本`Beamer`使用`Rmarkdown + Pandoc`生成，`tex`模板文件所在仓库：

github: <https://github.com/BruceZhaoR/Zh-beamer>
````