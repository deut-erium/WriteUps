load("message.py")

mat = Matrix(Zmod(N),3,3)
res = vector(Zmod(N),3)
known = b"Cyber"
for i in range(3):
    a,b = known[i],ct[i+1]
    mat[i] = [3*a**6, 3*a**3, 1]
    res[i]=b-a**9

xx = mat.solve_right(res)[0]

flag = bytearray()

decs = {}
for i in range(256):
    decs[int(pow(xx+i**3,3,N))]=i

for i in ct[1:]:
    flag.append(decs[i])

print(flag)

