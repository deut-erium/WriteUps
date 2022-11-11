"""Miller Rabins pseudo prime generation"""
from itertools import combinations
from random import shuffle
from argparse import ArgumentParser
from Crypto.Util.number import inverse
from sympy import primerange, isprime
from sympy.ntheory.modular import crt

def rand_combinations(iterable,r):
    combs = list(combinations(iterable,r))
    shuffle(combs)
    return combs


def generate_basis(base):
    """
    Generate a basis for base
    """
    basis = [True] * base
    for i in range(3, int(base**0.5) + 1, 2):
        if basis[i]:
            basis[i * i::2 * i] = [False] * ((base - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, base, 2) if basis[i]]


def miller_rabin(number, base):
    """
    Miller Rabin test testing over all
    prime basis < base
    """
    basis = generate_basis(base)
    if number in (2, 3):
        return True
    if number % 2 == 0:
        return False
    r, s = 0, number - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for base in basis:
        x = pow(base, s, number)
        if x in (1, number - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                break
        else:
            return False
    return True

def miller_rabin2(n,base):
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



def legendre(a, p):
    k = pow(a, (p - 1) // 2, p)
    if k == 0:
        return 0
    if k == 1:
        return 1
    return -1


def intersect(k2, k3, a):
    return RESIDUES[a].intersection(
        {(inverse(k2, 4 * a) * (i + k2 - 1)) % (4 * a) for i in RESIDUES[a]})\
        .intersection({(inverse(k3, 4 * a) * (i + k3 - 1)) % (4 * a) for i in RESIDUES[a]})


def all_possible_RESIDUES(k2, k3, list_of_a):
    return [sorted(list(intersect(k2, k3, a))) for a in As]


def select_combination(all_RESIDUES):
    first_res = all_RESIDUES[0][0]
    residue_selection = [first_res]
    for i in range(1, len(all_RESIDUES)):
        for residue in all_RESIDUES[i]:
            if (residue - first_res) % 4 == 0:
                residue_selection.append(residue)
                break
        if len(residue_selection) == i:
            return None  # unsuitable RESIDUES
    return residue_selection


def crt_comb(comb, list_of_a, k2, k3):
    return crt(
        [4 * a for a in list_of_a] + [k3, k2],
        comb + [inverse(-k2, k3), inverse(-k3, k2)])


def gen_pseudo_prime(nbit, base):
    global RESIDUES
    primes = list(primerange(1, 10000))
    #list_of_a = list(primerange(1, base))
    list_of_a = [0x2, 0x3, 0x5, 0x7, 0xb, 0xd, 0x11, 0x13, 0x17, 0x1d, 0x1f, 0x25, 0x29, 0x2b, 0x2f, 0x35, 0x3b, 0x3d, 0x43, 0x47, 0x49, 0x4f, 0x53, 0x59, 0x61, 0xc5, 0xc7, 0x1cf,
          0x209, 0x373, 0x463, 0x517, 0x65b, 0x9ad, 0xbe1, 0xc25, 0xc89, 0xd3f, 0xd8d, 0xe6b, 0xfa1, 0x10f1, 0x1127, 0x1645, 0x179b, 0x187f, 0x19b5, 0x19db, 0x19fd, 0x1c8d]
    list_of_k = list(primerange(100, base * 2))
    list_of_k = [i for i in primerange(1,0x1c8d) if i not in list_of_a]
    RESIDUES = {a: {p % (4 * a) for p in primes if legendre(a, p) == -1}
                for a in list_of_a}

    for k2, k3 in rand_combinations(list_of_k, 2):
        all_pos = [sorted(list(intersect(k2, k3, a))) for a in list_of_a]
        if all(all_pos):
            residue_selection = select_combination(all_pos)
            if not residue_selection:
                continue
            else:
                val, mod = crt_comb(residue_selection, list_of_a, k2, k3)
                initial_bitlength = (
                    nbit - k3.bit_length()) // 3 - mod.bit_length()
                initial_bitlength = max(initial_bitlength,0)
                i = 2**initial_bitlength
                print(i,mod)
                print(k2,k3)
                while True:
                    prime1 = val + i * mod
                    prime2 = k2 * (prime1 - 1) + 1
                    prime3 = k3 * (prime1 - 1) + 1
                    if isprime(prime1) and isprime(prime2) and isprime(prime3):
                        pseudo_prime = prime1 * prime2 * prime3
                        if pseudo_prime.bit_length() >= nbit and miller_rabin2(pseudo_prime, base):
                            return(prime1, prime2, prime3, pseudo_prime, k2, k3, val, mod)
                    i += 1


USAGE = """python3 pp.py <number of bits> <miller rabin base>
<number of bits> is the minimum number of bits in the generated pseudo prime
<miller rabin base> the maximum base upto which all miller rabin should pass"""

if __name__ == "__main__":
    PARSER = ArgumentParser(description="Miller rabin pseudo prime generation")
    PARSER.add_argument(
        '--random',
        help="Enable randomization for faster base selection",
        action="store_true")
    PARSER.add_argument(
        'nbits',
        type=int,
        help="size of pseudo prime in bits to generate")
    PARSER.add_argument(
        'base',
        type=int,
        help='The maximum base upto which all prime bases should satisfy miller rabins test')
    ARGS = PARSER.parse_args()
    NBITS = ARGS.nbits
    BASE = ARGS.base
    P1, P2, P3, P_PRIME, K2, K3, VALUE, MODULO = gen_pseudo_prime(
        NBITS, BASE)
    print("""pseudo prime found: {}
p1: {}
p2: {}
p3: {}
where pseudo prime = p1 * p2 * p3
p1 = {} + i * {}
p2 = {} * ( p1 - 1 ) + 1
p3 = {} * ( p1 - 1 ) + 1
""".format(P_PRIME, P1, P2, P3, VALUE, MODULO, K2, K3))
