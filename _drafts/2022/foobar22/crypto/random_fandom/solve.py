from output import *

from z3 import *
import random

limit = 2**32
weights = [random.randint(2**31,2**32) for i in range(32)]
sel_temp = [random.randint(0,1) for i in range(32)]
target = sum(i*j for i,j in zip(weights,sel_temp))

# target = enc_state[1][1]
# weights = pubkey

bs = sum(pubkey).bit_length()
# selected = [BitVec('sel_{}'.format(i),bs) for i in range(len(weights))]
selected = BoolVector('sel',len(weights))
s = Solver()
# for sel in selected:
#     s.add(Or(sel==0,sel==1))


s.add( sum([i*j for i,j in zip(selected,weights)])==target)

