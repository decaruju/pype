from functools import reduce


class PipeList(list):
    def __or__(self, function):
        return function(self)


class ArrayFunction:
    def __init__(self, function):
        self.function = function

    def __ror__(self, array):
        return PipeList(array) | self

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
        return PipeList(map(callback, array))
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


pdoublesum = pmap(pprod(2)) | preduce(padd)

a = [1, 2, 3] | pmap(pprod(2)) | preduce(padd)
b = [1, 2, 3] | pdoublesum
print(a)
print(b)
