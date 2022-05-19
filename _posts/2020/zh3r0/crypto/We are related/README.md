# We are related

## Description
```
I can help you send related messages can you out what it is?
nc crypto.zh3r0.ml 9841
```

Lets quickly take a look into server functionality  
```bash
nc crypto.zh3r0.ml 9841
__        __   _                            _
\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \
  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) |
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/

 ______     _____       ___     ____ _____ _____
|__  / |__ |___ / _ __ / _ \   / ___|_   _|  ___|
  / /| '_ \  |_ \| '__| | | | | |     | | | |_
 / /_| | | |___) | |  | |_| | | |___  | | |  _|
/____|_| |_|____/|_|   \___/   \____| |_| |_|

Enter the Selection from below:
1.Print PublicKey
2.Encrypt
0.Exit
1
-----BEGIN PUBLIC KEY-----
MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAl/DEzNkDSy545CVnRDY6
MvnY3uT9AqXvUawLjvPxkpGFvjNZgXUZDXz4d+OM+kI0wCitG/qKKyALNBCRV4H1
Ff032MF4M83DZauv9mekDRYTHt1kc3yjXGgkDKrbwx/52oK1zzjDpdL35+0DGrCV
MuM6UUGmwULkt9pwkltaQ7CnK/mD8r9/kxCvYrsOdXKfG7oa6M8jmJ2Fg8KI30K7
BNLBQnrHEd+gk9cbeZO2EPfCgpeRBIkpN/m+wCaVeF4MhvHAqO7WY8HWGnWOXTvX
s/s38/18neVZpi6sb+Xzd5bS3MXF6LAYnpsPFtlZQwkef0isv+fIbRehCBxOOXMO
cwIBAw==
-----END PUBLIC KEY-----
-
Enter the Selection from below:
1.Print PublicKey
2.Encrypt
0.Exit
2
Enter the string to encode: aaaaaa
Enc(flag + txt )=  6206434071172505020021970772953615274504334618015850893501208311915363726686848515553986827818840777322925424926979762114547563428575373316823436264390618726357037373547355224955186906604510511057750940859368577315593137395494135555748795713395693917243830787165763621456651998712558904600314030829240201187963545224252359593829242514527608390145873952760068476345341078313609446375182958802547847816648040378023443406558254598065981874822402697576681531448937375068150529057221519687478093391435441533870228158151564000522594159404647707671836726663992796867568542231674041333345847098215658414243656674504238331618
Enter the Selection from below:
1.Print PublicKey
2.Encrypt
0.Exit
0
BYE

```
So it works as following
- It gives out rsa public key, from which we can get `N` and `e`
- Gives out rsa encryption of `flag + input`

Seems like a nice application of [Franklin reiter Related message attack](https://en.wikipedia.org/wiki/Coppersmith%27s_attack#Franklin-Reiter_related-message_attack), which is  
If we have two linearly related messages, and their corresponding ciphertexts and a small exponent `e`, we can figure out the messages by factoring the polynomial  

Plan of actions go as follows:-
- Get public key, parse out `N` and `e`
- Get the encryption of `flag + ""` 
- Get the encryption of `flag + "a"` a small message
- So we have two messages, `int(flag) and 256*int(flag)+ord('a')`

```python
from pwn import remote
from Crypto.PublicKey import RSA
from base64 import b64decode
import re

HOST, PORT = "crypto.zh3r0.ml", 9841
REM = remote(HOST, PORT)

data = REM.recvuntil(b'0.Exit')
print(data.decode())

REM.sendline(b'1')
pub_key = REM.recvuntil(b'-----END PUBLIC KEY-----\n').strip()

rsa = RSA.importKey(b64decode(pub_key.split(b'\n-----END PUBLIC KEY-----\n')[0].split(b'-----BEGIN PUBLIC KEY-----')[1]))
print(pub_key.decode())

N = rsa.n
E = rsa.e

REM.sendline(b'2')
REM.sendline()
REM.sendline(b'2')
REM.sendline(b'a')
REM.sendline(b'0')
data = REM.recvuntil(b'BYE')
print(data.decode())

C1, C2 = map(int, re.findall(b'(\d+)\n',data))
```
This part of the calculation I did it in sage
```
diff = ord('a')
R.<X> = Zmod(n)[]
f1 = X^3 - C1
f2 = (256*X + r)^3 - C2
def my_gcd(a, b):
     return a.monic() if b == 0 else my_gcd(b, a % b)
mint=-my_gcd(f1, f2).coefficients()[0]
print(bytes.fromhex(hex(mint)[2:]).decode())

# mint = 84490476860330212673060501801652621134953572462322324101674679636525065183282486185148354532461487912067725608302199264119177290786545985493246692410205660189434658580866030237305212940461964070200849268673142227118980326807902129431038850502565588905103675210898161818686994591193583661769377667810413989357162402550803291023005993338743213389843385122094
# "RSA is secure and all but the only thing I want to say is zh3r0{Hey_y0u_Sh0u1dn't_S3nd_r3l4ted_m3ssag3s_0r_h4v3_shot_p4ddings_wh3n_e_1s_sm411!!!!!}.
```

### zh3r0{Hey_y0u_Sh0u1dn't_S3nd_r3l4ted_m3ssag3s_0r_h4v3_shot_p4ddings_wh3n_e_1s_sm411!!!!!}
