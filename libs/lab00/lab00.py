def twenty_twenty():
    """Come up with the most creative expression that evaluates to 2020,
    using only numbers and the +, *, and - operators.

    >>> twenty_twenty()
    2020
    """
    return ((1 * 3 * 5 * 7) + 400) * 4
print(twenty_twenty())


# shakespeare.txt for trying python
shakes = open("d:\AAAMint\Front-End\CS\libs\lab00\lab00\shakespeare.txt")
text = shakes.read().split()
words = set(text)
print('for' in words)
print({w for w in words if w == w[::-1]}) 
print({w for w in words if w[::-1] in words})
