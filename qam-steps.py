#!/usr/bin/env /usr/bin/python

# Copyright 2014 Clayton Smith, Ron Economos
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

# Generated with this C code
#    int    i, j;
#    unsigned int    c;
#    unsigned int    poly;
#
#    poly = 0xb1;
#    for (i = 0; i < 256; i++) {
#        for (c = i, j = 0; j < 8; j++) {
#            c = (c >> 1) ^ (poly & (-(c & 1)));
#        }
#        crctable[i] = (unsigned char)(c);
#        printf("0x%02x,", crctable[i]);
#    }

crctable = [
    0x00,0x1b,0x36,0x2d,0x6c,0x77,0x5a,0x41,0xd8,0xc3,0xee,0xf5,0xb4,0xaf,0x82,0x99,
    0xd3,0xc8,0xe5,0xfe,0xbf,0xa4,0x89,0x92,0x0b,0x10,0x3d,0x26,0x67,0x7c,0x51,0x4a,
    0xc5,0xde,0xf3,0xe8,0xa9,0xb2,0x9f,0x84,0x1d,0x06,0x2b,0x30,0x71,0x6a,0x47,0x5c,
    0x16,0x0d,0x20,0x3b,0x7a,0x61,0x4c,0x57,0xce,0xd5,0xf8,0xe3,0xa2,0xb9,0x94,0x8f,
    0xe9,0xf2,0xdf,0xc4,0x85,0x9e,0xb3,0xa8,0x31,0x2a,0x07,0x1c,0x5d,0x46,0x6b,0x70,
    0x3a,0x21,0x0c,0x17,0x56,0x4d,0x60,0x7b,0xe2,0xf9,0xd4,0xcf,0x8e,0x95,0xb8,0xa3,
    0x2c,0x37,0x1a,0x01,0x40,0x5b,0x76,0x6d,0xf4,0xef,0xc2,0xd9,0x98,0x83,0xae,0xb5,
    0xff,0xe4,0xc9,0xd2,0x93,0x88,0xa5,0xbe,0x27,0x3c,0x11,0x0a,0x4b,0x50,0x7d,0x66,
    0xb1,0xaa,0x87,0x9c,0xdd,0xc6,0xeb,0xf0,0x69,0x72,0x5f,0x44,0x05,0x1e,0x33,0x28,
    0x62,0x79,0x54,0x4f,0x0e,0x15,0x38,0x23,0xba,0xa1,0x8c,0x97,0xd6,0xcd,0xe0,0xfb,
    0x74,0x6f,0x42,0x59,0x18,0x03,0x2e,0x35,0xac,0xb7,0x9a,0x81,0xc0,0xdb,0xf6,0xed,
    0xa7,0xbc,0x91,0x8a,0xcb,0xd0,0xfd,0xe6,0x7f,0x64,0x49,0x52,0x13,0x08,0x25,0x3e,
    0x58,0x43,0x6e,0x75,0x34,0x2f,0x02,0x19,0x80,0x9b,0xb6,0xad,0xec,0xf7,0xda,0xc1,
    0x8b,0x90,0xbd,0xa6,0xe7,0xfc,0xd1,0xca,0x53,0x48,0x65,0x7e,0x3f,0x24,0x09,0x12,
    0x9d,0x86,0xab,0xb0,0xf1,0xea,0xc7,0xdc,0x45,0x5e,0x73,0x68,0x29,0x32,0x1f,0x04,
    0x4e,0x55,0x78,0x63,0x22,0x39,0x14,0x0f,0x96,0x8d,0xa0,0xbb,0xfa,0xe1,0xcc,0xd7
]

