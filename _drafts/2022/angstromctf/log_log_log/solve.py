q = 127049168626532606399765615739991416718436721363030018955400489736067198869364016429387992001701094584958296787947271511542470576257229386752951962268029916809492721741399393261711747273503204896435780180020997260870445775304515469411553711610157730254858210474308834307348659449375607755507371266459204680043
p = q * 2**1024 + 1

nbits = p.bit_length() - 1
flagbits = 880
a = 0xaf99914e5fb222c655367eeae3965f67d8c8b3a0b3c76c56983dd40d5ec45f5bcde78f7a817dce9e49bdbb361e96177f95e5de65a4aa9fd7eafec1142ff2a58cab5a755b23da8aede2d5f77a60eff7fb26aec32a9b6adec4fe4d5e70204897947eb441cc883e4f83141a531026e8a1eb76ee4bff40a8596106306fdd8ffec9d03a9a54eb3905645b12500daeabdb4e44adcfcecc5532348c47c41e9a27b65e71f8bc7cbdabf25cd0f11836696f8137cd98088bd244c56cdc2917efbd1ac9b6664f0518c5e612d4acdb81265652296e4471d894a0bd415b5af74b9b75d358b922f6b088bc5e81d914ae27737b0ef8b6ac2c9ad8998bd02c1ed90200ad6fff4a37

F = GF(p)
g = K.multiplicative_generator()
A = F(a)
# Kq = GF(q)
# aq = int(a)%q
# eq = discrete_log(Kq(aq),Kq(g))
# e = discrete_log(a, g)

def pohlig_hellman(g, A, F):
    p = F.order()
    factors = [p_i ** e_i for p_i, e_i in factor(F.order() - 1)]
    crt_array = []
    for p_i in factors:
        g_i = g ** ((p-1)//p_i)
        h_i = A ** ((p-1)//p_i)
        x_i = discrete_log(h_i, g_i)
        print(p_i, x_i)
        crt_array.append(x_i)

    return crt(crt_array, factors)

# actf{it's log, it's log, it's big, it's heavy, it's wood, it's log, it's log, it's better than bad, it's good}
