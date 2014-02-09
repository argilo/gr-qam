import random

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
