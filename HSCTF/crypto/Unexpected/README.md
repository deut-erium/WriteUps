# Unexpected

We are given 3 N's and 3 C's and given that all three share primes
i.e 
N1 = p*q
N2 = q*r
N3 = r*p

Now, we know factoring N into their factors is hard. However this can be don easily considering we have a common factor between pairs of N
i.e q is a common factor of N1 and N2, r is a common factor of N2 and N3
and p is a common factor of N3 and N1.

Once we get p, q and r, we can easily calculate Euler Totien phi and the modular inverse of E with respect to respective phis.
