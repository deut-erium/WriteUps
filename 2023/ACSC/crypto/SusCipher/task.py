#!/usr/bin/env python3
import hashlib
import os
import signal


class SusCipher:
    S = [
        43,  8, 57, 53, 48, 39, 15, 61,
         7, 44, 33,  9, 19, 41,  3, 14,
        42, 51,  6,  2, 49, 28, 55, 31,
         0,  4, 30,  1, 59, 50, 35, 47,
        25, 16, 37, 27, 10, 54, 26, 58,
        62, 13, 18, 22, 21, 24, 12, 20,
        29, 38, 23, 32, 60, 34,  5, 11,
        45, 63, 40, 46, 52, 36, 17, 56
    ]

    P = [
        21,  8, 23,  6,  7, 15,
        22, 13, 19, 16, 25, 28,
        31, 32, 34, 36,  3, 39,
        29, 26, 24,  1, 43, 35,
        45, 12, 47, 17, 14, 11,
        27, 37, 41, 38, 40, 20,
         2,  0,  5,  4, 42, 18,
        44, 30, 46, 33,  9, 10
    ]

    ROUND = 3
    BLOCK_NUM = 8
    MASK = (1 << (6 * BLOCK_NUM)) - 1

    @classmethod
    def _divide(cls, v: int) -> list[int]:
        l: list[int] = []
        for _ in range(cls.BLOCK_NUM):
            l.append(v & 0b111111)
            v >>= 6
        return l[::-1]

    @staticmethod
    def _combine(block: list[int]) -> int:
        res = 0
        for v in block:
            res <<= 6
            res |= v
        return res

    @classmethod
    def _sub(cls, block: list[int]) -> list[int]:
        return [cls.S[v] for v in block]

    @classmethod
    def _perm(cls, block: list[int]) -> list[int]:
        bits = ""
        for b in block:
            bits += f"{b:06b}"

        buf = ["_" for _ in range(6 * cls.BLOCK_NUM)]
        for i in range(6 * cls.BLOCK_NUM):
            buf[cls.P[i]] = bits[i]

        permd = "".join(buf)
        return [int(permd[i : i + 6], 2) for i in range(0, 6 * cls.BLOCK_NUM, 6)]

    @staticmethod
    def _xor(a: list[int], b: list[int]) -> list[int]:
        return [x ^ y for x, y in zip(a, b)]

    def __init__(self, key: int):
        assert 0 <= key <= self.MASK

        keys = [key]
        for _ in range(self.ROUND):
            v = hashlib.sha256(str(keys[-1]).encode()).digest()
            v = int.from_bytes(v, "big") & self.MASK
            keys.append(v)

        self.subkeys = [self._divide(k) for k in keys]

    def encrypt(self, inp: int) -> int:
        block = self._divide(inp)

        block = self._xor(block, self.subkeys[0])
        for r in range(self.ROUND):
            block = self._sub(block)
            block = self._perm(block)
            block = self._xor(block, self.subkeys[r + 1])

        return self._combine(block)

    # TODO: Implement decryption
    def decrypt(self, inp: int) -> int:
        raise NotImplementedError()


def handler(_signum, _frame):
    print("Time out!")
    exit(0)


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    key = int.from_bytes(os.urandom(6), "big")

    cipher = SusCipher(key)

    while True:
        inp = input("> ")

        try:
            l = [int(v.strip()) for v in inp.split(",")]
        except ValueError:
            print("Wrong input!")
            exit(0)

        if len(l) > 0x100:
            print("Long input!")
            exit(0)

        if len(l) == 1 and l[0] == key:
            with open('flag', 'r') as f:
                print(f.read())

        print(", ".join(str(cipher.encrypt(v)) for v in l))


if __name__ == "__main__":
    main()
