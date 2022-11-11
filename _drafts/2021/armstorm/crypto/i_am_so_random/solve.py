from sympy import factorint
from collections import Counter
from itertools import combinations, chain
from math import prod

def prod_powerset(Set):
    product = prod(Set)
    for elem in chain.from_iterable([combinations(Set,r) for r in range(1,len(Set)+1)]):
        prod1 = prod(elem)
        yield prod1, product//prod1

def get_next(seed):
    return int(str(seed**2).rjust(16,'0')[4:12])

def all_prods(num):
    products = set()
    x = list(Counter(factorint(num)).elements())
    for a in prod_powerset(x):
        products.add(tuple(sorted(a)))
    valid_products = []
    for x,y in products:
        if x<10**8 and y<10**8:
            valid_products.append([x,y])
    return valid_products

def find(out1,out2,out3):
    for a,b in all_prods(out1):
        if get_next(a)*get_next(b)==out2:
            a,b = get_next(a),get_next(b)
            a,b = get_next(a),get_next(b)
            print(a*b==out3)
            a,b = get_next(a),get_next(b)
            print(a,b,a*b)
            a,b = get_next(a),get_next(b)
            print(a,b,a*b)

#actf{middle_square_method_more_like_middle_fail_method}
