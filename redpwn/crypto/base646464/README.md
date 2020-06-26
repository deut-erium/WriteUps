# base646464

## Description
```
Encoding something multiple times makes it exponentially more secure!
```

## Files
- [cipher.txt](cipher.txt)
- [generate.js](generate.js)

Lets take a look at generate.js, which reads  
```javascript
const btoa = str => Buffer.from(str).toString('base64');

const fs = require("fs");
const flag = fs.readFileSync("flag.txt", "utf8").trim();

let ret = flag;
for(let i = 0; i < 25; i++) ret = btoa(ret);

fs.writeFileSync("cipher.txt", ret);
```

The function `btoa` is basically string to its base64 encoding.  
The flag is encoded repetitively 25 times in a for loop.  
We just need to base64 decode it 25 times and we will get the flag.

```python
from base64 import b64decode

with open('cipher.txt','r') as cipher_file:
    data = cipher_file.read()

for i in range(25):
    data = b64decode(data)

print(data)
```
A cool sarcasm on bad crypto challenges in CTFs :)  
### flag{l00ks_l1ke_a_l0t_of_64s}
