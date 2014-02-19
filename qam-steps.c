/*
 * Copyright 2014 Clayton Smith
 *
 * This file is part of qam-tx
 *
 * qam-tx is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * qam-tx is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with qam-tx; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// 4   MPEG Transport Framing

uint8_t crctable[] = {
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
};

uint8_t BitReverseTable[] = {
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
};

uint8_t compute_sum(uint8_t *bytes) {
    uint8_t i, bit, out, out1, out2, out3;

    uint8_t tapsG = 0xB1; // 10110001
    uint8_t tapsB = 0x45; //  1000101

    uint8_t register1 = 0;
    uint8_t register2 = 0;
    uint8_t register3 = 0;

    uint8_t result = 0x67;

    uint8_t first7[] = {0, 0, 0, 0, 0, 0, 0, 0};

    for (i = 0; i < 8; i++) {
        bit = (bytes[0] >> (7-i)) & 1;
        out = (register1 & 1) ^ bit;
        if (i < 7) {
            first7[i+1] = out;
        }
        register1 >>= 1;
        if (out == 1) {
            register1 ^= tapsG;
        }
    }

    for (i = 1; i < 187; i++) {
        register1 = crctable[((register1) ^ BitReverseTable[bytes[i]]) & 0xff];
    }

    for (i = 0; i < 8; i++) {
        out1 = register1 & 1;
        register1 >>= 1;
        if (out1 == 1) {
            register1 ^= tapsG;
        }

        out2 = (register2 & 1) ^ first7[i];
        register2 >>= 1;
        if (first7[i] == 1) {
            register2 ^= tapsB;
        }

        out3 = (register3 & 1) ^ out1 ^ out2;
        register3 >>= 1;
        if ((out1 ^ out2) == 1) {
            register3 ^= tapsG;
        }

        result ^= (out3 << (7-i));
    }

    return result;
}


// 5.1 Reed-Solomon Coding

uint8_t gf_mul_table[128][128];
uint8_t gf_exp[256];
uint8_t gf_log[128];

void init_rs() {
    uint8_t x;
    int i, j;

    gf_exp[0] = 1;
    gf_log[1] = 0;

    x = 1;
    for (i = 1; i < 127; i++) {
        x <<= 1;
        if (x & 0x80) {
            x = (x & 0x7F) ^ 0x09;
        }
        gf_exp[i] = x;
        gf_log[x] = i;
    }
    for (; i < 256; i++) {
        gf_exp[i] = gf_exp[i - 127];
    }

    for (i = 0; i < 128; i++) {
        for (j = 0; j < 128; j++) {
            if ((i == 0) || (j == 0)) {
                gf_mul_table[i][j] = 0;
            } else {
                gf_mul_table[i][j] = gf_exp[gf_log[i] + gf_log[j]];
            }
        }
    }
}

uint8_t gf_poly_eval(uint8_t *p, int len, uint8_t x) {
    uint8_t y = p[0];
    int i;

    for (i = 1; i < len; i++) {
        y = gf_mul_table[y][x] ^ p[i];
    }
    return y;
}

void reed_solomon(uint8_t *message, uint8_t *output) {
    // Generator polynomial from p.7 of ANSI/SCTE 07 2013
    uint8_t g[] = {1, gf_exp[52], gf_exp[116], gf_exp[119], gf_exp[61], gf_exp[15]};
    int i, j;

    memcpy(output, message, 122);
    memset(output + 122, 0, 6);

    for (i = 0; i < 122; i++) {
        for (j = 1; j < 6; j++) {
            output[i + j] ^= gf_mul_table[output[i]][g[j]];
        }
        output[i] = message[i];
    }

    output[127] = gf_poly_eval(output, 128, gf_exp[6]);
}

// 5.2 Interleaving

uint8_t control_word = 0x06;
#define I 128
#define J 4

int commutator = 0;
uint8_t registers[I][(I-1) * J];
int pointers[I];

void init_interleave() {
    int i;

    commutator = 0;
    memset(registers, 0, I * ((I-1) * J));
    memset(pointers, 0, I);
}

void interleave(uint8_t *symbols, int len) {
    int i, p;
    uint8_t temp;

    for (i = 0; i < len; i++) {
        if (commutator != 0) {
            p = pointers[commutator];

            temp = registers[commutator][p];
            registers[commutator][p] = symbols[i];
            symbols[i] = temp;

            pointers[commutator] = (p + 1) % (commutator * J);
        }
        commutator = (commutator + 1) % I;
    }
}


// 5.4 Randomization

uint8_t rseq[60 * 128];

void init_rand() {
    uint8_t c2 = 0x7F, c1 = 0x7F, c0 = 0x7F;
    uint8_t c2_new, c1_new, c0_new;
    int n, i;

    for (n = 0; n < 60 * 128; n++) {
        rseq[n] = c2;
        c2_new = c1;
        c1_new = c0 ^ c2;
        c0_new = c2;
        for (i = 0; i < 3; i++) {
            c0_new <<= 1;
            if (c0_new & 0x80) {
                c0_new = (c0_new & 0x7F) ^ 0x09;
            }
        }
        c2 = c2_new;
        c1 = c1_new;
        c0 = c0_new;
    }
}


// 5.5 Trellis Coded Modulation

void diff_precoder(uint8_t W, uint8_t Z, uint8_t *Xp, uint8_t *Yp) {
    uint8_t common, newX, newY;

    common = (Z & (*Xp ^ *Yp));
    newX = W ^ *Xp ^ common;
    newY = Z ^ W ^ *Yp ^ common;

    *Xp = newX;
    *Yp = newY;
}

uint8_t diff_precoder_table[4][16][16][3];
uint8_t G1table[32];
uint8_t G2table[32];

void init_trellis() {
    uint8_t XYp, W, Z, X, Y, Xp, Yp;
    int i;

    for (XYp = 0; XYp < 4; XYp++) {
        for (W = 0; W < 16; W++) {
            for (Z = 0; Z < 16; Z++) {
                X = 0;
                Y = 0;
                Xp = (XYp & 0b10) >> 1;
                Yp = (XYp & 0b01);
                for (i = 0; i < 4; i++) {
                    diff_precoder((W >> i) & 1, (Z >> i) & 1, &Xp, &Yp);
                    X |= (Xp << i);
                    Y |= (Yp << i);
                }
                diff_precoder_table[XYp][W][Z][0] = (Xp << 1) + Yp;
                diff_precoder_table[XYp][W][Z][1] = X;
                diff_precoder_table[XYp][W][Z][2] = Y;
            }
        }
    }

    for (i = 0; i < 32; i++) {
        G1table[i] = (i >> 4) ^ ((i & 0x04) >> 2) ^ (i & 1);
        G2table[i] = (i >> 4) ^ ((i & 0x08) >> 3) ^ ((i & 0x04) >> 2) ^ ((i & 0x02) >> 1) ^ (i & 1);
    }
}

/*
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
*/

