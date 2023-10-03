---
title: "平衡树 - 无旋Treap(FhqTreap) & AVL树"
date: 2023-09-29T15:29:23+08:00
draft: false
slug: 932240b5
author: "Kenshin2438"

summary: "数据结构敲一敲代码，算是FhqTreap的模板吧。关于时间复杂度，请参考Tarjan的关于Zip Tree的论文。"
description: "之前复习408数据结构还剩下平衡树部分，因为本人脑子不够用，看树上的旋转看得人有点麻……于是写了会儿无旋转的Treap，也就是著名的范浩强Treap。"
keywords: 
  - FhqTreap
  - 无旋Treap
  - AVL Tree
categories: 
  - Data Structure
tags: 
  - FhqTreap

weight: false
math: true
comments: true
ShowToc: true
TocOpen: true

cover:
  image: "" # image path/url
  alt: "" # alt text
  caption: "" # display caption under cover
  relative: false
---

## Misc

这里暂时（考完研就补上内容）仅给出一些链接。
+ [LOJ: #107. 维护全序集](https://loj.ac/p/106)
+ [Luogu: FHQ-Treap学习笔记](https://www.luogu.com.cn/blog/85514/fhq-treap-xue-xi-bi-ji)
+ [Tarjan - Zip Trees](https://arxiv.org/abs/1806.06726) Tarjan的论文，其中补充了许多关于并行优化的内容。
+ [Robert E.Tarjan lecture at the University of Latvia: Zip Trees](https://www.youtube.com/watch?v=NxRXhBur6Xs)

个人的理解就是，二叉搜索树的平衡性受到插入顺序的影响，FhqTreap使用随机**优先级**变相使得广义上的“插入顺序”也具有了随机性。

## Operations

+ `split(p, val, &lt, &rt)` 也可按照`size`分裂（本人在维护区间的时候使用）
  + 左子树`lt`所有值`<= val`；左子树`rt`所有值`> val`
+ `merge(&p, lt, rt)` 保持`heap`性质

虽然使用`split`和`merge`组合可以**比较方便地**实现如下的操作，但是为了保证效率应当减少它们的使用（毕竟对Treap进行了递归修改）。

---

1. `insert(val)` 插入
2. `remove(val)` 如若有多个，仅删除其中一个
3. `nth_element(n)` 第`n`小的元素，下标从1开始
4. `order_of_val(val)` 返回比`val`**小的数的个数（注意不是rank）**
5. `prev(val)` 小于`val`,且最大的数
6. `next(val)` 大于`val`,且最小的数

## Code

### FHQ Treap

代码量稍微大了一点点（但还是比 AVL Tree 和 Red-black Tree 少很多吧。。。）。

```cpp
std::mt19937 rng(std::random_device{}());

template <typename T>
class FhqTreap {
 private:
  struct TreapBase {
    int l = 0, r = 0, siz = 1;
    uint32_t prio = rng();
    T val;
    explicit TreapBase(const T& _val) : val{_val} {}
  };
  std::vector<TreapBase> data{TreapBase(2438)};
  int root = 0;
  constexpr inline auto newNode(const T& val) {
    auto idx = static_cast<int>(data.size());
    data.emplace_back(val);
    return idx;
  }

 private:
  auto size(const int& p) { return p == 0 ? 0 : data[p].siz; }
  auto pushUp(const int& p) {
    if (p == 0) return;
    data[p].siz = 1 + size(data[p].l) + size(data[p].r);
  }
  auto split(int p, int val, int& lt, int& rt) {
    if (p == 0) return lt = rt = 0, void();
    if (data[p].val <= val) {
      split(data[lt = p].r, val, data[p].r, rt);
    } else {
      split(data[rt = p].l, val, lt, data[p].l);
    }
    return pushUp(p);
  }
  auto merge(int& p, int lt, int rt) {
    if (lt == 0 or rt == 0) return p = lt | rt, void();
    if (data[lt].prio <= data[rt].prio) {
      merge(data[p = lt].r, data[lt].r, rt);
    } else {
      merge(data[p = rt].l, lt, data[rt].l);
    }
    return pushUp(p);
  }

 private:
  auto _insert(int& p, int q) {
    if (p == 0) return p = q, void();
    if (data[q].prio <= data[p].prio) {
      split(p, data[q].val, data[q].l, data[q].r);
      return pushUp(p = q);
    }
    if (data[q].val <= data[p].val) {
      _insert(data[p].l, q);
    } else {
      _insert(data[p].r, q);
    }
    return pushUp(p);
  }
  auto _remove(int& p, int val) {
    if (p == 0) return;
    if (data[p].val == val) return merge(p, data[p].l, data[p].r);
    if (val < data[p].val) {
      _remove(data[p].l, val);
    } else {
      _remove(data[p].r, val);
    }
    return pushUp(p);
  }
  auto _find_by_order(int k, int p) {
    if (size(p) < k) return -1;
    while (true) {
      if (size(data[p].l) >= k) {
        p = data[p].l;
      } else if (size(data[p].l) + 1 == k) {
        return data[p].val;
      } else {
        k -= size(data[p].l) + 1;
        p = data[p].r;
      }
    }
    assert(false);
  }

 public:
  FhqTreap() = default;
  auto insert(const T& val) { _insert(root, newNode(val)); }
  auto remove(const T& val) { _remove(root, val); }
  auto nth_element(const int& rank) { return _find_by_order(rank, root); }
  auto order_of_val(const int& val) {
    int p = root, rank = 0;
    while (p != 0) {
      if (val <= data[p].val) {
        p = data[p].l;
      } else {
        rank += size(data[p].l) + 1;
        p = data[p].r;
      }
    }
    return rank;
  }
  auto prev(const T& val) {
    int p = root, res = -1;
    while (p != 0) {
      if (val <= data[p].val) {
        p = data[p].l;
      } else {
        res = data[p].val;
        p = data[p].r;
      }
    }
    return res;
  }
  auto next(const T& val) {
    int p = root, res = -1;
    while (p != 0) {
      if (val >= data[p].val) {
        p = data[p].r;
      } else {
        res = data[p].val;
        p = data[p].l;
      }
    }
    return res;
  }
};
```

### AVL Tree

查询部分此处略去（仅使用到了Treap的二叉搜索树的性质，因此和上文中写的FhqTreap完全一致）

+ 旋转部分

```cpp
auto leftRotate(int& p) -> void {
  /** Left Rotate
   *     |                       |
   *     N                       S
   *    / \     l-rotate(N)     / \
   *   L   S    ==========>    N   R
   *      / \                 / \
   *     M   R               L   M
   */
  int successor = data[p].r;
  data[p].r = data[successor].l;
  pushUp(p);
  data[successor].l = p;
  pushUp(successor);
  p = successor;
}
auto rightRotate(int& p) -> void {
  /** Right Rotate
   *       |                   |
   *       N                   S
   *      / \   r-rotate(N)   / \
   *     S   R  ==========>  L   N
   *    / \                     / \
   *   L   M                   M   R
   */
  int predecessor = data[p].l;
  data[p].l = data[predecessor].r;
  pushUp(p);
  data[predecessor].r = p;
  pushUp(predecessor);
  p = predecessor;
}
auto maintain(int& p) -> void {
  if (p == 0) return;
  int Q = height(data[p].l) - height(data[p].r);
  if (Q == 2) {
    if (height(data[data[p].l].r) > height(data[data[p].l].l)) {
      /** Left-Right Case
       *     |                   |
       *     C                   C
       *    /   l-rotate(A)     /
       *   A    ==========>    B
       *    \                 /
       *     B               A
       */
      leftRotate(data[p].l);
    }
    /** Left-Left Case
     *       |
     *       C                 |
     *      /   r-rotate(C)    B
     *     B    ==========>   / \
     *    /                  A   C
     *   A
     */
    rightRotate(p);
  } else if (Q == -2) {
    if (height(data[data[p].r].l) > height(data[data[p].r].r)) {
      /** Right-Left Case
       *   |                 |
       *   A                 A
       *    \   r-rotate(C)   \
       *     C  ==========>    B
       *    /                   \
       *   B                     C
       */
      rightRotate(data[p].r);
    }
    /** Right-Right Case
     *   |
     *   A                     |
     *    \     l-rotate(A)    B
     *     B    ==========>   / \
     *      \                A   C
     *       C
     */
    leftRotate(p);
  }
  pushUp(p);
}
```

+ 插入和删除

```cpp
auto _insert(int& p, const int& q) -> void {
  if (p == 0) return p = q, void();
  if (data[q].val <= data[p].val) {
    _insert(data[p].l, q);
  } else {
    _insert(data[p].r, q);
  }
  return maintain(p);
}
auto _remove_successor(int& p) -> T {
  int res = -1;
  if (data[p].l == 0) {
    res = data[p].val;
    p = data[p].r;
  } else {
    res = _remove_successor(data[p].l);
    maintain(p);
  }
  return res;
}
auto _remove(int& p, const T& val) -> void {
  if (p == 0) return;
  if (data[p].val == val) {
    if (data[p].l == 0 or data[p].r == 0) {
      return p = data[p].l | data[p].r, void();
    }
    data[p].val = _remove_successor(data[p].r);
    return maintain(p);
  }
  if (val < data[p].val) {
    _remove(data[p].l, val);
  } else {
    _remove(data[p].r, val);
  }
  return maintain(p);
}
```