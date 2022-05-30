from z3 import *
import random

number_of_elements = 24
number_of_groups = 6

permutations = []
for _ in range(number_of_groups):
    x = list(range(number_of_elements))
    random.shuffle(x)
    permutations.append(x)


def apply_permutation(state, perm):
    res = [None]*len(perm)
    for i,v in enumerate(perm):
        res[v] = state[i]
    return res

def apply_perm_order(state, perms_ind):
    result = state.copy()
    for i in perms_ind:
        result = apply_permutation(result, permutations[i])
    return result


def give_order(starting, target, perms, num_steps):
    number_of_groups = len(perms)
    number_of_elements = len(starting)
    constraints = []

    selections = [Int(f'selection_{i}') for i in range(num_steps)]
    for s in selections:
        constraints.append(And(s>=0,s<number_of_groups))

    inps = [[Int(f'r{r}_i{i}') for i in range(number_of_elements)] for r in range(num_steps+1)]
    oups = [[Int(f'r{r}_o{i}') for i in range(number_of_elements)] for r in range(num_steps)]

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
        selected_permutation = is_permutation(inp, oup, perms[0])
        for i in range(1, number_of_groups):
            selected_permutation = If(selection == i,
                    is_permutation(inp, oup, perms[i]), selected_permutation)
        return selected_permutation

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

def solve(starting, target, perms, limit=40):
    for num_steps in range(1,limit):
        print("trying in {} steps".format(num_steps))
        result = give_order(starting, target,permutations, num_steps)
        if result:
            print("solved")
            return result

starting = list(range(number_of_elements))
random_order = [random.randint(0,number_of_groups-1) for _ in range(10)]
target = apply_perm_order(starting, random_order)
result = solve(starting, target, permutations )

