## CFB
c[i] = E(c[i-1]) ^ p[i]

c[1] = E(iv)^p[1]

p[1] = E(iv)^c[1]

p[1] = D(c[1])^iv1


c1 = E(iv2,k2)^E(E(p1,k0)^iv1,k1)
c2 = E(c1,k2) ^ E(E(p2,k0)^E(E(p1,k0)^iv1,k1),k1)

D( D( E( iv2,k2 )^c1, k1)^iv1, k0)

D( D( E(c1,k2)^c2,k1)^(E(iv2,k2)^c1) ,k0)

D( D( E(iv2,k2)^c2,k1) ^ (E(iv2,k2)^iv2,k0)

## ECB
c[i] = E(p[i])

## CBC
c[i] = E(p[i]^c[i-1])

### Dec
## CFB
p[i] = D(c[i-1]) ^ c[i]

D(E(p)) = D(C)
