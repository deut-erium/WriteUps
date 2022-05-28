
def storage:
  S0 is uint256 at storage 0
  result is uint256 at storage 1
  num is uint256 at storage 2
  S3 is uint256 at storage 3
  S4 is uint256 at storage 4
  S5 is uint256 at storage 5
  S6 is uint256 at storage 6
  S7 is uint256 at storage 7
  S8 is uint256 at storage 8
  S9 is uint256 at storage 9
  ukaddr is addr at storage 10

def S4() payable:
  return S4

def S5() payable:
  return S5

def S0() payable:
  return S0

def S3() payable:
  return S3

def S7() payable:
  return S7

def num() payable:
  return num

def S8() payable:
  return S8

def ukaddr() payable:
  return ukaddr

def S9() payable:
  return S9

def c() payable:
  return result

def S6() payable:
  return S6

def getResult() payable:
  return result

#
#  Regular functions
#

def _fallback() payable: # default function
  revert

def unknownf2626325(uint256 _param1) payable:
  require calldata.size - 4 >=ΓÇ▓ 32
  require _param1 == _param1
  num = 9
  return num

def unknown2b4e9638(uint256 _param1) payable:
  require calldata.size - 4 >=ΓÇ▓ 32
  require _param1 == bool(_param1)
  require S8 == 2
  return 9001

def unknown16bc9b3c() payable:
  require S9 == 3
  if S4 > -4097:
      revert with 'NH{q', 17
  S5 = S4 + 4096
  return S5

def sub(uint256 _a, uint256 _b) payable:
  require calldata.size - 4 >=ΓÇ▓ 64
  require _a == _a
  require _b == _b
  if _a < _b:
      revert with 'NH{q', 17
  result = _a - _b

def add(uint256 _a, uint256 _b) payable:
  require calldata.size - 4 >=ΓÇ▓ 64
  require _a == _a
  require _b == _b
  if _a > -_b - 1:
      revert with 'NH{q', 17
  result = _a + _b

def mul(uint256 _a, uint256 _b) payable:
  require calldata.size - 4 >=ΓÇ▓ 64
  require _a == _a
  require _b == _b
  if _a and _b > -1 / _a:
      revert with 'NH{q', 17
  result = _a * _b

def unknownd6b8e4b3(uint256 _param1) payable:
  require calldata.size - 4 >=ΓÇ▓ 32
  require _param1 == addr(_param1)
  require S8 == 2
  if not addr(_param1) - ukaddr:
      S9 = 3
  return 3

def div(uint256 _a, uint256 _b) payable:
  require calldata.size - 4 >=ΓÇ▓ 64
  require _a == _a
  require _b == _b
  if _b <= 0:
      revert with 0x8c379a000000000000000000000000000000000000000000000000000000000, 'The second parameter should be larger than 0'
  if not _b:
      revert with 'NH{q', 18
  result = _a / _b

def unknownf33030f7() payable:
  require S0 == 5 * 10^10
  S8 = 2
  require S8 == 2
  S6 = 9001
  if S3 > -S6 - 1:
      revert with 'NH{q', 17
  S4 = S3 + S6
  ukaddr = 0x5b38da6a701c568545dcfcb03fcb875f56beddc4
  return S4

def enter(uint256 _kitty) payable:
  require calldata.size - 4 >=ΓÇ▓ 32
  require _kitty == _kitty
  S0 = 9
  if not _kitty - 123:
      S3 = 6845
      S7 = 1
      require S7 == 1
      S0 = 5 * 10^10
      if S3 > -9276917453894:
          revert with 'NH{q', 17
      S3 += 9276917453893
  require S7 == 1
  S0 = 5 * 10^10
  if S3 > -9276917453894:
      revert with 'NH{q', 17
  S3 += 9276917453893
  return 0



