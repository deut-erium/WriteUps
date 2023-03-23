from Crypto.Util.number import *
alice_pub_result = int("99edb8ed8892c664350acbd5d35346b9b77dedfae758190cd0544f2ea7312e81", 16)
bob_pub_result = int("40716941a673bbda0cc8f67fdf89cd1cfcf22a92fe509411d5fd37d4cb926afd", 16)

modulus = 1 << 258

def Z2kDH_init(private_exponent):
        return pow(5, private_exponent, modulus) // 4

def Z2kDH_exchange(public_result, private_exponent):
        return pow(public_result * 4 + 1, private_exponent, modulus) // 4

alice_priv_exp = discrete_log(mod(4*alice_pub_result + 1,modulus), mod(5, modulus))

assert Z2kDH_init(alice_priv_exp) == alice_pub_result

bob_priv_exp = discrete_log(mod(4*bob_pub_result + 1,modulus), mod(5, modulus))

assert Z2kDH_init(bob_priv_exp) == bob_pub_result

ss = Z2kDH_exchange(bob_pub_result, alice_priv_exp)

print(long_to_bytes(ss))
