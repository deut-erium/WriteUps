from math import prod, gcd
from Crypto.Util.number import *
from itertools import chain, combinations
from tqdm import tqdm
from sympy import divisors, jacobi_symbol
import sympy
from collections import Counter
from operator import or_, and_

def powerset(x):
    return chain.from_iterable(combinations(x,r) for r in range(len(x)+1))

def powerset_c(x):
    return powerset(list(x.elements()))

def prod_c(x):
    return prod([i**j for i,j in x.items()])

facs_1025_2 = [2, 3, 5, 17, 257, 641, 65537, 274177, 2424833, 6700417, 67280421310721, 1238926361552897, 59649589127497217, 5704689200685129054721, 7455602825647884208337395736200454918783366342657, 93461639715357977769163558199606896584051237541638188580280321, 741640062627530801524787141901937474059940781097519023905821316144415759504705008092818711693940737]

def probable_primes(facs):
    primes = {}
    for r in tqdm(powerset(facs),total=2**len(facs)):
        if isPrime(prod(r)+1):
            # primes.setdefault(prod(r)+1,[]).append(set(r))
            primes[prod(r)+1] = set(r)
    return primes

def orall(lst):
    return reduce(or_,lst)

def andall(lst):
    return reduce(and_,lst)

def probable_subsets(pps):
    sets = [set(pps[i][0]) for i in pps]

def all_sol(subsets, exclude_set=set()):
    if len(subsets)==1:
        if not exclude_set&subsets[0]:
            return [subsets]
        return [[]]
    solutions = all_sol(subsets[1:],exclude_set)
    for sol in all_sol(subsets[1:],exclude_set|subsets[0]):
        if not orall(sol+[subsets[0]])&exclude_set:
            solutions.append([subsets[0]]+sol)
    return solutions


def inverse_phi(N,a=1):
    if N==1:
        if a>1:
            return [1]
        return [1,2]
    saved = []
    for div in divisors(N):
        if div<a or not isPrime(div+1):
            continue
        N_ = N//div
        div +=1
        P = div
        while True:
            saved.extend(list(map(lambda x:x*P, inverse_phi(N_, div))))
            # print(N_,div)
            if N_%div:
                break
            P*=div
            N_ //= div
    return saved

def inverse_phis(N_set:Counter,a=1):
    saved = {}
    if prod_c(N_set)==1:
        return {1:Counter([1])}
        if a>1:
            return [Counter([1])]
        return [Counter([1]),Counter([1,2])]
    for div in powerset_c(N_set):
        div = Counter(div)
        pdiv = prod_c(div)
        if pdiv<a or not isPrime(pdiv+1):
            continue
        N_ = N_set-div
        pdiv +=1
        P = Counter([pdiv])
        while True:
            for x in inverse_phis(N_,pdiv).values():
                saved[prod_c(P+x)] = P+x
                print(P+x)
            #     yield P+x
            # saved.extend(list(map(lambda x:P+x, inverse_phis(N_, pdiv))))
            if prod_c(N_)%pdiv:
                break
            P += Counter([pdiv])
            N_ -= Counter([pdiv])
    # return []
    return saved

def inverse_phis2(N_set:Counter,a=1):
    saved = {}
    if prod_c(N_set)==1:
        return {1:Counter([1])}
        if a>1:
            return [Counter([1])]
        return [Counter([1]),Counter([1,2])]
    for div in tqdm(powerset_c(N_set),total=2**sum(N_set.values())):
        div = Counter(div)
        pdiv = prod_c(div)
        if pdiv<a or not isPrime(pdiv+1):
            continue
        N_ = N_set-div
        pdiv +=1
        P = Counter([pdiv])
        while True:
            for x in inverse_phis(N_,pdiv).values():
                saved[prod_c(P+x)] = P+x
                # return saved
                print(P+x)
            #     yield P+x
            # saved.extend(list(map(lambda x:P+x, inverse_phis(N_, pdiv))))
            if prod_c(N_)%pdiv:
                break
            P += Counter([pdiv])
            N_ -= Counter([pdiv])
    # return []
    return saved


facs_1025_1 = [31, 601, 1801, 6151, 13367, 2252951 , 2940521 , 164511353 , 2721217151, 70171342151, 1330118582061732221401, 12477521332302115738661504201 , 3655725065508797181674078959681 , 519724488223771351357906674152638351 ,177900025086275986080877620282066695098333349981977325551662127751,111629689188078042218312790960657678513543611163160738935325094568020551]

