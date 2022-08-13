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

