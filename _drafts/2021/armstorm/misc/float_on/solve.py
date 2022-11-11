from z3 import *
import struct

d2l = lambda x:struct.unpack('L',struct.pack('d',x))

x = FP('x',FloatDouble())

nan = float('nan')
inf = float('inf')
minf = -float('inf')

def long_get_cond(conds):
    s = Solver()
    s.add(conds)
    if s.check()==sat:
        m = s.model()
        float_x = str(m[m.decls()[0]])
        if float_x=='NaN':
            float_x=nan
        elif float_x=='+oo':
            float_x=inf
        elif float_x=='-oo':
            float_x=minf
        else:
            float_x = eval(float_x)
        return d2l(float_x)

conds = [
    [x==-x],
    [x!=x],
    [x+1==x,x*2==x],
    [x+1==x,x*2!=x],
    [(1+x)-1!=1+(x-1)],
]
