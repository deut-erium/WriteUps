import pickle

with open("matrix.pickle", "rb") as f:
    mat,capacities, weights,q = pickle.load(f)


def solve_knapsack(weights, capacity, K=0):
    n = len(weights)
    N = ceil(sqrt(n)/2)
    if K:
        N = K
    M = Matrix(QQ, n+1, n+1)
    for i in range(n):
        M[i,i] = 1
        M[i,n] = N*weights[i]
        M[n,i] = 1/2
    M[n,n] = N*capacity
    a = M.LLL()
    for row in a:
        #print(row)
        if max(row)==1/2 and min(row)==-1/2:
            p = [1 if x==-1/2 else 0 for x in row[:-1]]
            return p

def solve_knapsack2(weights, capacity, K=10**100):
    n = len(weights)
    M = Matrix(n+1, n+1)
    for i in range(n):
        M[i,i] = 1
        M[i,n] = weights[i]
        M[n,i] = 1
    M[n,n] = -K*capacity
    a = M.LLL()
    for row in a:
        if all(i in (0,1) for i in row):
            print(row)
            return row

def solve_knapsack3(weights, capacity, K=10**100):
    n = len(weights)
    M = Matrix(QQn+1, n+1)
    for i in range(n):
        M[i,i] = 1
        M[i,n] = weights[i]
        M[n,i] = 1/2
    M[n,n] = K*capacity
    a = M.LLL()
    for row in a:
        if all(i in (0,1) for i in row):
            print(row)
            return row


#for k in range(1,256):
#    print(k)
#    solv = solve_knapsack(weights[0], -capacities[0]+k*q)
#    if solv:
#        break
#

