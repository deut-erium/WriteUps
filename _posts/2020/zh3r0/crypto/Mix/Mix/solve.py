import base65536
with open('chall_encrypted.txt','r') as chall_enc:
    data = chall_enc.read()

data1 = "".join( chr(ord(i)%256)+chr(ord(i)//256) for i in data )

d = base65536.decode(data)
print(d.decode())

f1 = "Yjod od s lrunpstf djogy vo[jrtyrcy jrtr od upi g;sh xj4t-}U-i+dit4+"

f2 = "3030313130313030203031313130303130203030313130303131203031303131313131203030313130313030203031313130313131203030313130303131203031313130303131203030313130303030203031313031313031203030313130303131203031303131313131203031313130313131203031313031303031203030313130313131203031313031303030"

f3 = "MTExMTExMTExMTAwMTAwMDEwMTAxMDExMTAxMDExMTExMTEwMTAxMTExMTExMTExMDExMDExMDExMDExMDAwMDAxMTAxMDAxMDAxMDAxMDAwMDAwMDAwMDAwMDAwMDAwMTAxMDAxMTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTAxMDAwMDAwMDAwMDAwMTAxMDAwMTAxMDAxMDAwMTAxMDAxMTExMTExMTAwMTAxMDAxMDExMTExMTExMTAwMTAxMDAxMTAwMDAwMDAwMDAwMDAwMTAxMDAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMTAxMDExMTExMTExMTExMTExMTExMTExMDAxMDEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxMDEwMDAwMDAwMDAxMDEwMDExMDAwMDAwMDAxMDEwMDAxMDEwMTExMTAwMTAxMDAxMDExMTExMTExMTExMTExMTExMTExMDAxMDEwMDExMDExMDExMTExMTExMTExMTAwMTAxMA=="

print(bytes.fromhex(f2))
# b'00110100 01110010 00110011 01011111 00110100 01110111 00110011 01110011 00110000 01101101 00110011 01011111 01110111 01101001 00110111 01101000'
flag2 = "".join(chr(int(i,2)) for i in bytes.fromhex(f2).split())
print(flag2)

flag3 = b"_411_7h3_ski115}" # SPOON decode
flag1 = b"This is a keyboard shift ciphertext here is you flag zh3r0{Y0u_sur3_" 

print(flag1.decode()+flag2+flag3.decode())
