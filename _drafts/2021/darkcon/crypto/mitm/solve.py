#powerLL = pow(x,n,p)
import pwn
from Crypto.Cipher import AES

HOST_B,PORT_B = "13.233.166.242", 49155
HOST_A,PORT_A = "13.233.166.242", 49154
pwn.context(log_level=0)
p =  [1697841911,1438810907,666397859,941857673]
alice_pk = [955933435,757576380,387586730,437367991]
bob_pk = [220422733,801253003,596847162,571072501]

G = "13061880230110805485346525688018595113271880103717720219673350299083396780730251766148414377512386061643807530751287373200960399392170617293251618992497053"

gs = [int(G)%i for i in p]

#priv_alice,priv_bob = [],[]
#for i in range(4):
#    K = GF(p[i])
#    g = K(gs[i])
#    a = K(alice_pk[i])
#    b = K(bob_pk[i])
#    priv_alice.append(discrete_log(a,g,K.order()-1))
#    priv_bob.append(discrete_log(b,g,K.order()-1)
    
priv_alice = [1103453346, 1237583171, 324917814, 555140471]
priv_bob = [854824228, 801028375, 622748412, 194801235]

for i in range(4):
    assert pow(gs[i],priv_alice[i],p[i])==alice_pk[i]
    assert pow(gs[i],priv_bob[i],p[i])==bob_pk[i]

key = [pow(gs[i],priv_alice[i]*priv_bob[i],p[i]) for i in range(4)]

def power_strings(sa,sb,p):
    #a,b = 0,0
    #for i in range(len(sa)):
    #    a = (a * 10 + int(sa[i]))%p
    #for i in range(len(sb)):
    #    b = (b * 10 + int(sb[i]))%(p-1)
    a,b = int(sa)%p, int(sb)%(p-1)
    return a,b,pow(a,b,p)

ALICE = pwn.remote(HOST_A,PORT_A)
BOB = pwn.remote(HOST_B,PORT_B)

for i in range(4):
    BOB.sendline(str(alice_pk[i]))

for i in range(4):
    ALICE.sendline(str(bob_pk[i]))


#enc_flag = bytes([ 0x0A ,0x56 ,0x04 ,0xCE ,0x6B ,0xC3 ,0xD8 ,0x41 ,0x97 ,0x22 ,0x57 ,0x84 ,0x19 ,0x2A ,0x64 ,0x40 ,0x09 ,0xEB ,0x46 ,0x0C ,0x60 ,0x34 ,0xD7 ,0xF2 ,0x52 ,0xDE ,0xD1 ,0x06 ,0x61 ,0xC2 ,0xE4 ,0xC2])

enc_flag = bytes([0x89, 0xD9, 0x20, 0x35, 0xC0, 0x03, 0xBF, 0x39, 0x6D, 0xDD, 0x5E, 0xDA, 0xBA, 0x5F, 0x82, 0xDA, 0xCB, 0xAF, 0x55, 0xFF, 0xEF, 0x58, 0x38, 0x98, 0xCE, 0x62, 0x71, 0xBD, 0x57, 0xDC, 0xC7, 0x54])

enc_flag2 = bytes([0x9E, 0x12, 0x60, 0x22, 0x52, 0x8C, 0xD9, 0x31, 0xE9, 0xA9, 0x36, 0xFE, 0x64, 0xE6, 0x16, 0xE5, 0xA1, 0x77, 0x36, 0x88, 0x51, 0x1D, 0x01, 0xB1, 0x08 ,0x59, 0x70, 0x8B, 0xDF, 0xA8 ,0x19, 0x5D])

#key1 = b''.join([ int.to_bytes(i,4,'big') for i in key ])
key2 = b''.join([ int.to_bytes(i,4,'little') for i in key ])

#c = AES.new(key1,AES.MODE_CBC,iv = b'\x00'*16)
#print(c.decrypt(enc_flag))

c = AES.new(key2,AES.MODE_CBC,iv = b'\x00'*16)
print(c.decrypt(enc_flag))

#c = AES.new(key1,AES.MODE_CBC,iv = enc_flag[:16])
#print(c.decrypt(enc_flag[16:]))

#c = AES.new(key2,AES.MODE_CBC,iv = enc_flag[:16])
#print(c.decrypt(enc_flag[16:]))
