import pwn
HOST, PORT = "157.245.45.46",32123

REM = pwn.remote(HOST, PORT)

VALID_PRIMES = list(prime_range(2**4, 2**6))
REM.recvuntil(b'[C]heat\n\n>')
REM.sendline(b'T')
REM.recvuntil(b'[C]heat\n\n>')

REM.sendline(b"C")
REM.recvline()
ct = eval(REM.recvline())
key = eval(REM.recvline())

max_num = max(max( max(i) for i in key), max( max(i) for i in ct))
prob_prime = next_prime(max_num)

prob_pt = matrix(GF(prob_prime),ct) * (matrix(GF(prob_prime),key)^-1)
prob_pt_list = [int(j) for row in prob_pt for j in row]
assert prob_pt_list[0] == ord("H")%prob_prime
assert prob_pt_list[1] == ord("T")%prob_prime
assert prob_pt_list[2] == ord("B")%prob_prime
assert prob_pt_list[3] == ord("{")%prob_prime
assert prob_pt_list[-1] == ord("}")%prob_prime

FLAG = b"HTB{l00k_@t_7h3_st4rs!!!}"

