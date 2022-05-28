from output import *
from sympy import jacobi_symbol

pbits, qbits = [],[]
for i in range(512):
    if jacobi_symbol(enc_pq[i],N)==1:
        pbits.append(0)
    else:
        pbits.append(1)


for i in range(512):
    if jacobi_symbol(enc_pq[512+i],N)==1:
        qbits.append(0)
    else:
        qbits.append(1)

p_msb = int( "".join(map(str,pbits)),2)
q_lsb = int( "".join(map(str,qbits)),2)


from z3 import *
p_msbc = BitVecVal(p_msb,512)
q_lsbc = BitVecVal(q_lsb,512)
zeroc = BitVecVal(0,1024)
p_full = BitVec('p',1024)
q_full = BitVec('q',1024)
plsb = BitVec('plsb',512)
qmsb = BitVec('qmsb',512)
s = Solver()
s.add(Concat(p_msbc,plsb)==p_full)
s.add(Concat(qmsb,q_lsbc)==q_full)
s.add( Concat(zeroc,p_full)*Concat(zeroc,q_full)==N)
if s.check()==sat:
    print(s.statistics())
    m = s.model()
    p = m[p_full].as_long()
    q = m[q_full].as_long()
    assert p*q==N

# p = BitVec('p',2048)
# q = BitVec('q',2048)

# s = Solver()
# s.add([p>0,p<2**1024])
# s.add([q>0,q<2**1024])
# s.add([p*q==N])
# s.add(Extract(511,0,q)==q_lsb)
# s.add(Extract(1023,512,p)==p_msb)

# if s.check()==sat:
#     print(s.statistics())
#     m = s.model()
#     p = m[p].as_long()
#     q = m[q].as_long()
#     assert p*q == N

phi = (p-1)*(q-1)
d = pow(e,-1,phi)
msg = pow(c,d,N)
print(msg.to_bytes( (msg.bit_length()+7)//8,'big'))

