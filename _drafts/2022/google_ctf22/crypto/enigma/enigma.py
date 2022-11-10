class Rotor:
    def __init__(self, sbox:str, notch_pos,ring_set=0,rot_pos=0):
        self.sbox = [ord(i)-65 for i in sbox]
        self.inv_sbox = [self.sbox.index(i) for i in range(len(sbox))]
        self.rot_pos = rot_pos
        self.ring_set = ring_set
        self.notch = notch_pos

    def forward(self,c):
        # essentially sbox[i+shift] - shift
        shift = self.rot_pos - self.ring_set
        return (self.sbox[(c+shift+26)%26] - shift + 26)%26

    def backward(self,c):
        shift = self.rot_pos - self.ring_set
        return (self.inv_sbox[(c+shift+26)%26] - shift + 26)%26

    def turnover(self):
        self.rot_pos = (self.rot_pos+1)%26

    def is_notch(self):
        return self.rot_pos in self.notch

class PlugBoard:
    def __init__(self, pairs):
        self.sbox = list(range(26))
        for i,j in pairs:
            self.sbox[i] = j
            self.sbox[j] = i
    def forward(self, c):
        return self.sbox[c]

class Reflector:
    def __init__(self, sbox:str):
        self.sbox = [ord(i)-65 for i in sbox]
    def forward(self,c):
        return self.sbox[c]

ROTORS = {i:Rotor(sbox,notch_pos) for i,sbox,notch_pos in \
            [("I","EKMFLGDQVZNTOWYHXUSPAIBRCJ", {16}),
            ("II","AJDKSIRUXBLHWTMCQGZNPYFVOE", {4}),
            ("III","BDFHJLCPRTXVZNYEIWGAKMUSQO", {21}),
            ("IV","ESOVPZJAYQUIRHXLNFTGKDCMWB", {9}),
            ("V","VZBRGITYUPSDNHLXAWMJQOFECK", {25}),
            ("VI","JPGVOUMFYQBENHZRDKASXLICTW", {12, 25}),
            ("VII","NZJHGRCXMYSWBOUFAIVLPEKQDT", {12, 25}),
            ("VIII","FKQHTLXOCBJSPDZRAMEWNIUYGV", {12, 25})]}

REFLECTOR_B = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
def to_int(cr):
    return ord(cr)-65

class Enigma:
    def __init__(self, rotors, plugboard, reflector=REFLECTOR_B):
        self.l, self.c, self.r = rotors
        self.plug = plugboard
        self.ref = reflector

    def init_string(self,set_str):
        lr, cr, rr, rng_set, *plgbrd, rotpos = set_str.split()
        self.l = ROTORS[lr]
        self.c = ROTORS[cr]
        self.r = ROTORS[rr]
        self.l.ring_set = to_int(rng_set[0])
        self.c.ring_set = to_int(rng_set[1])
        self.r.ring_set = to_int(rng_set[2])
        self.l.rot_pos = to_int(rotpos[0])
        self.c.rot_pos = to_int(rotpos[1])
        self.r.rot_pos = to_int(rotpos[2])

        self.plug = PlugBoard([map(to_int,i) for i in plgbrd])

    def encrypt(self,c):
        self.rotate()
        c = self.plug.forward(c)

        c = self.r.forward(c)
        c = self.c.forward(c)
        c = self.l.forward(c)

        c = self.ref.forward(c)

        c = self.l.backward(c)
        c = self.c.backward(c)
        c = self.r.backward(c)
        c = self.plug.forward(c)
        return c

    def encrypt_string(self,st):
        return "".join(chr(self.encrypt(ord(c)-65)+65) for c in st)

    def rotate(self):
        if self.c.is_notch():
            self.c.turnover()
            self.l.turnover()
        elif self.r.is_notch():
            self.c.turnover()
        self.r.turnover()


