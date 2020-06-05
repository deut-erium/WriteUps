import gmpy2

p = 404993569381
G = (391109997465, 167359562362)
P = (209038982304, 168517698208)
b = 54575449882

diff = (G[1]**2 - P[1]**2) - (G[0]**3 - P[0]**3)
diff = diff % p
a = gmpy2.invert(G[0] - P[0], p) * diff
a = a % p

E = EllipticCurve(GF(p), [a, b])

G = E(G)
P = E(P)
pk = G.discrete_log(P)
print(pk)
G * pk == P
# 17683067357
