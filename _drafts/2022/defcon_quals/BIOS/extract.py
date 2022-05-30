import re
with open('bios-nautilus.bin',"rb")as f:
    x=f.read()
print(len(x))
s=[m.start() for m in re.finditer(b'LARCHIVE', x)]
for i in range(0,len(s)):
    tmp="extracted/%d.bin"%i
    if i==len(s)-1:
        with open(tmp,'wb')as dd:
            dd.write(x[s[i]:])
    else:
        with open(tmp,'wb')as dd:
            dd.write(x[s[i]:s[i+1]])
