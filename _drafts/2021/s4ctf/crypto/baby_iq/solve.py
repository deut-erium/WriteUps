enc = [[122, 83, 52, 67, 84, 70], [89, 114, 79, 48, 67, 125], [95, 121, 114, 53, 116, 55], [123, 95, 80, 51, 52, 95], [102, 115, 114, 95, 119, 107], [52, 117, 109, 33, 97, 112]]


from math import sqrt
import os
import random
import base64

def chunkchunk(msg, l):
    return [msg[l * i:l * (i + 1)] for i in range(0, len(msg) // l)]

def pad(msg):
    r = int(sqrt(len(msg))) + 1
    head = base64.b64encode(os.urandom(r**2))[:r**2 - (len(msg))]
    msg = head + msg.encode('utf-8')
    msg = chunkchunk(msg, r)
    return [list(m) for m in msg]

def encrypt(A):
    row = len(A)
    col = len(A[0])
    top = 0
    left = 0
    tmp = []
    while (top < row and left < col):
        for i in range(left, col):
            tmp.append(A[top][i])
        top += 1
        for i in range(top, row):
            tmp.append(A[i][col - 1])
        col -= 1
        if (top < row):
            for i in range(col - 1, left - 1, -1):
                tmp.append(A[row - 1][i])
            row -= 1

        if (left < col):
            for i in range(row - 1, top - 1, -1):
                tmp.append(A[i][left])
            left += 1
    result = []
    for i in range(len(A)):
        r = []
        for j in range(len(A[0])):
            r.append(tmp[i * len(A[0]) + j])
        result.append(r)
    return result

#flag = bytearray(b'abcdefghijklmnopqrstuvwx')
#random.shuffle(flag)
#flag = flag.decode()
#enc = pad(flag)
#print(b"".join([bytes(i) for i in enc]))
#for _ in range(len(enc)):
#    _ = encrypt(enc)
#    enc = _
#    print(b"".join([bytes(i) for i in enc]))
#
matrix = [[(j,i) for i in range(5)] for j in range(5)]
for _ in range(10):
    matrix = encrypt(matrix)

dec = [[None for i in range(5)] for j in range(5)]
for i in range(5):
    for j in range(5):
        x,y = matrix[i][j]
        dec[x][y] = enc[i][j]

flag_dec = b"".join([bytes(i) for i in dec])
print(flag_dec)
#print(flag_dec.decode()[1:]==flag)
