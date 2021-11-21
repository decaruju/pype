# pype
`pype` was written to mimic `apl` programming in python, but replacing arcane runes with more understandable function names as a way to understand programs.
All functions are prefixed with `p` as a way to avoid collisions for the proof of concept.
Symbols might change, I have to use the python's priority of operations, so symbols might not be the most intuitive.

Programs in python are usually use twice the amount of tokens because python doesn't support having tokens side by side, `a b # SyntaxError`, so we need an operator between each functions
# examples
`|` is a function call
```python
prange(3) # [0, 1, 2]
prange(3) | padd(2) # [2, 3, 4]
prange(3) | prod(2) # [0, 2, 4]
```

Binary functions such as padd, prod, pmax, peq can be either curried `padd(2)` to create a unary function, used as is with an implicit map or used element-wise on two arrays.
```python
prange(3) | padd(1) | prod(2) # [2, 4, 6]
prange(3) | padd & prange(3) # [0, 2, 4]
prance(3) | padd ^ piden # [0, 2, 4]
```

`*` is used for composition `a * b == a(b(x))` 
```python
prange(3) | padd(1) | prod(2) | preduce * padd # 12
prange & (prange(3) | padd(1) | prod(2) | preduce * padd) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
prange & (prange(3) | padd(1) | prod(2) | preduce * padd) | preduce * pmax # 11
```

`^` is used for the chain `a ^ b = a(b(x))(x)`
```python
prange(3) | pmask ^ peq(2)  ==== pmask(peq(2)(prange(3)))(prange(3)) # [2]
```

`^+` is used for the fork `a ^ b + c = a(b(x), c(x))`
the gcd of the min and max of an array is
```python
gcd_of_min_and_max = pgcd ^ preduce * pmax + preduce * pmin 
[2, 4, 10] | gcd_of_min_and_max # 2
```

The maximum depth of a string of parenthesized expressions is
```python
parenthesis_depth = ptransform('()', [1, -1, 0]) | pscan & padd | preduce & pmax
'(1+(2*(2+3))*(1+1))' | parenthesis_depth # 3
```

Value of x after incrementing and decrementing
```python
value_after_iteration = ptransform(['x++', '++x', 'x--', '--x'], [1, 1, -1, -1, 0]) | preduce * padd
['x++', '++x', 'x--', '++x', '--x', 'x++'] | value_after_iteration # 2

```

# Use-cases
none
