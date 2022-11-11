nums = [
    571950745479432267005464851096356774896792314093,
    442389987284185335289253341364665422032816391623,
    674689295937843496428836795727103849648022363056,
    534115548763794721117336167251846846861246743872
    ]

p,q,g = 7723227163652206196072315877851665970492409383498621787915763836703165497532056144920977718337221463593649391334584803149362349291402576071382757173855489,1419435951773960878522380192164715964887544050251,3177589275498063000838438765591095514446952503023627047492796256311729225229378235819032575431223841654220960177156277529073194075117755794549781574237012

sign_0 = (1068578444686700850472665790275239904755324934637, 773641167123158554564050069711067502164705010631)
sign_1 = (1261138445303763427942699370178218831470626347614, 466653063468278381121557045661962018351821473529)

from math import gcd
from sympy import factorint
from hashlib import sha1
from Crypto.Util.number import bytes_to_long,long_to_bytes
from sympy.ntheory.modular import crt

diffs = [j-i for i,j in zip(nums,nums[1:])]
diffs2 = [a2*a0 - a1**2 for a0,a1,a2 in zip(diffs,diffs[1:],diffs[2:])]
facsm=[3,727,96823,156435354953,996091343376681387892852529,1086448931741173136362453140818209978717054020739]
m = facsm[-1]
a = (diffs[1]*pow(diffs[0],-1,m))%m
b = (nums[1]-a*nums[0])%m

for i,j in zip(nums,nums[1:]):
    assert j == (a*i+b)%m

r0,s0 = sign_0
r1,s1 = sign_1

# s0k0 = h0 + xr0
# s1k1 = h1 + xr1
# k1 = a*k0 + b%m
# k1 = a*k0 + b + cm
# s1ak0 + s1b + s1cm = h1 + xr1
# s0s1ak0 + s0bs1 + s0cms1 = s0h1 + s0xr1
# s1ah0 + s1axr0 + s0bs1 + s0cms1 = s0h1 + s0xr1
# x(s1ar0-s0r1) = s0h1 - s1ah0 - s0bs1 - s0cms1 % q
# x(s1ar0-s0r1) = s0h1 - s1ah0 - s0bs1 - s0cms1 + dq


h0 = bytes_to_long(sha1(b"Hello").digest())
h1 = bytes_to_long(sha1(b"there").digest())

# x_d = q//2
# k1_d, k2_d = m//2, m//2
# gm_x = min(x_d, q-x_d)
# gm_k1 = min(k1_d, m-k1_d)
# gm_k2 = min(k2_d, m-k2_d)

# INVM = q

# gmi_x, gmi_k1, gmi_k2 = [pow(t,-1,INVM) for t in (gm_x, gm_k1, gm_k2)]

# matrix = [[ -r1, s1, 0, q, 0, 0],
#            [-r2, 0, s2, 0, q, 0],
#            [0,  -a, 1, 0,  0, m],
#            [gmi_x,0,0, 0, 0, 0 ],
#            [0, gmi_k1,0,0,0,0  ],
#            [0,0, gmi_k2, 0,0,0 ]]

# target = [h1, h2, b, x_d*gmi_x, k1_d*gmi_k1, k2_d*gmi_k2]

# from sage.modules.free_module_integer import IntegerLattice

# def Babai_CVP(mat, target):
#     M = IntegerLattice(mat, lll_reduce=True).reduced_basis
#     G = M.gram_schmidt()[0]
#     diff = target
#     for i in reversed(range(G.nrows())):
#         diff -=  M[i] * ((diff * G[i]) / (G[i] * G[i])).round()
#     return target - diff

# X = Babai_CVP(Matrix(ZZ,matrix), vector(ZZ,target))






val1 = h1*s0 - s1*a*h0 - s1*s0*b
val2 = s1*a*r0 -  r1*s0
val3 = s0*s1

## x*val2 = val1 + val3*m*c + dq
## x_m * val2_m = val1_m + d*q_m
## x_q * val2_q = val1_q + val3_q*m*c_q
## x_q * val2_q = val1_q mod m
#r = q%m
## x_r = ((val1%m)*pow(val2%m,-1,r))%r
#x_q = ((val1%q)*pow(val2%q,-1,m))%m

## crtt, modd = crt([r,q],[x_r, x_q])



##pp = (h1*s0 - s1*a*h0 - s1*s0*b)*pow(s1*a*r0 -  r1*s0,-1,q)
#pp = ((h1*s0 - s1*a*h0 - s1*s0*b)%m)*pow((s1*a*r0 -  r1*s0)%m,-1,q)


