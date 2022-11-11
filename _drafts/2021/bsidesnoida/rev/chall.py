charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{}"

def enc(s, a, b):
    index = []
    out = ""
    for i in range(len(s)):
        index.append(charset.index(s[i]))
    for i in range(len(index)):
        out += charset[(index[i] * a + i + b) % len(charset)]
    return out

#c = a*p+b % v
#a*p = c-b
# p = c/a - b/a

# ainv = pow(a,-1,v)
# p = ainv *c - b*ainv
a*ainv = 1%v

def dec(s, a, b):
    ainv = pow(a,-1,65)
    binv = (-b*ainv)%65
    index = []
    out = ""
    for i in range(len(s)):
        index.append(charset.index(s[i])-i)
    for i in range(len(index)):
        out += charset[(index[i] * ainv + binv) % len(charset)]
    return out

flag_enc = 'Ri}uXETL3fxnRXnCNHgVHJwwVzN6EGsYTeCg07LSr8y'
flag_pref = 'BSNoida{'
orig_pos = [charset.index(i) for i in flag_pref]
pos = [charset.index(i) for i in flag_enc]

for i in range(65):
    for j in range(65):
        try:
            x = dec(flag_enc,i,j)
        except:
            continue
        if x.startswith('BSNoida'):
            print(x,i,j)

