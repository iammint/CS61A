# Chapter 1 Building Abstractions with Functions

# 1.1 Interactive Sessions

## Statements and Expressions

- Statements typically describe actions.
- Expressions typically describe computations.

## Functions

Functions encapsulate logic that manipulates data.

## Objects

Objects supports set operations like computing intersections and membership. An object seamlessly bundles together data and the logic that manipulates that data, in a way that manages the complexity of both.

## Interpreters

Evaluating compound expressions requires a precise procedure that interprets code in a predictable way. A program that implements such a procedure, evaluating compound expressions, is called an interpreter.

In the end, we will find that all of these core concepts are closely related: functions are objects, objects are functions, and interpreters are instances of both. However, developing a clear understanding of each of these concepts and their role in organizing code is critical to mastering the art of programming.

In programming, we deal with two kinds of elements: functions and data. (Soon we will discover that they are really not so distinct.) Informally, data is stuff that we want to manipulate, and functions describe the rules for manipulating the data. Thus, any powerful programming language should be able to describe primitive data and primitive functions, as well as have some methods for combining and abstracting both functions and data.

# 1.2 Call expressions

> The most important kind of compound expression is a call expression, which applies a function to some arguments.

## Evaluating Nested Expressions

To evaluate a call expression, Python will do the following:

1. Evaluate the operator and operand subexpressions, then
2. Apply the function that is the value of the operator subexpression to the arguments that are the values of the operand subexpressions.

## Pure and Non-pure Functions

**Pure functions**. Functions have some input (their arguments) and return some output (the result of applying them).

**Non-pure functions**. In addition to returning a value, applying a non-pure function can generate side effects, which make some change to the state of the interpreter or computer. A common side effect is to generate additional output beyond the return value, using the `print` function.

## Nested expression with `Print`

None indicates that nothing is returned

```py
print(print(1), print(2))
# 1
# 2
# None None
```

```py
def if_function(condition, true_result, false_result):
    """Return true_result if condition is a true value, and
    false_result otherwise.""""
    if condition:
        return true_result
    else:
        return false_result


def with_if_statement():
    """
    >>> result = with_if_statement()
    47
    >>> print(result)
    None
    """
    if cond():
        return true_func()
    else:
        return false_func()

def with_if_function():
    """
    >>> result = with_if_function()
    42
    47
    >>> print(result)
    None
    """
    return if_function(cond(), true_func(), false_func())

def cond():
    return 42 > 47
def true_func():
    print(42)
def false_func():
    print(47)

```

Functions `cond()`, `true_func()`, and `false_func()` will execute before if_function.

# 1.3 Define new functions

**How to define a function.**
Function definitions consist of a `def` statement that indicates a `<name>` and a comma-separated list of named `<formal parameters>`, then a `return` statement, called the function body, that specifies the `<return expression>` of the function, which is an expression to be evaluated whenever the function is applied:

```py
def <name>(<formal parameters>):
    return <return expression>
```

## Function Signatures

> A description of the formal parameters of a function is called the function's signature.

# 1.4 Defining functions

- **Each function should have exactly one job.** That job should be identifiable with a short name and characterizable in a single line of text. Functions that perform multiple jobs in sequence should be divided into multiple functions.
- **Don't repeat yourself is a central tenet of software engineering.** The so-called **DRY** principle states that multiple fragments of code should not describe redundant logic. Instead, that logic should be implemented once, given a name, and applied multiple times. If you find yourself copying and pasting a block of code, you have probably found an opportunity for functional abstraction.

- A function's domain is the set of all inputs it might possibly take as arguments.
- A function's range is the set of output values it might possibly return.

## Documentation

A function definition will often include documentation describing the function, called a docstring, which must be indented along with the function body. Docstrings are conventionally triple quoted. The first line describes the job of the function in one line. The following lines can describe arguments and clarify the behavior of the function:

```py
>>> def pressure(v, t, n):
        """Compute the pressure in pascals of an ideal gas.

        Applies the ideal gas law: http://en.wikipedia.org/wiki/Ideal_gas_law

        v -- volume of gas, in cubic meters
        t -- absolute temperature in degrees kelvin
        n -- particles of gas
        """
        k = 1.38e-23  # Boltzmann's constant
        return n * k * t / v
```

When you call help with the name of a function as an argument, you see its docstring (type q to quit Python help).

