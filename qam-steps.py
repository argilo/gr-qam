# Copyright 2014 Clayton Smith
#
# This file is part of qam-tx
#
# qam-tx is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# qam-tx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qam-tx; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

### 4   MPEG Transport Framing

C = [
    0xb0f3,0x857f,0x97a5,0x0ddb,0xeba0,0xcaa3,0x58c1,0x2da9,0xa7ee,0x67b2,
    0x1039,0x2627,0x5688,0xa47c,0x05c7,0x78b3,0x61e7,0x0aff,0x2f4a,0x1bb7,
    0xd741,0x9546,0xb182,0x5b53,0x4fdc,0xcf64,0x2072,0x4c4e,0xad11,0x48f8,
    0x0b8e,0xf166,0xc3ce,0x15fe,0x5e94,0x376f,0xae83,0x2a8d,0x6304,0xb6a6,
    0x9fb9,0x9ec8,0x40e4,0x989d,0x5a22,0x91f0,0x171d,0xe2cd,0x879c,0x2bfc,
    0xbd28,0x6edf,0x5d06,0x551a,0xc609,0x6d4d,0x3f73,0x3d90,0x81c9,0x313a,
    0xb445,0x23e0,0x2e3b,0xc59b,0x0f38,0x57f9,0x7a50,0xddbe,0xba0c,0xaa35,
    0x8c12,0xda9a,0x7ee6,0x7b21,0x0392,0x6275,0x688a,0x47c0,0x5c77,0x8b36,
    0x1e70,0xaff2,0xf4a1,0xbb7d,0x7419,0x546b,0x1825,0xb534,0xfdcc,0xf642,
    0x0724,0xc4ea,0xd114,0x8f80
]

Cbits = [0] * 1504
bit = 0
for Cword in C:
    for i in range(16):
        Cbits[bit] = (Cword >> (15-i)) & 1
        bit += 1
Cbits = Cbits[0:1497]

def compute_sum(bytes):
    result = 0

    row = [0] * 1504
    bit = 0
    for byte in bytes:
        for i in range(8):
            row[bit] = (byte >> (7-i)) & 1
            bit += 1

    for i in range(8):
        total = (0x47 >> (7-i)) & 1
        for j in range(1496):
            total ^= row[i+j] & Cbits[j]
        row[1496+i] = total
        result |= (total << (7-i))

    return result

def verify_packet(bytes):
    result = 0

    row = [0] * 1504
    bit = 0
    for byte in bytes:
        for i in range(8):
            row[bit] = (byte >> (7-i)) & 1
            bit += 1

    for i in range(8):
        total = 0
        for j in range(1497):
            total ^= row[i+j] & Cbits[j]
        result |= (total << (7-i))

    return result


### 5.1 Reed-Solomon Coding

gf_exp = [1] * 256
gf_log = [0] * 128
x = 1
for i in range(1, 127):
    x <<= 1
    if x & 0b10000000 != 0:
        x = (x & 0b1111111) ^ 0b0001001
    gf_exp[i] = x
    gf_log[x] = i
for i in range(127, 256):
    gf_exp[i] = gf_exp[i - 127]

def gf_mul(x, y):
    if x == 0 or y == 0:
        return 0
    return gf_exp[gf_log[x] + gf_log[y]]

def gf_poly_eval(p, x):
    y = p[0]
    for i in range(1, len(p)):
        y = gf_mul(y, x) ^ p[i]
    return y

def reed_solomon(message):
    # Generator polynomial from p.7 of ANSI/SCTE 07 2013
    g = [1, gf_exp[52], gf_exp[116], gf_exp[119], gf_exp[61], gf_exp[15]]

    dividend = message + [0, 0, 0, 0, 0]
    for i in range(len(message)):
        coeff = dividend[i]
        for j in range(len(g)):
            dividend[i + j] ^= gf_mul(coeff, g[j])

    result = message + dividend[-5:] + [0]
    result[-1] = gf_poly_eval(result, gf_exp[6])

    return result


### 5.2 Interleaving

control_word = 0b0110
I = 128
J = 4
commutator = 0
registers = []
for i in range(I):
    registers.append([0] * i * J)

def interleave(symbols):
    global commutator

    result = []
    for symbol in symbols:
        registers[commutator] = [symbol] + registers[commutator]
        result.append(registers[commutator].pop())
        commutator = (commutator + 1) % I
    return result


### 5.4 Randomization

rseq = []
c2 = 0b1111111
c1 = 0b1111111
c0 = 0b1111111
for n in range(128 * 60):
    rseq.append(c2)
    c2_new = c1
    c1_new = c0 ^ c2
    c0_new = c2
    for x in range(3):
        c0_new <<= 1
        if c0_new & 0b10000000 != 0:
            c0_new = (c0_new & 0b1111111) ^ 0b0001001
    c2 = c2_new
    c1 = c1_new
    c0 = c0_new
    

### 5.5 Trellis Coded Modulation

Xp = 0
Yp = 0

def diff_precoder(W, Z):
    global Xp, Yp

    common = (Z & (Xp ^ Yp))
    X = W ^ Xp ^ common
    Y = Z ^ W ^ Yp ^ common
    Xp = X
    Yp = Y
    return X, Y

Xq = [0,0,0,0]
Yq = [0,0,0,0]

def trellis_code(rs):
    global Xq, Yq

    A = (rs[1] << 7) | rs[0]
    B = (rs[3] << 7) | rs[2]

    qs = [0, 0, 0, 0, 0]

    for n in range(5):
        qs[n] |= ((A >> (2*n)) & 3) << 4
        qs[n] |= ((B >> (2*n)) & 3) << 1

    nn = 0
    for n in range(4):
        X, Y = diff_precoder((A >> (n+10)) & 1, (B >> (n+10)) & 1)
        Xq = [X] + Xq
        Yq = [Y] + Yq

        if n == 3:
            qs[nn] |= (Xq[0] ^ Xq[2] ^ Xq[4]) << 3
            qs[nn] |= (Yq[0] ^ Yq[2] ^ Yq[4])
            nn += 1
        qs[nn] |= (Xq[0] ^ Xq[1] ^ Xq[2] ^ Xq[3] ^ Xq[4]) << 3
        qs[nn] |= (Yq[0] ^ Yq[1] ^ Yq[2] ^ Yq[3] ^ Yq[4])
        nn += 1

        Xq = Xq[0:4]
        Yq = Yq[0:4]        

    return qs


### 5.3 Frame Synchronization

# Encodes 60 Reed-Solomon blocks (each consisting of 122 7-bit symbols)
# into a frame.
def encode_frame(symbols):
    frame = []

    for i in range(0, len(symbols), 122):
        frame = frame + interleave(reed_solomon(symbols[i:i+122]))

    for i in range(len(frame)):
        frame[i] ^= rseq[i]

    return frame + [0x75, 0x2C, 0x0D, 0x6C, control_word << 3, 0x00]


test_vector = [0] * 122 * 60

frames = encode_frame(test_vector) + encode_frame(test_vector)
output = []
for i in range(0, len(frames), 4):
    output += trellis_code(frames[i:i+4])
print len(output)
