
triangle =[[1]]
flag = open('flag.txt','rb').read()
from tqdm import tqdm
# from math import comb
from Crypto.Util.number import getPrime,bytes_to_long
from math import gcd
p = 751921
code = [1]
res = 1
for i in tqdm(range(p)):
    res = res*(p-i)
    res = res//(i+1)
    code.append(res&1)

enc = 9820620269072860401665805101881284961421302475382405373888746780467409082575009633494008131637326951607592072546997831382261451919226781535697132306297667495663005072695351430953630099751335020192098397722937812151774786232707555386479774460529133941848677746581256792960571286418291329780280128419358700449
N = 84317137476812805534382776304205215410373527909056058618583365618383741423290821410270929574317899945862949829480082811084554009265439540307568537940249227388935154641779863441301292378975855625325375299980291629608995049742243591901547177853086110999523167557589597375590016312480342995048934488540440868447
d = int("".join(map(str,code)),2)
m = pow(enc,d,N)
print(m.to_bytes((m.bit_length()+7)//8,'big'))

#flag{1ts_ch00se_a11_a10ng??}
