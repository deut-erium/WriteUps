with open('mobydick.txt','r') as f1:
    m1 = f1.read().split()

with open('solved.txt','r') as f2:
    m2 = f2.read().split()

assert len(m1) == len(m2)

for i in range(len(m1)):
    if m1[i] != m2[i]:
        print(m1[i], m2[i])

# quickly bquickly
# landlord alandlord
# the tthe
# more's more’s
# boarders pboarders
# young wyoung
# fellow's fellow’s
# HE he
# tints, ntints,
# Andes' Andes’
# "Grub, “Grub,
# ho!" ho!”
# landlord, {landlord,
# traveller, travelhler,
# Mungo's Mungo’s
# performances—this performances—thiis
# circumstance circumstadnce
# after aftder
# and and3
# sea-dogs, nsea-dogs,
# slightest _slightest
# boarded mboarded
# breakfast obreakfast
# timid btimid
# them—at them—ayt
# to _to
# THAT that
# people's people’s
# estimation, destimation,
# genteelly. igenteelly.
# not cnot
# Queequeg's Queequeg’s
# breakfast kbreakfast
# a a}

# apart from single quotes, and case differences, we get the flag batpwn{hidd3n_moby_dick}
