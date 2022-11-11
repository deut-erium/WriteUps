from output import cipher as ct, pub as pk

n = len(pk)
K = 10**200  #int(sqrt(n/2))+1
A = Matrix(QQ,n+1,n+1)
for i in range(n):
    A[i,i]=1
    A[i,n]=K*pk[i]
    A[n,i]=1/2
A[n,n] = ct*K
a = A.LLL()
for row in a:
    if max(row)==1/2 and min(row)==-1/2:
        p = [1 if x==-1/2 else 0 for x in row[:-1]]
        t = int("".join(map(str,p)),2)
        print(int.to_bytes(t,(t.bit_length()+7)//8,'big'))
