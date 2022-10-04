---
title: "Hello World - Hugo博客搭建笔记"
date: 2022-04-01T01:47:10+08:00
draft: false
slug: a8baf211

author: "Kenshin2438"
description: ""
categories: 
  - Blog
tags: 
  - hugo

weight: 1
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

## Hello World

无法忍受`hexo`的速度，故换到`hugo`，使用主题为`PaperMod`，正在一步步转移博客内容。

<!--more-->

## 各种参考源

感谢互联网，让本前端菜鸡也能尽可能找到自己想要的实现方式。

+ [hugo-PaperMod](https://github.com/adityatelange/hugo-PaperMod) 官方文档（~~个人感觉不是很全~~，出现问题先去`issue`找）
+ [LoveIt](https://github.com/dillonzq/LoveIt) 挺好看的一个主题，各项功能也很完善，但是我还是喜欢`PaperMod`多一点
  + `admonition` 支持。（实际代码来自`hugo-backup`）
  + ~~`bilibili` 视频引入。~~ （**已删除**）
+ [Sulv's Blog](https://www.sulvblog.cn) 使用了`PaperMod`的一个博客，做了许多修改，[文章合集](https://www.sulvblog.cn/posts/blog/)。
  + 侧边`toc`栏，[文章链接](https://www.sulvblog.cn/posts/blog/hugo_toc_side/)。（效果不太满意，已经放弃）
  + `twikoo`移植，[参考](https://www.sulvblog.cn/posts/blog/hugo_twikoo/)代码的添加方式。（目前为`hugo-backup`的实现方式）
  + `friend-link` 页面样式。
+ [hugo-backup](https://github.com/YazidLee/hugo-backup) 一个基于[PaperMod](https://adityatelange.github.io/hugo-PaperMod/)的定制主题。
  + `fontawsome` 直接copy了代码。
  + 侧边`go to buttom`按钮。
  + `twikoo` 评论区样式。
+ ~~[Mathjax](https://www.mathjax.org/) 数学公式渲染~~(**已更换**为`KaTex` [Wiki](https://github.com/KaTeX/KaTeX.wiki.git))
+ [Source Code Pro](https://github.com/adobe-fonts/source-code-pro) 代码字体
+ [favicon.io](https://favicon.io/) 网站图标
  
  > This favicon was generated using the following font:
  > - Font Title: Lexend Zetta
  > - Font Author: Copyright 2019 The Lexend Project Authors (https://github.com/googlefonts/lexend)
  > - Font Source: http://fonts.gstatic.com/s/lexendzetta/v22/ll8uK2KYXje7CdOFnEWcU8synQbuVYjYB3BCy9bG0z5jbs8qbts.ttf
  > - Font License: SIL Open Font License, 1.1 (http://scripts.sil.org/OFL))
+ [highlight.js](https://highlightjs.org/) 使用highlight.js提供代码高亮，官方的`chroma`实在简陋了
  + `atom-one-dark.min.css` 目前出了点问题，和预期的效果有点出入
+ [cdnjs](https://cdnjs.com/)`cdn`支持了`twikoo.js`和`mathjax.js`。
+ [hugo-encryptor](https://github.com/Li4n0/hugo_encryptor) 使用参考[link](https://www.10101.io/2019/04/17/encrypt-content-in-hugo?PageSpeed=noscript)

## TODO

+ [x] **failed** ~~尝试用pandoc渲染（不行就算了，等会了再来）~~
+ [x] 筛选旧博客，剔除/修改部分低创内容，与主题相适应。
+ [x] **failed** 更换字体，并解决`Mathjax`字体大小同全局字体的冲突
+ [x] `permalinks`修改，~~正在考虑换域名一事~~
+ [ ] 内容加密，类似[hexo-blog-encrypt](https://github.com/D0n9X1n/hexo-blog-encrypt)的实现方式
+ [ ] `img lazyload`（暂时用不到）
+ [x] **deleted** `bilibili`视频引入。（受到b站api限制，画面质量太低，准备清除）
+ [ ] 寻找更好的侧边`toc`实现方式。
+ [x] 使用`<!--more-->`自动摘要
+ [x] 解决移动端`Mathjax`公式过长带来的问题
+ [x] 修复`cases`大括号断裂 (已替换为`svg`格式显示)
+ [x] 解决`code`块出现黑色背景色的问题，恢复圆角显示
+ [x] 停用hugo官方提供的`chroma`，使用`highlight.js`高亮代码
+ [ ] `twikoo` 评论邮箱自动通知部署
+ [x] 更换适合国内网络环境的`cdn`，或者放在本地（次之）。包含`twikoo`, `mathjax`。

---

## 测试

### Math

When $a \ne 0$, there are two solutions to \\(ax^2 + bx + c = 0\\) and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$

测试较长公式的处理

+ 行内公式（使用`$...$`）

**未解决**

<!-- $A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B$ -->

+ 行间公式（使用`$$...$$`）

$$
A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B=A=B
$$

### Admonition

{{< admonition node "node" false >}}Something{{< /admonition >}}
{{< admonition abstract "abstract" false >}}Something{{< /admonition >}}
{{< admonition info "info" false >}}Something{{< /admonition >}}
{{< admonition tip "tip" false >}}Something{{< /admonition >}}
{{< admonition success "success" false >}}Something{{< /admonition >}}
{{< admonition question "question" false >}}Something{{< /admonition >}}
{{< admonition warning "warning" false >}}Something{{< /admonition >}}
{{< admonition failure "failure" false >}}Something{{< /admonition >}}
{{< admonition danger "danger" false >}}Something{{< /admonition >}}
{{< admonition bug "bug" false >}}Something{{< /admonition >}}
{{< admonition example "example" false >}}Something{{< /admonition >}}
{{< admonition quote "quote" false >}}Something{{< /admonition >}}

### Highlight

```cpp
#include <iostream>

int main() {
	std::cout << "Hello World!" << std::endl;
	return 0;
}
```
