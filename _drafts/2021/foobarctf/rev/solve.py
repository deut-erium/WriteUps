from nltk.corpus import words
from tqdm import tqdm
wordlist = words.words()

starts = [104, 108, 116, 112, 108, 92, 116, 108, 92, 96, 112, 112, 100, 108, 96, 108, 120]

def check(word,start):
    for ind,char in enumerate(word):
        if not ord(char) in range(start[ind],start[ind]+4):
            return False
    return True

for word in tqdm(wordlist):
    if 9>=len(word)>=5:
        for i in range(len(word)-4):
            if check(word[i:i+5],starts[:5]):
                print(word)

for word in tqdm(wordlist):
    if len(word)==8:
        if check(word,starts[-8:]):
            print(word)