// 5.3 Frame Synchronization

// Encodes 60 Reed-Solomon blocks (each consisting of 122 7-bit symbols)
// into a frame.
void encode_frame(uint8_t *symbols, uint8_t *frame) {
    int i = 0, j = 0;

    while (i < 60 * 122) {
        reed_solomon(symbols + i, frame + j);
        i += 122;
        j += 128;
    }

    interleave(frame, 60 * 128);

    for (j = 0; j < 60 * 128; j++) {
        frame[j] ^= rseq[j];
    }

    frame[j++] = 0x75;
    frame[j++] = 0x2C;
    frame[j++] = 0x0D;
    frame[j++] = 0x6C;
    frame[j++] = control_word << 3;
    frame[j++] = 0x00;
}

// Convert MPEG transport stream to QAM symbols

void repack_bytes(uint8_t *bytes, uint8_t *result) {
    result[0] =                             bytes[0] >> 1;
    result[1] = ((bytes[0] & 0x01) << 6) | (bytes[1] >> 2);
    result[2] = ((bytes[1] & 0x03) << 5) | (bytes[2] >> 3);
    result[3] = ((bytes[2] & 0x07) << 4) | (bytes[3] >> 4);
    result[4] = ((bytes[3] & 0x0F) << 3) | (bytes[4] >> 5);
    result[5] = ((bytes[4] & 0x1F) << 2) | (bytes[5] >> 6);
    result[6] = ((bytes[5] & 0x3F) << 1) | (bytes[6] >> 7);
    result[7] =   bytes[6] & 0x7F;
}


