from z3 import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from zlib import crc32
from tqdm import tqdm
P = 93327214260434303138080906179883696131283277062733597039773430143631378719403851851296505697016458801222349445773245718371527858795457860775687842513513120173676986599209741174960099561600915819416543039173509037555167973076303047419790245327596338909743308199889740594091849756693219926218111062780849456373


def hashAF(x):
    res = []
    final = b""
    bytesAF = long_to_bytes(x)
    a = bytesAF[:len(bytesAF) % 8]
    res.append(a)
    res.append(long_to_bytes(crc32(a)))
    t = (len(bytesAF) // 8)
    bytesAF = bytesAF[len(bytesAF) % 8:]
    for i in range(t):
        a = bytesAF[i*8:(i+1)*8]
        res.append(a)
        res.append(long_to_bytes(crc32(a)))
    for i in res:
        final += i
    res = bytes_to_long(final)
    print(res)
    return (res + (res >> 600)) & 2**(600)-1


def evaluate(a, x, P=P):
    return (a[0]+a[1]*x+a[2]*x ** 2+a[3]*x ** 3) % P


def SSSS(secret):
    pt = bytes_to_long(secret.encode())
    a = []
    fragments = []
    a.append(hashAF(pt))
    for i in range(3):
        a.append(hashAF(a[i]))
    for i in range(4):
        fragments.append([a[i], evaluate(a, a[i])])
    return fragments


frag1 = [2720495220767623469285353744013822381852003568708186036185616503729980637299872397663528775139327535373882372413441024067687853130042950311733094495718491989102461186253653660920574, 15843669386575231305658351759203181197336939290074172277291278488719033553337092007099376279196087414169431058207783322243407822366880172512356717418627958539974211317395928935201076097698103133753750610845316760255658006438109555979823148869170489527876600496043886788103609669557918594073292264548123406903]

def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t))
    def fix_term(s, m, t):
        s.add(t == m.eval(t))
    def all_smt_rec(terms):
        if sat == s.check():
           m = s.model()
           yield m
           for i in range(len(terms)):
               s.push()
               block_term(s, m, terms[i])
               for j in range(i):
                   fix_term(s, m, terms[j])
               yield from all_smt_rec(terms[i:])
               s.pop()   
    yield from all_smt_rec(list(initial_terms))  

def rev_addshift(result, bitlen):
    x = BitVec('x',bitlen)
    s = Solver()
    s.add((x + LShR(x,600))&(2**(600)-1)  ==result)
    for m in all_smt(s,[x]):
        return m[x].as_long()

def check_crc_structure(num):
    num_b = long_to_bytes(num)
    res = []
    a = num_b[:len(num_b)%12]
    res.append(a)
    t = len(num_b)//12
    num_b = num_b[len(num_b)%12:]
    for i in range(t):
        res.append(num_b[i*12:(i+1)*12])
    for i in res:
        x,crc_x = i[:-4],i[-4:] 
        if crc32(x)!=bytes_to_long(crc_x):
            return False
    return True

def create_table():
    a = []
    for i in range(256):
        k = i
        for j in range(8):
            if k & 1:
                k ^= 0x1db710640
            k >>= 1
        a.append(k)
    return a

crc_table = create_table()

def crc_update(buf, crc):
    crc ^= 0xffffffff
    for k in buf:
        crc = (crc >> 8) ^ crc_table[(crc & 0xff) ^ k]
    return crc ^ 0xffffffff

# def z3crc32(data,length):
    



for bl in tqdm(range(8,700)):
    rr = rev_addshift(frag1[0],bl)
    if check_crc_structure(rr):
        print(bl)
