import pyshark
from twister import MT19937
pcap = pyshark.FileCapture('knockd.pcap')
pcap.load_packets()
ports = []
for packet in pcap:
    if packet.tcp.dstport!='2222' and packet.ip.src_host=='192.168.0.105' and int(packet.tcp.flags,16)==2:
        ports.append(int(packet.tcp.dstport))

outputs = [(ports[i]<<16)+ports[i+1] for i in range(0,len(ports),4)]
rand = MT19937()
rand.clone(outputs)
next_num = rand.randint()
print(divmod(next_num,2**16))
#VolgaCTF{15094,7850}
