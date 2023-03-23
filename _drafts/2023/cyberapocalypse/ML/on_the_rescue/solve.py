import torch
from architecture import *

model = BigramLanguageModel(len(vocab))
model.load_state_dict(torch.load("bigram_model.pt"))

def pred_next(text):
    idx = torch.tensor([vocab.index(c) for c in text])
    logits = model(idx.unsqueeze(0))
    pred_idx = torch.argmax(logits, dim=-1)
    pred_chars = [vocab[i] for i in pred_idx.squeeze()]
    pred_seq = "".join(pred_chars)
    return pred_seq[-1]

flag = "HTB{"
while True:
    x = pred_next(flag)
    flag+=x
    print(flag)
    if x=='}':
        break

# HTB{Pr0t3c7_L1fe}
# flag = "HTB{"
# flag = ""
# norms = []
# for i in vocab:
#     for j in vocab:
#         last_norm = get_norms(flag+i+j)[-2:]
#         norms.append(((i,j),last_norm))
# print(max(norms,key=lambda x:x[1][0]**2 + x[1][1]**2))
