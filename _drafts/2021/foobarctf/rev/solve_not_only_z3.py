from z3 import *
V11 = [BitVec(f'x[{i}]',32) for i in range(32)]
V9 = [0 for i in range(25)]


def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t))
    def fix_term(s, m, t):
        s.add(t == m.eval(t))
    def all_smt_rec(terms):
        if sat == s.check():
           m = s.model()
           yield m
           for i in range(len(terms)):
               s.push()
               block_term(s, m, terms[i])
               for j in range(i):
                   fix_term(s, m, terms[j])
               for m in all_smt_rec(terms[i:]):
                   yield m
               s.pop()
    for m in all_smt_rec(list(initial_terms)):
        yield m


"""
  v[12] = __readfsqword(0x28u);
  printf("Enter the string : ");
  __isoc99_scanf("%s", s);
  v[3] = strlen(s);
  bytes2md5((__int64)s, v[3], (__int64)v[11]);
  for ( i = 0; i <= 24; ++i )
    v[9][5 * (i / 5) + i % 5] = v[11][i];
  for ( j = 0; j <= 4; ++j )
  {
    for ( k = 0; k <= 1; ++k )
    {
      v[9][5 * j + k] ^= v[9][5 * j + 3 + k];
      v[9][5 * j + 3 + k] ^= v[9][5 * j + k];
      v[9][5 * j + k] ^= v[9][5 * j + 3 + k];
    }
  }
  for ( l = 0; l <= 24; ++l )
    v[11][l] = v[9][5 * (l / 5) + l % 5];
  if ( (unsigned int)check(v[11]) == 1 )
    printf("\nConratulations : GLUG{%s_%s}\n\n", s, v[11]);
  return 0;
"""


for j in range(5):
    for k in range(2):
        V11[5*j+k] ^= V11[5*j+3+k]
        V11[5*j+3+k] ^= V11[5*j+k]
        V11[5*j+k] ^= V11[5*j+3+k]

V11 = [simplify(i) for i in V11]


constraints = [4 * V11[3] + 8 * V11[2] + 9 * V11[0] + 3 * V11[1] + 2 * V11[4] == 1328
, 6 * V11[3] + 7 * V11[2] + 7 * V11[1] + 6 * V11[0] + 7 * V11[4] == 1685
, 4 * V11[2] + 4 * V11[0] + 5 * V11[1] + 4 * V11[3] + 6 * V11[4] == 1176
, V11[2] + 9 * V11[0] + 3 * V11[1] + 4 * V11[3] + 7 * V11[4] == 1245
, V11[0] + V11[1] + 7 * V11[2] + V11[3] + 7 * V11[4] == 862
, 2 * V11[8] + 4 * V11[7] + V11[5] + 2 * V11[6] + 8 * V11[9] == 1277
, 9 * (V11[6] + V11[5]) + 4 * V11[7] + 3 * V11[8] + 8 * V11[9] == 2151
, 6 * V11[7] + 3 * V11[6] + 7 * V11[5] + 6 * V11[8] + V11[9] == 1302
, V11[8] + 4 * V11[7] + 3 * V11[5] + 6 * V11[6] + V11[9] == 852
, 4 * V11[8] + 5 * V11[6] + 9 * V11[5] + 9 * V11[7] + 4 * V11[9] == 1871
, 7 * V11[11] + 6 * V11[10] + 9 * V11[12] + 2 * V11[13] + 3 * V11[14] == 1724
, 9 * V11[11] + 6 * V11[10] + 3 * V11[12] + 2 * V11[13] + 5 * V11[14] == 1712
, 9 * V11[13] + 6 * V11[12] + 6 * V11[11] + 4 * V11[10] + 3 * V11[14] == 1703
, 7 * V11[12] + 6 * V11[11] + 4 * V11[10] + 7 * V11[13] + 2 * V11[14] == 1605
, 7 * V11[12] + 6 * V11[11] + V11[10] + 9 * V11[13] + 2 * V11[14] == 1551
, 4 * V11[18] + 4 * V11[17] + 8 * V11[16] + 6 * V11[15] + 2 * V11[19] == 1822
, 6 * V11[18] + 5 * (V11[16] + V11[15]) + 4 * V11[17] + 3 * V11[19] == 1784
, 4 * V11[17] + 5 * V11[15] + 7 * V11[16] + V11[18] + 5 * V11[19] == 1800
, 3 * V11[16] + 6 * V11[15] + 9 * V11[17] + V11[18] + 7 * V11[19] == 2399
, 5 * V11[17] + 7 * V11[16] + 3 * V11[15] + 5 * V11[18] + 2 * V11[19] == 1622
, 6 * V11[22] + 6 * V11[21] + V11[20] + 9 * V11[23] + V11[24] == 1263
, 9 * V11[20] + V11[21] + 6 * V11[22] + V11[23] + 9 * V11[24] == 1370
, 9 * V11[23] + 6 * V11[22] + 7 * V11[21] + 4 * V11[20] + 5 * V11[24] == 1686
, 7 * V11[22] + 6 * V11[21] + 3 * V11[20] + 5 * V11[23] + 2 * V11[24] == 1250
, 5 * V11[23] + 4 * (2 * V11[21] + V11[20]) + V11[22] + 3 * V11[24] == 1157
, V11[25] + 8 * V11[26] + 5 * V11[27] + 4 * V11[28] + 9 * V11[29] == 1400
, 8 * V11[28] + 6 * V11[26] + V11[25] + 3 * V11[27] + V11[29] == 1012
, 5 * V11[25] + 6 * V11[26] + V11[27] + 7 * V11[28] + 8 * V11[29] == 1427
, 5 * V11[27] + V11[25] + 4 * V11[26] + 5 * V11[28] + 2 * V11[29] == 895
, 7 * V11[28] + 7 * V11[27] + 3 * V11[26] + 2 * V11[25] + 3 * V11[29] == 1163
, V11[30] == 55
, V11[31] == 51]



for i in range(32):
    constraints.append(V11[i]>=0)
    constraints.append(V11[i]<=128)


s = Solver()
s.add(constraints)
for m in all_smt(s,V11):
    md5_chars = { str(i):m[i] for i in m.decls()}
    md5_chars = [ md5_chars[f'x[{i}]'].as_long() for i in range(32) ]
    #md5_chars = [ m.eval(V11[i]).as_long() for i in range(32) ]
    print(bytes(md5_chars))



