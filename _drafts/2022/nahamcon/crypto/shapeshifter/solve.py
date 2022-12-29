from Crypto.Util.number import bytes_to_long as b2l

class LFSR():
    def __init__(self, iv):
        self.state = [int(c) for c in iv]
        #self.state = self.iv

    def shift(self):
        s = self.state
        newbit = s[15] ^ s[13] ^ s[12] ^ s[10] # ^ s[0]
        s.pop()
        self.state = [newbit] + s

    def revshift(self):
        s = self.state
        newbit = s[11] ^ s[13] ^ s[14] ^ s[0]
        self.state.append(newbit)
        self.state = self.state[1:]

flag = b''

with open("output.txt", "r") as f:
    data = f.read().strip().split()

for i in data:
    lfsr = LFSR(i)
    for _ in range(31337):
        lfsr.revshift()

    finalstate = int(''.join([str(c) for c in lfsr.state]),2)
    flag+=int.to_bytes(finalstate,2,'big')
    # print(f'{finalstate}')
print(flag)

#flag{70f817ce030904aa1db980686ffa0fa8}
