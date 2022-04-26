---
title: "Cpp Tricks - 语言向进阶（？）指南"
date: 2022-04-17T18:57:19+08:00
draft: false
slug: 84f84658

author: "Kenshin2438"
description: "记录一些常用的C++代码技巧（竞赛向），可能会用到比较高的C++版本。"
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
update at 2022-04-25 内容未完，之后写代码过程中见到或者想到的好的技巧都会逐步添加。

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
#define PII pair<int, int>
#define vec vector
#define str string
#define fi first
#define se second
#define all(a) (a).begin(), (a).end()
#define SZ(x) static_cast<int>((x).size())

using db = double;
using ll = long long;
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
可以见，这中写法并非**变量声明**，而是**赋值**。
{{< /admonition >}}

## 迭代器 与 `all()`宏

```cpp
#define all(a) (a).begin(), (a).end()
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

#### `lambda` 表达式 (`c++11`)

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
vec G(V, vec<int>());
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
vec<int> a{ 0, 1, 2, 2, 2, 3, 4 };

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
vec<int> a = {4, 5, 3, 1, 6, 2};
int k = 2;
nth_element(a.begin(), next(a.begin(), k), a.end());
for (int x : a) cout << x << ' ';

// 输出：2 1 3 4 5 6
```

可以见，该函数并非排序，而是将前`K`小的数放在最前面的`K`个位置，且令第`K`位上为第`K`大。

如果仅仅需要一般的查找，使用`find`或者`find_if`即可，后者搭配`lambda`表达式，可以按需搜索。使用时请注意复杂度，对于一般容器，该函数使用的是顺序遍历，时间复杂度为$\mathcal{O}(n)$。

**此处补充一点，查找元素无果，返回的迭代器为`end()`。特别的，`string`中`find`失败得到的是`string::npos`。**

### 计算相关

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
  vec<str_node> a{ str_node{"abc"},
                   str_node{"123"},
                   str_node{"def"},
                   str_node{"456"},
                   str_node{"!@#"}
                  };
  str_node sum = accumulate(1 + all(a), a[0]);
  cout << sum.s << endl;
}

// 输出：abc + 123 + def + 456 + !@#
```

+ `count` 和 `count_if`

统计元素个数时可用前者 `count(all(a), val)` ，如果需要按满足条件来统计，使用后者再搭配上`lambda`表达式即可。

**值得说明的一点是，`map`和`set`中的`find`和`count`函数的复杂度是$\mathcal{O}(\log n)$，可以放心使用。**

+ `all_of` `any_of` `none_of`

顾名思义。

## 杂项 与 写法上的技巧

+ `iota(all(a), val)`

从`val`开始递增地赋值，赋值后地数组为 `{ val, val + 1, ... }`。

+ `auto [min_val, max_val] = minmax(a, b)` 

同时获得两数的最大值和最小值，~~啥用没用~~ 实际使用很少。

+ `rotate` 旋转，放在圆（环）上理解可能会好点。

```cpp
template< class ForwardIt >
void rotate( ForwardIt first, ForwardIt n_first, ForwardIt last );

rotate(a.begin(), next(a.begin(), 2), a.end()); 
// a.begin() + 2, a.end() 和 a.begin(), a.begin() + 2 整体交换位置
```

+ 求数组中不同元素的个数 

```cpp
int num = SZ(set<int>(all(a)));
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