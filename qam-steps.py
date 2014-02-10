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

import random

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

print(["{0:06b}".format(symbol) for symbol in trellis_code([0x75, 0x2C, 0x0D, 0x6C])])
for x in range(1000):
    print(["{0:06b}".format(symbol) for symbol in trellis_code([random.randint(0,127), random.randint(0,127), random.randint(0,127), random.randint(0,127)])])