BitReverseTable = [
    0x00,0x80,0x40,0xC0,0x20,0xA0,0x60,0xE0,0x10,0x90,0x50,0xD0,0x30,0xB0,0x70,0xF0, 
    0x08,0x88,0x48,0xC8,0x28,0xA8,0x68,0xE8,0x18,0x98,0x58,0xD8,0x38,0xB8,0x78,0xF8, 
    0x04,0x84,0x44,0xC4,0x24,0xA4,0x64,0xE4,0x14,0x94,0x54,0xD4,0x34,0xB4,0x74,0xF4, 
    0x0C,0x8C,0x4C,0xCC,0x2C,0xAC,0x6C,0xEC,0x1C,0x9C,0x5C,0xDC,0x3C,0xBC,0x7C,0xFC, 
    0x02,0x82,0x42,0xC2,0x22,0xA2,0x62,0xE2,0x12,0x92,0x52,0xD2,0x32,0xB2,0x72,0xF2, 
    0x0A,0x8A,0x4A,0xCA,0x2A,0xAA,0x6A,0xEA,0x1A,0x9A,0x5A,0xDA,0x3A,0xBA,0x7A,0xFA,
    0x06,0x86,0x46,0xC6,0x26,0xA6,0x66,0xE6,0x16,0x96,0x56,0xD6,0x36,0xB6,0x76,0xF6, 
    0x0E,0x8E,0x4E,0xCE,0x2E,0xAE,0x6E,0xEE,0x1E,0x9E,0x5E,0xDE,0x3E,0xBE,0x7E,0xFE,
    0x01,0x81,0x41,0xC1,0x21,0xA1,0x61,0xE1,0x11,0x91,0x51,0xD1,0x31,0xB1,0x71,0xF1,
    0x09,0x89,0x49,0xC9,0x29,0xA9,0x69,0xE9,0x19,0x99,0x59,0xD9,0x39,0xB9,0x79,0xF9, 
    0x05,0x85,0x45,0xC5,0x25,0xA5,0x65,0xE5,0x15,0x95,0x55,0xD5,0x35,0xB5,0x75,0xF5,
    0x0D,0x8D,0x4D,0xCD,0x2D,0xAD,0x6D,0xED,0x1D,0x9D,0x5D,0xDD,0x3D,0xBD,0x7D,0xFD,
    0x03,0x83,0x43,0xC3,0x23,0xA3,0x63,0xE3,0x13,0x93,0x53,0xD3,0x33,0xB3,0x73,0xF3, 
    0x0B,0x8B,0x4B,0xCB,0x2B,0xAB,0x6B,0xEB,0x1B,0x9B,0x5B,0xDB,0x3B,0xBB,0x7B,0xFB,
    0x07,0x87,0x47,0xC7,0x27,0xA7,0x67,0xE7,0x17,0x97,0x57,0xD7,0x37,0xB7,0x77,0xF7, 
    0x0F,0x8F,0x4F,0xCF,0x2F,0xAF,0x6F,0xEF,0x1F,0x9F,0x5F,0xDF,0x3F,0xBF,0x7F,0xFF
]

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
    tapsG = 0b10110001
    tapsB = 0b1000101

    register1 = 0
    register2 = 0
    register3 = 0

    result = 0x67

    first7 = [0]

    byte = bytes[0]
    for i in range(8):
        bit = (byte >> (7-i)) & 1
        out = (register1 & 1) ^ bit
        if i < 7:
            first7.append(out)
        register1 >>= 1
        if out == 1:
            register1 ^= tapsG

    for byte in bytes[1:]:
        register1 = crctable[((register1) ^ BitReverseTable[byte]) & 0xff];

    for i in range(8):
        out1 = register1 & 1
        register1 >>= 1
        if out1 == 1:
            register1 ^= tapsG

        out2 = (register2 & 1) ^ first7[i]
        register2 >>= 1
        if first7[i] == 1:
            register2 ^= tapsB

        out3 = (register3 & 1) ^ out1 ^ out2
        register3 >>= 1
        if (out1 ^ out2) == 1:
            register3 ^= tapsG

        result ^= (out3 << (7-i))

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

gf_mul_table = [[gf_mul(x, y) for x in range(128)] for y in range(128)]

def gf_poly_eval(p, x):
    y = p[0]
    for i in range(1, len(p)):
        y = gf_mul_table[y][x] ^ p[i]
    return y

def reed_solomon(message):
    # Generator polynomial from p.7 of ANSI/SCTE 07 2013
    g = [1, gf_exp[52], gf_exp[116], gf_exp[119], gf_exp[61], gf_exp[15]]

    dividend = message + [0, 0, 0, 0, 0]
    for i in range(len(message)):
        coeff = dividend[i]
        for j in range(1, len(g)):
            dividend[i + j] ^= gf_mul_table[coeff][g[j]]

    result = message + dividend[-5:] + [0]
    result[-1] = gf_poly_eval(result, gf_exp[6])

    return result


### 5.2 Interleaving

control_word = 0b0110
I = 128
J = 4
commutator = 0
registers = []
pointers = [0] * I
for i in range(I):
    registers.append([0] * i * J)

def interleave(symbols):
    global commutator

    result = []
    for symbol in symbols:
        if commutator == 0:
            result.append(symbol)
        else:
            p = pointers[commutator]
            result.append(registers[commutator][p])
            registers[commutator][p] = symbol
            pointers[commutator] = (p + 1) % (commutator * J)
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

def diff_precoder(W, Z, Xp, Yp):
    common = (Z & (Xp ^ Yp))
    X = W ^ Xp ^ common
    Y = Z ^ W ^ Yp ^ common
    return X, Y

