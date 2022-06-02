from output import enc

p = 8443

l = len(enc)
flag = bytearray(l)
for flag_pos in range(l):
    values = [row[flag_pos] for row in enc]
    lookup_table = []
    for v in range(10,126):
        lookup_table.append({((flag_pos+1)*r*v)%p  for r in range(127)})
    for v in range(116):
        if all(rvs in lookup_table[v] for rvs in values):
            flag[flag_pos]=v+10

print(flag)
#CCTF{H0w_f1Nd_th3_4lL_3I9EnV4Lu35_iN_FiN173_Fi3lD5!???}
