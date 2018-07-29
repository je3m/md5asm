#!/usr/bin python3
import struct
import array

def leftrotate (x, c):
    return (x << c) | (x >> (32-c));

# Note: All variables are unsigned 32 bit and wrap modulo 2^32 when calculating
message = 'a'
# s specifies the per-round shift amounts
s = []
s[ 0:15] = [7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22]
s[16:31] = [5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20]
s[32:47] = [4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23]
s[48:63] = [6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21]

# (Or just use the following precomputed table):
K=[]
K[ 0: 3] = [ 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee ]
K[ 4: 7] = [ 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501 ]
K[ 8:11] = [ 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be ]
K[12:15] = [ 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821 ]
K[16:19] = [ 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa ]
K[20:23] = [ 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8 ]
K[24:27] = [ 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed ]
K[28:31] = [ 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a ]
K[32:35] = [ 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c ]
K[36:39] = [ 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70 ]
K[40:43] = [ 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05 ]
K[44:47] = [ 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665 ]
K[48:51] = [ 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039 ]
K[52:55] = [ 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1 ]
K[56:59] = [ 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1 ]
K[60:63] = [ 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391 ]

# Initialize variables:
a0 = 0x67452301   # A
b0 = 0xefcdab89   # B
c0 = 0x98badcfe   # C
d0 = 0x10325476   # D


#  Notice: the input bytes are considered as bits strings,
#   where the first bit is the most significant bit of the byte.[48]
message = bytes([0x61]) + bytes([0x80]) + bytes([0x00])*54 + (bytes([0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
# Pre-processing: padding with zeros
# append "0" bit until message length in bits ≡ 448 (mod 512)
# append original length in bits mod 264 to message

message = [message]
print(message)
# Process the message in successive 512-bit chunks:
for chunk in message:
    # break chunk into sixteen 32-bit words M[j], 0 ≤ j ≤ 15
    M = [struct.unpack("<I", bytearray(x))[0] for x in [(chunk[i:i+4]) for i in range(0, 64, 4)]]
    # Initialize hash value for this chunk:
    A = a0
    B = b0
    C = c0
    D = d0
    # Main loop:
    for i in range(64):
        F = None
        g = None
        if 0 <= i <= 15:
            F = (B & C) | ((~B) & D)
            g = i
        elif 16 <= i <= 31:
            F = (D & B) | ((~D) & C)
            g = (5*i + 1) % 16
        elif 32 <= i <= 47:
            F = B ^ C ^ D
            g = (3*i + 5) % 16
        elif 48 <= i <= 63:
            F = C ^ (B | (~D))
            g = (7*i) % 16
        # Be wary of the below definitions of a,b,c,d
        F = (F + A + K[i] + M[g]) % 2**32
        A = D
        D = C
        C = B
        B = (B + leftrotate(F, s[i])) % 2**32
  
        print('i={} a={} b={} c={} d={} f={}'.format(i, hex(A), hex(B), hex(C), hex(D), hex(F)))

    # Add this chunk's hash to result so far:
    a0 = (a0 + A) % 2**32
    b0 = (b0 + B) % 2**32
    c0 = (c0 + C) % 2**32
    d0 = (d0 + D) % 2**32

a0 = [hex(x)[2:].zfill(2) for x in a0.to_bytes(4, 'little')]
b0 = [hex(x)[2:].zfill(2) for x in b0.to_bytes(4, 'little')]
c0 = [hex(x)[2:].zfill(2) for x in c0.to_bytes(4, 'little')]
d0 = [hex(x)[2:].zfill(2) for x in d0.to_bytes(4, 'little')]

digest = ''.join(a0+b0+c0+d0) # (Output is in little-endian)

print(digest)
# leftrotate function definition
