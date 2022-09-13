# Chapter 4 Data Processing

## Implicit Sequence

可以表示一个序列，而无需将每个元素显式地储存在计算机中。也就是说，我们可以构造一个对象，该对象提供对某个顺序数据集的所有元素的访问，而无需预先计算每个元素的值。相反，我们按需计算元素。

`Range`就是一个例子。当从一个范围请求一个元素时，它才会被计算。因此，我们可以在不使用大块内存的情况下表示非常大范围的整数。只有范围的端点存储为范围对象的一部分。

```py
>>> r = range(10000, 1000000000)
>>> r[45006230]
45016230
```

在此示例中，并非在构造范围实例时存储了此范围中的所有 999,990,000 个整数。而是在访问第 45006230 个元素时，才通过将第一个元素与索引相加来计算该元素的值。

## Lazy Computation

Computing values on demand, rather than retrieving them from an existing representation, is an example of `lazy computation`. In computer science, `lazy computation` describes any program that delays the computation of a value until that value is needed.

# 4.1 Iterators

> An `iterator` is an object that provides sequential access to values, one by one.

The iterator abstraction has two components:

1. a mechanism for retrieving the next element in the sequence being processed.
2. a mechanism for signaling that the end of the sequence has been reached and no further elements remain.

```py
>>> primes = [2, 3, 5, 7]
>>> type(primes)
<class 'list'>
>>> iterator = iter(primes)
>>> type(iterator)
<class 'list_iterator'>
>>> next(iterator)
2
>>> next(iterator)
3
>>> next(iterator)
5
>>> try:
        next(iterator)
    except StopIteration:
        print('No more values')
No more values
```

Once an iterator has returned all the values in an `iterable`, subsequent calls to next
on that iterable will result in a `StopIteration` exception. In order to be able to
access the values in the iterable a second time, you would have to create a second
iterator.

Iterators are also iterables, that is, calling iter on them will return
an iterator. However, calling `iter` on most iterators will not create a new iterator - instead, it will simply return the same iterator.

# 4.2 Iterables 可迭代对象

> Any value that can produce iterators is called an iterable value.

In Python, an iterable value is anything that can be passed to the built-in iter function. Iterables include sequence values such as `strings` and `tuples`, as well as other containers such as `sets` and `dictionaries`. `Iterators` are also iterables, because they can be passed to the iter function.

If a dictionary changes in structure because a key is added or removed, then all iterators become invalid and future iterators may exhibit arbitrary changes to the order their contents. On the other hand, changing the value of an existing key does not change the order of the contents or invalidate iterators.

|      iterable      |              iterator              |
| :----------------: | :--------------------------------: |
|     可迭代对象     | 可迭代对象的迭代器：iter(iterable) |
| 包含需要迭代的数据 |          记录数据中的顺序          |

# 4.3 Built-in Iterators

`map`, `filter`, `zip`, `reversed` are all built-in iterators.

```py
>>> def double_and_print(x):
        print('***', x, '=>', 2*x, '***')
        return 2*x
>>> s = range(3, 7)
>>> doubled = map(double_and_print, s)  # double_and_print not yet called
>>> next(doubled)                       # double_and_print called once
*** 3 => 6 ***
6
>>> next(doubled)                       # double_and_print called again
*** 4 => 8 ***
8
>>> list(doubled)                       # double_and_print called twice more
*** 5 => 10 ***
*** 6 => 12 ***
[10, 12]

>>> lst = range(3, 8)
>>> m = map(double_and_print, lst)
>>> f = lambda x: x >= 10
>>> t = filter(f, m)
>>> next(t)
*** 3 => 6 ***
*** 4 => 8 ***
*** 5 => 10 ***
10
>>> list(t)
[]
>>> list(filter(f, map(double_and_print, range(3, 8))))
*** 3 => 6 ***
*** 4 => 8 ***
*** 5 => 10 ***
*** 6 => 12 ***
*** 7 => 14 ***
[10, 12, 14]
```

# 4.4 For Statement

The `for` statement in Python operates on iterators.

Objects are iterable (an interface) if they have an **iter** method that returns an iterator. Iterable objects can be the value of the <expression> in the header of a for statement:

```py
for <name> in <expression>:
    <suite>
```

We can implement the execution rule of a `for` statement in terms of `while`, assignment, and `try` statements.

```py
count = [1, 2, 3, 4]
items = count.__iter__()
try:
    while True:
        item = items.__next__()
        print(item)
    except StopIteration:
        pass
```

# 4.5 Generators

> A generator is a special kind of iterator. Generator functions are distinguished from regular functions in that rather than containing `return` statements in their body, they use `yield` statement to return elements of a series.

|             iterator             |               generator               |
| :------------------------------: | :-----------------------------------: |
| 通过`iter(iterable)`产生的迭代器 | 使用`for/while循环+yield`产生的迭代器 |

```py
def letters_generator():
    current = 'a'
    while current <= 'f':
        yield current
        current = chr(ord(current) + 1)

for letters in letters_generator():
    print(letters)
# a
# b
# c
# d
# e
# f

letters = letters_generator()
letters.__next__()
# a
letters.__next__()
# b
```

## Exercise 1

Write a generator function generate_subsets that returns all subsets of the positive
integers from 1 to n. Each call to this generator's next method will return a list of
subsets of the set [1, 2, ..., n], where n is the number of previous calls to next.

```py
def generate_subsets():
    """
    >>> subsets = generate_subsets()
    >>> for _ in range(3):
    ... print(next(subsets))
    ...
    [[]]
    [[], [1]]
    [[], [1], [2], [1, 2]]
    """
    subsets = [[]]
    n = 1
    while True:
        yield subsets
        subsets = subsets + [s + [n] for s in subsets]
        n += 1
```

## Exercise 2

Implement sum paths gen, which takes in a tree t and and returns a generator which yields the sum of all the nodes from a path from the root of a tree to a leaf. You may yield the sums in any order.

```py
def sum_paths_gen(t):
    """
    >>> t1 = tree(5)
    >>> next(sum_paths_gen(t1))
    5
    >>> t2 = tree(1, [tree(2, [tree(3), tree(4)]), tree(9)])
    >>> sorted(sum_paths_gen(t2))
    [6, 7, 10]
    """
    if is_leaf(t):
        yield label(t)
    for b in branches(t):
        for s in sum_paths_gen(b):
            yield s + label(t)
```

# 4.6 Generators can `yield from` iterators

> A `yield from` statement yields all values from an iterator or iterable.

```py
>>> list(a_then_b([3, 4], [5, 6]))
[3, 4, 5, 6]
def a_then_b(a, b):
    for i in a:
        yield i
    for i in b:
        yield i

def a_then_b(a, b):
    yield from a
    yield from b
```

```py
>>> list(countdown(5))
[5, 4, 3, 2, 1]
# Iteratively
def countdown(n):
    while n > 0:
        yield n
        n -= 1

# Recursively
def countdown(n):
    if n > 0:
        yield n
        yield from countdown(n - 1)
    else:
        yield 'Blast off'
>>> t = countdown(5)
>>> next(t)
5
>>> next(t)
4
```

```py
def prefixes(s):
    if s:
        yield from prefixes(s[:-1])
        yield s
>>> prefixes('hello')
['h', 'he', 'hel', 'hell', 'hello']

def substrings(s):
    if s:
        yield from prefixes(s)
        yield from substrings(s[1:])
>>> substrings('hello')
['h', 'he', 'hel', 'hell', 'hello', 'e', 'el', 'ell', 'ello', 'l', 'll', 'llo', 'l', 'lo', 'o']
```
