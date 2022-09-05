# Chapter 3 Mutable Data

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
