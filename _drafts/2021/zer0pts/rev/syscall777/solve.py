from z3 import *

flag = [BitVec(f'flag[{i}]',8) for i in range(56)]


#args = [BitVec(f'args[{i}]',32) for i in range(4)]
   
def mem_from_args(args):
    mem = [None for _ in range(12)]
    mem[0] = args[0]
    mem[1] = args[0] ^ args[1]
    mem[2] = args[0] ^ args[1] ^ args[2]
    mem[3] = args[0] ^ args[1] ^ args[2] ^ args[3]
    mem[4] = mem[0] + mem[1] + mem[2] + mem[3]
    mem[5] = mem[0] - mem[1] + mem[2] - mem[3]
    mem[6] = mem[0] + mem[1] - mem[2] - mem[3]
    mem[7] = mem[0] - mem[1] - mem[2] + mem[3]
    mem[8] = (mem[4] | mem[5]) ^ (mem[6] & mem[7])
    mem[9] = (mem[5] | mem[6]) ^ (mem[7] & mem[4])
    mem[10] = (mem[6] | mem[7]) ^ (mem[4] & mem[5])
    mem[11] = (mem[7] | mem[4]) ^ (mem[5] & mem[6])
    return mem


def check_mem(mem):
    return Or([
    And([mem[8] == 4127179254,mem[9] == 4126139894,mem[10] == 665780030 ,mem[11] == 666819390]),
    And([mem[8] == 1933881070,mem[9] == 3064954302,mem[10] == 3086875838,mem[11] == 3120414398]),
    And([mem[8] == 4255576062,mem[9] == 3116543486,mem[10] == 3151668710,mem[11] == 4290701286]),
    And([mem[8] == 1670347938,mem[9] == 4056898606,mem[10] == 2583645294,mem[11] == 2583645294]),
    And([mem[8] == 2720551936,mem[9] == 1627051272,mem[10] == 1627379644,mem[11] == 2720880308]),
    And([mem[8] == 2307981054,mem[9] == 3415533530,mem[10] == 3281895882,mem[11] == 2174343406]),
    And([mem[8] == 2673307092,mem[9] == 251771212 ,mem[10] == 251771212 ,mem[11] == 2673307092]),
    And([mem[8] == 4139379682,mem[9] == 3602496994,mem[10] == 3606265306,mem[11] == 4143147994]),
    And([mem[8] == 4192373742,mem[9] == 4088827598,mem[10] == 3015552726,mem[11] == 3119098870]),
    And([mem[8] == 530288564 ,mem[9] == 530288564 ,mem[10] == 3917315412,mem[11] == 3917315412]),
    And([mem[8] == 4025255646,mem[9] == 2813168974,mem[10] == 614968622 ,mem[11] == 1827055294]),
    And([mem[8] == 3747612986,mem[9] == 1340672294,mem[10] == 1301225350,mem[11] == 3708166042]),
    And([mem[8] == 3098492862,mem[9] == 3064954302,mem[10] == 3086875838,mem[11] == 3120414398]),
    And([mem[8] == 2130820044,mem[9] == 2115580844,mem[10] == 2130523044,mem[11] == 2145762244])])

checks = []
args = [None for i in range(4)]
for i in range(1,15):
    args[0] = Concat( flag[4*i-4:4*i-4+4][::-1] )
    args[1] = Concat( flag[4*(i%14):4*(i%14)+4][::-1] )
    args[2] = Concat( flag[4*((i+1)%14):4*((i+1)%14)+4][::-1] )
    args[3] = Concat( flag[4*((i+2)%14):4*((i+2)%14)+4][::-1] )
    #print(args)
    mem = mem_from_args(args)
    checks.append(check_mem(mem))
 
def get_sols(constraint,n):
    s = Solver()
    s.add(constraint)
    solutions = []
    while s.check()==sat and len(solutions)<n:
        m = s.model()
        print(len(solutions))
        s.add( Or(*[m[i]!=i() for i in m.decls()] ))
        results = {str(i):m[i].as_long() for i in m}
        print(results)
        solutions.append([ results[f'flag[{i}]'] for i in range(56)])
    return solutions



