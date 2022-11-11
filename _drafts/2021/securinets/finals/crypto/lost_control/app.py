from Crypto.Cipher import AES
import random
import hashlib
import signal


def is_prime(n):
    _B = [0x2, 0x3, 0x5, 0x7, 0xb, 0xd, 0x11, 0x13, 0x17, 0x1d, 0x1f, 0x25, 0x29, 0x2b, 0x2f, 0x35, 0x3b, 0x3d, 0x43, 0x47, 0x49, 0x4f, 0x53, 0x59, 0x61, 0xc5, 0xc7, 0x1cf,
          0x209, 0x373, 0x463, 0x517, 0x65b, 0x9ad, 0xbe1, 0xc25, 0xc89, 0xd3f, 0xd8d, 0xe6b, 0xfa1, 0x10f1, 0x1127, 0x1645, 0x179b, 0x187f, 0x19b5, 0x19db, 0x19fd, 0x1c8d]

    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for a in _B:
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def send_flag(shared_secret):
    shared_secret = shared_secret.to_bytes(
        (shared_secret.bit_length() + 7) // 8, 'big')
    key = hashlib.sha1(shared_secret).digest()[:16]
    iv = hashlib.sha1(shared_secret).digest()[-16:]
    flag = open("flag.txt", "rb").read()
    return AES.new(key, AES.MODE_CBC, iv).encrypt(flag).hex()


def exchange():
    g = 2
    p = int(input("p = "))

    assert p.bit_length() > 2200 and p.bit_length() < 2500
    assert is_prime(p)

    x = int(input("x = "))
    assert x > 2 and x < p - 2

    user = pow(g, x, p)
    server = pow(g, random.randrange(2, p - 2), p)
    shared_secret = pow(server, x, p)

    print(send_flag(shared_secret))


BANNER = """
 _                  _                              _
| | __  __      ___| |__   __ _ _ __   __ _  ___  | |
| | \ \/ /____ / __| '_ \ / _` | '_ \ / _` |/ _ \ | |
| |  >  <_____| (__| | | | (_| | | | | (_| |  __/ | |
| | /_/\_\     \___|_| |_|\__,_|_| |_|\__, |\___| | |
|_|                                   |___/       |_|

"""
if __name__ == "__main__":
    print(BANNER)
    signal.alarm(20)
    exchange()
