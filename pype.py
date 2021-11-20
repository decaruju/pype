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

    def __and__(self, rhs):
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
                    return [int(function(lhs, e)) for e in element]
                return function(element, lhs)
            return monadic
        else:
            return int(function(lhs, rhs))
    return inner


@functionize
def plookup(lookup):
    @functionize
    def inner(array):
        return [lookup[index] for index in array]
    return inner


@functionize
def pindexof(lookup):
    @functionize
    def inner(array):
        return [lookup.index(element) if element in lookup else len(lookup) for element in array]
    return inner


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
prange = functionize(lambda x: list(range(x)))
pchars = functionize(lambda x: [c for c in x])





# TODO make pmap implicit with arithmetic functions
# pdoublesum = pmap(pprod(2)) | preduce(padd)
# odds = pfilter(pmod(2) | peq(1))

# lst = list

double_sum = pprod(2) | preduce & padd

string = '(1+(2*(2+3))*(1+1))'
parenthesis_depth = pfilter & pin('()') | pindexof('()') | plookup([1, -1, 0]) | pscan & padd | preduce & pmax
print(string | parenthesis_depth)

# array = [1, 2, 3]
# print(array | pscan & peq)
# print(array | pin & (prange(2) | padd(1)))
# a = [1, 2, 3] | pmap(pprod(2)) | preduce(padd)
# b = [1, 2, 3] | pdoublesum
# print(array | odds)
# print(a)
# print(b)


# TODO binary should have implicit monadic definition and array support
# padd = binary(lambda x, y: x + y)

# odds = mask ^ (pmod(2) | peq(1), piden)
