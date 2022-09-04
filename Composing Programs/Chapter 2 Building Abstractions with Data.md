# Chapter 2 Building Abstractions with Data

# 构造数据抽象

> **数据抽象**： 构造出一些使用复合数据对象的程序，使他们就像在抽象数据上操作一样。程序分为两个部分，选择函数和构造函数，除了完成当前工作所必要的东西之外。不对所用数据作任何多余假设，具体数据表示的定义也应该与程序中使用数据的方式无关。

基本思想： 为每一类数据对象标识出一组操作(构造函数和选择函数)，使得对这类数据对象的所有操作都可以基于它们表述，而且在操作这些数据对象时也只使用它们。

# 2.1 Lists ans Strings

## Sequence unpacking in For Statement

```py
pairs = [[1, 2], [2, 2], [3, 5], [4, 4]]
count = 0
for x, y in pairs:
    if x == y:
        count += 1
print(count)
```

## The Range Type

> A range is a sequence of consecutive integers.

```py
list(range(-2, 2))
# [-2, -1, 0, 1]
```

## List Comprehensions

```py
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# A new list
[letters[i] for i in [1, 3, 5]]
# ['b', 'd', 'f']

odds = [1, 3, 5, 7, 9]
[x+1 for x in odds]
# [2, 4, 6, 8, 10]
[x for x in odds if 25 % x == 0]
# [1, 5]
[x + 1 for x in odds if 25 % x == 0]
# [2, 6]
```

```py
def division(n):
    return [1] + [x for x in range(2, n) if n % x == 0]

```

# 2.2 Data Abstraction

The basic idea of data abstraction is to structure programs so that they operate on abstract data. That is, our programs should use data in such a way as to make as few assumptions about the data as possible. At the same time, a concrete data representation is defined as an independent part of the program.

These two parts of a program, the part that operates on abstract data and the part that defines a concrete representation, are connected by a small set of functions that implement abstract data in terms of the concrete representation. To illustrate this technique, we will consider how to design a set of functions for manipulating rational numbers.

## Rational numbers

A rational number is a ratio of integers, and rational numbers constitute an important sub-class of real numbers. A rational number such as 1/3 or 17/29 is typically written as:

`<numerator>/<denominator>`

However, we can create an exact representation for rational numbers by combining together the numerator and denominator.

- `rational(n, d)` returns the rational number with numerator `n` and denominator `d`.
- `numer(x)` returns the numerator of the rational number `x`.
- `denom(x)` returns the denominator of the rational number `x`.

**We are using here a powerful strategy for designing programs: wishful thinking. We haven't yet said how a rational number is represented, or how the functions numer, denom, and rational should be implemented.**

Even so, if we did define these three functions, we could then add, multiply, print, and test equality of rational numbers:

```py
def add_rationals(x, y):
    nx, dx = numer(x), denom(x)
    ny, dy = numer(y), denom(y)
    return rational(nx * dy + ny * dx, dx * dy)

def mul_rationals(x, y):
    nx, dx = numer(x), denom(x)
    ny, dy = numer(y), denom(y)
    return rational(nx * ny, dx * dy)

def equal_rationals(x, y):
    nx, dx = numer(x), denom(x)
    ny, dy = numer(y), denom(y)
    return nx * dy == ny * dx

def print_rational(x):
    print(numer(x), '/', denom(x))
```

We can use `pairs`.

```py
# 构造函数
def rational(n, d):
    return [n, d]

# 选择函数
def numer(x):
    return x[0]

# 选择函数
def denom(x):
    return x[1]
```

We can remedy this flaw by changing the implementation of `rational`.

```py
from fractions import gcd
def rational(n, d):
    g = gcd(n, d)
    return [n//g, d//g]
```

## Abstraction Barriers

我们构建了一层层抽象屏障(Abstraction Barriers)，这样的思想的好处就是使程序很容易维护和修改。之后数据表示的方式改变了，我们程序的其他部分并不需要修改。

