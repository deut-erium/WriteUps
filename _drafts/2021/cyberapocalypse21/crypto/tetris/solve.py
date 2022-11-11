from cipher_solver.simple import SimpleSolver

with open('dec1.txt') as f:
    data = f.read().strip()

def transpose(x, l):
    return ''.join(x[i::l] for i in range(l))

def transpose_rev(x,l):
    lst = []
    xx = list(range(len(x)))
    for i in range(l):
        lst.extend(xx[i::l])
    retlst = [None for _ in range(len(x))]
    for i,v in enumerate(lst):
        retlst[v]=x[i]
    return "".join(retlst)

for i in range(1,100):
    g = transpose_rev(data,i)
    s = SimpleSolver(g)
    s.solve()
    x=s.plaintext()
    #print(x[-100:])
    score = s._score(s._get_digram_matrix(x))
    if 'CHTB' in x:
        print(x,i)
    #if 'CHTB' in s.plaintext():
        #print(s.plaintext())
    #print(i,transpose_rev(data,i))
#CHTB{UNFORTUNATELYQUIPQIUPDOESNTSUPPORTTRANSPOSITIONS}
