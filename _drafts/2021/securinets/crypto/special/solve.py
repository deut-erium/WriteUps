from gmpy2 import isqrt
e = 65537
rq,rp = 1337,1187

N = 9205101698706979739826801043045342787573860852370120009782047065091267165813818945944938567077767109795693195306758124184300669243481673570359620772491153042678478312809811432352262322016591328649959068333993409371541201650938826630256112619578125044564261211415732174900162604077497313177347706230511508892968172603494805342653386527679619380762253476920434736431368696225307809325876263469267138456334317623292049963916185087736277032965175422891773251267119088153064627668031982940139865703040003065759250189294830016815658342491949959721771171008624698225901660128808998889116825507743256985320474353400908203

c = 7936922632477179427776336441674861485950589109838466370248848810603305227730610589646741819313897162184198914593449584513298801516246072184328924490958302064664202813944180474377318619755541891685799909623945111729243482919086734358170659346187530089396234296268433976153029353575494866263288471212406042845186256151549768916089844077364464961133610687655801313809083988904726871667971720011220619598069236604397523051054337851497256894302257378216064087800301371122182309897203436049352850483968349573626245496903689129366737214112517774597434631637719018819317503710042658242522690613437843118568709251604555104


def special(N,rp,rq,m=2):
    lower = isqrt(rp*rq)+1
    upper = rq//2 + 2**((m//2)+1)*rq+1
    for i in range(lower,upper+1):
        sig = (isqrt(N)-i)**2
        z = (N-rp*rq)%sig
        det = isqrt(z**2 - 4*sig*rp*rq)
        x1,x2 = (z-det)//2, (z+det)//2
        p1,p2 = (x1//rq)+rp, (x2//rq)+rp
        if N%p1==0:
            return p1,N//p1
        elif N%p2==0:
            return p2,N//p2
    print('sad reaxx')

p,q = special(N,rp,rq)
m = int(pow(c,pow(65537,-1,(p-1)*(q-1)),N))
print(int.to_bytes(m,(m.bit_length()+7)//8,'big'))


#i = iroot(rp*rq,2)
#i = i[0] if i[1] else i[0]+1
##while i < rq//2 + rp + 1:
#while True:
#    sig = (iroot(N,2)[0]-i)**2
#    #quad = lambda X: X**2-z*X+sig*rp*rq
#    z = (N-rp*rq)%sig
#    z = z*rp*rq
#
#    for x in range(x1-5,x1+5):
#        if iroot(x//rq,2)[1]:
#            print(i)
#            p = x//rq+rp
#            if N%p==0:
#                break
#            print(i)
#        if iroot(x//rp,2)[1]:
#            p = x//rp+rq
#            print(i)
#            if N%p==0:
#                break
##while True:
#    sig = (iroot(N,2)[0]-i)**2
#    #quad = lambda X: X**2-z*X+sig*rp*rq
#    z = (N-rp*rq)%sig
#    det = iroot( z**2-4*sig*rp*rq,2)[0]
#    #x1,x2 = (z+det)//2, (z-det)//2
#    x1 = (z+det)//2
#    for x in range(x1-5,x1+5):
#        if iroot(x//rq,2)[1]:
#            print(i)
#            p = x//rq+rp
#            if N%p==0:
#                break
#            print(i)
#        if iroot(x//rp,2)[1]:
#            p = x//rp+rq
#            print(i)
#            if N%p==0:
#                break
#    #if iroot(x1//rq,2)[1] or iroot(x2//rp,2)[1]:
#        #print(i)
#    #if N%((x1//rq) + rp) or N%((x2//rp) + rq):
#    i+=1
#    #else:
#    #    print(i)
#    #    break
#

#i = ceil(sqrt(rp*rq))
#limit = floor(rq/2+rp+1)
#print(i,limit)
#while i< limit:
#    #sig = int((sqrt(N)-i)**2)
#    sig = (int(sqrt(N))-i)^2
#    z = (N-rp*rq)%sig
#    det = sqrt((z**2)-4*sig*rp*rq)
#    root = int((z-det)/(2*rq) +rp)
#    if N%root==0:
#        print(i)
#        break
#    i+=1
#    #x1,x2 = (z+det)/2, (z-det)/2
#    #if (N/( (x2/rq)+rp )).is_integer():
#    #    print("solution",i)
#    #    break
#    #print(i)
#    #i+=1
#    #if N%int((x1/rq) + rp): #or N%int((x2/rp) + rq):
#        i+=1
#        print(i)
#    else:
#        print("solution",i)
#        break
