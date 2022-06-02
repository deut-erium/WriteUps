import random
from tqdm import tqdm
LIMIT = 26**3
SIZE = 10**9

correct = 0
for t in tqdm(range(SIZE)):
    passwords = [random.randint(0,LIMIT-1) for i in range(3)]
    correct += (sum(passwords)<150)

print(correct,correct/SIZE)


