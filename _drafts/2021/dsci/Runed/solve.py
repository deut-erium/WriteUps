with open('runed.txt','rb') as f:
    data = f.read().decode()

import string

data=data.replace(' ','')
data=data.replace('\n','')
data=data.replace('\r','')
chars = list(set(data))
mapping = {i:v for i,v in zip(chars,string.ascii_letters)}

data2 = data.translate("".maketrans(mapping))
