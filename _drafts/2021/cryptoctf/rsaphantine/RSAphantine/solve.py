import sympy
k1 = 47769864706750161581152919266942014884728504309791272300873440765010405681123224050402253883248571746202060439521835359010439155922618613520747411963822349374260144229698759495359592287331083229572369186844312169397998958687629858407857496154424105344376591742814310010312178029414792153520127354594349356721
k2 = 89701863794494741579279495149280970802005356650985500935516314994149482802770873012891936617235883383779949043375656934782512958529863426837860653654512392603575042842591799236152988759047643602681210429449595866940656449163014827637584123867198437888098961323599436457342203222948370386342070941174587735051
k3 = 47769864706750161581152919266942014884728504309791272300873440765010405681123224050402253883248571746202060439521835359010439155922618613609786612391835856376321085593999733543104760294208916442207908167085574197779179315081994735796390000652436258333943257231020011932605906567086908226693333446521506911058

y6_plus_x3 = k3-k1

def calc(x):
    y = sympy.integer_nthroot(y6_plus_x3-x**3,6)[0]
    z = (k2-(x**4+y**5))//(x*y)
    diff = 2*z**5 - x**3 + y*z - k1
    return y,z, diff



start = -100000000000000000000000000000000000000000000000000000000000000000000000000000
end = -10000000000000000000000000000000000000000000000000000000000000000000000000000
lo,hi = start,end

while lo<=hi:
    mid = (lo+hi)//2
    val = calc(mid)
    print(mid,val[2])
    if val[2]>0:
        lo=mid
    elif val[2]==0:
        x,(y,z) = mid,val[:2]
        break
    else:
        hi = mid

from sympy import nextprime
p = nextprime(x**2 + z**2 + y**2 << 76)
q = nextprime(z**2 + y**3 - y*x*z ^ 67)
n, e = p * q, 31337
c = 486675922771716096231737399040548486325658137529857293201278143425470143429646265649376948017991651364539656238516890519597468182912015548139675971112490154510727743335620826075143903361868438931223801236515950567326769413127995861265368340866053590373839051019268657129382281794222269715218496547178894867320406378387056032984394810093686367691759705672

m = pow(c, pow(e,-1,(p-1)*(q-1)), n)
flag = int.to_bytes(m, (m.bit_length()+7)//8, 'big')

#CCTF{y0Ur_jO8_C4l13D_Diophantine_An4LySI5!}


# y = sympy.integer_nthroot(y6_plus_x3,6)[0]
# x3 = y6_plus_x3 - y**6
# x = sympy.integer_nthroot(x3,3)[0]
# z = (k2-(x**4+y**5))//(x*y)
# y6_plus_x3 = k3-k1
# x = sympy.integer_nthroot(y6_plus_x3,3)[0]
# y6 = y6_plus_x3 - x**3
# y = sympy.integer_nthroot(y6,6)[0]
# z = (k2-(x**4+y**5))//(x*y)
