import base64
import gmpy2
OUTPUT = """
-*-*-*- BEGIN ARR ESS AYY MSG -*-*-*-
     0000000000000000000000000000000
     0000000000000000000000000000000
     0000000000000000000000000000000
     0000000000000000000000000000000
     0000000000000000000000000000000
     00000s&nYASMBl==Raa6f1mSybO1&`P
     n=MSlA^HVasQovKL?f9nB=?Wjz*-}bj
     4rNeU}9v(Tcn16Ji;Mjv?)4T@pD@76=
     9j%)LevT&=&p%BMcIckO@P450UqkjIR
     6DT^igJmh5<xI<alHa3p;VuZ%5HWp>1
                #T6e(?T*2I
                  00962
     jx@>fERjV6gRSH!+pdv<kOoEVD#<P05
     <nAMIT@fYQOcbQ{VfQh+sli_--_zE8)
     G@9Y^2j=XLkGz;kZTPS&eJtOKwM~!V6
     SmtDRCJ%568a_utlnc?ywyQ^??W!-Ro
     `%%d9c?q+nQ*s<4Sn4@*0vXe9sl<*c8
                  *WY0^
-*-*-*- END ARR ESS AYY MSG -*-*-*-
"""


def encrypt(message):
    p, q = rsa.prime_pair(bits=1024)
    ct = base64.b85encode(
        rsa.encrypt(
            rsa.solve_for(
                p=p,
                q=q,
                e=e),
            message.encode()))
    ct = b'\n'.join(ct[i:i + 31].center(41)for i in range(0, len(ct), 31))
    p, q = int.to_bytes(p, 128, 'big'), int.to_bytes(q, 128, 'big')
    s, key = 0, bytearray()
    for(i, j) in zip(p, q):
        key.append(i ^ s)
        key.append((j ^ (s := s ^ i), s := s ^ j)[0])
    key = base64.b85encode(key)
    key = b'\n'.join(key[i:i + 31].center(41)for i in range(0, len(key), 31))
    e_str = base64.b85encode(int.to_bytes(e, 4, 'big')).center(41)
    return b'  -*-*-*- BEGIN ARR ESS AYY MSG -*-*-*-\n' + key + b'\n' + \
        e_str + b'\n' + ct + b'\n' + b'   -*-*-*- END ARR ESS AYY MSG -*-*-*-\n'


key_part = """
     0000000000000000000000000000000
     0000000000000000000000000000000
     0000000000000000000000000000000
     0000000000000000000000000000000
     0000000000000000000000000000000
     00000s&nYASMBl==Raa6f1mSybO1&`P
     n=MSlA^HVasQovKL?f9nB=?Wjz*-}bj
     4rNeU}9v(Tcn16Ji;Mjv?)4T@pD@76=
     9j%)LevT&=&p%BMcIckO@P450UqkjIR
     6DT^igJmh5<xI<alHa3p;VuZ%5HWp>1
                #T6e(?T*2I
"""

e_str_part = """00962"""

ct_part = """
     jx@>fERjV6gRSH!+pdv<kOoEVD#<P05
     <nAMIT@fYQOcbQ{VfQh+sli_--_zE8)
     G@9Y^2j=XLkGz;kZTPS&eJtOKwM~!V6
     SmtDRCJ%568a_utlnc?ywyQ^??W!-Ro
     `%%d9c?q+nQ*s<4Sn4@*0vXe9sl<*c8
                  *WY0^
"""

key_b85 = "".join(i for i in key_part.strip().split()).encode()
key = base64.b85decode(key_b85)
e = int.from_bytes(base64.b85decode(e_str_part.encode()), "big")
ct_b85 = "".join(i for i in ct_part.strip().split()).encode()
ct = int.from_bytes(base64.b85decode(ct_b85), "big")


def get_pq(key):
    s = 0
    p = bytearray()
    q = bytearray()
    for i in range(0, len(key), 2):
        a, b = key[i:i + 2]
        p.append(a ^ s)
        q.append(a ^ b)
        s = b
    return int.from_bytes(p, 'big'), int.from_bytes(q, 'big')


p, q = get_pq(key)
phi = (p - 1) * (q - 1)
d = gmpy2.invert(e, phi)
m = pow(ct, d, p * q)
print(bytes.fromhex(hex(m)[2:]))
