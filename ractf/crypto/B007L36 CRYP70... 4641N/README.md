# B007L36 CRYP70... 4641N

After finally solving [B007l3G CRYP70](https://github.com/deut-erium/WriteUps/tree/master/ractf/crypto/BOO7l3G%20CRYP70), we are again presented with another variant. The description reads as follows:-

```
As you continue your pentest of MEGACORP, you make your way to an 
admin-only subnet of the network. There, you find yet another custom
crypto implementation. You also previously found this zip file on a 
user's desktop. Solving this may be the last step to gaining full 
access to the company's network
```
And [encryption_service.zip](encryption_service.zip), the contents of which are :-  

[ciphertext.txt](ciphertext.txt)
```
w4bDkMKDw6jDi8Ouw6JQw6jDh8OZwojCmMONw4nDnsKtwqnDk8OiwqLDosKdw6XDhsOVw6
rDj8Oew5NcwpTDhMOiw4vCpcOYw5bDoFTCrcOHw6LCpsKUw6PDm8ONw4jClMOdw6TDosKY
wpTDmMOjw53CpX/DicObwqHCqcOAw6fCrMKUw6bDpcOUw5jDmcOKwpvDocKVw5fDkcOZw5
xTw4rDi8OlVMKaw43DnVPDmcOrw6XDlsOVw5nChsOvw5bCkcOof8Odw5xTw5HDi8OfwqnC
pcOTw6xTw53Dq8KSw5XDi8OZwobDnsOXwqDDnMOEw6bDnMKYw5fDmsKawqjCscOTwpnCmc
Odw6nDl8KP
```
[plaintext.txt](plaintext.txt)
```
To test the encryption service, encrypt this file with your company 
issued secret key and ensure that it results in the ciphertext.txt file.
```
Aand a [password.txt](password.txt)
```
w6TDgsOGw6jDjMO2w5RgwqTDi8OTw5Vmwr7CncOjZcKcwpLDmGjDnMKxw5/ClMOCwqTDlMOaw5tjw7E=
```

Lets first begin with by checking some stuff like we did in [B007l3G CRYP70]() with the encryption service
```
Please enter the secret key to encrypt the data with: a
Please enter the data that you would like to encrypt: a
Your encrypted message is: w4I=

Please enter the secret key to encrypt the data with: b
Please enter the data that you would like to encrypt: a
Your encrypted message is: w4M=
```
Notice the encrypted message appears to be base64 encoded.  
Lets check the decoded values

```python
from base64 import b64decode as d64
d64('w4M=')
# b'\xc3\x83'
d64('w4I=')
# b'\xc3\x82'
```
EWW, looks odd probably because of [unicode](https://en.wikipedia.org/wiki/Unicode). Lets deal with string-objects instead of byte-objects by simply calling `decode()`

```python
from base64 import b64decode as d64
d64('w4M=').decode()
# 'Ã'
d64('w4I=').decode()
# 'Â'
ord('Ã')
# 195
ord('Â')
# 194
```

Hehe, we start getting a hint already, changing the key by 1, encryption changes by 1. There is probably something *Very Linear* about the encryption.

To help with encryption process, I created a small helper function `encrypt`which calls encrypt on the server and return the `ord` values of base64 decoded string.

```python
from pwn import remote
from base64 import b64decode as d64
from base64 import b64encode as e64

HOST, PORT = "95.216.233.106", 60246

with open('password.txt', 'r') as password_file:
    password = d64(password_file.read().strip()).decode()

with open('ciphertext.txt', 'r') as ciphertext_file:
    ct = d64(ciphertext_file.read().strip()).decode()

with open('plaintext.txt', 'r') as plaintext_file:
    pt = plaintext_file.read().strip()

REM = remote(HOST, PORT)
print(REM.recvline())
print(REM.recvline())

def encrypt(pt, key):
    REM.recvuntil(b'data with:')
    REM.sendline(key)
    REM.sendline(pt)
    data = REM.recvuntil(b'\n\n')
    encrypted = data.split(b'message is: ')[-1].strip()
    return [ord(i) for i in d64(encrypted).decode()]
```

Lets play around a little bit more...
```python
>>> encrypt(b'aaaa','a')
[194, 194, 194, 194]
>>> encrypt(b'aaaa','ab')
[194, 195, 194, 195]
>>> encrypt(b'aaaa','abcd')
[194, 195, 196, 197]
>>> encrypt(b'abcd','aaaa')
[194, 195, 196, 197]
```
We can make the following observations :-
* `key` is repeated if `plaintext` is longer than the `key`
* The encryption is changed only by 1 on varying either `key` or `plaintext` by 1
* The `key`, `plaintext` and `ciphertext` are related just by an addition modulo 256

So, all we need to do now is to figure out what the provided files mean.  
Let us try checking the key with which [ciphertext.txt](ciphertext.txt) and [plaintext.txt](plaintext.txt) are related.  

```python
ct_arr = [ord(i) for i in ct]
pt_arr = [ord(i) for i in pt]
diff_arr = [ct_arr[i] - pt_arr[i] for i in range(len(ct_arr))]
print("".join(chr(i) for i in diff_arr))
```
`ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ractf{n0t_th3_fl49_y3t}ra`

YES, it indeed verifies all our hypothesis and we now know the `company issued secret key` is `ractf{n0t_th3_fl49_y3t}`

Lets quickly decrypt the contents of [password.txt](password.txt) with the key
```python
key = "ractf{n0t_th3_fl49_y3t}"
flag = "".join( chr(ord(password[i]) - ord(key[i%len(key)])) for i in range(len(password)) )
print(flag)
```
And we finally get our flag `ractf{f00l_m3_7w1c3_5h4m3_0n_m3}`  
CHEERS YOU ALL!
