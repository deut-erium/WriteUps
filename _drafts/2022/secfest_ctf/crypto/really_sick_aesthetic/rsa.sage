from morfarshatt import flagga

g = lambda k: random_prime(2^k) * random_prime(2^k)
r = lambda m: randint(1, m)

n1 = g(512)
n2 = g(512)
n3 = g(512)

m = min(n1, n2, n3)
a, b = r(m), r(m)
c, d = r(m), r(m)

x = int.from_bytes(flagga, byteorder='big')
assert(x < m)

c1 = pow(x, 3, n1)
c2 = pow(a*x + b, 3, n2)
c3 = pow(c*x + d, 3, n3)

print(f'n1, n2, n3 = {n1}, {n2}, {n3}')
print(f'a, b, c, d = {a}, {b}, {c}, {d}')
print(f'c1, c2, c3 = {c1}, {c2}, {c3}')
print(f'{len(flagga)}')