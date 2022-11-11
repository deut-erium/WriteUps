from z3 import *


code = """
size_t
  _Hash_bytes(const void* ptr, size_t len, size_t seed)
  {
    static const size_t mul = (((size_t) 0xc6a4a793UL) << 32UL)
                              + (size_t) 0x5bd1e995UL;
    const char* const buf = static_cast<const char*>(ptr);
    // Remove the bytes not divisible by the sizeof(size_t).  This
    // allows the main loop to process the data as 64-bit integers.
    const int len_aligned = len & ~0x7;
    const char* const end = buf + len_aligned;
    size_t hash = seed ^ (len * mul);
    for (const char* p = buf; p != end; p += 8)
      {
        const size_t data = shift_mix(unaligned_load(p) * mul) * mul;
        hash ^= data;
        hash *= mul;
      }
    if ((len & 0x7) != 0)
      {
        const size_t data = load_bytes(end, len & 0x7);
        hash ^= data;
        hash *= mul;
      }
    hash = shift_mix(hash) * mul;
    hash = shift_mix(hash);
    return hash;
  }

shift_mix(std::size_t v)
  { return v ^ (v >> 47);}
"""

from z3 import *
def shift_mix(v): return v^(v>>47)

v = BitVec('v',64)
TARGET = 0x3dba201d32b78891 # insert your value here
MUL = 0xc6a4a7935bd1e995 # mul constant
SEED = 0xc70f6907 # seed constant

MASK = 0xffffffffffffffff

hash = (SEED ^ (8*MUL))&MASK
data = shift_mix(v*MUL)*MUL
hash = ((hash^data)*MUL)&MASK
hash = shift_mix(hash)*MUL
hash = shift_mix(hash)

s = Solver()
s.add(hash == TARGET)
if s.check() == sat:
    model = s.model()




