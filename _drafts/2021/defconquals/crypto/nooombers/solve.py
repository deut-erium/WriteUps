import pwn

HOST, PORT = "nooombers.challenges.ooo",8765

REM = pwn.remote(HOST,PORT)

REM.sendline()
REM.recvline()
#REM.interactive()
menu = REM.recvuntil(b' ')
options = menu.decode().split()
prompt,options = options[0][0],options[1:]

def get_option(num,data:list):
    REM.sendline(options[num])
    for i in data:
        REM.sendline(i)
    response = REM.recvuntil(menu)[:-len(menu)]
    return response.decode().split()

values = []
# A
vals = get_option(0,[])
values.append(vals[1])

# B
vals = get_option(1,[values[i] for i in [0]])
values.extend(vals[3:])

# D
vals = get_option(3,[values[i] for i in [0,2]])
values.append(vals[-1])

## C
#vals = get_option(2,[values[0]])
#values.append(vals[-1])
#
## E
#vals = get_option(4,[values[i] for i in [0,4]])
#values.append(vals[-1])
#
## D
##vals = get_option(3,[values[i] for i in [3,5]])
#
## D
#vals = get_option(3,[values[i] for i in [5,5]])
#values.append(vals[-1])
#
## D
#vals = get_option(3,[values[i] for i in [6,5]])
#values.append(vals[-1])
#
## D
#vals = get_option(3,[values[i] for i in [7,5]])
#values.append(vals[-1])
#
## D
#vals = get_option(3,[values[i] for i in [8,5]])
#values.append(vals[-1])
#
## D
#vals = get_option(3,[values[i] for i in [9,5]])
#values.append(vals[-1])
#
## D
#vals = get_option(3,[values[i] for i in [10,5]])
#values.append(vals[-1])
#
## D
#vals = get_option(3,[values[i] for i in [11,5]])
#values.append(vals[-1])

# D
#vals = get_option(3,[values[i] for i in [12,5]])
#values.append(vals[-1])



#t= [vals[3+0]==values[3],vals[3+1]==values[5],vals[3+2]==values[1],vals[3+3]==values[5]]
#assert all(t)
#values.append(vals[-1])


