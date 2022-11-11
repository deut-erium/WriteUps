import gmpy2
from functools import reduce
def gcd(*args):
    return reduce(gmpy2.gcd,args)

seeds = [885247661,590732011,616008796,241172185,1079271406,1667638080,1184133563,1001836592,1595809264,843032665]
seeds = [284777197,1656784463,1303502639,1488170626,2089158220,1124575090,729960383,2017565417,455177389,829626309]

diffs = [j-i for i,j in zip(seeds,seeds[1:])]
diffs2 = [b**2 - a*c  for a,b,c in zip(diffs,diffs[1:],diffs[2:]) ]
p = gcd(*diffs2)
a = (diffs[1]*gmpy2.invert(diffs[0],p))%p
b = (seeds[1]-a*seeds[0])%p

assert all(j == (a*i+b)%p for i,j in zip(seeds,seeds[1:]))
print("P:",p)
print("a:",a)
print("b:",b)

next = (a*seeds[-1]+b)%p


"""
 ================ !!! CORRECT !!! ================


                 NNNhhsssssssssyhdmN
             NmdsoososyhhhhdhhhhyooosymN
           Nhos+oyhhysyyssssssyyyhddysosymN
         Ndo//----:+sssssssssssssyo/::::++shN
       Ndo/:::::::::yss+osssso+syo//:::::::/o
      ms/:::::://///yss.`/ss+``sho/////::::::/d
     mo::::://///+++ys+ ``.- ` /ys+++/////::::/hN
    dy::://///+++++ohs. +o-.oo `sho+++++/////::/y
   N+o/////+++++oooyyo `ssssss. +hsooo+++++/////ys
   yos//+++++oooooshyyyyyhddhhyyyyhsooooo+++++//hoN
  N+sms+++oooooosyhyyydmy+::/ommyyyhysoooooo+++ymhy
  d/hdyhyyyyyyyyhyyyyNh..`` `.`+NhyyyhyyyyyyyyyyhNo
  dodNmmmmmmmmmmmmmmmN`.      . yNmmmmmmmmmmmmmmm s
  dohs//////////////o `.      . hh//////////////+ s
  moys               sd-``````.sd.              :my
   som                :yhs++oyh+`             `.yh
   m+do                 `.::-``              `./Ny
    d+d:                                    `.:do
     yom:    darkCON{P0k3m0ns_4nd_RNG!!!} `../mh
      hoho`                              `.-ohy
       Nysy/`                          ``./yyhN
        Ndyys/.                      ``-+yhyN
          Nmmsys/.`                `-/shydN
             Ndymyss/:-...``...-:/oyydmmN
                 NdmmhdyhhhhhhhdddmmN

"""

