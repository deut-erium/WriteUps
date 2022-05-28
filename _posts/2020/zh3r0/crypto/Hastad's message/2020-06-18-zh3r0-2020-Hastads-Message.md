---
title: "zh3r0 2020 Crypto - Hastads Message"
tags: zh3r0 2020 cryptography RSA netcat hastad_broadcast 
key: zh3r02020hastadmessage
aside:
  toc: true
sidebar:
  nav: aboutnav
author: deuterium
full_width: true
mathjax: false
mathjax_autoNumber: false
mermaid: false
chart: false
show_edit_on_github: true
comment: false
show_author_profile: true
excerpt_separator: <!--more-->
---

# Hastad's message

## Description
```
My friend Hastad send me a message but I am not able to read it. Only thing I know is its different each time.

nc crypto.zh3r0.ml 7419

Author : Finch
```
Lets see what happens on netcatting the server
```bash
nc crypto.zh3r0.ml 7419
N: 23960949631136549010580709371447459320771722990641656469289715710142295495124948621158687847083208321529502678539090062646598194881513644884917107213812662366208358112312352493421491108487646779847913555365232445323100586810554337396802321687583853564014322973591145624358708717154959936810785468753949008206142023804817260040790518084021622384353866920735686392298903432107818842976616256573476622111842313072427546938261932845421278479601467336933001268076347078440263527121488940955096416278279178798796690987949446654662309459137968716222579092928758172393534109727678426842059547321144586394122734488337726519323
CT: 227059187351066098625783541971089392467634459318790709268858559192434047499480309412579083821300334591844236270609009973361475929758503137053407947719992678067213345691730884130984948269760409377387182408382901865063563197855973716061186698464514471396611589444565490413420291027976549067671317090855345614720660091447411352743154483543882911609825811237463533161033015225348903818654092266745103119323634975445483632136349285067303046354417457399725704445620542851629021518600614724115418587100535103614591024058009100867886873645448085895672556328107317146860148115428326779626735944070697777532801165480737197887

nc crypto.zh3r0.ml 7419
N: 19791835797467968357781023201751418927414446960804616978761511157078113663179187861424084330439298752016426827511729758116017707091810721778115106421089836091446335664873679115986024499553368018618180980675378966672270277223004345804456079490509644500315527668853314227967157724434593288928717409769329504108075955720491368982617136637949677075904806255856973263169683471225088227111875834893684890773308254690749350361499046839876782311421321293581596891957063996822944880748413912918449495187723853846990398774013411469435139373416719302794535340647770663325255798177030402073444060330933741585572502434974728609629
CT: 10711359293091554845881300822684711074568687131225620493949233624467865101717568049146348940908572825867892102293917086246693559590253393642111568749678496708913448534499719991790370596573494298284551208853926324027482089457255364249679293745545596390096142487991844667316810725319734547236480559387130970727056695739296995521658873612344594309074750945101640289646280263680077704687362201539836493130512269933864993372038031365219372876820509384843218417119861722826817692819050782742051978075955954644891972344674684686471352127887490340543050726681324525005791961696941767799080026081048866749630207206154339441796
```

Seems like its encrypting the same message with different `N` and a same `e`each time which we dont know

This could be a variant of [Hastad's broadcast attac](https://en.wikipedia.org/wiki/Coppersmith%27s_attack#H%C3%A5stad's_broadcast_attack) as the name of the challenge suggests.  
One can read about RSA attacks and their implementations on [ENOENT's Blog](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-2/)

If we have a small `e`, we know each `M` < `Ni`  
So if we can get `e` messages somehow, we know 
```
M^e < N1N2N3...Ne
```
and 
```
M^e = C
```
There would be no wrap-around of modulus `N1N2...Ne`We can simply calculate `e`th root of `M^e` to get `M`

But we dont know what the `e` is!  
No problems, we can request the server as many times we wish, 
Basic idea is to apply [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_Remainder_Theorem) over the set of C's and N's till we get a valid decryption.  

```python
from pwn import remote
from sympy.ntheory.modular import crt
from gmpy2 import iroot

HOST, PORT = "crypto.zh3r0.ml", 7419
n = []
c = []

REM = remote(HOST, PORT)
n.append(int(REM.recvline().strip()[2:]))
c.append(int(REM.recvline().strip()[3:]))
REM.close()
e=2
while True:
    print(e)
    REM = remote(HOST, PORT)
    n.append(int(REM.recvline().strip()[2:]))
    c.append(int(REM.recvline().strip()[3:]))
    resultant, mod = crt(n,c)
    value, is_perfect = iroot(resultant,e)
    if is_perfect:
        print(bytes.fromhex(hex(value)[2:]).decode())
        break
    e+=1
    REM.close()

```

```
Its great that you have come till here. As promised here is your flag: zh3r0{RSA_1s_0n3_of_th3_b4st_encrypt10n_Bu66y}
```
## zh3r0{RSA_1s_0n3_of_th3_b4st_encrypt10n_Bu66y}
