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

# 2.5 Mutable data

One powerful technique for creating modular programs is to incorporate data that may change state over time. In this way, a single data object can represent something that evolves independently of the rest of the program. The behavior of a changing object may be influenced by its history, just like an entity in the world. **Adding state to data** is a central ingredient of a paradigm called object-oriented programming.

创建模块化程序的一项强大技术是合并可能随时间改变状态的数据。 通过这种方式，单个数据对象可以代表独立于程序其余部分发展的东西。 一个不断变化的对象的行为可能会受到其历史的影响，就像世界上的一个实体一样。 **向数据添加状态**是称为面向对象编程范式的核心要素。

# 3.1 The Object Metaphor

> Objects combine data values with behavior. Objects represent information, but also behave like the things that they represent.

## 3.2 Sequence Object

Instances of primitive built-in values such as numbers are immutable. Lists on the other hand are mutable.

```py
from datetime import date
today = date(2022, 9, 5)
print(today.strftime('%A %B %d'))
```

Lists can be copied using the `list` constructor function. Changes to one list do not affect another, unless they share structure.

```py
suits = ['♠', '♥', '♦', '♣']
next = list(suits)  # Bind "nest" to a second list with the same elements
# next is ['♠', '♥', '♦', '♣']
nest[0] = suits     # Create a nested list
# next is [['♠', '♥', '♦', '♣'], '♥', '♦', '♣']
```

According to this environment, changing the list referenced by `suits` will affect the nested list that is the first element of `nest`, but not the other elements.

```py
suits.insert(2, 'Joker')
# next is [['♠', '♥', 'Joker', '♦', '♣'], '♥', '♦', '♣']
```

And likewise, undoing this change in the first element of `nest` will change `suits` as well.

Because two lists may have the same contents but in fact be different lists, we require a means to test whether two objects are the same. Python includes two comparison operators, called is and is not, that test whether two expressions in fact evaluate to the identical object. Two objects are identical if they are equal in their current value, and any change to one will always be reflected in the other. Identity is a stronger condition than equality.

```py
suits is next[0]  # True
suits is ['♠', '♥', 'Joker', '♦', '♣']   # False
suits == ['♠', '♥', 'Joker', '♦', '♣']  # True
```

**`is` checks for identity, while `==` checks for the equality of content**

## List Comprehension

> A list comprehension always creates a new list.

For example, `unicodedata` module tracks the official names of every character in the Unicode alphabet. We can look up the characters corresponding to names, including those for card suits.

```py
cards = ['heart', 'diamond', 'spade', 'club']
from unicodedata import lookup
[lookup('WHITE ' + s.upper() + ' SUIT') for s in cards]
# ['♡', '♢', '♤', '♧']
```

This resulting list does not share any of its contents with `cards`, and evaluating the list comprehension does not modify the `cards` list.

# 3.3 Dictionaries

A dictionary contains key-value pairs, where **both the keys and values are objects**.

The dictionary type also supports various methods of iterating over the contents of the dictionary as a whole. The methods `keys`, `values`, and `items` all return iterable values.

```py
numerals = {'I': 1, 'V': 5, 'X': 10}
numerals['L'] = 50
sum(numerals.values())
# 66
```

A list of key-value pairs can be converted into a dictionary by calling the dict constructor function.

```py
dict([(3, 9), (4, 16), (5, 25)])
# {3: 9, 4: 16, 5: 25}
```

Dictionaries also have a comprehension syntax analogous to those of lists. A key expression and a value expression are separated by a colon. Evaluating a dictionary comprehension creates a new dictionary object.

```py
{x: x*x for x in range(3,6)}
# {3: 9, 4: 16, 5: 25}
```

# 3.4 Mutable Functions

## Local State

Lists and dictionaries have local state: they are changing values that have some particular contents at any point in the execution of a program. The word "state" implies an evolving process in which that state may change. Functions can also have local state.

For instance, let us define a function that models the process of withdrawing money from a bank account. We will create a function called withdraw, which takes as its argument an amount to be withdrawn. If there is enough money in the account to accommodate the withdrawal, then withdraw will return the balance remaining after the withdrawal. Otherwise, withdraw will return the message 'Insufficient funds'. For example, if we begin with $100 in the account, we would like to obtain the following sequence of return values by calling withdraw:

```py
def make_withdraw(balance):
    """withdraw = make_withdraw(100)
    >>> withdraw(25)
    75
    >>> withdraw(25)
    50
    >>> withdraw(60)
    'Insufficient funds'
    >>> withdraw(15)
    35"""
    def withdraw_helper(amount):
        nonlocal balance
        if amount <= balance:
            balance -= amount
        else:
            return 'Insufficient balance'
        return balance
    return withdraw_helper
```

Mutable values can be changed without a `nonlocal` statement.

```py
def make_withdraw(balance):
    b = [balance]
    def withdraw_helper(amount):
        if amount <= b[0]:
            b[0] -= amount
        else:
            return 'Insufficient balance'
        return b[0]
    return withdraw_helper
```

## Multiple Mutable Functions

```py
def f(x):
    x = 4
    def g(y):
        def h(z):
            nonlocal x
            x = x + 1
            return x + y + z
        return h
    return g
a = f(1)
b = a(2)
total = b(3) + b(4)
```

```py
def oski(bear):
    def cal(berk):
        nonlocal bear
        if bear(berk) == 0:
            return [berk + 1, berk - 1]
        bear = lambda ley: berk - ley
        return [berk, cal(berk)]
    return cal(2)
print(oski(abs))
```

# 2.6 Obejct-Oriented Programming

> Object-oriented programming (OOP) is a method for organizing programs that brings together many of the ideas introduced in this chapter.

## 1. Objects and classes

