from decimal import Decimal, getcontext
from Crypto.Cipher import AES

getcontext().prec = 50

P = (Decimal("45702021340126875800050711292004769456.2582161398"), Decimal("310206344424042763368205389299416142157.00357571144"))
Q = (Decimal("55221733168602409780894163074078708423.359152279"), Decimal("347884965613808962474866448418347671739.70270575362"))
R = (Decimal("14782966793385517905459300160069667177.5906950984"), Decimal("340240003941651543345074540559426291101.69490484699"))
enc_flag = bytes.fromhex('838371cd89ad72662eea41f79cb481c9bb5d6fa33a6808ce954441a2990261decadf3c62221d4df514841e18c0b47a76')

def line_through(P,Q):
    # ax+by=c
    a = Q[1]-P[1]
    b = P[0]-Q[0]
    c = a*P[0] + b*P[1]
    return a,b,c

def perp_bisect(P,Q,a,b,c):
    mid_pt = [(P[0]+Q[0])/2,(P[1]+Q[1])/2]
    c = -b*mid_pt[0] + a*mid_pt[1]
    return -b,a,c

def intersect_line(a1,b1,c1,a2,b2,c2):
    det = a1*b2-a2*b1
    return (b2*c1-b1*c2)/det, (a1*c2-a2*c1)/det

def circumcenter(P,Q,R):
    a,b,c = line_through(P,Q)
    e,f,g = line_through(Q,R)
    a,b,c = perp_bisect(P,Q,a,b,c)
    e,f,g = perp_bisect(Q,R,e,f,g)
    rx,ry = intersect_line(a,b,c,e,f,g)
    #assertion
    d1 = ((P[0]-rx)**2 + (P[1]-ry)**2).sqrt()
    d2 = ((Q[0]-rx)**2 + (Q[1]-ry)**2).sqrt()
    d3 = ((R[0]-rx)**2 + (R[1]-ry)**2).sqrt()
    print(d1-d2,d2-d3,d3-d1) #should be negligible
    return rx,ry

key,iv = circumcenter(P,Q,R)
key = int.to_bytes(round(key),16,'big')
iv = int.to_bytes(round(iv),16,'big')
cipher = AES.new(key,AES.MODE_CBC,iv=iv)
print(cipher.decrypt(enc_flag))


