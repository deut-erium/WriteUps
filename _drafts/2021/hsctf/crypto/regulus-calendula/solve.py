import pwn
import z3
HOST, PORT = "regulus-calendula.hsc.tf", 1337
REM = pwn.process('python3 regulus-calendula.py',shell=True)

#pow_str = REM.recvuntil(b'Solution?')
#pow_chall = pwn.re.search(b'solve (.*)\n==',pow_str)[1].decode()
#pow_cmd = 'python3 pow.py solve '+pow_chall
#REM.sendline(pwn.process(pow_cmd,shell=True).recvall().split()[1])

BITS = 512

REM.sendline('2')
pub_data = REM.recvuntil(b'e = 65537\n')
n = int(pwn.re.search(b'n = (\d+)\n',pub_data)[1])

P = z3.BitVec('P',2*BITS)
Q = z3.BitVec('Q',2*BITS)
solver = z3.Solver()
solver.add(z3.Extract(2*BITS-1,BITS,P)==0)
solver.add(z3.Extract(2*BITS-1,BITS,Q)==0)
solver.add(P*Q==n)

guesses = '13579bdf'
responses_p = []
for guess in guesses:
    REM.sendline('4')
    REM.sendline(guess*(BITS//4))
    response = REM.recvregex(b'[01]{%d}' % (BITS//4,) )
    response = pwn.re.search(b'[01]{%d}' % (BITS//4,) ,response)[0].decode()
    responses_p.append(response)
    for i in range(BITS//4):
        if response[i]=='1':
            solver.add(z3.Extract(BITS-1-4*i,BITS-4-4*i,P)==int(guess,16))


responses_q = []
for guess in guesses:
    REM.sendline('4')
    REM.sendline(guess*(BITS//4))
    response = REM.recvregex(b'[01]{%d}' % (BITS//4,))
    response = pwn.re.search(b'[01]{%d}' % (BITS//4,), response)[0].decode()
    responses_q.append(response)
    for i in range(BITS//4):
        if response[i]=='1':
            solver.add(z3.Extract(BITS-1-4*i,BITS-4-4*i,Q)==int(guess,16))


