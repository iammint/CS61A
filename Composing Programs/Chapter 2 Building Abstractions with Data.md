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

## Partition Trees

Trees can also be used to represent the partitions of an integer. A partition tree for n using parts up to size m is a binary (two branch) tree that represents the choices taken during computation. In a non-leaf partition tree:

- the left (index 0) branch contains all ways of partitioning n using at least one m,
- the right (index 1) branch contains partitions using parts up to m-1, and
- the root label is m.
