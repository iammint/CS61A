# Higher-Order Function

> A **higher order function (HOF)** is a function that manipulates other func-
> tions by taking in functions as arguments, returning a function, or both.

For example, the function `compose1` below takes in two functions as arguments
and returns a function that is the composition of the two arguments.

```py
def compose1(f, g):
    # return lambda x: f(g(x))
    def h(x):
        return f(g(x))
    return h
```

# Lambda Expressions

A lambda expression by itself evaluates to a function but does not bind it to
a name. Also note that the return expression of this function is not evaluated
until the lambda is called.

Unlike def statements, lambda expressions can be used as an operator or
an operand to a call expression. This is because they are simply one-line
expressions that evaluate to functions.

```py
(lambda y: y + 4)(5)
# 9
(lambda f, x: f(x))(lambda y: y + 4, 5)
# 9
```

# Currying

> One important application of **HOF**s is converting a function that takes mul-
> tiple arguments into a chain of functions that each take a single argument.
> This is known as currying.

For example, the function below converts the pow function into its curried form:

```py
def curried_pow(x):
    def h(y):
        return pow(x, y)
    return h
print(curried_pow(2)(3))
# 8
```

```py
def curry2(h):
    def f(x):
        def g(y):
            return h(x, y)
        return g
    return f
print(curry2(lambda x, y: x + y)(2)(3))
```

Lambda expression:

```py
curry2 = lambda h: lambda x: lambda y: h(x, y)
print(curry2(lambda x, y: x + y)(3)(2))
```

## One example

```py
n = 7
def f(x):
    n = 8
    return x + 1

def g(x):
    n = 9
    def h():
        return x + 1
    return h

def f(f, x):
    return f(x + n)

f = f(g, n)
g = (lambda y: y())(f)
# 15
```

## Another example

```py
y = "y"
h = y
def y(y):
    h = "h"
    if y == h:
        # 此处的y是传入的参数，而不是全局变量y
        return y + "i"
    y = lambda y: y(h)
    return lambda h: y(h)
y = y(y)(y)
```

先执行`y(y)`，将全局变量`y = "y"`传入函数，不满足`if`条件，`return lambda h: lambda y: y(h)` ，此时`h == "h"`，将函数`y`传入返回的函数继续调用，满足`if`条件，因此返回'hi'

# Writing higher order functions

Write a function that takes in a function `cond` and a number `n` and prints numbers from 1 to `n` where calling `cond` on that number returns `True`.

```py
def is_even(n):
    return n % 2 == 0

def keep_ints(cond, n):
    for i in range(n+1):
        if i > 0 and cond(i):
            print(i)
        i += 1

keep_ints(is_even, 10)
```

Write a function similar to keep_ints like before, but now it takes in a
number n and returns a function that has one parameter cond. The returned
function prints out numbers from 1 to n where calling cond on that number
returns True.

```py
>>> make_keeper(5)(is_even)

def is_even(n):
    return n % 2 == 0

def make_keeper(n):
    def keep_print(cond):
        i = 1
        while i <= n:
            if cond(i):
                print(i)
            i += 1
    return keep_print

make_keeper(10)(is_even)
```

# Self-Reference

> Self-reference refers to a particular design of **HOF**, where a function even-
> tually returns itself. In particular, a self-referencing function will not return
> a function call, but rather the function object itself.

As an example, take a look at the `print_all` function.

```py
def print_all(x):
    print(x)
    return print_all
```

Self-referencing functions will oftentimes employ helper functions that refer-
ence the outer function:

```py
def print_sums(n):
    print(n)
    def next_sum(k):
        return print_sums(n + k)
    return next_sum

print_sums(1)(2)(3)
# 1
# 3
# 6
```

## Writing functions

Write a function `print_delayed` delays printing its argument until the next function call.

`print_delayed` takes in an argument `x` and returns a new function `delay_print`. When `print_delayed` is called, it prints out `x` and returns another `delay_print`.

```py
def print_delayed(x):
"""Return a new function. This new function, when called, will print out x and return another function with the same behavior.
>>> f = print_delayed(1)
>>> f = f(2)
1
>>> f = f(3)
2
>>> f = f(4)(5)
3
4
>>> f("hi")
5
<function print_delayed> # a function is returned
"""
def print_delayed(x):
    def delay_print(y):
        print(x)
        return print_delayed(y)
    return delay_print
```

## What's the result?

```py
def yes(no):
    yes = 'no'
    return no
no = 'no'
def no(no):
    return no + yes(no)
yes = yes(yes)(no)('ok')

print(yes)
# okok
```

`yes(yes)` is a self-referencing function. 结果返回`yes`函数，接着调用`yes(no)`，由于后面还会继续调用所以无法传入`no`字符串，因此继续返回`no`函数，将'ok'字符串传入，返回'okok'

# 1. Compose

```py
def compose1(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f
```

# 2. Curry

```py
def curry2(h):
    def f(x):
        def g(y):
            return h(x, y)
        return g
    return f
```

# 3. Self-Reference

```py
def print_delayed(x):
    def print_later(y):
        print(x)
        return print_delayed
    return print_later
```
