# Morbid

![](Capture.PNG)

### Contents of Morbit.pdf
```
MORBIT (50-75 plaintext letters)

Choose a  9-letter  keyword  to  set  up an  array  as  shown.  Plaintext  is  enciphered
exactly  as in  the  Fractionated  Morse,  x  between  letters,  xx  between  words.  The
result is then taken off in units of 2, placed vertically, and numbers are taken from
the array to form the ciphertext. Numbers represent alphabetical order of the key. (It
is often as easy to read pairs horizontally as to rearrange them vertically.) Morse
code letters, numbers, and punctuation can be found in Appendix 1.

Key:

 W I S E C R A C K
 9 5 8 4 2 7 1 3 6
 • • • – – – x x x
 • – x • – x • – x

pt: Once upon a time.

pt:   o      n       c     e   /    u        p       o       n
MC: – – – x – • x – • – • x • x x • • – x • – – • x – – – x – •
CT: 2   7   4   3   5   8   8   1   5   1   2   8   2   7   4

 /  a    /  t    i     m    e
x x • – x x – x • • x – – x • x
6   5   6   7   9   3   7   8

CT: 27435 88151 28274 65679 378.
```

> We have to decrypt 118289293938434193849271464117429364476994241473157664969879696938145689474393647294392739247721652822414624317164228466

Since Morse code is (Huffman encoded)[https://en.wikipedia.org/wiki/Huffman_coding], the frequencies of - (dash) and . (dot) would be equivalent in the ciphertext.
(I am not sure about x since spaces are way more frequent than any letter.) Without thinking more about analyzing the problem statistically, one simple way to solve the problem is (brute-forcing)[https://en.wikipedia.org/wiki/Brute-force_attack]
the key which is 9 different decimal characters i.e 9! (362880) permutations to check, which is fairly easy.


