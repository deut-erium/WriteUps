from output import *

import random
from tqdm import tqdm
target = enc_state[1][1]

def rev_knapsack_state(target,pubkey=pubkey):
    n = len(pubkey)
    A = Matrix(n+1,n+1)
    for i in range(n):
        A[i,i] = 1
        A[i,n] = pubkey[i]
    A[n,n] = -target

    a = A.LLL()
    for row in a:
        if set(row)=={0,1}:
            selected = row[:32]
            assert sum(i*j for i,j in zip(selected,pubkey))==target
            return int("".join(map(str,selected)),2)

# dec_state_one = list(map(rev_knapsack_state,enc_state[1]))
dec_state_one = [rev_knapsack_state(i) for i in tqdm(enc_state[1])]
assert dec_state_one[-1] == 624
assert dec_state_one[0] == 0x80000000
state = (enc_state[0],tuple(dec_state_one),enc_state[2])
random.setstate(state)
random_number = random.randint(1, 2**8)

shuffled_flag= []
while enc_flag:
    for i in range(10,128):
        if (enc_flag-i)% (random_number**i)==0:
            shuffled_flag.append(i)
            enc_flag = (enc_flag-i)//(random_number**i)

shuffled_flag = shuffled_flag[::-1]

len_flag = len(shuffled_flag)
shuffle_order = random.sample(list(range(len_flag)), len_flag)
flag = bytearray(len_flag)
for i,v in enumerate(shuffle_order):
    flag[v] = shuffled_flag[i]

print(flag)





