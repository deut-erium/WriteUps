import bisect
from itertools import combinations
ms = [166622, 182684, 186759, 178534, 141154, 182134, 178729, 135140, 170071, 182617, 180827, 167277, 179855, 176311, 169730, 142330, 177811, 135341, 181153, 135838, 181180, 182870, 87784, 136060, 168509, 86798, 134204, 135602, 174401, 173333, 131472, 182295, 140223, 176108, 164898, 179723, 178701, 181539, 175671, 177411, 132234, 140029, 175359, 131186, 138630, 92284, 189556, 185402, 179780, 182123, 128234, 170809, 128909, 178841, 91454, 183302]
coins  = [42384, 43186, 41604, 47770, 42598, 48978, 46080, 44429, 48206, 43822, 46414, 41190, 44123, 45392, 46883, 46619, 49138, 47673, 40156, 47954, 40198, 45154, 43069, 43138, 41370, 46426, 48160, 47213, 47274, 46241, 43492, 43180, 40634, 41448, 45865, 47777, 43570, 40943, 42984, 41777, 44435, 46992, 43518, 49854, 44317, 43596, 44871, 49484, 44339, 47569, 41810, 41731, 40569, 41397, 49739, 47063, 49903, 42256, 49486, 42127, 43846, 43924, 47226, 43057, 41050, 40779, 45196, 41174, 43503, 43837, 43532, 46377, 40304, 42465, 40108, 46679, 48623, 42784, 45523, 44912, 45326, 40557, 47090, 40713, 45840, 46726, 42548, 46132, 48825, 47472, 48450, 41074, 45925, 46976, 45763, 40771, 47750, 41666, 42186, 42762, 43442, 48618, 49464, 49471, 42769, 41369, 46422, 44865, 47530, 48798, 47268, 48903, 42828, 47126, 44345, 45947, 46130, 44928, 45696, 45251, 49666, 49628, 41511, 42919, 40668, 42714, 44750, 41353, 42210, 42825, 46179, 41398, 40890, 48642, 47727, 41922, 45676, 46263, 40798, 43329, 48279, 41984, 46601, 42086, 49433, 43359, 48812, 47159, 41831, 41266, 43796, 40856, 49244, 44857, 45647, 48444, 46532, 43497, 42495, 46668, 45497, 45835, 40390, 44203, 42379, 47374, 42025, 43330, 41187, 45773, 46535, 40428, 40786, 40941, 40115, 43617, 45122, 47273, 45073, 41534, 45651, 42577, 46079, 45444, 45632, 40233, 42526, 48644, 40069, 42024, 42090, 46120, 47951, 43119, 47037, 44647, 44629, 47282, 44532, 48172]
# ms = sorted(ms)

def satisfy_with_four(ms,coins):
    ms = sorted(ms)
    coins = sorted(coins)
    result = []
    removed = 0
    i = 0
    while removed < 24:
        fours = sum(coins[i:i+4])
        ind = bisect.bisect(ms,fours)
        smaller_value = ms[ind-1]
        if smaller_value > 150000:
            selected = coins[i:i+4]
            result.append((selected, ms.pop(ind-1)))
            for x in selected:
                coins.remove(x)
            removed +=1
        else:
            i+=1

    i = 0
    while ms[0]<120000:
        twos = sum(coins[i:i+2])
        if ms[0] <= twos:
            result.append((coins[i:i+2], ms.pop(0)))
            for x in coins[i:i+2]:
                coins.remove(x)
        else:
            i+=1
    i = 0
    while ms[0]<160000:
        threes = sum(coins[i:i+3])
        if ms[0] <= threes:
            result.append((coins[i:i+3], ms.pop(0)))
            for x in coins[i:i+3]:
                coins.remove(x)
        else:
            i+=1
    i = 0
    while i<len(coins)-8:
        fours = sum(coins[i:i+4])
        if ms[0] <= fours:
            result.append((coins[i:i+4], ms.pop(0)))
            for x in coins[i:i+4]:
                coins.remove(x)
        else:
            i+=1
    return ms,coins,result




ms,coins,result = satisfy_with_four(ms,coins)
print(len(ms), len(coins), len(result))


from z3 import *
# from cvc5.pythonic import *
num_machines = len(ms)
num_coins = num_machines*4
coins += [0]*(num_coins -len(coins))
constraints = []

# machines = IntVector('machines',num_coins)

# coin_vals = Array('coin_vals', IntSort(), IntSort())

machines = [BitVec(f'machine_{i}',9) for i in range(num_coins)]
coin_vals = Array('coin_vals', BitVecSort(9), BitVecSort(19))


constraints.append(Distinct(machines))
for i in machines:
    constraints.append(And(i<=num_coins,i>=0))

for i,v in enumerate(coins):
    constraints.append(coin_vals[i]==v)

for i in range(num_machines):
    constraints.append(sum(coin_vals[j] for j in machines[4*i:4*i+4]) >= ms[i] )


import time
start_time = time.time()
solver = Solver()
solver.add(constraints)
if solver.check() == sat:
    print("solved",time.time() - start_time)
    model = solver.model()
    assignments = [model.eval(i).as_long() for i in machines]
    values = []
    for i in range(num_machines):
        values.append(sum(coins[j] for j in assignments[4*i:4*i+4]))
    assert all(i>=j for i,j in zip(values, ms))






