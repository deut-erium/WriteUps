from scapy.all import *
from tqdm import tqdm
from hashlib import md5

hashlookup = {md5(hex(i)[2:].zfill(2).encode()).hexdigest():hex(i)[2:].zfill(2) for i in range(256)}

# pcap = PcapReader("chall.pcap")
# f = open('dump.txt', 'wb')
# for p in pcap:
#     if IP in p and TCP in p:
#         f.write(bytes(p[TCP].payload))
#         f.write(b'\n')

with open("dump.txt") as f:
    data = f.read().strip().split('\n\n')

real = []
for line in data:
    q, resp = line.split()
    if resp != 'Match':
        real.append(hashlookup[resp])
    else:
        real.append(q)

with open('final','wb') as f:
    f.write(bytes.fromhex(''.join(real)))




# data = []
# currbyte = ''
# counter = 0
# for p in pcap:
#     counter +=1
#     if counter<16:
#         continue
#     if IP in p and TCP in p:
#         print(p[IP].payload)
#         if p[IP].src == '10.95.45.2':
#             currbyte = bytes(p[TCP].payload)
#         elif p[IP].src == '10.95.12.45':
#             if p[IP].payload == b'Match':
#                 data.append(bytes.fromhex(currbyte.decode()))
#             else:
#                 hash = bytes(p[TCP].payload).split()[-1]
#                 data.append(hashlookup.get(hash.decode(),b''))
#     print(data)




