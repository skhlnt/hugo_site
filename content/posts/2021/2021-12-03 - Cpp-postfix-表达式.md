---
title: 用来避免行末空格的cout<<"\n "[i < n];是什么语法？
date: 2021-12-03 21:50:00
draft: false
slug: b1757d4d

author: "Kenshin2438"
description: "算法竞赛中，用来避免行末空格的cout<<\"\\n \"[i < n];是什么语法支撑的？"
keywords:
  - 避免行末空格
  - postfix-expression
  - 后缀表达式
  - C++
categories:
  - 漫谈
tags:
  - Cpp

weight: false
math: true
comments: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

在算法竞赛中，很多赛题都需要输出一整个数组，但是由于评测姬的机制不同，某些OJ会卡行末空格，这样的体验是很痛苦的，如果不报PE那更是要命。

在众多避免行末空格的方法中，`cout << "\n "[i < n];`显得十分简洁，但是它究竟是什么语法允许的？之前一直想不通，今天突然想到了下标，测试了一下果真如此，同时也找到了具体的语法依赖。

## 先上结论：其实就是下标

详情见下图实例：

![实例](/images/postfix.png)

那么，当`[i < n]`为真，`"\n "[1]`为`' '`；
反之为`"\n "[0]`，即`'\n'`。

这样，在数组最后一个元素输出后，输出的就不是空格，而是换行。

## 具体过程

{{< admonition node "Water" false>}}
以前在大佬们（第一次好像是在**逆十字**的代码里看到的）的代码中总是看见这种避免行末空格的写法，但是并不知道这是什么语法（但是好用）。

开始以为是c++11开始的lambda表达式，但是我找文档啃了半天也找不到对应实例。然后今天终于开窍了。（误，其实答案早就找到了，倒是没太仔细求证给忽视了）
{{< /admonition >}}

在微软的文档中写的为`postfix表达式`，即**后缀**表达式。

它其实说明了一个问题，这个`"\n "`和一个普通的数组一样。也就是说，这个语句在编译器中就和`cout << s[i];`一样自然。

当然，如果你知道`"abcd"`的类型实际是`const char *`，后面下标运算符其实带来的结果就是对指针的加减，那么，这种写法已不构成理解问题。

---

## 其他发现

{{< admonition quote "下标运算符" true >}}
下标运算符是可交换的。 因此，只要下标运算符未重载，表达式 `array[index]` 和 `index[array]` 就是等效的。 第一种形式是最常见的编码做法，但它们都有效。
{{< /admonition >}}
事实上，下面的代码也能得到一致的结果。

```cpp
for (int i = 0; i < 4; i++) {
  cout << (i)["abcd"] << ' ';
}
```

## 参考链接

+ [Docs Microsoft C++、C 和 汇编程序 C++ 语言 C++ 语言参考 内置运算符、优先级和关联性 下标运算符：](https://docs.microsoft.com/zh-cn/cpp/cpp/subscript-operator?view=msvc-170)

摘录一下我们需要的依赖项：

{{< admonition quote "Docs Microsoft C++" true>}}
### 语法
```
postfix-expression [ expression ]
```
### 备注
...</br>
通常 ，postfix-expression 表示的值是指针值（如数组标识符）和 expression 是整数值 (包括枚举类型) 。 **但是，从语法上来说，只需要一个表达式是指针类型，另一个表达式是整型。** 因此，整数值可以位于postfix-expression位置，指针值可以位于表达式或下标位置的方括号中。
{{< /admonition >}}

+ c++中字符串字面值为`const char *`类型

虽然是基本事实，但是细想起来总感觉有问题。

当然，这些问题都很容易找到解答，下面为我查找的时候看到的关于`char *`和`const char *`的问题。

参阅：[Zhihu:字符串字面值传入函数时候是用什么形式？](https://www.zhihu.com/question/51180342)
