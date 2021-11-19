from functools import reduce


class ArrayFunction:
    def __init__(self, function):
        self.function = function

    def __ror__(self, array):
        return self.function(array)

    def __or__(self, rhs):
        @functionize
        def inner(*args):
            return rhs(self(*args))

        return inner

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
def padd(lhs, rhs):
    if rhs is None:
        @functionize
        def inner(elem):
            return elem + lhs
        return inner
    return lhs + rhs


@functionize
def pmap(callback):
    @functionize
    def inner(array):
        return list(map(callback, array))
    return inner


@functionize
def pprod(lhs, rhs=None):
    if rhs is None:
        @functionize
        def inner(elem):
            return elem * lhs
        return inner
    else:
        return lhs * rhs

@functionize
def peq(lhs, rhs=None):
    if rhs is None:
        @functionize
        def inner(elem):
            return elem == lhs
        return inner
    else:
        return lhs == rhs

@functionize
def pmod(lhs, rhs=None):
    if rhs is None:
        @functionize
        def inner(elem):
            return elem % lhs
        return inner
    else:
        return lhs % rhs

@functionize
def pfilter(callback):
    if isinstance(callback, list):
        return [x for x in callback if x]

    @functionize
    def inner(array):
        return [x for x in array if callback(x)]
    return inner



# TODO make pmap implicit with arithmetic functions
pdoublesum = pmap(pprod(2)) | preduce(padd)
odds = pfilter(pmod(2) | peq(1))

lst = list

array = [1, 2, 3]
a = [1, 2, 3] | pmap(pprod(2)) | preduce(padd)
b = [1, 2, 3] | pdoublesum
print(array | odds)
print(a)
print(b)