diff_precoder_table = []
for XYp in range(4):
    Wlist = []
    for W in range(16):
        Zlist = []
        for Z in range(16):
            X = 0
            Y = 0
            Xp = (XYp & 0b10) >> 1
            Yp = (XYp & 0b01)
            for i in range(4):
                Xp, Yp = diff_precoder((W >> i) & 1, (Z >> i) & 1, Xp, Yp)
                X |= (Xp << i)
                Y |= (Yp << i)
            Zlist.append(((Xp << 1) + Yp, X, Y))
        Wlist.append(Zlist)
    diff_precoder_table.append(Wlist)

G1table = [(n >> 4) ^ ((n & 0b00100) >> 2) ^ (n & 1) for n in range(32)]
G2table = [(n >> 4) ^ ((n & 0b01000) >> 3) ^ ((n & 0b00100) >> 2) ^ ((n & 0b00010) >> 1) ^ (n & 1) for n in range(32)]

trellis_table_x = []
trellis_table_y = []
for state in range(16):
    x_table = []
    y_table = []
    for xy in range(16):
        nn = 0
        qs = [0, 0, 0, 0, 0]
        Xq = state
        for n in range(4):
            Xq = (Xq << 1) + ((xy >> n) & 1)

            if n == 3:
                qs[nn] |= G1table[Xq] << 3
                nn += 1
            qs[nn] |= G2table[Xq] << 3
            nn += 1

            Xq &= 0b1111

        x_table.append((Xq, qs))
        y_table.append((Xq, [(q >> 3) for q in qs]))
    trellis_table_x.append(x_table)
    trellis_table_y.append(y_table)

XYp = 0

Xq = 0
Yq = 0

def trellis_code(rs):
    global Xq, Yq, XYp

    A = (rs[1] << 7) | rs[0]
    B = (rs[3] << 7) | rs[2]

    qs = [0, 0, 0, 0, 0]

    for n in range(5):
        qs[n] |= ((A >> (2*n)) & 3) << 4
        qs[n] |= ((B >> (2*n)) & 3) << 1

    nn = 0
    XYp, X, Y = diff_precoder_table[XYp][A >> 10][B >> 10]
    Xq, qsx = trellis_table_x[Xq][X]
    Yq, qsy = trellis_table_y[Yq][Y]
    return [a|b|c for (a,b,c) in zip(qs, qsx, qsy)]


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


# Convert MPEG transport stream to QAM symbols

def repack_bytes(bytes):
    result = [0] * 8

    result[0] =                                   bytes[0] >> 1
    result[1] = ((bytes[0] & 0b00000001) << 6) | (bytes[1] >> 2)
    result[2] = ((bytes[1] & 0b00000011) << 5) | (bytes[2] >> 3)
    result[3] = ((bytes[2] & 0b00000111) << 4) | (bytes[3] >> 4)
    result[4] = ((bytes[3] & 0b00001111) << 3) | (bytes[4] >> 5)
    result[5] = ((bytes[4] & 0b00011111) << 2) | (bytes[5] >> 6)
    result[6] = ((bytes[5] & 0b00111111) << 1) | (bytes[6] >> 7)
    result[7] =   bytes[6] & 0b01111111

    return result

import sys

args = sys.argv[1:]
if len(args) != 2:
    sys.stderr.write("Usage: qam-steps.py input_file output_file\n");
    sys.exit(1)

CHUNK_SIZE = 188 * 6405

with open(args[0], 'rb') as fin:
    with open(args[1], 'wb') as fout:
        bytes = fin.read(CHUNK_SIZE)
        while len(bytes) == CHUNK_SIZE:
            chunk_framed = []
            for i in range(0, CHUNK_SIZE, 188):
                if ord(bytes[i]) != 0x47:
                    sys.stderr.write("Error: MPEG packet didn't begin with 0x47\n")
                    sys.exit(1)
                packet = [ord(byte) for byte in bytes[i+1:i+188]]
                chunk_framed += (packet + [compute_sum(packet)])
            print len(chunk_framed),

            chunk_repacked = []
            for i in range(0, CHUNK_SIZE, 7):
                chunk_repacked += repack_bytes(chunk_framed[i:i+7])
            print len(chunk_repacked),

            chunk_encoded = []
            for i in range(0, len(chunk_repacked), 122*60):
                chunk_encoded += encode_frame(chunk_repacked[i:i+122*60])
            print len(chunk_encoded)

            for i in range(0, len(chunk_encoded), 4):
                fout.write(bytearray(trellis_code(chunk_encoded[i:i+4])))
            fout.flush()
            
            bytes = fin.read(CHUNK_SIZE)
