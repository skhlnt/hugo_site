---
title: "Cpp Tricks - 语言向进阶（？）指南"
date: 2022-04-17T18:57:19+08:00
draft: false
slug: 84f84658

author: "Kenshin2438"
description: "记录一些常用的C++代码技巧（竞赛向），可能会用到比较高的C++版本。"
summary: "记录一些常用的C++代码技巧（竞赛向），可能会用到比较高的C++版本。"
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

{{< admonition info "Info" true >}}
+ update at 2022-08-27 '重写了部分代码实例，以及补充了部分内容'
+ update at 2022-04-25 '关于auto和bool的一个问题'
+ update at 2022-05-21 'accumulate返回值类型的细节'
+ update at 2022-05-23 '增加了bit部分的内容'

内容未完，之后写代码过程中见到或者想到的好的技巧都会逐步添加。

---

**使用的编译指令：**
```bash
"g++" -std=c++17 -Wall -Ofast -DLOCAL "ac.cpp" -o "ac.exe" 
```

**`g++` 版本：**
```bash
@Kenshin2438 ➜  ~  g++ -v
...
gcc version 11.2.0 (GCC)
```

**尽量只使用宏：**
```cpp
using ll = long long;
#define all(a) begin(a), end(a)
#define sz(x) (int)((x).size())
```

**参考**
+ [cppreference 中文参考手册](https://zh.cppreference.com/w/cpp)
{{< /admonition >}}

---

## 常见容器

+ `string`
+ `array` - `vector` - `deque`
+ `map` - `multimap` - `unordered_map`
+ `set` - `multiset` - `unordered_set`
+ `stack` - `queue` - `prority_queue`
+ `tuple`
+ `bitset`

支持顺序访问的容器可以用下面的办法快速枚举：

```cpp
for (auto value : container) {
  // value 为容器中的元素
  // auto  为c++11加入的，可以自动推断元素类型
}
```

对于结构体，一定程度上可以使用`tuple`代替。

{{< admonition warning "c++17 开始支持" true >}}
两者在访问时都可以使用`auto`对其**结构化绑定声明**，语法大概如下：

```cpp
tuple<type_1, type_2, ....> container;
// 或者 struct，按照定义变量的顺序来即可
auto [value_1, value_2, ...] : container;
```
上面两种可以协同使用，遍历结构体`vector<tuple<...>>`

但是，如果仅仅是需要**结构化绑定**，可以使用`tie()`:

```cpp
tuple<int, int> container;
int a, b;

tie(a, b) = container;
```
可以见，这种写法并非**变量声明**，而是**赋值**。
{{< /admonition >}}

### 关于`Range-based for loop`的一些问题

+ 使用`for (auto val : v)`确实会发生拷贝，但并不是说`v`中元素就**一定不会改变**

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  int n = 5;
  vector<bool> v(n, true);
  for (auto val : v) val = false;
  for (int i = 0; i < n; i++) {
    cout << (v[i] ? "true" : "false");
    cout << " \n"[i + 1 == n];
  }
  return 0;
}

/** output: 
false false false false false
**/
```

不过，会出现上面情况的应该也就是`vector<bool>`这个奇葩了。显然`auto`判断类型为`_Bit_reference`，通过下面代码可以验证：

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  cout << boolalpha;
  vector<bool> v = {false};
  for (auto val : v) {
    cout << is_same<_Bit_reference, decltype(val)>::value << '\n';
  }
  return 0;
}

/** output: 
true
**/
```

同时，如果你使用了`auto &val : v`，那么你将面临下面的报错：

![compile error](/images/compile_error_Sample.png)

---

+ 如果想用`auto`自动识别变量类型的引用，但又不想出错，你应当使用`auto &&val : v`来代替。
+ 使用`const auto &val : v`来彻底避免内存拷贝以及保证元素不被修改。

## 迭代器 与 `all()`宏

```cpp
#define all(a) begin(a), end(a)
```

