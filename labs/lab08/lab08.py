
def make_generators_generator(g):
    """Generates all the "sub"-generators of the generator returned by
    the generator function g.
    Returns a generator that yields generator 
    >>> def every_m_ints_to(n, m):
    ...     i = 0
    ...     while (i <= n):
    ...         yield i
    ...         i += m
    ...
    >>> def every_3_ints_to_10():
    ...     for item in every_m_ints_to(10, 3):
    ...         yield item
    ...
    >>> for gen in make_generators_generator(every_3_ints_to_10):
    ...     print("Next Generator:")
    ...     for item in gen:
    ...         print(item)
    ...
    Next Generator:
    0
    Next Generator:
    0
    3
    Next Generator:
    0
    3
    6
    Next Generator:
    0
    3
    6
    9
    """
    "*** YOUR CODE HERE ***"
    lst = list(g())
    def fn(counter):
        new_iter = iter(lst)
        for i in range(counter): 
            yield next(new_iter)
    counter = 1
    while counter <= len(lst):
        yield fn(counter) 
        counter += 1

