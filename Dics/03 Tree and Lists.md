# Tree

Parent node: A node that has branches. Parent nodes can have multiple branches.

- Child node: A node that has a parent. A child node can only belong to one parent.
- Root: The top node of the tree. In our example, the node that contains 7 is the root.
- Label: The value at a node. In our example, all of the integers are values.
- Leaf: A node that has no branches. In our example, the nodes that contain
  −4, 0, 6, 17, and 20 are leaves.
- Branch: A subtree of the root. Note that trees have branches, which are
  trees themselves: this is why trees are recursive data structures.
- Depth: How far away a node is from the root. In other words, the number
  of edges between the root of the tree to the node. In the diagram, the node
  containing 19 has depth 1; the node containing 3 has depth 2. Since there are
  no edges between the root of the tree and itself, the depth of the root is 0.
- Height: The depth of the lowest leaf. In the diagram, the nodes containing
  −4, 0, 6, and 17 are all the “lowest leaves,” and they have depth 4. Thus, the
  entire tree has height 4.
  In computer science, there are many different types of trees. Some vary in the
  number of branches each node has; others vary in the structure of the

## Exercise1.

Write a function that returns the height of a tree. Recall that the height of a tree
is the length of the longest path from the root to a leaf.

```py
def height(t):
    """Return the height of a tree.
    >>> t = tree(3, [tree(5, [tree(1)]), tree(2)])
    >>> height(t)
    2
    """
    if is_leaf(t):
        return 0
    else:
        return 1 + max([height(b) for b in branches(t)])
```

## Exercise2

Write a function that takes in a tree and squares every value. It should return a
new tree. You can assume that every item is a number.

```py
def square_tree(t):
    """Return a tree with the square of every element in t
    >>> numbers = tree(1,
    ...                 [tree(2,
    ...                     [tree(3),
    ...                     tree(4)]),
    ...                  tree(5,
    ...                     [tree(6,
    ...                         [tree(7)]),
    ...                     tree(8)])])
    >>> print_tree(square_tree(numbers))
    1
        4
            9
            16
        25
            36
                49
            64
    """
    return tree(label(t) ** 2, [square_tree(b) for b in branches(t)])
```

## Exercise3

Write a function that takes in a tree and a value x and returns a list containing the
nodes along the path required to get from the root of the tree to a node containing
x.

If x is not present in the tree, return None. Assume that the entries of the tree are
unique.

```py
def find_path(tree, x):
    """
    >>> t = tree(2, [tree(7, [tree(3), tree(6, [tree(5), tree(11)])] ), tree(15)])
    >>> find_path(t, 5)
    [2, 7, 6, 5]
    >>> find_path(t, 10) # returns None
    """
    if label(tree) == x:
        return [x]
    for b in branches(tree):
        path = find_path(b, x)
        if path:
            return [label(tree)] + path
```

## Exercise4

What does the expression evaluate to?

```py
t = tree(1, [tree(2), tree(3)])
print(branches(tree(2, tree(t, [])))[0])
# [1, [2], [3]]
```

# Mutation

```py
lst1 = [1, 2, 3]
lst2 = lst1
lst2.extend([5, 6])
>>>lst2
[1, 2, 3, 5, 6]
lst1.append([-1, 0, 1])
>>>lst1
[1, 2, 3, 5, 6, [-1, 0, 1]]
lst3 = lst2[:]
lst3.insert(3, lst2.pop(3))
# i in pop(i) is index
>>>lst3
[1, 2, 3, 5, 5, 6, [-1, 0, 1]]
>>>lst2
[1, 2, 3, 6, [-1, 0, 1]]
>>>lst1
[1, 2, 3, 6, [-1, 0, 1]]
>>> lst1[4] is lst3[6]
True
>>> lst1[:3] is lst2[:3]
False
>>> lst1[:3] == lst2[:3]
True
x = (1, 2, [4, 5, 6])
x[2] = [3, 4, 5]
# Error: 'tuple' object does not support item assignment
>>>x
(1, 2, [4, 5, 6])
x[2][0] = 3
>>>x
(1, 2, [3, 5, 6])
```

## Exercise1

Write a function that takes in a value x, a value el, and a list and adds as many
el’s to the end of the list as there are x’s. Make sure to modify the original
list using list mutation techniques.

```py
def add_this_many(x, el, lst):
    """ Adds el to the end of lst the number of times x occurs
    in lst.
    >>> lst = [1, 2, 4, 2, 1]
    >>> add_this_many(1, 5, lst)
    >>> lst
    [1, 2, 4, 2, 1, 5, 5]
    >>> add_this_many(2, 2, lst)
    >>> lst
    [1, 2, 4, 2, 1, 5, 5, 2, 2]
    """
    count = lst.count(x)
    for i in range(count):
        lst.append(el)
    return lst
```

## Exercise2

Write a function that takes in a sequence `s` and a function `fn` and returns a dictionary.
The values of the dictionary are lists of elements from `s`. Each element `e` in a list
should be constructed such that `fn(e)` is the same for all elements in that list.
Finally, the key for each value should be fn(e).

```py
def group_by(s, fn):
    """
    >>> group_by([12, 23, 14, 45], lambda p: p // 10)
    {1: [12, 14], 2: [23], 4: [45]}
    >>> group_by(range(-3, 4), lambda x: x * x)
    {0: [0], 1: [-1, 1], 4: [-2, 2], 9: [-3, 3]}
    """
    dict = {}
    for num in s:
        if fn(num) not in dict.keys():
            dict[fn(num)] = []
        dict[fn(num)].append(num)
    return dict
```

## Exercise3

Implement the following function partition_options which outputs all the ways to partition a number
total using numbers no larger than biggest.

```py
def patition_options(total, biggest):
    """
    >>> partition_options(2, 2)
    [[2], [1, 1]]
    >>> partition_options(3, 3)
    [[3], [2, 1], [1, 1, 1]]
    >>> partition_options(4, 3)
    [[3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]
    """
    # It seems like it's a wrong solution
    if total == 0:
        return [[]]
    elif biggest == 0 or total < 0:
        return []
    else:
        with_biggest = patition_options(total - biggest, biggest)
        without_biggest = patition_options(total, biggest - 1)
        with_biggest = [[biggest, ele] for ele in with_biggest]
        return with_biggest + without_biggest
```

## Exercise4

Return the minimum number of elements from the list that need to be summed in order to add up to `T`.
The same element can be used multiple times in the sum.

For example, for T = 11 and lst = [5, 4, 1] we should return 3 because at minimum we need to add 3 numbers together (5, 5, and 1). You can assume that there always exists a linear combination of the elements in lst that equals T.

```py
def min_elements(T, lst):
    """
    >>> min_elements(10, [4, 2, 1]) # 4 + 4 + 2
    3
    >>> min_elements(12, [9, 4, 1]) # 4 + 4 + 4
    3
    >>> min_elements(0, [1, 2, 3])
    0
    """
    if T == 0:
        return 0
    return min(1 + min_elements(T - ele, lst) for ele in lst if ele <= T)
```
