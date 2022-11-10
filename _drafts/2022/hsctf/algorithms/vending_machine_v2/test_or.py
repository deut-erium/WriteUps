from ortools.sat.python import cp_model


ms = [166622, 182684, 186759, 178534, 141154, 182134, 178729, 135140, 170071, 182617, 180827, 167277, 179855, 176311, 169730, 142330, 177811, 135341, 181153, 135838, 181180, 182870, 87784, 136060, 168509, 86798, 134204, 135602, 174401, 173333, 131472, 182295, 140223, 176108, 164898, 179723, 178701, 181539, 175671, 177411, 132234, 140029, 175359, 131186, 138630, 92284, 189556, 185402, 179780, 182123, 128234, 170809, 128909, 178841, 91454, 183302]
coins  = [42384, 43186, 41604, 47770, 42598, 48978, 46080, 44429, 48206, 43822, 46414, 41190, 44123, 45392, 46883, 46619, 49138, 47673, 40156, 47954, 40198, 45154, 43069, 43138, 41370, 46426, 48160, 47213, 47274, 46241, 43492, 43180, 40634, 41448, 45865, 47777, 43570, 40943, 42984, 41777, 44435, 46992, 43518, 49854, 44317, 43596, 44871, 49484, 44339, 47569, 41810, 41731, 40569, 41397, 49739, 47063, 49903, 42256, 49486, 42127, 43846, 43924, 47226, 43057, 41050, 40779, 45196, 41174, 43503, 43837, 43532, 46377, 40304, 42465, 40108, 46679, 48623, 42784, 45523, 44912, 45326, 40557, 47090, 40713, 45840, 46726, 42548, 46132, 48825, 47472, 48450, 41074, 45925, 46976, 45763, 40771, 47750, 41666, 42186, 42762, 43442, 48618, 49464, 49471, 42769, 41369, 46422, 44865, 47530, 48798, 47268, 48903, 42828, 47126, 44345, 45947, 46130, 44928, 45696, 45251, 49666, 49628, 41511, 42919, 40668, 42714, 44750, 41353, 42210, 42825, 46179, 41398, 40890, 48642, 47727, 41922, 45676, 46263, 40798, 43329, 48279, 41984, 46601, 42086, 49433, 43359, 48812, 47159, 41831, 41266, 43796, 40856, 49244, 44857, 45647, 48444, 46532, 43497, 42495, 46668, 45497, 45835, 40390, 44203, 42379, 47374, 42025, 43330, 41187, 45773, 46535, 40428, 40786, 40941, 40115, 43617, 45122, 47273, 45073, 41534, 45651, 42577, 46079, 45444, 45632, 40233, 42526, 48644, 40069, 42024, 42090, 46120, 47951, 43119, 47037, 44647, 44629, 47282, 44532, 48172]

# ms = sorted(ms)

# num_machines = 50
# num_coins = 200

# model = cp_model.CpModel()
# coin_machine = [model.NewIntVar(0,num_machines, f'coin_machines_{i}') for i in range(num_coins)]
# machines = [model.NewIntVar(0,sum(sorted(coins)[:5]), f'machine{i}') for i in range(num_machines)]

# # machines = IntVector('machines', num_machines)
# for i in range(num_machines):
#     for j in range(num_coins):
#         model.AddImplication(coin_machine[j]==i, machines[i] == machines[i]+coins[j])
#         # machines[i] = If(coin_machine[j]==i, machines[i]+coins[j], machines[i])
#     constraints.append(machines[i]>=ms[i])
# for coin_val,coin_m in zip(coins,coin_machine):
#     constraints.append(And(coin_m<num_machines, coin_m>=0))

# for i in range(num_machines):
#     constraints.append(
#             sum(If(coin_machine[j]==i,coins[j],0) for j in range(num_coins)) >= ms[i]
#             )

# import time
# start_time = time.time()
# solve(constraints)
# print(time.time() - start_time)


from z3 import *
num_machines = 56
num_coins = num_machines*4
coins += [0]*(num_coins -len(coins))

model = cp_model.CpModel()
machines = [model.NewIntVar(0,num_coins-1, f'machines_{i}') for i in range(num_coins)]

model.AddAllDifferent(machines)

solver = cp_model.CpSolver()
# constraints.append(Distinct(machines))
# for i in machines:
#     constraints.append(And(i<=num_coins,i>=0))

# for i,v in enumerate(coins):
#     constraints.append(coin_vals[i]==v)

# for i in range(num_machines):
#     constraints.append(sum(coin_vals[j] for j in machines[4*i:4*i+4]) >= ms[i] )



