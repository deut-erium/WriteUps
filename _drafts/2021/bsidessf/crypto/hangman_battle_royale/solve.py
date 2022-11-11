import re
from twister import MT19937
import pwn

HOST,PORT = "hangman-battle-royale-2d147e0d.challenges.bsidessf.net", 2121

REM = pwn.remote(HOST,PORT)
REM.sendline('10') # we need atleast 624
#pwn.context(log_level=1)
with open('words.txt','r') as f:
    wordlist = f.read().strip().split('\n')

with open('first-names.txt','r') as f:
    firstnames = f.read().strip().split('\n')

with open('last-names.txt','r') as f:
    lastnames = f.read().strip().split('\n')

def guess(template):
    pattern = template.replace(' ','').replace('_','.')
    matches = []
    for word in wordlist:
        if len(word) == len(pattern) and re.match(pattern,word):
            matches.append(word)
    return matches

def get_int_from_name(first_name,last_name):
    i1 = firstnames.index(first_name)
    i2 = lastnames.index(last_name)
    return (i2<<16)+i1

def opponent_name(number):
    return f'{firstnames[number&0xffff]} {lastnames[number>>16]}'


participants = REM.recvuntil(b'GOOD LUCK!!')
x = re.findall( b'(\w+) (\w+).*\-vs\-  (\w+) (\w+)',participants)
random_integers = []
for i in x:
    random_integers.append(get_int_from_name(i[0].decode(),i[1].decode()))
    random_integers.append(get_int_from_name(i[2].decode(),i[3].decode()))

random = MT19937()
random.clone(random_integers[:624])
for _ in range(1023-624):
    random.sample()
word = wordlist[random.sample()]
REM.sendline(word)
REM.sendline()
REM.sendline()

l = 1023
while l:
    for _ in range(l-1):
        random.sample()
    word = wordlist[random.sample()]
    REM.sendline(word)
    REM.sendline()
    REM.sendline()
    l = l//2


REM.interactive()

#CTF{hooray_mt19937}
















