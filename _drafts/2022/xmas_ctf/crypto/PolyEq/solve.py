import pwn
import ast
from collections import Counter
from sage.all import *
import sympy
import time

start_time = time.time()

WHITELIST = (ast.Load, ast.Tuple, ast.List, ast.Expression, ast.Constant)

def safeeval(expr):
    tree = ast.parse(expr, mode="eval")
    if all(isinstance(i,WHITELIST) for i in ast.walk(tree)):
        return eval(compile(tree,filename="",mode="eval"),{},{})

def get_filters(points,N,total_points,valid_points):
    filters = {}
    for fac in factors:
        counts = [Counter() for _ in range(fac)]
        if fac/(total_points-valid_points)<0.005:
            filters[fac] = []
            for x,y in points:
                counts[x%fac][y%fac]+=1
            for i in range(fac):
                filters[fac].append((i,counts[i].most_common(1)[0][0]))
    return filters

def filter_valid(points,filters):
    res = []
    for x, y in points:
        if all((x%mod,y%mod) in v for mod,v in filters.items()):
            res.append((x,y))
    return res

HOST, PORT = "challs.htsp.ro", 10002
REM = pwn.remote(HOST, PORT)
for _ in range(3):
    print(REM.recvline())
for _ in range(10):
    for _ in range(2):
        print(REM.recvline())

    N = int(REM.recvline().strip().split()[-1])
    total_points = int(REM.recvline().strip().split()[-1])
    valid_points = int(REM.recvline().strip().split()[-1])
    degree = int(REM.recvline().strip().split()[-1])
    points = safeeval(REM.recvline().strip().split(b" = ")[-1])
    factors = list(sympy.factorint(N).keys())
    print(factors)


    filtered_points = filter_valid(points, get_filters(points,N,total_points,valid_points))
    print(len(filtered_points))

    PR = PolynomialRing(Zmod(N), names=[f"a{i}" for i in range(degree)] + [f"b{i}" for i in range(degree)])
    a_list, b_list = PR.gens()[:degree], PR.gens()[degree:]
    mat = matrix(Zmod(N), len(filtered_points), 2*degree)
    vec = vector(Zmod(N), len(filtered_points))
    for i,(x,y) in enumerate(filtered_points):
        poly_numer = x**degree
        for j in range(degree):
            a = a_list[j]
            poly_numer += a * x**j
        poly_denom = x**degree
        for j in range(degree):
            b = b_list[j]
            poly_denom += b * x**j
        coeffs = [(poly_denom * y - poly_numer).coefficient(elem)  for elem in a_list + b_list]
        assert len(coeffs) == 2*degree
        const = (poly_denom * y - poly_numer).constant_coefficient()
        for j in range(2*degree):
            mat[i, j] = coeffs[j]
        vec[i] = -const


    while True:
        indices = sample(range(len(filtered_points)),2*degree)
        M = matrix(Zmod(factors[-1]), 2*degree, 2*degree)
        V = vector(Zmod(factors[-1]), 2*degree)
        for i,v in enumerate(indices):
            M[i] = mat[v]
            V[i] = vec[v]
        try:
            tmp = M.solve_right(V)
        except:
            continue
        if Counter((mat*tmp -vec).list())[0] >= valid_points:
            print("found")
            print(time.time()-start_time)
            break

    rkm,c,VS = {},{},{}
    for fac in factors:
        M = matrix(Zmod(fac), 2*degree, 2*degree)
        V = vector(Zmod(fac), 2*degree)
        for i,v in enumerate(indices):
            M[i] = mat[v]
            V[i] = vec[v]
        c[fac] = M.solve_right(V)
        rkm[fac] = M.right_kernel_matrix()
        VS[fac] = VectorSpace(Zmod(fac), rkm[fac].nrows())

    vi = {}
    for fac in factors:
        vi[fac] = c[fac]
    for fac in factors:
        vi[fac] += (VS[fac].random_element())*rkm[fac]
    v = []
    for i in range(2*degree):
        v.append(crt([int(vi[fac][i]) for fac in factors],factors))

    REM.sendline(" ".join(map(str,v[:degree])))
    REM.sendline(" ".join(map(str,v[degree:])))

REM.interactive()
#X-MAS{Spl1771ng_1nt0_gr0up5_b453d_0n_2_3_4nd_5_1s_cl3v3r_4ls0_nu11_p0lyn0m14ls_4r3_4_m3m3}




