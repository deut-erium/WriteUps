import math
import hashlib
from Crypto.Cipher import AES
import sympy
import sys
sys.set_int_max_str_digits(100000)

ENC_MSG = open('msg.enc', 'rb').read()
NUM_HASH = "636e276981116cf433ac4c60ba9b355b6377a50e"

# @lru_cache
def f(i):
    if i < 5:
        return i+1

    return 1905846624*f(i-5) - 133141548*f(i-4) + 3715204*f(i-3) - 51759*f(i-2) + 360*f(i-1)

def f_symb(n,a,b,c,d,e):
    res = [a,b,c,d,e]
    for i in range(n):
        res.append(1905846624*res[0] - 133141548*res[1] + 3715204*res[2] - 51759*res[3] + 360*res[4])
        res = res[1:]
    return res[0]

fi = sympy.symbols('f1:6')

MOD = pow(10,31337)
mat = []
for i in range(5):
    symb = f_symb(5+i, *fi)
    mat.append([int(symb.coeff(j)) for j in fi])

def matmul(a,b):
    n,m = len(a),len(b[0])
    res = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(b)):
                res[i][j] += a[i][k]*b[k][j]
                res[i][j] %= MOD
    return res

def matadd(a,b):
    n = len(a)
    res = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            res[i][j] = a[i][j]+b[i][j]
    return res

def identity(n):
    res = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    return res

def matexp(a,n):
    if n==1:
        return a
    if n==0:
        return identity(len(a))
    tmp = matexp(a,n//2)
    res = matmul(tmp,tmp)
    if n&1:
        res = matmul(res,a)
    return res


def fexp(n):
    m = matexp(mat,n//5)
    return matmul(m, [[1],[2],[3],[4],[5]])[n%5][0]


# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % pow(10,31337)
    sol = str(sol)
    num_hash = hashlib.sha1(sol.encode()).hexdigest()
    key = hashlib.sha256(sol.encode()).digest()
    if num_hash != NUM_HASH:
        print('number not computed correctly')
        exit()
    iv = b'\x00'*16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg_dec = cipher.decrypt(ENC_MSG)
    print(msg_dec)

if __name__ == "__main__":
    # ret = f(13371337)
    ret = fexp(13371337)
    decrypt_flag(ret)

#flag{3f04dfb7f06a4d57a6b6150bdd61dfcd}

