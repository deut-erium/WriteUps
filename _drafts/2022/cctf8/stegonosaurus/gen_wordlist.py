import sys

f2 = open('wordlist.txt', 'wb')
with open(sys.argv[1], 'rb') as f:
    for line in f.read().strip().split(b'\n'):
        f2.write(b"%s%s%s_%s%s%s\n" % tuple([line]*6))
        line = line[:1].upper()+line[1:].strip()
        f2.write(b"%s%s%s_%s%s%s\n" % tuple([line]*6))