在`c++`的STL中，更常用的是迭代器，而非下标（指针），这与纯`c`写法有较大区别。

`begin()`，`end()` 作为容器的起始迭代器和末尾的迭代器

`rbegin()`，`rend()` 逆向的迭代器

用于遍历的函数如下（虽然有许多容器的迭代器重载了`++`和`--`，可以直接像下标一样处理，但还是推荐）：

```cpp
prev(iterator) // 上一个迭代器
next(iterator) // 下一个迭代器
```

定义这个宏的原因是：使用算法库的函数经常需要填写迭代器范围。

下面将介绍一些比较常见的函数（如果平时码风比较偏`c`语言，可能就不太常见）

## 算法库

[cpp手册 - 算法库](https://zh.cppreference.com/w/cpp/algorithm)

此处仅记录一些**本人**常用的部分，`<algorithm>`内容十分丰富，并且还在随版本更新，惟愿本文能抛砖引玉，引起读者的兴趣。

---

### 排序 `std::sort` 与 `lambda`表达式

`std::sort()`，应该是一个很常见的函数，用来排序数组的时，一些偏向`c`的写法会使用头尾指针来确定范围，再写外部函数确定排序规则。

但是，在使用如`vector`等可以排序的容器时，我们一般会动态开空间，所以此时待排序的范围就是全部元素。

```cpp
vector<int> a(n);
sort(all(a)); // 对全部元素排序
sort(1 + all(a)); // 对下标从 1 开始的部分排序

sort(all(a), less<int>()); // 升序 （默认）
sort(all(a), greater<int>()); // 降序
```

与`std::sort`比较相似的还有`std::stable_sort`，后者是能够保证，相同大小的元素在排序前后的相对位置不变。

+ 检验数组是否有序：`std::is_sorted()`

### 关于 `lambda` 表达式 (`c++11`)

在`sort`函数中，第三个参数可以为我们定义的排序规则，如果不使用`lambda`表达式，我们往往会把它们写在外面，然后填写函数指针。

{{< admonition tip "Tip" true >}}
关于`lambda`表达式，受篇幅限制这里无法展开，建议访问[cpp手册 - lambda表达式](https://en.cppreference.com/w/cpp/language/lambda)。
{{< /admonition >}}

基础语法如下：
```cpp
[ captures ] ( params ) specs requires(optional) { body }

[ 获取的变量 &表示引用，=表示传值 可以写多个变量，但一般缺省，只写& ]
( 在表达式中定义的变量 )
specs requires(optional) 一般缺省，或者写成 -> 返回值类型，如 -> int
{ 具体表达式 函数体 }
```

放在`sort`中使用的实例：
```cpp
struct Node {
  int a, b;
  Node(int _a = 0, int _b = 0)
    : a(_a), b(_b) {}
};

...

sort(all(v), [&](const Node &p, const Node &q) {
  return p.a * q.b <= q.a * p.b;
});
```

更多的，如果关联使用`<functional>`，可以将外部函数写在主函数内。

+ **这里还有一个问题，那就是如何写递归函数？**

使用 `function` 类是一种解决办法，如下面的`dfs`代码：

```cpp
int V = 100;
vector G(V, vector<int>(V));

function<void (int, int)> dfs = [&](int u, int fa) {
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs(v, u);
  }
};
dfs(source, -1); // 使用方式
```

如果不按照`function`类来声明该函数，`[ captures ]`无法获知自己的存在，所以一个可行的方案就是，在传值的时候将**自己**传入。

```cpp
auto dfs = [&](auto self, int u, int fa) {
  for (auto v : G[u]) {
    if (v == fa) continue;
    self(self, v, u);
  }
};
dfs(dfs, source, -1); // 注意调用时需要将 自己 传入
```

### 搜索相关

我们知道，对于有序容器，我们可以利用其单调性来进行二分。

进行了上面的排序操作，我们的数组（暂且这么称呼）已经变得有序，如何利用`STL`中写好的二分函数呢？

对于一般容器而言，二分函数的写法比较统一（以`vector<int> a`为例好了）：

```cpp
vector<int> a { 0, 1, 2, 2, 2, 3, 4 };

// 第一个大于等于 value 的位置（迭代器）
auto it = lower_bound(all(a), value); 

// 第一个大于 value 的位置（迭代器）
auto it = upper_bound(all(a), value); 

// 同时获得上述两者 返回为 std::pair<ForwardIt, ForwardIt>
auto P = equal_range(all(a), 2);
```

{{< admonition warning "特殊容器" true >}}
对于`map`，`set`，这类使用**红黑树**或者其他非线性数据结构实现的容器，如果你直接按照上面的写法二分，那么时间复杂度将直接退化到$\mathcal{O}(n)$。

正确的使用方法是直接调用其内部封装好的二分函数：
```cpp
set<int> S;
auto it = S.lower_bound(value);
```
{{< /admonition >}}

更一般的情况是，我们只需要数组中最值。

```cpp
auto it_min = min_element(all(v)); // 最小元素对应的迭代器（可以理解为下标）
auto it_max = max_element(all(v)); // 最大元素

cout << *it_min; // 用于输出
```

**如果你需要知道是一个数组的第`K`大的数（比如中位数），该怎么办呢，直接排序吗？**

在某些时候，我们可能连$\mathcal{O}(n\log n)$的算法也无法接受，此时可以使用均摊复杂度为$\mathcal{O}(n)$的函数`nth_element()`

```cpp
vector<int> a {4, 5, 3, 1, 6, 2};
int k = 2;
nth_element(a.begin(), next(a.begin(), k), a.end());
for (int x : a) cout << x << ' ';

// 输出：2 1 3 4 5 6
```

可以见，该函数并非排序，而是将前`K`小的数放在最前面的`K`个位置，且令第`K`位上为第`K`大。

如果仅仅需要一般的查找，使用`find`或者`find_if`即可，后者搭配`lambda`表达式，可以按需搜索。使用时请注意复杂度，对于一般容器，该函数使用的是顺序遍历，时间复杂度为$\mathcal{O}(n)$。

**此处补充一点，查找元素无果，返回的迭代器为`end()`。特别的，`string`中`find`失败得到的是`string::npos`。**

### 计算相关

+ `count` 和 `count_if`

统计元素个数时可用前者 `count(all(a), val)` ，如果需要按满足条件来统计，使用后者再搭配上`lambda`表达式即可。

**值得说明的一点是，`map`和`set`中的`find`和`count`函数的复杂度是$\mathcal{O}(\log n)$，可以放心使用。**

+ `all_of` `any_of` `none_of`

顾名思义，对于一个范围，判断满足条件（一般用`lambda`表达式写）的集合与全集的关系。

+ `partial_sum`

前缀和函数，`partial_sum(all(a), begin(b))`，**此处的 `b` 需要先开够空间。**

类似的还有**前向差分**函数。

+ `accumulate`

比较常见的要求是对数组求和，我们直接利用`accumulate(all(a), 0)`即可，但是该函数还有许多值得探究的部分（[参考链接](https://en.cppreference.com/w/cpp/algorithm/accumulate)）。

其参数中，**求和**并非恒定不变，使用`lambda`表达式或者重载符号`+`也能够对其修改。

```cpp
struct str_node {
  str s; // define str string
  str_node operator +(const str_node &oth) const {
    return str_node{this->s + " + " + oth.s};
  }
};

void example() {
  vector<str_node> a{ 
                      str_node{"abc"},
                      str_node{"123"},
                      str_node{"def"},
                      str_node{"456"},
                      str_node{"!@#"}
                   };
  str_node sum = accumulate(1 + all(a), a.front());
  cout << sum.s << endl;
}

// 输出：abc + 123 + def + 456 + !@#
```

### 使用 `accumulate` 值得注意的问题

先来阅读两份源码：

{{< admonition quote "accumulate - cppreference.com" true >}}
**First version**
```cpp 
template<class InputIt, class T>
constexpr // since C++20
T accumulate(InputIt first, InputIt last, T init)
{
    for (; first != last; ++first) {
        init = std::move(init) + *first; // std::move since C++20
    }
    return init;
}
```
**Second version**
```cpp 
template<class InputIt, class T, class BinaryOperation>
constexpr // since C++20
T accumulate(InputIt first, InputIt last, T init, 
             BinaryOperation op)
{
    for (; first != last; ++first) {
        init = op(std::move(init), *first); // std::move since C++20
    }
    return init;
}
```
{{< /admonition >}}

可以发现，无论是哪一种，`accumulate`的返回值类型都**不是由数组元素的类型来决定**。

所以，一个常犯的错误就是（此处 ~~点名批评~~ 感谢[pbrgg](https://rivego.cn/)提供的素材）

```cpp
vector<long long> v;
...
long long sum = accumulate(all(v), 0);

// 正确的写法如下：
// long long sum = accumulate(all(v), 0LL);
// 或者
// long long sum = accumulate(1 + all(v), v.front());
```

问题何在呢？相信读者应该马上就能反应出来，**由于`0`的类型为`int`在求和的过程种结果已经溢出。**

---

## Bit相关

这部分主要和`c++20`标准库头文件`<bit>`相关，但是考虑到现在许多的编译器还未能完全支持`c++20`，因此在后面加入了一部分来自`GCC Built-in Functions`的位操作函数。

### `c++20 <bit>`常用的函数

+ `has_single_bit` 检查一个数是否为二的整数次幂
+ `bit_ceil` 寻找不小于给定值的最小的二的整数次幂
+ `bit_floor` 寻找不大于给定值的最大的二的整数次幂
+ `countl_zero` 从最高位起计量连续的 `0` 位的数量
+ `countl_one` 从最高位起计量连续的 `1` 位的数量
+ `countr_zero` 从最低位起计量连续的 `0` 位的数量
+ `countr_one` 从最低位起计量连续的 `1` 位的数量
+ `popcount` 计量无符号整数中为 `1` 的位的数量

### `bitset` 容器

补充一个不怎么常用的容器，`bitset`本质上就是一个`01`序列。

**其占用内存很小并且也重载了位操作（`&`, `|`, `>>`, `<<`等）因此有时也用于卡常数。**

常用的操作大致如下（以`bitset<N> b;`为例）：
```cpp
b.all();
b.any();
b.none();
// 检查是否所有、任一或无位被设为 true

b.count();  // 返回设置为true的位的数量
b.set();    // 将位置为 true
b.reset();  // 将位置为 false
b.flip();   // 翻转位的值

b.to_ullong();
// 转换 bitset 的内容为 unsigned long long 整数
// bitset 的首位对应数的最低位，而尾位对应最高位
// 若值不能以 unsigned long long 表示，则为 std::overflow_error
```

### 来自`GCC Built-in Functions`的位操作函数

官方的介绍 <https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html>

```cpp
__builtin_clz()        // count leading  0s   前面0的数目
__builtin_ctz()        // count trailing 0s   后面0的数目
__builtin_popcount()   // count bit 1         比特位为1的数目

/**
(16)10 = (00000000 00000000 00000000 00010000)2
__builtin_clz      : 27
__builtin_ctz      :  4
__builtin_popcount :  1

对于 long 类型的在函数名后面加 'l'
对于 long long 类型的在后面加 'll' 如 __builtin_popcountll
*/
```

既然写到了gcc的内建函数，不妨也提一下其它的双下划线函数：

+ `__gcd()`，顾名思义，一个用于求两数最大公因数的函数。

值得注意的是，在`c++17`中，已经加入了`gcd()`函数，可以不加下划线使用。

+ `__builtin_ia32_rdtsc()`

`rdtsc`的原文大概是`Read Time Stamp Counter`，这个函数原本是用于测量cpu时钟的，用于竞赛大概只能生成随机数种子。所以为什么在这提呢？主要是由于我的随机数生成代码中包含这一个函数。

```cpp
#include <random>

std::mt19937 rng(__builtin_ia32_rdtsc());
template<typename T> inline T randint(T l, T r) {
  return std::uniform_int_distribution<T>(l, r)(rng);
}
template<typename E> inline E randreal(E l, E r) {
  return std::uniform_real_distribution<E>(l, r)(rng);
}
```

### 位运算的其它操作

+ `^` 异或

对于二值集合`{a, b}`，**如何找到不同与x的另一个数呢？**，直接`if-else`判断当然可以，但没必要。最快的写法利用**相同数的异或为`0`，同时任何数与`0`异或都等于它本身**这两个所有人熟知的性质，写成`x ^ a ^ b`就可以了。

+ 二进制枚举

主要是在`dfs`由数组确定的集合时用到，当然直接写`dfs`也是可行的，甚至更快。（但，私以为二进制枚举最优雅）

+ 取模$2^k$

等价为 `&` 上 $2^k-1$。用法大概是，最后 `&` 一下就行（大概。

**注意，$2^{32}-1$需要`int64_t`。此时用`uint32_t`自然可以，但是会比`int32_t`慢。**

---

## 杂项 与 写法上的技巧

+ `iota(all(a), val)`

从`val`开始递增地赋值，赋值后地数组为 `{ val, val + 1, ... }`。

十分适合用来写**并查集**的初始化（当然，还有不同的写法是初始化成-1）。

+ `auto [min_val, max_val] = minmax(a, b)` 

同时获得两数的最大值和最小值，~~啥用没用~~ 实际使用很少。

**低版本建议的写法是 `tie(min_val, max_val) = minmax(a, b)` ，需要先声明变量。**

{{< admonition danger "注意！！" true >}}
`tie(a, b) = minmax(a, b)` 为**错误写法！**

1. 函数 `minmax()` 的返回值类型为 `pair<const T &, const T &>`。

2. 函数 `tie(Types&... args)` 会**依次赋值**。

那么，如果 $a>b$，则会出现如下的情况：
```
tie(a, b) = minmax(a, b)

   a = (const T&) b
   b = (const T&) a // 此时，由于此处为 a 的引用，所以值已经改变
```

最后所有的数都变成原先的最小值！
{{< /admonition >}}

+ `rotate` 旋转，放在圆（环）上理解可能会好点。

```cpp
template< class ForwardIt >
void rotate( ForwardIt first, ForwardIt n_first, ForwardIt last );

rotate(a.begin(), next(a.begin(), 2), a.end()); 
// a.begin() + 2, a.end() 和 a.begin(), a.begin() + 2 整体交换位置
```

+ 求数组中不同元素的个数 

```cpp
int num = sz(set<int>(all(a)));
```

+ `next_permutation` 和 `prev_permutation`

枚举数组的所有排列，常见的写法是：

```cpp
sort(all(p));
do {
  // ... 
} while (next_permutation(all(p)));
```

+ `substr`

`string`中的`STL`用得比较少，一般使用的就是`substr`获取子串。

```cpp
s.substr(start，length); // length 参数缺省时表示后续直到 end()
```

+ `cout << " \n"[i == n];`

避免行末空格，原理见[我的另一篇博客](../b1757d4d.html/)。

## `std::vector` 内存回收问题

[CF1706D2](https://codeforces.com/problemset/problem/1706/D2)

对于`std::vector`而言，`pop_back()`，`clear()`，`resize()`都不会**立即**回收已经使用过的内存（程序做的应该只是**迭代器的移动**操作，具体细节本人未作研究，建议读者自行查阅`STL`的相关源代码）。这大抵是为了方便后续的写入，省去再次分配空间的消耗。要做到立马回收空间，行之有效的方式是，利用`std::swap()`的机制，将使用的内存交换走。

```cpp
vector<T>().swap(v);
```