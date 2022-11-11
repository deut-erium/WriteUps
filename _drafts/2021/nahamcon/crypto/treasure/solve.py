with open('hackers.txt','r') as f:
    data = f.read()

data2 = "".join(data.split())
data3 = data.translate("".maketrans({i:"" for i in " \n\t.,-():/'\""  }))
indices = [4661, 5099, 13243, 11578, 14382, 734, 14024, 10621, 14382, 2, 3383, 8702, 6087, 10621, 7417, 14382, 12352, 615 ,1208, 4246 ,4657, 9975, 7203, 2658, 770, 4 ,10621, 8702, 6125, 980]

print("".join(data[i] for i in indices))
print("".join(data2[i] for i in indices))
print("".join(data3[i] for i in indices))
