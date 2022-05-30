
from z3 import *
import random
perms ={
'd':[
    0, 1, 2, 3, 4, 5, 6, 7,
    8, 9, 10, 11, 12, 21, 22, 23,
    16, 17, 18, 19, 20, 29, 30, 31,
    24, 25, 26, 27, 28, 37, 38, 39,
    32, 33, 34, 35, 36, 13, 14, 15,
    42, 44, 47, 41, 46, 40, 43, 45
    ],
'r':[
     0, 1, 37, 3, 35, 5, 6, 32,
     8, 9, 10, 11, 12, 13, 14, 15,
     16, 17, 2, 19, 4, 21, 22, 7,
     26, 28, 31, 25, 30, 24, 27, 29,
     47, 33, 34, 44, 36, 42, 38, 39,
     40, 41, 18, 43, 20, 45, 46, 23
    ],
'b':[
     13, 11, 8, 3, 4, 5, 6, 7,
     45, 9, 10, 46, 12, 47, 14, 15,
     16, 17, 18, 19, 20, 21, 22, 23,
     24, 25, 0, 27, 1, 29, 30, 2,
     34, 36, 39, 33, 38, 32, 35, 37,
     40, 41, 42, 43, 44, 31, 28, 26
    ],
'u':[
     2, 4, 7, 1, 6, 0, 3, 5,
     32, 33, 34, 11, 12, 13, 14, 15,
     8, 9, 10, 19, 20, 21, 22, 23,
     16, 17, 18, 27, 28, 29, 30, 31,
     24, 25, 26, 35, 36, 37, 38, 39,
     40, 41, 42, 43, 44, 45, 46, 47
    ],
'f':[
     0, 1, 2, 3, 4, 24, 27, 29,
     8, 9, 7, 11, 6, 13, 14, 5,
     18, 20, 23, 17, 22, 16, 19, 21,
     42, 25, 26, 41, 28, 40, 30, 31,
     32, 33, 34, 35, 36, 37, 38, 39,
     10, 12, 15, 43, 44, 45, 46, 47
    ],
'l':[
     16, 1, 2, 19, 4, 21, 6, 7,
     10, 12, 15, 9, 14, 8, 11, 13,
     40, 17, 18, 43, 20, 45, 22, 23,
     24, 25, 26, 27, 28, 29, 30, 31,
     32, 33, 5, 35, 3, 37, 38, 0,
     39, 41, 42, 36, 44, 34, 46, 47
    ],
'x':list(range(48))
}

perms_names = 'drbuflx'

perms = [perms[i] for i in perms_names]

starting = [40, 25, 29, 46, 27, 45, 33, 34, 15, 38, 13, 3, 12, 18, 11, 47, 39, 1, 8, 19, 28, 31, 30, 32, 0, 20, 23, 35, 14, 26, 17, 16, 42, 4, 21, 43, 9, 10, 41, 24, 37, 44, 2, 36, 6, 7, 22, 5]
target = list(range(48))

def apply_permutation(state, perm):
    res = [None]*len(perm)
    for i,v in enumerate(perm):
        res[v] = state[i]
    return res

def apply_perm_order(state, perms_ind):
    result = state.copy()
    for i in perms_ind:
        result = apply_permutation(result, perms[i])
    return result


def give_order(starting, target, num_steps=20):
    constraints = []

    selections = [Int(f'selection_{i}') for i in range(num_steps)]
    for s in selections:
        constraints.append(And(s>=0,s<7))

    inps = [[Int(f'r{r}_i{i}') for i in range(48)] for r in range(num_steps+1)]
    oups = [[Int(f'r{r}_o{i}') for i in range(48)] for r in range(num_steps)]

    for s,iss in zip(inps[0],starting):
        constraints.append(s==iss)

    for s,oss in zip(inps[-1], target):
        constraints.append(s==oss)

    def is_permutation(inp,oup,perm):
        constraints = []
        for i,v in enumerate(perm):
            constraints.append(oup[v] == inp[i])
        return And(constraints)

    def permute_on_selection(selection, inp, oup):
        return  If(selection==0, is_permutation(inp,oup, perms[0]),
                If(selection==1, is_permutation(inp,oup, perms[1]),
                If(selection==2, is_permutation(inp,oup, perms[2]),
                If(selection==3, is_permutation(inp,oup, perms[3]),
                If(selection==4, is_permutation(inp,oup, perms[4]),
                If(selection==5, is_permutation(inp,oup, perms[5]),
                                 is_permutation(inp,oup, perms[6])))))))

    for i in range(num_steps):
        constraints.append(permute_on_selection(selections[i], inps[i], oups[i]))
        for inpi, oupi in zip(inps[i+1], oups[i]):
            constraints.append(inpi==oupi)

    solver = Solver()
    solver.add(constraints)
    print("added constraints")
    if solver.check() == sat:
        m = solver.model()
        return [m.eval(selections[i]).as_long() for i in range(len(selections))]
    else:
        print("not possible")

def solve(starting, target, limit=40):
    for num_steps in range(1,limit):
        print("trying in {} steps".format(num_steps))
        result = give_order(starting, target, num_steps)
        if result:
            print("solved")
            return result


result = give_order(starting, target)