#define MPEG_PACKET_SIZE 188
#define CHUNK_SIZE (MPEG_PACKET_SIZE * 6405)
#define ENCODED_WORDS (CHUNK_SIZE * 8 / 7 / 60 / 122 * (60 * 128 + 6))

int main (int argc, char *argv[]) {
    FILE *fin, *fout;
    uint8_t *bytes, *chunk_repacked, *chunk_encoded;
    uint8_t sync_byte;
    uint8_t trellis_symbols[5];
    int i;

    if (argc != 3) {
        fprintf(stderr, "Usage: qam-steps input_file output_file\n");
        exit(1);
    }

    fin = fopen(argv[1], "rb");
    if (fin == NULL) {
        fprintf(stderr, "Error: Could not read input file\n");
        exit(1);
    }

    fout = fopen(argv[2], "wb");
    if (fout == NULL) {
        fprintf(stderr, "Error: Could not write output file\n");
        fclose(fin);
        exit(1);
    }

    bytes = malloc(sizeof(uint8_t) * (CHUNK_SIZE + 1));
    if (bytes == NULL) {
        fprintf(stderr, "Error: Out of memory.\n");
        fclose(fin);
        fclose(fout);
        exit(1);
    }

    chunk_repacked = malloc(sizeof(uint8_t) * (CHUNK_SIZE * 8 / 7));
    if (chunk_repacked == NULL) {
        fprintf(stderr, "Error: Out of memory.\n");
        free(bytes);
        fclose(fin);
        fclose(fout);
        exit(1);
    }

    chunk_encoded = malloc(sizeof(uint8_t) * ENCODED_WORDS);
    if (chunk_encoded == NULL) {
        fprintf(stderr, "Error: Out of memory.\n");
        free(bytes);
        free(chunk_repacked);
        fclose(fin);
        fclose(fout);
        exit(1);
    }

    init_rand();
    init_rs();
    init_interleave();
    init_trellis();

    while (CHUNK_SIZE == fread(bytes, sizeof(uint8_t), CHUNK_SIZE, fin)) {
        sync_byte = bytes[0];
        for (i = 0; i < CHUNK_SIZE; i += MPEG_PACKET_SIZE) {
            if (sync_byte != 0x47) {
                fprintf(stderr, "Error: MPEG packet didn't begin with 0x47\n");
                free(bytes);
                free(chunk_repacked);
                free(chunk_encoded);
                fclose(fin);
                fclose(fout);
                exit(1);
            }
            sync_byte = bytes[i+MPEG_PACKET_SIZE];
            bytes[i+MPEG_PACKET_SIZE] = compute_sum(bytes + (i+1));
        }

        for (i = 0; i < CHUNK_SIZE / 7; i++) {
            repack_bytes(bytes + 1 + (i*7), chunk_repacked + (i*8));
        }

        for (i = 0; i < 188; i++) {
            encode_frame(chunk_repacked + i*60*122, chunk_encoded + i*(60*128+6));
        }

        for (i = 0; i < ENCODED_WORDS; i += 4) {
//            trellis_code(chunk_encoded + i, trellis_symbols);
            fwrite(trellis_symbols, sizeof(uint8_t), 5, fout);
        }
    }

    free(bytes);
    free(chunk_repacked);
    free(chunk_encoded);
    fclose(fin);
    fclose(fout);
}