assert prod(facs_1025_2) == 2**1025 - 2
assert prod(facs_1025_1) == 2**1025 - 1
e = 65537
n = 0x99efa9177387907eb3f74dc09a4d7a93abf6ceb7ee102c689ecd0998975cede29f3ca951feb5adfb9282879cc666e22dcafc07d7f89d762b9ad5532042c79060cdb022703d790421a7f6a76a50cceb635ad1b5d78510adf8c6ff9645a1b179e965358e10fe3dd5f82744773360270b6fa62d972d196a810e152f1285e0b8b26f5d54991d0539a13e655d752bd71963f822affc7a03e946cea2c4ef65bf94706f20b79d672e64e8faac45172c4130bfeca9bef71ed8c0c9e2aa0a1d6d47239960f90ef25b337255bac9c452cb019a44115b0437726a9adef10a028f1e1263c97c14a1d7cd58a8994832e764ffbfcc05ec8ed3269bb0569278eea0550548b552b1
ct = 0x339be515121dab503106cd190897382149e032a76a1ca0eec74f2c8c74560b00dffc0ad65ee4df4f47b2c9810d93e8579517692268c821c6724946438a9744a2a95510d529f0e0195a2660abd057d3f6a59df3a1c9a116f76d53900e2a715dfe5525228e832c02fd07b8dac0d488cca269e0dbb74047cf7a5e64a06a443f7d580ee28c5d41d5ede3604825eba31985e96575df2bcc2fefd0c77f2033c04008be9746a0935338434c16d5a68d1338eabdcf0170ac19a27ec832bf0a353934570abd48b1fe31bc9a4bb99428d1fbab726b284aec27522efb9527ddce1106ba6a480c65f9332c5b2a3c727a2cca6d6951b09c7c28ed0474fdc6a945076524877680

# factors of prod([(i+1) for i in facs_1025_2])=
# facs_xp1=[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,7,11,43,83,107,107,109,331,733,1259,18401,137089,1863581,3350209,6813678835133,13562889751591,167982422287027,206487726925483,407477800048937789623,7397205338652138126604651761133609,
# 6858383112618019943789085627966716441736433191317,496412357849752879199991393508659621191392758432074313189974107191710682399400942498539967666627]
# assert prod([(i+1) for i in facs_1025_2])==prod(facs_xp1)

# facs_xp2 = [2]*3+[3]*3+[53]+facs_xp1[34:]  # 52*2 = 106 since 107^2 appears
# # taking only a few instances of 2s and 3s

# for p in powerset(facs_xp2):
#     prob_fac = prod([(j+1) for j in i])
#     if gcd(prob_fac+1,n)!=1:
#         print(gcd(prob_fac+1,n))
#         break

def factorize_cycle(e,cl,n):
    f = 1
    while True:
        if pow(e,cl,2**f)!=1:
            break
        f+=1
    f-=1
    print("f=",f)
    y = (pow(e,cl)-1)//2**f
    count=0
    while True:
        count+=1
        a = randint(1,n)
        while jacobi_symbol(a,n)!=-1:
            a = randint(1,n)
        b = pow(a,y,n)
        if b in (1,n-1):
            continue
        c = pow(b,2,n)
        if c == n-1:
            continue
        if c==1:
            if gcd(b-1,n)!=1:
                print(count)
                return gcd(b-1,n)


def get_cycle(n):
    pt = 123
    i = 0
    while True:
        pt = pow(pt,65537,n)
        i+=1
        if pt==123:
            break
    return i

def simulate(nbits=20):
    pp,qq = getPrime(nbits), getPrime(nbits)
    pphi = (pp-1)*(qq-1)
    nn = pp*qq
    phiphi = sympy.totient(pphi)
    for d in divisors(phiphi)[::-1]:
        if 123==pow(123,pow(65537,d,pphi),nn):
            cl = d
    print("pp,qq=",pp,",",qq)
    print("pphi=",factor(pphi))
    print("phiphi=",factor(phiphi))
    print("cl=",factor(cl))
    print("mul=",factor(phiphi//cl))
    print(int(pphi).bit_length(), int(phiphi).bit_length(), int(cl).bit_length())
    print("com=",factor(gcd(pphi,phiphi)))