![Snipaste_2022-08-31_22-17-13.png](https://media.haochen.me/Snipaste_2022-08-31_22-17-13.png)

In each layer above, the functions in the final column enforce an abstraction barrier. These functions are called by a higher level and implemented using a lower level of abstraction.

An abstraction barrier violation occurs whenever a part of the program that can use a higher level function instead uses a function in a lower level. For example, a function that computes the square of a rational number is best implemented in terms of `mul_rational`, which does not assume anything about the implementation of a rational number.

```py
def square_rational(x):
    return mul_rational(x, x)
```

Referring directly to numerators and denominators would violate one abstraction barrier.

```py
def square_rational_violating_once(x):
        return rational(numer(x) * numer(x), denom(x) * denom(x))
```

Assuming that rationals are represented as two-element lists would violate two abstraction barriers.

```py
def square_rational_violating_twice(x):
        return [x[0] * x[0], x[1] * x[1]]
```

Abstraction barriers make programs easier to maintain and to modify. The fewer functions that depend on a particular representation, the fewer changes are required when one wants to change that representation.

## Rational Data Abstraction Implemented as Functions

```py
def rational(n, d):
    def selector(x):
        if x == 'n':
            return n
        elif x == 'd':
            return d
    return selector

def numer(f):
    return f('n')

def denom(f):
    return f('d')
```

Abstraction barriers shape the way in which we think about data. A valid representation of a rational number is not restricted to any particular implementation (such as a two-element list); it is a value returned by rational that can be passed to `numer`, and `denom`. In addition, the appropriate relationship must hold among the constructor and selectors. That is, if we construct a rational number `x` from integers `n` and `d`, then it should be the case that `numer(x)/denom(x)` is equal to `n/d`.

In general, we can express abstract data using a collection of selectors and constructors, together with some behavior conditions. As long as the behavior conditions are met (such as the division property above), the selectors and constructors constitute a valid representation of a kind of data. The implementation details below an abstraction barrier may change, but if the behavior does not, then the data abstraction remains valid, and any program written using this data abstraction will remain correct.

This point of view can be applied broadly, including to the pair values that we used to implement rational numbers. We never actually said much about what a pair was, only that the language supplied the means to create and manipulate lists with two elements. The behavior we require to implement a pair is that it glues two values together. Stated as a behavior condition:

- If a pair `p` was constructed from values `x` and `y`, then `select(p, 0)` returns `x`, and `select(p, 1)` returns `y`.

We don't actually need the `list` type to create `pairs`. Instead, we can implement two functions `pair` and `select` that fulfill this description just as well as a two-element list.

```py
def pair(x, y):
    """Return a function that represents a pair."""
    def get(index):
        if index == 0:
            return x
        elif index == 1:
            return y
    return get

def select(p, i):
    """Return the element at index i of pair p."""
    return p(i)
```

With this implementation, we can create and manipulate pairs.

```py
>>> p = pair(20, 14)
>>> select(p, 0)
20
>>> select(p, 1)
14
```

# 2.3 Sequences

## 1. Lists

Lists can be added together and multiplied by integers.

```py
list = [1, 2, 3, 4]
>>> [7, 8] + list * 2
[7, 8, 1, 2, 3, 4, 1, 2, 3, 4]
```

## 2. Higher-order Function

The common patterns we have observed in sequence processing can be expressed using higher-order functions. First, evaluating an expression for each element in a sequence can be expressed by applying a function to each element.

```py
def map_all(map_fn, s):
    return [map_fn(x) for x in s]

def filter_all(filter_fn, s):
    return [x for x in s if filter_fn(x)]

def reduce(reduce_fn, s, initial):
    reduced = initial
    for x in s:
        reduced = reduce_fn(reduced, x)
    return reduced
>>> reduce(mul, [1, 2, 3], 1)
6

def divisors_of(n):
    return filter_all(lambda x: n % x == 0, range(2, n))
```

## 3. Sequence Abstraction

## Slicing Notation

> In Python, sequence slicing is expressed similarly to element selection, using square brackets. A colon separates the starting and ending indices. Any bound that is omitted is assumed to be an extreme value: 0 for the starting index, and the length of the sequence for the ending index.

```py
a[start:stop:step] # start through not past stop, by step
```

- a[start:stop] # items start through stop-1
- a[start:] # items start through the rest of the array
- a[:stop] # items from the beginning through stop-1
- a[:] # a copy of the whole array

- a[-1] # last item in the array
- a[-2:] # last two items in the array
- a[:-2] # everything except the last two items

- a[::-1] # all items in the array, reversed
- a[1::-1] # the first two items, reversed
- a[:-3:-1] # the last two items, reversed
- a[-3::-1] # everything except the last two items, reversed

## Write function1

Write a function that takes a list s and returns a new list that keeps only the even-indexed elements of s and multiplies them by their corresponding index.

```py
def even_weighted(list):
    return [i * list[i] for i in range(len(list)) if i % 2 == 0]

```

## Write function2

Write a function that takes in a list and returns the maximum product that can be formed using nonconsecutive elements of the list. The input list will contain only numbers greater than or equal to 1.

```py
def max_product(s):
    """Return the maximum product that can be formed using non-consecutive
    elements of s.
    >>> max_product([10,3,1,9,2]) # 10 * 9
    90
    >>> max_product([5,10,5,10,5]) # 5 * 5 * 5
    125
    >>> max_product([])
    1
    """
    if len(s) == 0:
        return 1
    elif len(s) == 1:
        return s[0]
    return max(max_product(s[1:]), s[0] * max_product(s[2:]))
```

## Write function3

A hole number is a number in which every other digit dips below the digits immediately adjacent to it. For example, the number 968 would be considered a hole number because the number 6 is smaller than both of its surrounding digits. Other hole numbers include 9192959 or 324364989. The number 544 would not be considered a hole number. For simplicity assume that we only pass in numbers that have an odd number of digits. Define the following function so that it properly identifies hole numbers

```py
def check_hole_number(n):
    if n // 10 == 0:
        return True
    return check_hole_number(n // 100) and (n // 10 % 10 < n % 10) and (n // 10 % 10 < n // 100 % 10)
```

## Write function4

Define the following function so that it properly identifies mountain numbers. A mountain number is a
number that either

1. has digits that strictly decrease from right to left OR strictly increase from right to left
2. has digits that increase from right to left up to some point in the middle of the number (not necessarily the exact middle digit). After reaching the maximum digit, the digits to the left of the maximum digit should strictly decrease.

```py
def check_mountain_number(n):
    """
    >>> check_mountain_number(103)
    False
    >>> check_mountain_number(153)
    True
    >>> check_mountain_number(123456)
    True
    >>> check_mountain_number(2345986)
    True
    """
    def helper(x, is_full_mountain):
        if x // 10 == 0:
            return True
        if is_full_mountain and x % 10 < x // 10 % 10:
            return helper(x // 10, is_full_mountain)
        return x % 10 > x // 10 % 10 and helper(x // 10, False)
    return helper(n, True)
```

# 2.4 Trees

Our ability to use lists as the elements of other lists provides a new means of combination in our programming language. This ability is called a `closure` property of a data type.

Nesting lists within lists can introduce complexity. The tree is a fundamental data abstraction that imposes regularity on how hierarchical values are structured and manipulated.

- `root`: the node at the top of the tree
- `label`: the value in a node, selected by the label function
- `branches`: a list of trees directly under the tree's root, selected by the branches function
- `leaf`: a tree with zero branches
- `node`: any location within the tree (e.g., root node, leaf nodes, etc.)

The data abstraction for a tree consists of the `constructor` tree and the `selectors` label and branches. We begin with a simplified version.

```py
def tree(root_label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
        return [root_label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)
```

Trees can be constructed by nested expressions. The following tree t has root label 3 and two branches.

```py
>>> t = tree(3, [tree(1), tree(2, [tree(1), tree(1)])])
>>> t
[3, [1], [2, [1], [1]]]
>>> label(t)
3
>>> branches(t)
[[1], [2, [1], [1]]]
>>> label(branches(t)[1])
2
>>> is_leaf(t)
False
>>> is_leaf(branches(t)[0])
True
```

## Example1: fib_tree

```py
def fib_tree(n):
    if n <= 1:
        return tree(n)
    left, right = fib_tree(n - 2), fib_tree(n - 1)
    fib_n = label(left) + label(right)
    return fib_tree(fib_n, [left, right])

>>> fib_tree(5)
[5, [2, [1], [1, [0], [1]]], [3, [1, [0], [1]], [2, [1], [1, [0], [1]]]]]
```

## Example2: count_leaves

```py
def count_leaves(tree):
    if is_leaf(tree):
        return 1
    else:
        return sum([count_leaves(b) for b in branches(tree)])
```

## Example3: leaves

Implement `leaves`, which returns a list of the leaf labels of a tree.

Hint: If you **sum** a list of lists, you get a list containing the elements of those lists.

```py
>>> sum([[1], [2, 3], [4]], [])
[1, 2, 3, 4]
>>> sum([[1]], [])
[1]
>>> sum([[[1]], [2]], [])
[[1], 2]
```

```py
def leaves(tree):
    """Return a list containing the leaf labels of tree
    >>> leaves(fib_tree(5))
    [1, 0, 1, 0, 1, 1, 0, 1]
    """
    if is_leaf(fib_tree(5)):
        return [label(tree)]
    else:
        return sum(leaves(b) for b in branches(tree),[])
```

## Example4: Creating leaves

```py
def increment_leaves(t):
    """Return a tree like t but leaf labels incremented."""
    if is_leaf(t):
        return tree(label(t) + 1)
    else:
        bs = [increment_leaves(b) for b in branches(t)]
        return tree(label(t), bs)
```

## Example5: increment

```py
def increment(t):
    """Return a tree like t but with all labels incremented."""
    return tree(label(t) + 1, [increment(b) for b in branches(t)])
```

## Example6: print_tree

```py
def print_tree(t, indent=0):
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print(b, indent + 1)
```

## 1. Partition tree

> Trees can also be used to represent the partitions of an integer.

A partition tree for n using parts up to size m is a binary (two branch) tree that represents the choices taken during computation. In a non-leaf partition tree:

- the left (index 0) branch contains all ways of partitioning `n` using at least one `m`,
- the right (index 1) branch contains partitions using parts up to `m-1`, and
- the root label is `m`.

```py
def partition_tree(n, m):
        """Return a partition tree of n using parts of up to m."""
        if n == 0:
            return tree(True)
        elif n < 0 or m == 0:
            return tree(False)
        else:
            left = partition_tree(n-m, m)
            right = partition_tree(n, m-1)
            return tree(m, [left, right])
```

Printing the partitions from a partition tree is another tree-recursive process that traverses the tree, constructing each partition as a list. Whenever a `True` leaf is reached, the partition is printed.

```py
def print_parts(tree, partition=[]):
        if is_leaf(tree):
            if label(tree):
                print(' + '.join(partition))
        else:
            left, right = branches(tree)
            m = str(label(tree))
            print_parts(left, partition + [m])
            print_parts(right, partition)
```

## Tree Slicing

Slicing can be used on the branches of a tree as well. For example, we may want to place a restriction on the number of branches in a tree. A binary tree is either a leaf or a sequence of at most two binary trees. A common tree transformation called `binarization` computes a binary tree from an original tree by grouping together adjacent branches.

```py
def right_binarize(tree):
    """Construct a right-branching binary tree."""
    if is_leaf(tree):
        return tree
    if len(tree) > 2:
        tree = [tree[0], tree[1:]]
    return [right_binarize(b) for b in tree]
>>> right_binarize([1, 2, 3, 4, 5, 6, 7])
[1, [2, [3, [4, [5, [6, 7]]]]]]
```


