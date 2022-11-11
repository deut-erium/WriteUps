class MT19937:
    def __init__(self, c_seed=0):
        # MT19937
        (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
        self.a = 0x9908B0DF
        (self.u, self.d) = (11, 0xFFFFFFFF)
        (self.s, self.b) = (7, 0x9D2C5680)
        (self.t, self.c) = (15, 0xEFC60000)
        self.l = 18
        self.f = 1812433253
        self.MT = [0 for i in range(self.n)]
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1  # 0x7FFFFFFF
        self.upper_mask = (1 << self.r)  # 0x80000000
        self.seed_mt(c_seed)
        self.num_bits = 32

    def seed_mt(self, num):
        """initialize the generator from a seed"""
        self.MT[0] = num
        self.index = self.n
        for i in range(1, self.n):
            temp = self.f * (self.MT[i - 1] ^
                             (self.MT[i - 1] >> (self.w - 2))) + i
            self.MT[i] = temp & ((1 << self.w) - 1)

    def twist(self):
        """ Generate the next n values from the series x_i"""
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper_mask) + \
                (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def randint(self):
        if self.index >= self.n:
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return y & ((1 << self.w) - 1)

    def ut(self, num):
        """
        untamper
        """
        def get_bit(number, position):
            if position < 0 or position > self.num_bits - 1:
                return 0
            return (number >> (self.num_bits - 1 - position)) & 1

        def set_bit_to_one(number, position):
            return number | (1 << (self.num_bits - 1 - position))

        def undo_right_shift_xor_and(result, shift_len, andd=-1):
            original = 0
            for i in range(self.num_bits):
                if get_bit(result, i) ^ \
                   (get_bit(original, i - shift_len) &
                        get_bit(andd, i)):
                    original = set_bit_to_one(original, i)
            return original

        def undo_left_shift_xor_and(result, shift_len, andd):
            original = 0
            for i in range(self.num_bits):
                if get_bit(result, self.num_bits - 1 - i) ^ \
                   (get_bit(original, self.num_bits - 1 - (i - shift_len)) &
                        get_bit(andd, self.num_bits - 1 - i)):
                    original = set_bit_to_one(original, self.num_bits - 1 - i)
            return original
        num = undo_right_shift_xor_and(num, self.l)
        num = undo_left_shift_xor_and(num, self.t, self.c)
        num = undo_left_shift_xor_and(num, self.s, self.b)
        num = undo_right_shift_xor_and(num, self.u, self.d)
        return num

    def clone(self,outputs):
        self.MT = list(map(self.ut,outputs))
        self.index = 624

import pwn
import re
HOST,PORT = "challs.dvc.tf", 3096
REM = pwn.remote(HOST,PORT)

REM.recvuntil(b'thinking of?')

outputs = []
for _ in range(624):
    REM.sendline('0')
    chall = REM.recvuntil(b'thinking of?')
    outputs.append(int(re.search(b' (\d+)\n',chall)[1]))

m = MT19937()
m.clone(outputs)
REM.sendline(str(m.randint()))
REM.interactive()
#dvCTF{tw1st3d_numb3rs}

