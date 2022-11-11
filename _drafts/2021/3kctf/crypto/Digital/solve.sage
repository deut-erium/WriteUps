import hashlib

def rol(val, r_bits, max_bits): return (val << r_bits % max_bits) & (
    2**max_bits - 1) | ((val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits)))


class Random():
    def __init__(self, seed):
        self.state = seed
        self.bits = self.state.bit_length()

    def next(self):
        self.state ^= self.state << 76
        self.state = rol(self.state, 32, self.bits)
        self.state ^= self.state >> 104
        self.state = rol(self.state, 20, self.bits)
        self.state ^= self.state << 116
        self.state = rol(self.state, 12, self.bits)
        return self.state

p = 0x433fd29e6352ba4f433aaf05634348bf2fa7df007861ec24e1088b4105307a9af5645fff0bb561f31210b463346f6d2990a8395e51f0abf6f0affad2364a09ef3ab2cfa66497ebb9d6ac7ed98710634c5a39ddc9d423294911cfa787e28ac2943df345ed6b979ed9a383e1be05e35b305c797f826c9502280dd5b8af4ff532527eed2e91d290b145fac6d647c81127ed06eaa580d64bcf2740ee8ed2aa158cc297ca9315172df731f149927ba7b6e72adf88bde00d13cc7784c717ce1d042cbc3bd8db1549a75fb5c4d586ed1d67fe0129e522f394236b8053513905277b8e930101b0660807598039a4796e66018113fbf3f1703303bb3808779e3613995cb9
q = 0xc313d1a2bf3516a555c54875798a59a3d219ea76179b712886beec177263cec7
g = 0x21ac05c17f3cc476fa34ea77b5e2252e848f2ab35cf4e1f6cc53f15349af6e56f1c5ad36fe7cdf0a00c8162032b623d1271b4f586d26dba704706c32d0cefa01937e82d8af632596e9d27ff10a7cad23766ae97c07bb7dc3b2e24a482ab30c02435c8ce99b0cc356146c371bda04582ee1b40b2f29227ba8225aa490b4bd788662168929fdd2cfbce0e0dc59da3db76651ee91fbc654d36f277003f96ff6b045b2ab5187b0d4024a32281672c606206aebb1f3fe9b75877e38dcd38c73aa588ec01ae3fca344befbdf745a47f7a45b4d06643fea5e4e9b02f763cc5b2e7e8488945b0fe12b56b83a29cbe47ec9d276197d0245d11abc8833f88d114f3a897f81

y =  5624204323708883762857532177093000216929823277043458966645372679201025592769376026088466517180933057673841523705217308006821461505613041092599344214921758292705684588442147606413017270932589190682167865180010809895170865252326994825400330559172774619220024016595462686075240147992717554220738390033531322461011161893179173499597221230442911598574630392043521768535083211677909300720125573266145560294501586465872618003220096582182816143583907903491981432622413089428363003509954017358820731242558636829588468685964348899875705345969463735608144901602683917246879183938340727739626879210712728113625391485513623273477
r1 =  53670875511938152371853380079923244962420018116685861532166510031799178241334
s1 =  6408272343562387170976380346088007488778435579509591484022774936598892550745
r2 =  3869108664885100909066777013479452895407563047995298582999261416732594613401
s2 =  63203374922611188872786277873252648960215993219301469335034797776590362136211

MSG1 = b'Joe made the sugar cookies.'
MSG2 = b'Susan decorated them.'
hm1 = int(hashlib.sha256(MSG1).hexdigest(), 16)
hm2 = int(hashlib.sha256(MSG2).hexdigest(), 16)
s1_inv = pow(s1,-1,q)
s2_inv = pow(s2,-1,q)

v1,v2 = (s1_inv*r1)%q, (s2_inv*r2)%q
v3,v4 = (-(s1_inv*hm1))%q,(-(s2_inv*hm2))%q

B = 2**128
M=Matrix(QQ,\
[[q ,0 ,0  ,0],
 [0 ,q ,0  ,0],
 [v1,v2,B/q,0],
 [v3,v4,0  ,B]])

rows = M.LLL()
for row in rows:
    x = ((QQ(-row[-2]) * q)/B)%q
    if pow(g,x,p)==y:
        print( int.to_bytes(x,256,'big'))
        
m = [hm2,hm1]
r = [r2,r1]
s = [s2,s1]
M = matrix(QQ, len(m)+2, len(m)+2)
B = 2**128

order = q-1

for i in range(len(m)):
    M[i,i] = order

for i in range(len(m)):
    M[len(m), i] = mod(r[i] * inverse(s[i], order), order)
    M[len(m)+1, i] = -mod(m[i] * inverse(s[i], order), order)  # <- minus a_i

M[len(m), i+1] = QQ(B)/QQ(order)          # <- remember QQ
M[len(m)+1, len(m)+1] = QQ(B)
rows = M.LLL()
for row in rows:    
    x = ((QQ(-(row[-2])) * order) / B) % order
    nonce = -row[0]   # negative because of -a_i        
    privkey = int((inverse(r[0], order) * ((nonce * s[0]) - m[0])) % order)
    print(x,privkey,x==privkey)
    if pow(g,x,p)==y:
        print( int.to_bytes(x,256,'big'))
