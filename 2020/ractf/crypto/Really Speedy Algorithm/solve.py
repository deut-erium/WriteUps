from pwn import remote
from gmpy2 import invert

#HOST, PORT = "95.216.233.106" ,62467
HOST, PORT = "139.59.190.222", 31337
REM = remote(HOST, PORT)


def recieve():
    n = None
    p = None
    q = None
    ct = None
    pt = None
    e = None
    d = None
    phi = None
    param = None
    while True:
        data = REM.recvn(3).decode()
        print(data, end="")
        if data.startswith('[!]'):
            print(REM.recvline().decode().strip())
            print(REM.recvline().decode().strip())
        elif data.startswith('[:]'):
            param_name = REM.recvuntil(b': ').decode().strip()[:-1]
            print(param_name)
            val = int(REM.recvline().decode().strip())
            if param_name == 'n':
                n = val
            elif param_name == 'p':
                p = val
            elif param_name == 'q':
                q = val
            elif param_name == 'ct':
                ct = val
            elif param_name == 'pt':
                pt = val
            elif param_name == 'phi':
                phi = val
            elif param_name == 'e':
                e = val
            elif param_name == 'd':
                d = val
        elif data.startswith('[?]'):
            param = REM.recvuntil(b': ').decode().strip()[:-1]
            print(param)
            return (n, p, q, ct, pt, e, d, phi, param)
            break
        elif data.startswith('[*]') or data.startswith('[c]'):
            print(REM.recvline().decode().strip())
        else:
            print(data)
            print(REM.recvall().decode().strip())
    return (n, p, q, ct, pt, e, d, phi, param)


def solve(values):
    print(values)
    n, p, q, ct, pt, e, d, phi, param = values
    if param == 'pt':
        d = invert(e, phi)
        q = phi // (p - 1) + 1
        n = p * q
        pt = pow(ct, d, n)
        return pt
    elif param == 'ct':
        ct = pow(pt, e, p * q)
        return ct
    elif param == 'q':
        return n // p
    elif param == 'p':
        return n // q
    elif param == 'n':
        return p * q
    elif param == 'd':
        phi = (p - 1) * (q - 1)
        return int(invert(e, phi))
    else:
        print("NOT IMPLEMENTED", param)


def send(val):
    REM.sendline(str(val).encode())


while True:
    rec = solve(recieve())
    print(rec)
    send(rec)
