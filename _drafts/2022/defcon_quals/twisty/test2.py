def print_maze(maze):
    for row in maze:
        for item in row:
            print(item, end='')
        print()

from pwn import *
import zlib
import random

context.log_level = 100

# Start game
conn = remote('twisty-2mjh4xgp7zubo.shellweplayaga.me', 10000)
conn.recvuntil('Ticket please: ')
conn.sendline('ticket{WindwardPier4836n22:pd7pinOYiKO8ewdWu3NpQ3jXlYlCm03yuKzAkPkMXcQsZXbH}')
conn.recvuntil('Good luck')
conn.recvline()

opposite = {"N":"S", "S":"N", "W":"E", "E":"W", "U":"D", "D":"U"}

dirs = ['N','U','E','S','D','W']
dird = [(-1,0,0),(0,0,1),(0,1,0),(1,0,0),(0,0,-1),(0,-1,0)]

level = 0
r = 0
c = 0
h = 0
par = {}
tra = {}

while level < 5:
    data = conn.recv(4)
    size = struct.unpack('i', data)[0]
    data = conn.recv(size)
    res = zlib.decompress(data).decode()
    if 'Congratulations' in res:
        level += 1
        print('Passed level',level)
        r = 0
        c = 0
        h = 0
        par = {}
        tra = {}
        continue

    res = res.split('\n')
    res, next_dir = res[:-1],res[-1].split()[1]
    # print_maze(res)
    # print(r,c,h,next_dir)
    if len(tra) == 0:
        move = next_dir[0]
        tra[(r,c,h)] = [move]
        dr,dc,dh = dird[dirs.index(move)]
        r,c,h = r+dr,c+dc,h+dh
        par[(r,c,h)] = opposite[move]
        conn.sendline(move)
        # print(move)
    else:
        moved = False
        i = 0
        while i < len(next_dir) and not moved:
            move = next_dir[i]
            if move == par[(r,c,h)]:
                i+=1
                continue

            if (r,c,h) in tra and move in tra[(r,c,h)]:
                i+=1
                continue

            if (r,c,h) in tra:
                tra[(r,c,h)] += [move]
            else:
                tra[(r,c,h)] = [move]

            dr,dc,dh = dird[dirs.index(move)]
            r,c,h = r+dr,c+dc,h+dh

            if (r,c,h) not in par:
                par[(r,c,h)] = opposite[move]

            conn.sendline(move)
            # print(move)
            moved = True
        if not moved:
            move = par[(r,c,h)]
            dr,dc,dh = dird[dirs.index(move)]
            r,c,h = r+dr,c+dc,h+dh

            conn.sendline(move)
            # print(move)

    # a = input().strip()
    # if a == 'w' and 'N' in next_dir:
    #     conn.sendline('N')
    # elif a == 'a' and 'W' in next_dir:
    #     conn.sendline('W')
    # elif a == 's' and 'S' in next_dir:
    #     conn.sendline('S')
    # elif a == 'd' and 'E' in next_dir:
    #     conn.sendline('E')
    # elif a == 'q' and 'U' in next_dir:
    #     conn.sendline('U')
    # elif a == 'e' and 'D' in next_dir:
    #     conn.sendline('D')
    # else:
    #     print('fuckup. sending',next_dir[0])
    #     conn.sendline(next_dir[0])

conn.interactive()