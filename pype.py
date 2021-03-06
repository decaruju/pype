import math
from functools import reduce


class Fork:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


class ArrayFunction:
    def __init__(self, function):
        self.function = function

    def __ror__(self, array):
        return self.function(array)

    def __add__(self, rhs):
        return Fork(self, rhs)

    def __xor__(self, rhs):
        @functionize
        def inner(array):
            if isinstance(rhs, Fork):
                return self(rhs.lhs(array), rhs.rhs(array))
            return self(rhs(array))(array)
        return inner

    def __or__(self, rhs):
        @functionize
        def inner(*args):
            return rhs(self(*args))

        return inner

    def __mul__(self, rhs):
        return self(rhs)

    def __call__(self, *args):
        return self.function(*args)


def functionize(function):
    return ArrayFunction(function)


@functionize
def preduce(callback):
    @functionize
    def inner(array):
        return reduce(callback, array)
    return inner

@functionize
def pscan(callback):
    @functionize
    def inner(array):
        if len(array) == 0:
            return None
        acc = [array[0]]
        last_value = array[0]
        for item in array[1:]:
            new_value = callback(last_value, item)
            acc.append(new_value)
            last_value = new_value
        return acc
    return inner

@functionize
def pmap(callback):
    @functionize
    def inner(array):
        return list(map(callback, array))
    return inner

@functionize
def pfilter(callback):
    if isinstance(callback, list):
        return [x for x in callback if x]

    @functionize
    def inner(array):
        return [x for x in array if callback(x)]
    return inner



def binary(function):
    @functionize
    def inner(lhs, rhs=None):
        if rhs is None:
            @functionize
            def monadic(element):
                if isinstance(element, list):
                    if isinstance(lhs, list):
                        return [int(function(e, l)) for e, l in zip(element, lhs)]
                    return [int(function(e, lhs)) for e in element]
                return function(element, lhs)
            return monadic
        else:
            if isinstance(rhs, list):
                if isinstance(lhs, list):
                    return [int(function(e, l)) for e, l in zip(rhs, lhs)]
                return [int(function(e, lhs)) for e in rhs]
            return int(function(rhs, lhs))
    return inner


@functionize
def plookup(lookup):
    @functionize
    def inner(array):
        return [lookup[index] for index in array]
    return inner

@functionize
def pget(key):
    @functionize
    def inner(array):
        return [element[key] for element in array]
    return inner


@functionize
def pconstant(constant):
    @functionize
    def inner(_array):
        return constant
    return inner

@functionize
def pgetattr(key):
    @functionize
    def inner(array):
        if isinstance(array, list):
            return [getattr(element) for element in array]
        return getattr(array, key)
    return inner

@functionize
def psetattr(key, value):
    @functionize
    def inner(array):
        array[key] = value
        return array
    return inner



@functionize
def pindexof(lookup):
    @functionize
    def inner(array):
        return [lookup.index(element) if element in lookup else len(lookup) for element in array]
    return inner

@functionize
def ptransform(initial, final):
    @functionize
    def inner(array):
        return [final[initial.index(element)] if element in initial else len(initial) for element in array]
    return inner



@functionize
def pmask(mask):
    @functionize
    def inner(array):
        return [element for element, melem in zip(array, mask) if melem]
    return inner

@functionize
def piden(array):
    return array

@functionize
def psort(array):
    return sorted(array)


padd = binary(lambda x, y: x + y)
psub = binary(lambda x, y: x - y)
pmod = binary(lambda x, y: x % y)
pprod = binary(lambda x, y: x * y)
pdiv = binary(lambda x, y: x / y)
peq = binary(lambda x, y: x == y)
pneq = binary(lambda x, y: x != y)
pgt = binary(lambda x, y: x > y)
plt = binary(lambda x, y: x < y)
pgeq = binary(lambda x, y: x >= y)
pleq = binary(lambda x, y: x <= y)
pmax = binary(lambda x, y: x if x > y else y)
pmin = binary(lambda x, y: x if x < y else y)
pin = binary(lambda x, y: x in y)
pgcd = binary(lambda x, y: math.gcd(x, y))
prange = functionize(lambda x: list(range(x)))
pchars = functionize(lambda x: [c for c in x])
