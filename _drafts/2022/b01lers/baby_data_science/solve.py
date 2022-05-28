from random import random
import re
import pwn
from pwn import remote
import numpy as np
from scipy.optimize import minimize, LinearConstraint, minimize_scalar, Bounds, dual_annealing
from tqdm import tqdm
pwn.context.log_level=100


HOST, PORT = "ctf.b01lers.com", 9001

def lo(A,B,C):
    D = (B*B-4*A*C)**0.5
    xlo = (-B+D)/(2*A)
    xhi = (-B-D)/(2*A)
    xmid = (xhi+xlo)/2
    print(f"{A=}, {B=} {C=} {xlo=} {xmid=} {xhi=}")



def compute(A,B,C,a,b):
    D = (B*B-4*A*C)**0.5
    xlo = (-B+D)/(2*A)
    xhi = (-B-D)/(2*A)
    xmid = (xhi+xlo)/2
    # print(f'{xlo=}, {xmid=}, {xhi=}')
    N = 1000
    d = (b-a)/N
    x = [0]*(N+1)
    y = [0]*(N+1)
    for i in range(N+1):
        x[i] = a+ i*d
        y[i] = A*x[i]*x[i] + B*x[i] + C

    for i in range(N+1):
        if xlo<=x[i]<=xmid:
            y[i] = y[i]**0.5

    kmax, imax, ymax = -1, -1, 0
    for i in range(N+1):
        if y[i]>ymax:
            ymax = y[i]
            kmax = (ymax - a)//d
            imax = i
    # print(f'{ymax=} {kmax=} {imax=} {x[imax]=}')

    k0 = kmax
    for i in range(imax, -1, -1):
        if y[i]>0:
            continue
        k0 = (y[i]-a)//d
        break
    # print(f'{k0=} {i=} {x[i]=}')
    s = 0
    kprev = kmax
    is_sel = []
    for i in range(N+1):
        # breakpoint()
        if x[i]>xmid:
            continue
        k = (y[i]-a)//d
        if k<k0 or k>kmax or k==kprev:
            continue
        kprev = k
        s += x[i] - xlo
        is_sel.append(i)
    # print(is_sel)
    # print(s,d,s*d)
    s*=d
    return s

def minm(x):
    a,b = x[0], x[1]
    if a>b:
        # return float('inf')
        return 1e300
    if a<-400:
        return float('inf')
    try:
        y = compute(A,B,C,a,b)
        if y==0:
            # return float('inf')
            return 1e300
        return y
    except:
        # return float('inf')
        return 1e300

def minm2(x,bound=-400):
    a,b = -x,x
    if a<-400 or a>b:
        return 1e10-x
    try:
        y = compute(A,B,C,a,b)
        if y==0:
            return 1e10-x
        return y
    except:
        # return float('inf')
        return 1e10-x

def gen():
    A = -1 - random()
    B = 2*random()-1
    if B>0:
        B+=2
    else:
        B-=2
    C = 0.4 + 3*random()
    return A,B,C

x = np.array([-400,0])
# constraint = LinearConstraint([[0,1],[1,0],[-1,1]],[-400,-400,0],[400,400,np.inf])
constraint = LinearConstraint([[0,1],[1,0]],[-400,-400],[400,400])
bounds = [Bounds(-400,400), Bounds(-400,400)]
bounds = [(-400,400), (-400,400)]

# A,B,C = gen()
# lo(A,B,C)

from numpy import arange, meshgrid
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

def objective(x,y):
    try:
        return compute(A,B,C,x,y)
    except:
        return 0

objective = np.vectorize(objective)

def plot(diff=0.1):
    r_mina, r_maxa = -400, 10
    r_minb, r_maxb = -10, 400
    # xaxis = arange(-400, 400, diff)
    xaxis = np.array(sorted(r_mina+ (r_maxa-r_mina)*(np.random.rand(diff))))
    # yaxis = sorted(r_minb+ (r_maxb-r_minb)*(np.random.rand(diff)))
    yaxis = -1*xaxis
    # yaxis = arange(-400, 400, diff)
    x,y = meshgrid(xaxis, yaxis)
    results = objective(x,y)
    print(np.min(results))
    figure = pyplot.figure()
    axis = figure.gca(projection='3d')
    axis.plot_surface(x,y,results,cmap='jet')
    pyplot.show()


# res = {}
# fun_min = float('inf')
# for i in tqdm(np.arange(-400,400,0.01)):
#     v = minimize_scalar(lambda x: minm2(x,i),bounds=(-400,400))
#     if v.fun<fun_min:
#         fun_min = v.fun
#         print(v.fun, i, v.x)
    # res[i] = v

# while True:
#     try:
#         REM = remote(HOST, PORT)
#         data = REM.recvuntil(b'[a,b]: ')
#         A,B,C = map(float,re.search(b'A=(.*)\n  B=(.*)\n  C=(.*)\n', data).groups())
#         if A<-1.9 and C<1:
#             print(A,B,C)
#             a,b = dual_annealing(minm,bounds=((-400,-380),(380,400)),maxiter=1000).x
#             print(a,b)
#             REM.sendline(f'{a},{b}')
#             # REM.sendline(f'{-400+1e-10},{lo(A,B,C)+1e-10}')
#             data = REM.recvall()
#             print(data)
#             if b'flag' in data:
#                 print(data)
#         REM.close()
#     except pwn.exception.PwnlibException:
#         print('failed')
#         continue
# A = -1.9
# B = -2
# C = 0.9
A,B,C =  gen()

# for A in (-1,-2):
#     for B in (-2,2):
#         for C in (0.4,3.4):
#             print(A,B,C)
#             print(dual_annealing(minm,bounds=((-400,-390),(-10,10)),maxiter=2000))
            # print(dual_annealing(minm,bounds=((-10,10),(-10,10)),maxiter=2000))

