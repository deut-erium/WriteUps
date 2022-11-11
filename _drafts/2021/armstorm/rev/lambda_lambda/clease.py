from itertools import product

with open('chall.py','r') as f:
    data = f.read()

c=0
for prod in product('lL','aA','mM','bB','dD','aA'):
    name = "".join(prod)
    if name=="lambda":
        continue
    if name in data:
        data = data.replace(name,f'func_{c}')
        c+=1

with open('chall2.py','w') as f:
    f.write(data)


