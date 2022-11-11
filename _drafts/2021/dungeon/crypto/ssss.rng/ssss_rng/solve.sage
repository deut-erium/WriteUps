p=2908561168050746475465170048583677924550221390147321314856251074876765877416890922338619139786060615096740196376171212325702080653039392939240436429222829
vs = [(1, 1651293975450381579706844999808202297670211173037061827272908790114230592434748044848097133563469251678879059156225205298834971071359017469397331605782920), (2, 49656064002974834481096383104316375265711545391722811288216446968986145936494966876404160910407919885451814058823146922107458035910700220495010462147112), (3, 1481214561214496310917942246038921499126047497749957535731608952096552856013930232284898279007009260107597472601959627310496773682697020898442717240484400), (4, 1950790377868548708758723604473108315857898618124646291056275632619091046294238343215502355242288776617394025418770078552886012721353626716473759644786481)]
fflag = 708078355843841364722603057137729966137248436075776171805731561888875332687774464375592593202164126123800524500062359645261336234459019198930345744751457

#PR.<X> = PolynomialRing(GF(p))

import sympy
#a,b,xx,flag = sympy.symbols('a b xx flag')

import z3
a,b,xx,flag = z3.Ints('a b xx flag')


def poly(x):
    return xx*(1 + a*x + a**2*x**2 + a**3*x**3 + a**4*x**4 + a**5*x**5) \
        + b*(x + x**2 + x**3 + x**4 + x**5) \
        + a*b*(x**2 + x**3 + x**4 + x**5) \
        + a**2*b*(x**3 + x**4 + x**5) \
        + a**3*b*( x**4 + x**5) \
        + a**4*b*( x**5) 

eqns = [z3.ToInt(poly(v))%p==u for v,u in vs]+[poly(flag)==fflag]
