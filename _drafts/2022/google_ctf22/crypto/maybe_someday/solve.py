from chall import *
from Crypto.Util.number import *

secrets = [hashlib.sha512(long_to_bytes(i)).hexdigest().encode() for i in range(2**16)]
secrets1 = list(map(bytes_to_long,secrets))
