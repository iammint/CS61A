# Recursive Functions

> A function is called recursive if the body of that function calls itself, either directly or indirectly.

```py
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n-1)
```

There are **three** common steps in a recursive definition:

1. **Figure out your base case.**
2. **Make a recursive call with a simpler argument.**

   Simplify yourproblem, and assume that a recursive call for this new problem will simply work. This is called the \leap of faith". For factorial, we reduce the problem by calling factorial(n-1).

3. **Use your recursive call to solve the full problem.**

   Remember that we are assuming the recursive call works. With the result of the recursive call, how can you solve the original problem you were asked? For factorial, we just multiply (n - 1)! by n.

## is_prime

- Iteration:

```py
def is_prime(n):
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True
```

- Recursion:

Implement the recursive is prime function. Do not use a while loop, use
recursion. As a reminder, an integer is considered prime if it has exactly two
unique factors: 1 and itself.

```py
def is_prime(n):

```

# 1. Mutual Recursion

Credit Card: Luhn Algorithm

```py
def split(n):
    return n // 10, n % 10

def sum_digits(n):
    if n < 10:
        return n
    else:
        all_but_last, last = split(n)
        return sum_digits(all_but_last) + last

def luhn_sum(n):
    if n < 10:
        return n
    else:
        all_but_last, last = split(n)
        return luhn_sum_double(all_but_last) + last

def luhn_sum_double(n):
    all_but_last, last = split(n)
    luhn_digit = sum_digits(2 * last)
    if n < 10:
        return luhn_digit
    else:
        return luhn_sum(all_but_last) + luhn_digit
```

# 2. Iteration VS Recursion

**Iteration is a special case of recursion.**

## Recursion to Iteration

Idea: Figure out what state must be maintained by the iterative function.

```py
def split(n):
    return n // 10, n % 10

```

- Recursion:

```py
def sum_digits(n):
    if n < 10:
        return n
    else:
        all_but_last, last = split(n)
        return sum_digits(all_but_last) + last
```

- Iteration:

```py
def sum_digits_iter(n):
    digit_sum = 0
    while n > 0:
        n, last = split(n)
        digit_sum += last
    return digit_sum
```

## Iteration to Recursion

Idea: The state of an iteration can be passed as arguments.

- Iteration:

```py
def sum_digits_iter(n):
    digit_sum = 0
    while n > 0:
        n, last = split(n)
        digit_sum += last
    return digit_sum
```

- Recursion:

```py
def sum_digits_rec(n, digit_sum):
    if n == 0:
        return digit_sum
    else:
        n, last = split(n)
        return sum_digits_rec(n, digit_sum + last)
```

# 3. Order of Recursive Calls

```py
def cascade(num):
    if num < 10:
        print(num)
    else:
        print(num)
        cascade(num // 10)
        print(num)

cascade(2013)
# 2013
# 201
# 20
# 2
# 20
# 201
# 2013
```

## Inverse cascade

```py
# 1
# 12
# 123
# 1234
# 123
# 12
# 1
def inverse_cascade(n):
    grow(n)
    print(n)
    shrink(n)

def f_then_g(f, g, n):
    if n:
        f(n)
        g(n)

grow = lambda n: f_then_g(grow, print, n // 10)
shrink = lambda n: f_then_g(print, shrink, n // 10)

inverse_cascade(1234)
```

# 4. Tree Recursion

> Tree-shaped processes arise whenever executing the body of a recursive function makes more than one call to that function.

![Snipaste_2022-08-22_19-22-15.png](https://media.haochen.me/Snipaste_2022-08-22_19-22-15.png)

The process is highly repetitive; fib is called on the same argument multiple times.

```py
def paths(m, n):
    """Return the number of paths from one corner of an M by N grid to the opposite corner.
    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    if m == 0 or n == 0:
        return 1
    return paths(m-1, n) + paths(m, n-1)
```

## Counting Partitions

The number of partitions of a positive integer `n`, using parts up to size `m`, is the number of ways in which `n` can be expressed as the sum of positive integer parts up to `m` in increasing order.

![Snipaste_2022-08-24_13-36-10.png](https://media.haochen.me/Snipaste_2022-08-24_13-36-10.png)

```py
def count_partitions(n, m):
    if n == 0:
        return 1
    elif n < 0 or m == 0:
        return 0
    else:
        with_m = count_partitions(n-m, m)
        without_m = count_partitions(n, m-1)
        return with_m + without_m
```

## All_nums

Write a function `all_nums(k)` that prints binary numbers between `1` and `k` digits. For example, `all_nums(3)` should print `0, 1, 10, 11, 100, 101, 110, 111`.

![Snipaste_2022-08-27_11-17-50.png](https://media.haochen.me/Snipaste_2022-08-27_11-17-50.png)

```py
def all_nums(k):
    def helper(k, prefix):
        # base case
        if k == 0:
            print(prefix)
            return
        helper(k-1, prefix * 10)
        helper(k-1, prefix * 10 + 1)
    helper(k, 0)

all_nums(3)
```

## Implementing Functions

1. Read the description
2. Verify the examples & pick a simple one
3. Read the template
4. Implement without the template, then change your implementation to match the template.
   OR
   If the template is helpful, use it.
5. Annotate names with values from your chosen example.
6. Write code to compute the result.
7. Did you really return the right thing?
8. Check your solution with the other examples.

```py
def remove(n, digit):
    """Return all digits of non-negative `n` that are not `digit`, for some non-negative `digit` less than 10.
    >>> remove(231, 3)
    21
    >>> remove(243132, 2)
    4313
    """
    kept, digits = 0, 0
    while n > 0:
        n, last = n // 10, n % 10
        if last != digit:
            kept = kept + last * 10 ** digits
            digits += 1
    return kept
```

```py
def remove(n, digit):
    """Return all digits of non-negative `n` that are not `digit`, for some non-negative `digit` less than 10.
    >>> remove(231, 3)
    21
    >>> remove(243132, 2)
    4313
    """
    kept, digits = 0, 0
    while n > 0:
        n, last = n // 10, n % 10
        if last != digit:
            kept = kept / 10 + last
            digits += 1
    return kept * 10 ** digits
```
