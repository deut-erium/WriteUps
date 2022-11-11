import random
g = 820325443930302277
h = 4697802211516556112265788623731306453433385478626600383507434404846355593172244102208887127168181632320398894844742461440572092476461783702169367563712341297753907259551040916637774047676943465204638648293879569

def find_crt(a, m, b, n):
    _, u, v = xgcd(m, n)
    l = (a-b)/gcd(m, n)
    return (b + n*l*v)%lcm(m, n)

def gen_candidates():
    for i in range(500):
        try:
            x = discrete_log(mod(h, Primes()[i]), mod(g, Primes()[i]))
            candidates.append(Primes()[i])
        except:
            continue
    candidates.append(2)


def find_q():
    while True:
        q=1
        while q<2**1024:
            q*=random.choice(candidates[110:])
            if is_prime(q+1):
                break
        if not is_prime(q+1):
            continue
        x = discrete_log(mod(h, q+1), mod(g, q+1))
        if x%2==1:
            return q+1


def find_p():
    while True:
        q=1
        while q<2**1024:
            q*=random.choice(candidates[:110])
            if is_prime(q+1):
                break
        if not is_prime(q+1):
            continue
        x = discrete_log(mod(h, q+1), mod(g, q+1))
        if x%2==1:
            return q+1

def attempt():
    p = find_p()
    q = find_q()
    d = find_crt(discrete_log(mod(h, p), mod(g, p)), p-1, discrete_log(mod(h, q), mod(g, q)), q-1)
    print(gcd(d, (p-1)*(q-1)))
    try:
        e = inverse_mod(d, (p-1)*(q-1))
        print(f"e: {e}")
        print(f"d: {d}")
        print(f"N: {p*q}")
    except:
        print("ERROR")

candidates = []
gen_candidates()
candidates.remove(13)
for i in range(100):
    try:
        attempt()
        break
    except:
        continue