# 1.5 Control

Rather than being evaluated, statements are executed.

```py
>>> def square(x):
        mul(x, x) # Watch out! This call doesn't return a value.
```

The body of the function consists of an expression. An expression by itself is a valid statement, but the effect of the statement is that the mul function is called, and the result is discarded. If you want to do something with the result of an expression, you need to say so: you might store it with an assignment statement or return it with a return statement.

At its highest level, the Python interpreter's job is to execute programs, composed of statements. However, much of the interesting work of computation comes from evaluating expressions. Statements govern the relationship among different expressions in a program and what happens to their results.

## Compound statements

- Expressions, return statements, and assignment statements are simple statements.
- A def statement is a compound statement. The suite that follows the def header defines the function body.

To execute a sequence of statements, execute the first statement. If that statement does not redirect control, then proceed to execute the rest of the sequence of statements, if any remain.

This definition exposes the essential structure of a recursively defined sequence: a sequence can be decomposed into its first element and the rest of its elements. The "rest" of a sequence of statements is itself a sequence of statements! Thus, we can recursively apply this execution rule.

```py
def search(f):
    x = 0
    while not f(x):
        x += 1
    return x

def square(x):
    return x * x

def inverse(f):
    return lambda y: search(lambda x: f(x) == y)

sqrt = inverse(square)

print(sqrt(256))
# 16
```

## Conditional Expressions

A conditional expression has the form

```py
<consequent> if <predicate> else <alternative>
```

**Evaluation rule:**

1. Evaluate the <predicate> expression
2. If it's a true value, the value of the whole expression is the value of the <consequent>
3. Otherwise, the value of the whole expression is the value of the <alternative>

```py
>>> x = 0
>>> abs(1/x if x!= 0 else 0)
0
```

## Testing

> Testing a function is the act of verifying that the function's behavior matches expectations.

**Assertions**. Programmers use `assert` statements to verify expectations, such as the output of a function being tested. An `assert` statement has an expression in a boolean context, followed by a quoted line of text (single or double quotes are both fine, but be consistent) that will be displayed if the expression evaluates to a false value.

```py
>>> assert fib(8) == 13, 'The 8th Fibonacci number should be 13'
```

When the expression being asserted evaluates to a true value, executing an `assert` statement has no effect. When it is a false value, `assert` causes an error that halts execution.

```py
>>> def fib_test():
        assert fib(2) == 1, 'The 2nd Fibonacci number should be 1'
        assert fib(3) == 1, 'The 3rd Fibonacci number should be 1'
        assert fib(50) == 7778742049, 'Error at the 50th Fibonacci number'
```

When writing Python in files, rather than directly into the interpreter, tests are typically written in the same file or a neighboring file with the suffix `_test.py`.

## Doctests

Python provides a convenient method for placing simple tests directly in the docstring of a function. The first line of a docstring should contain a one-line description of the function, followed by a blank line. A detailed description of arguments and behavior may follow. In addition, the docstring may include a sample interactive session that calls the function:

```py
>>> def sum_naturals(n):
        """Return the sum of the first n natural numbers.

        >>> sum_naturals(10)
        55
        >>> sum_naturals(100)
        5050
        """
        total, k = 0, 1
        while k <= n:
            total, k = total + k, k + 1
        return total
```

Then, the interaction can be verified via the doctest module. Below, the globals function returns a representation of the global environment, which the interpreter needs in order to evaluate expressions.

Then, the interaction can be verified via the <font color="red">doctest module</font>. Below, the globals function returns a representation of the global environment, which the interpreter needs in order to evaluate expressions.

```py
>>> from doctest import testmod
>>> testmod()
TestResults(failed=0, attempted=2)
```

# Higher-Order Function

## The properse of Higher-order functions

**Functions are first-class:** Functions can be manipulated as values in our programming language.

Higher-order function: A function takes a function as an argument value or returns a function as a result.

Higher-order functions:

- Express general methods of computation
- Remove repetition from programs
- Seperate concerns among functions

## Function Currying

> Currying: Transforming a multi-argument function into a single-argument, higher-order function.

```py
def curry2(f):
    def g(x):
        def h(y):
            return f(x, y)
        return h
    return g
```

```py
curry2 = lambda f: lambda x: lambda y: f(x, y)
m = curry2(add)
m(1)(2)
# 3
```
