def crc(msg,poly,bits):
    mask = (2**bits)-1
    crc = mask
    for byte in msg:
        for _ in range(8):
            if (byte^crc)&1:
                crc = (crc>>1)^poly
            else:
                crc>>=1
            byte>>=1
    return crc^mask
