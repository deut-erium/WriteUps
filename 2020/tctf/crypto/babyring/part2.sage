last_64 = [15358749963209991260, 378308928256207547, 3123812763769384410, 11396253402115505781, 7515326433971021135, 6690912353342611008, 8112671349578408294, 14187003746859602588, 520403579989697783, 15565254829283843456, 11093115555945605369, 6675697843247987806, 940793759804036398, 4271819274916099901, 9599471660238663670, 10825869877069188108, 13351959091760411402, 1617903979117669972, 15330980875166694510, 181622928990578978, 11336275035351744495, 17094614858250387923, 5654591548198046490, 3304560256334604855, 6336466022714036308, 3201835284012535979, 4028486200859410711, 15074014686663007202, 8742968117092195322, 3776751443202676799, 1211547090914465752, 14274998475695071456, 15954290579262726234, 11811652654563814687, 9770628958889979891, 2459615839954359952, 12532936939246760, 2841589397081585807, 15058115057405336624, 9859939296446429087, 353918551023370860, 6472782004751239315, 4924408521923396337, 12819730153302066300, 14562140169881556528, 5974207222554706084, 6347901213133172200, 16451064694092648235, 7962387794911479040, 6257623171379700357, 2515104189235730352, 3679683532782804001, 5967404995224064372, 15557019607012690882, 14419951376779290285, 10130788997381517479, 17962859451300312998, 1020036897740161094, 14424050503035998718, 5615758097873457040, 3631625732406650283, 2978067290246498806, 12660506848721508904, 632728823217740849]
#last_64 = [pow(2,e,i)%(1<<64) for i in Ns]
invariant = 911494890333775973 #for msg = b'aaa'
I = GF(2**64)
last_64_mat = [ list(map(int, bin(i)[2:].zfill(64))) for i in last_64  ]
mat = matrix(I,last_64_mat)
invariant_vec = list(map(int, bin(invariant)[2:].zfill(64)))
invariant_vec = matrix(I,invariant_vec)
op = mat.solve_left(invariant_vec)
print(op[0])

assertion = 0
for i in range(64):
    if (op[0][i] == 1):
        assertion ^^= last_64[i]
print(assertion == invariant)

