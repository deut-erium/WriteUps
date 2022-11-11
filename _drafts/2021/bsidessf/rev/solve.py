from struct import pack
from hashlib import sha256
desired_hash = 'ed2591b6660b2b05a0e5b22152b120cd59458eb2504c529927ff9a4890b6912e'
from tqdm import tqdm
def find():
    num0 = 1766
    for num1 in tqdm(range(0,0x800,3),total=((0x800//3)*(0x800//22)*(0x800//15))):
        for num2 in range(0,0x800,22):
            for num3 in range(0,0x800,15):
                num4 = 85^1766^num1^num2^num3
                if num4 in range(0,0x800):
                    word = pack('<5I',num0,num1,num2,num3,num4)
                    if sha256(sha256(word).digest()).hexdigest() == desired_hash:
                        print(num0,num1,num2,num3,num4)
                        return num0,num1,num2,num3,num4

find()
                    
