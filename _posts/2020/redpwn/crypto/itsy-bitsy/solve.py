from pwn import remote

HOST, PORT = "2020.redpwnc.tf", 31284


def bits_to_str(bitstring):
    return "".join( chr(int(bitstring[i:i+7],2)) for i in range(0,len(bitstring),7) )

def bit_str_xor(bit_str_1, bit_str_2):
    xor_res = ''
    for i in range(len(bit_str_1)):
        bit_1 = bit_str_1[i]
        bit_2 = bit_str_2[i]
        xor_res += str(int(bit_1) ^ int(bit_2))
    return xor_res

def generate_random_bits(lower_bound, upper_bound, number_of_bits):
    bit_str = ''
    while len(bit_str) < number_of_bits:
        r = randint(lower_bound, upper_bound)
        bit_str += bin(r)[2:]
    return bit_str[:number_of_bits]

def get_ct(num_bits):
    REM = remote(HOST, PORT)
    REM.sendline(str(num_bits -1).encode())
    REM.sendline(str(num_bits).encode())
    data = REM.recvline()
    ciphertext = data.split(b':')[-1].strip()
    #print(data)
    REM.close()
    return ciphertext

flag_bits = bytearray(301)
flag_bits[0] = 49
flag_bits[1] = 49
for num_bits in range(2,301):
    if flag_bits[num_bits] == 0:
        ct = get_ct(num_bits)
        for i in range(num_bits, 301, num_bits):
            flag_bits[i] = 48 if ct[i] == 49 else 49
print(bits_to_str(flag_bits))

# flag{bits_leaking_out_down_the_water_spout}
