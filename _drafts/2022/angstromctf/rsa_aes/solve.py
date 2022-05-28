from pwn import remote, re, process
from sympy import nextprime
import sys
from math import prod
HOST, PORT = "challs.actf.co", 31500

# REM = remote(HOST, PORT)
n = 0xbb7bbd6bb62e0cbbc776f9ceb974eca6f3d30295d31caf456d9bec9b98822de3cb941d3a40a0fba531212f338e7677eb2e3ac05ff28629f248d0bc9f98950ce7e5e637c9764bb7f0b53c2532f3ce47ecbe1205172f8644f28f039cae6f127ccf1137ac88d77605782abe4560ae3473d9fb93886625a6caa7f3a5180836f460c98bbc60df911637fa3f52556fa12a376e3f5f87b5956b705e4e42a30ca38c79e7cd94c9b53a7b4344f2e9de06057da350f3cd9bd84f9af28e137e5190cbe90f046f74ce22f4cd747a1cc9812a1e057b97de39f664ab045700c40c9ce16cf1742d992c99e3537663ede6673f53fbb2f3c28679fb747ab9db9753e692ed353e3551
e = 0x10001
REM = process('python3.10 rsaaes2.py',shell=True)

# n = int(REM.recvline())
p = int(REM.recvline())
q = int(REM.recvline())
n = p*q
enc = int(REM.recvline())
delim_mess = b'Enter message to sign:'
REM.recvuntil(delim_mess)



def get_enc_len(m):
    REM.sendline(str(m))
    REM.recvline()
    enc_line = REM.recvline().decode()
    enc_len = len(eval(enc_line))
    REM.recvuntil(delim_mess)
    return enc_len

def is_factor_of_m(i):
    enc_len_recv = get_enc_len((pow(i,-e,n)*enc)%n)
    print(enc_len_recv)
    return enc_len_recv != 272

def is_factor_of_km(k,i):
    enc_len_recv = get_enc_len((pow(i,-e,n)*enc*pow(k,e,n))%n)
    print(enc_len_recv)
    return enc_len_recv != 272

def read_flag_value():
    with open('flag_factors.txt2','r') as flag_file:
        flag_facs = set(map(eval,flag_file.read().strip().split('\n')))
    return prod([i[2] for i in flag_facs]), [i[2] for i in flag_facs]



# prime = 2
# flag = 1
# flag = 3*41*71*607*6299*6673*11311*11489*14951*16091*17977*19079*20233*23011\
#       *27919*28277*29537*29599*35963*36847*37589*40903
# primes = [3,41,71,607,6299,6673,11311,11489,14951,16091,17977,19079,20233,23011,27919,28277,29537,29599,35963,36847,37589,40903]
if len(sys.argv)>1:
    prime = int(sys.argv[1])
    primeend = int(sys.argv[2])
    flag, flag_facs = read_flag_value()
else:
    flag = 1
    prime = 2
    primeend = 10**6
    facs = []
while True:
    print(f'Trying prime: {prime}')
    i = 1
    while is_factor_of_m(prime**i):
        i+=1
    if i>1:
        print(f"{prime}^{i-1} is factor of flag")
        with open('flag_factors2.txt', 'a') as flag_file:
            flag_file.write(f'{prime,i-1,prime**(i-1)}\n')
        flag *= prime**(i-1)
        facs.append(prime**(i-1))
        # flag, flag_facs = read_flag_value()
        flag_bytes = flag.to_bytes((flag.bit_length()+7)//8,'big')
        print('flag bits:',flag_bytes)
        if flag_bytes.startswith(b'actf'):
            break
    prime = nextprime(prime)
    if prime>primeend:
        break

# flag, flag_facs = read_flag_value()
# flag_facs = sorted(flag_facs)
# flag_facs2 = []
# flag = 1
# for fac in flag_facs:
#     if is_factor_of_km(2,fac):
#         flag_facs2.append(fac)
#         flag *= fac
#         flag_bytes = flag.to_bytes((flag.bit_length()+7)//8,'big')
#         # if flag_bytes.startswith(b'actf'):
#         print(len(flag_bytes),flag_bytes)


# [[195479,200000],[209659,220000],[229403,240000],[248987,260000],
# [269039,280000],[286673,300000],[306359,320000]]

