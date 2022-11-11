from Crypto.Util.number import getPrime
from secret import flag
pt=int(flag.hex(),16)

def gen():
    p,q=getPrime(512),getPrime(512)
    e,n=65537,p*q
    ct=pow(pt,e,n)
    d=pow(e,-1,(p-1)*(q-1))
    return ct,d,n,[p,q]

if __name__ == '__main__':
    ct,d1,n,pq=gen()
    print(pq)
    d2=int(input("> "))
    if d2!=d1:
        if pow(ct,d2,n)==pt:
            print(f"Good Job!!\n{flag.decode()}")
        else:
            print("bruh")
    else:
        print("Are you for real??")
        
        
    