> A class serves as a template for all objects whose type is that class. Every object is an instance of some particular class.

```py
class Account:
    def __init__(self, account_holder):
        self.balance = 0
        self.holder = account_holder
    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance
    def withdraw(self, amount):
        if amount > self.balance:
            return 'Insufficient funds'
        self.balance = self.balance - amount
        return self.balance
```

## 2. Functions and Methods

Python distinguishes between functions and methods.

Bound methods couple together a function and the object on which that method will be invoked.

- Object + Function = Bound Method

```py
>>> type(Account.deposit)
<class 'function'>
>>> type(tom_account.deposit)
<class 'method'>

>>> Account.deposit(tom_account, 100)
100
>>> tom_account.deposit(100)
200
```

## 3. Inheritance

Instance attributes are found before class attributes; class attributes are inherited.

```py
class Worker:
    greeting = 'Sir'
    def __init__(self):
        self.elf = Worker
    def work(self):
        return self.greeting + ', I work'
    def __repr__(self):
        return Bourgeoisie.greeting

class Bourgeoisie(Worker):
    greeting = 'Peon'
    def work(self):
        print(Worker.work(self))
        return 'I gather wealth'

jack = Worker()
john = Bourgeoisie()
jack.greeting = 'Maam'

>>> Worker.work()
'Sir, I work'
>>> jack
Peon
>>> jack.work()
'Maam, I work'
>>> john.work()
Peon, I work
'I gather wealth'
>>> john.elf.work(john)
'Peon, I work'
```

## Exercise1

```py
class A:
    z = -1
    def f(self, x):
        return B(x - 1)
class B(A):
    n = 4
    def __init__(self, y):
        if y:
            self.z = self.f(y)
        else:
            self.z = C(y + 1)
class C(B):
    def f(self, x):
        return x

a = A()
b = B(1)
b.n = 5

C(2).n
# 4
a.z == C.z
# True
# It's `a.z` not `A.z`
a.z == b.z
# False

# Which evaluates to an integer?
# b.z
# b.z.z
# b.z.z.z √
# b.z.z.z.z
```

# 2.7 Linked list

> We can develop sequence representations that are not built into Python. A common representation of a sequence constructed from nested pairs is called a **linked list**.

```py
four = [1, [2, [3, [4, 'empty']]]]
empty = 'empty'
def is_link(s):
    """s is a linked list if it is empty or a (first, rest) pair."""
    return s == empty or (len(s) == 2 and is_link(s[1]))

def link(first, rest):
    """Construct a linked list from its first element and the rest."""
    assert is_link(rest), 'rest must be a linked list.'
    return [first, rest]

def first(s):
    """Return the first element of a linked list s."""
    assert is_link(s), 'first only applies to linked lists.'
    assert s != empty, 'empty linked list has no first element.'
    return s[0]

def rest(s):
    """Return the rest of the elements of a linked list s."""
    assert is_link(s), 'rest only applies to linked lists.'
    assert s != empty, 'empty linked list has no rest.'
    return s[1]

def len_link(s):
    length = 0
    while s!= empty:
        s, length = rest(s), length + 1
    return length

def getitem_link(s, i):
    """Return the element at index i of linked list s."""
    while i > 0:
        s, i = rest(s), i - 1
    return first(s)
```

# 2.8 Recursive Objects

> Objects can have other objects as attribute values. When an object of some class has an attribute value of that same class, it is a recursive object.

## 1. Linked List Class

A linked list, introduced earlier in this chapter, is composed of a first element and the rest of the list. The rest of a linked list is itself a linked list — a recursive definition. The empty list is a special case of a linked list that has no first element or rest. A linked list is a sequence: it has a finite length and supports element selection by index.

We can now implement a class with the same behavior. In this version, we will define its behavior using special method names that allow our class to work with the built-in len function and element selection operator (square brackets or operator.getitem) in Python. These built-in functions invoke special method names of a class: length is computed by **len** and element selection is computed by **getitem**. The empty linked list is represented by an empty tuple, which has length 0 and no elements.

```py
class Link:
    """A linked list with first element and the rest."""
    empty = ()
    def __init__(self, first, rest = empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

        def __getitem__(self, i):
            if i = 0:
                return self.first
            else:
                return self.rest[i - 1]

        def __len__(self):
            return 1 + len(self.rest)

        def __repr__(self):
            if self.rest:
                rest = ', ' + repr(self.rest)
            else:
                rest = ''
            return 'Link({0}{1})'.format(self.first, rest)

        @property
        def second(self):
            return self.rest.first

        @second.setter
        def second(self, value):
            self.rest.first = value
```

A Python list stores all of its elements in a single object, and each element can be accessed by using its index. A linked list, on the other hand, is a recursive object that only stores two things: its first value and a reference to the rest of the list, which is another linked list.

## Tree class

```py
class Tree:
    def __init__(self, label, branches=[]):
        self.label = label
        for branch in branches:
            assert isinstance(branch, Tree)
        self.branches = list(branches)
```

## Memoization

```py
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def count(f):
    def counted(n):
        counted.call_count += 1
        return f(n)
    counted.call_count = 0
    return counted

# 每次都会计算底部，因此消耗大量时间，可以将已计算过的fib数记起来

```

> Idea: Remember the results that have been computed before.

```py
def memo(f):
    cache = {}
    def memoized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memoized
# 没有储存记忆，计算较慢
fib(30)

# 储存记忆，计算更快
fib = memo(fib)
fib(30)

# count版本fib
fib = count(fib)
counted_fib = fib

# 储存记忆版本的counted_fib
fib = memo(fib)
fib = count(fib)
fib(30)
>>> fib.call_count
59
>>> counted_fib.call_count
31
```
