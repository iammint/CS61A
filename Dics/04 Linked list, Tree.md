# Linked list

```py
class Link:
    empty = ()
    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest:
            rest_str = ', ' + repr(self.rest)
        else:
            rest_str = ''
        return 'Link({0}{1})'.format(self.first, rest_str)

    def __str__(self):
        string = "<"
        while self.rest is not Link.empty:
            string += str(self.first) + ", "
            self = self.rest
        return string + str(self.first) + ">"
```

## Write function1

Write a function that takes in a linked list and returns the sum of all its elements. You may assume all elements in `lnk` are integers.

```py
def sum_link(lnk):
    """Return the sum of all elements in lnk.

    >>> s = Link(1, Link(2, Link(3)))
    >>> sum_link(s)
    6
    """
    if lnk is Link.empty:
        return 0
    return lnk.first + sum_link(lnk.rest)
```

## Write function2

Write a function that takes in a Python list of linked lists and multiplies them
element-wise. It should return a new linked list.
If not all of the Link objects are of equal length, return a linked list whose length is
that of the shortest linked list given. You may assume the Link objects are shallow
linked lists, and that lst of lnks contains at least one linked list.

```py
def multiply_lnk(lst_of_lnks):
    """Return a new linked list that is the element-wise product of all the
    linked lists in lst_of_lnks.

    >>> s = Link(1, Link(2, Link(3)))
    >>> t = Link(4, Link(5, Link(6)))
    >>> u = Link(7, Link(8, Link(9)))
    >>> multiply_lnk([s, t, u])
    Link(28, Link(80, Link(162)))
    """
    product = 1
    for lnk in lst_of_lnks:
        if lnk is Link.empty:
            return Link.empty
        product *= lnk.first
    list_of_lnks_rest = [lnk.rest for lnk in lst_of_lnks]
    return Link(product, multiply_lnk(list_of_lnks_rest))
```

## Write function3

Implement `filter_link`, which takes in a linked list link and a function `f` and
returns a generator which yields the values of link for which `f` returns `True`.
Try to implement this both using a `while` loop and without using any form of
iteration.

```py
def filter_link(link, f):
    """
    >>> link = Link(1, Link(2, Link(3)))
    >>> g = filter_link(link, lambda x: x % 2 == 0)
    >>> next(g)
    2
    >>> next(g)
    StopIteration
    >>> list(filter_link(link, lambda x: x % 2 != 0))
    [1, 3]
    """
    while link is not Link.empty:
        if f(link.first):
            yield link.first
        link = link.rest
```

```py
def filter_no_iter(link, f):
    if link is Link.empty:
        return Link.empty
    elif f(link.first):
        return Link(link.first, filter_no_iter(link.rest, f))
    return filter_no_iter(link.rest, f)
```

# Trees using object

```py
class Tree:
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = branches

    def is_leaf(self):
        return not self.branches
```

## Write function1

Define a function `make_even` which takes in a tree `t` whose values are integers, and
mutates the tree such that all the odd integers are increased by 1 and all the even
integers remain the same.

```py
def make_even(t):
    """
    >>> t = Tree(1, [Tree(2, [Tree(3)]), Tree(4), Tree(5)])
    >>> make_even(t)
    >>> t.label
    2
    >>> t.branches[0].branches[0].label
    4
    """
    if t.label % 2 == 1:
        t.label += 1
    for b in t.branches:
        make_even(b)
    return
```

## Write function2

Define a function `square_tree(t)` that squares every value in the non-empty tree
`t`. You can assume that every value is a number.

```py
def square_tree(t):
    """Mutates a Tree t by squaring all its elements."""
    t.label = t.label ** 2
    for b in t.branches:
        square_tree(b)
```

## Write function3

Define the procedure `find_path` that, given a Tree `t` and an `entry`, returns a list
containing the nodes along the path required to get from the root of `t` to `entry`. If
`entry` is not present in `t`, return `False`.
Assume that the elements in t are unique. Find the path to an element.

```py
def find_path(t, entry):
    paths = []
    if t.label == entry:
        paths.append([t.label])
    for b in t.branches:
        for path in find_paths(b, entry):
            paths.append([t.label] + path)
    return paths
```

## Write function4

Assuming that every value in t is a number, define `average(t)`, which returns the
average of all the values in `t`. You may not need to use all the provided lines.

```py
def average(t):
    """Return the average of all the values in t."""
    def sum_helper(t):
        total, count = 0, 0
        for b in t.branches:
            subTreeTotal, subTreeCount = sum_helper(b)
            total += subTreeTotal
            count += subTreeCount
        total += t.label
        count += 1
        return total, count
    total, count = sum_helper(t)
    return total/count
```
