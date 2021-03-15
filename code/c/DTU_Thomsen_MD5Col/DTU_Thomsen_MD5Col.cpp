#include <stdio.h>
#include <time.h>

typedef unsigned long word;

static word Q[65];
static word T, T2, stop;
static word iva, ivb, ivc, ivd;
static word myIVA, myIVB, myIVC, myIVD;

static int ok, i, start_over, changed, ctr;

#define TRY2 0x10000
#define TRY1 0xffff

#define IVA 0x67452301
#define IVB 0xefcdab89
#define IVC 0x98badcfe
#define IVD 0x10325476

#define t0 0xd76aa478
#define t1 0xe8c7b756
#define t2 0x242070db
#define t3 0xc1bdceee
#define t4 0xf57c0faf
#define t5 0x4787c62a
#define t6 0xa8304613
#define t7 0xfd469501
#define t8 0x698098d8
#define t9 0x8b44f7af
#define t10 0xffff5bb1
#define t11 0x895cd7be
#define t12 0x6b901122
#define t13 0xfd987193
#define t14 0xa679438e
#define t15 0x49b40821
#define t16 0xf61e2562
#define t17 0xc040b340
#define t18 0x265e5a51
#define t19 0xe9b6c7aa
#define t20 0xd62f105d
#define t21 0x02441453
#define t22 0xd8a1e681
#define t23 0xe7d3fbc8
#define t24 0x21e1cde6
#define t25 0xc33707d6
#define t26 0xf4d50d87
#define t27 0x455a14ed
#define t28 0xa9e3e905
#define t29 0xfcefa3f8
#define t30 0x676f02d9
#define t31 0x8d2a4c8a
#define t32 0xfffa3942
#define t33 0x8771f681
#define t34 0x6d9d6122
#define t35 0xfde5380c
#define t36 0xa4beea44
#define t37 0x4bdecfa9
#define t38 0xf6bb4b60
#define t39 0xbebfbc70
#define t40 0x289b7ec6
#define t41 0xeaa127fa
#define t42 0xd4ef3085
#define t43 0x04881d05
#define t44 0xd9d4d039
#define t45 0xe6db99e5
#define t46 0x1fa27cf8
#define t47 0xc4ac5665
#define t48 0xf4292244
#define t49 0x432aff97
#define t50 0xab9423a7
#define t51 0xfc93a039
#define t52 0x655b59c3
#define t53 0x8f0ccc92
#define t54 0xffeff47d
#define t55 0x85845dd1
#define t56 0x6fa87e4f
#define t57 0xfe2ce6e0
#define t58 0xa3014314
#define t59 0x4e0811a1
#define t60 0xf7537e82
#define t61 0xbd3af235
#define t62 0x2ad7d2bb
#define t63 0xeb86d391

word m[16], m1[16];

#define rot(x, s) (((x)<<(s))^((x)>>(32-(s))))
#define rotr(x, s) (((x)<<(32-(s)))^((x)>>(s)))

#define F(u, v, w) ((w) ^ ((u) & ((v) ^ (w))))
#define G(u, v, w) ((v) ^ ((w) & ((u) ^ (v))))
#define H(u, v, w) ((u) ^ (v) ^ (w))
#define I(u, v, w) ((v) ^ ((u) | ~(w)))

#define msb_equal(x, y) (((~x)^(y))&0x80000000)
#define bitsequal(x, n, y) (((~(x)^(y))>>n)&1)
#define random_word() (random()) // mrand48()

//double current_time_micros() {
//    /* returns current time in microseconds */
//    struct timeval curtime;
//    gettimeofday(&curtime, 0);
//    return ((double)curtime.tv_sec) * 1000000 +
//        ((double)curtime.tv_usec);
//}

int X;
int random_word() {
    X = (1103515245 * X + 12345) & 0xffffffff;
    return X;
}

// FIRST BLOCK:

inline void search1() {
    //  int i;
    word k = IVA + F(IVB, IVC, IVD) + t0;
    do {
        ok = 0;

        Q[3] = random_word();
        Q[3] &= 0xfff7f7bf;

        Q[4] = random_word(); // bit 32 = 0
        Q[4] &= 0xff7fffbf;
        Q[4] |= 0x00080800;
        Q[4] ^= (Q[3] ^ Q[4]) & 0x77f780;

        Q[5] = random_word();
        Q[5] &= 0xfd40003f;
        Q[5] |= 0x08400025;
        Q[5] ^= (Q[4] ^ Q[5]) & 0x80000000;
        if (!(rotr(Q[5] - Q[4], 7) >> 31)) continue; // T_4

        Q[6] = random_word();
        Q[6] &= 0xf77fbc5b;
        Q[6] |= 0x827fbc41; // 32 = 1
        Q[6] ^= (Q[5] ^ Q[6]) & 0x7500001a;
        if (rotr(Q[6] - Q[5], 12) & 0x80000) continue; // T_5

        Q[7] = 0x03fef820;
        T = rotr(Q[7] - Q[6], 17); // T_6
        if (T & 0x4000 || !((T >> 10) & 0xf)) continue;
        m[6] = T - F(Q[6], Q[5], Q[4]) - Q[3] - t6;

        Q[8] = random_word();
        Q[8] &= 0x01f15540;
        Q[8] |= 0x01910540;
        T = rotr(Q[8] - Q[7], 22); // T_7
        // - these T-conditions are always satisfied
        m[7] = T - F(Q[7], Q[6], Q[5]) - Q[4] - t7;

        do {
            do {
                Q[9] = random_word();
                Q[9] &= 0xfbf07f3d;
                Q[9] |= 0x7b102f3d;
                Q[9] ^= (Q[8] ^ Q[9]) & 0x1000;
                Q[9] ^= (~Q[7] ^ Q[9]) & 0x80000000;
                T = rotr(Q[9] - Q[8], 7); // T_8
                if (!(T >> 31) || !(T & 0x1000000)) continue;
                m[8] = T - F(Q[8], Q[7], Q[6]) - Q[5] - t8;

                Q[10] = random_word();
                Q[10] &= 0xff7fde7c;
                Q[10] |= 0x401f9040;
                Q[10] ^= (~Q[9] ^ Q[10]) & 0x80000000;
                T = rotr(Q[10] - Q[9], 12); // T_9
                if (!(~T >> 27)) continue;
                m[9] = T - F(Q[9], Q[8], Q[7]) - Q[6] - t9;

                Q[11] = random_word();
                Q[11] &= 0xbff1cefc;
                Q[11] |= 0x000180c2;
                Q[11] ^= (Q[10] ^ Q[11]) & 0x80004000;
                T = rotr(Q[11] - Q[10], 17); // T_10
            } while (!(~T & 0x6000) || !(T >> 27));
            m[10] = T - F(Q[10], Q[9], Q[8]) - Q[7] - t10;

            Q[12] = random_word();
            Q[12] &= 0xbff81f7f;
            Q[12] |= 0x00081100;
            Q[12] ^= (Q[11] ^ Q[12]) & 0x83000000;
            T = rotr(Q[12] - Q[11], 22); // T_11
        } while (!(T & 0x300) || !(T >> 24));

        m[11] = T - F(Q[11], Q[10], Q[9]) - Q[8] - t11;

        // No strict conditions on T_12
        Q[13] = random_word();
        Q[13] &= 0xfdfffe7f;
        Q[13] |= 0x410fe008;
        Q[13] ^= (Q[12] ^ Q[13]) & 0x80000000;
        m[12] = rotr(Q[13] - Q[12], 7) -
            F(Q[12], Q[11], Q[10]) - Q[9] - t12;

        do {
            // No strict conditions on T_13
            Q[14] = random_word();
            Q[14] &= 0xdcfbffff;
            Q[14] |= 0x000be188;
            Q[14] ^= (Q[13] ^ Q[14]) & 0x80000000;
            m[13] = rotr(Q[14] - Q[13], 12) -
                F(Q[13], Q[12], Q[11]) - Q[10] - t13;

            Q[15] = random_word();
            Q[15] &= 0xfdfffff7; // Removed 31 = 0
            Q[15] |= 0x21008000;
            T = rotr(Q[15] - Q[14], 17); // T_14
            if (!(T >> 30)) continue;
            m[14] = T - F(Q[14], Q[13], Q[12]) - Q[11] - t14;

            Q[16] = random_word();
            Q[16] |= 0x20000000;
            Q[16] ^= (Q[15] ^ Q[16]) & 0x80000000;

            T = rotr(Q[16] - Q[15], 22); // T_15
            m[15] = T - F(Q[15], Q[14], Q[13]) - Q[12] - t15;
            if ((T & 0x380) && (~T >> 26)) break;

        } while (1);

        ctr = 0;
        do {
            ctr++;
            if (ctr > TRY1) break;
            Q[17] = random_word();
            Q[17] &= 0xfffdffff;
            Q[17] ^= (Q[16] ^ Q[17]) & 0x80008008;
            Q[18] = Q[17] +
                rot(G(Q[17], Q[16], Q[15]) + Q[14] + m[6] + t17, 9);
            Q[19] = Q[18] +
                rot(G(Q[18], Q[17], Q[16]) + Q[15] + m[11] + t18, 14);
        } while (!((Q[18] >> 17) & 1) ||
            (Q[17] ^ Q[18]) & 0xa0000000 ||
            (Q[19] & 0x20000) ||
            (Q[18] ^ Q[19]) & 0x80000000);
        if (ctr > TRY1) continue;

        T = rotr(Q[17] - Q[16], 5); // T_16
        if (T & 0x1000000) continue;
        m[1] = T - G(Q[16], Q[15], Q[14]) - Q[13] - t16;

        ok = 0;
        stop = ~Q[19] & 0x80000000;
        for (Q[20] = Q[19] & 0x80000000; Q[20] != stop; Q[20]++) {
            T = rotr(Q[20] - Q[19], 20); // T_19
            if (!(T >> 29)) continue;
            m[0] = T - G(Q[19], Q[18], Q[17]) - Q[16] - t19;

            Q[1] = IVB + rot(k + m[0], 7);
            Q[2] = Q[1] +
                rot(IVD + F(Q[1], IVB, IVC) + t1 + m[1], 12);
            m[2] = rotr(Q[3] - Q[2], 17) - F(Q[2], Q[1], IVB) -
                IVC - t2;
            m[3] = rotr(Q[4] - Q[3], 22) - F(Q[3], Q[2], Q[1]) -
                IVB - t3;
            m[4] = rotr(Q[5] - Q[4], 7) - F(Q[4], Q[3], Q[2]) -
                Q[1] - t4;
            m[5] = rotr(Q[6] - Q[5], 12) - F(Q[5], Q[4], Q[3]) -
                Q[2] - t5;

            // check rest
            Q[21] = Q[20] +
                rot(Q[17] + G(Q[20], Q[19], Q[18]) + t20 + m[5], 5);
            if (!bitsequal(Q[21], 17, Q[20]) ||
                !msb_equal(Q[21], Q[20])) continue;


            Q[22] = Q[21] +
                rot(Q[18] + G(Q[21], Q[20], Q[19]) + t21 + m[10], 9);
            if (!msb_equal(Q[22], Q[21])) continue;

            // T_22
            T = Q[19] + G(Q[22], Q[21], Q[20]) + t22 + m[15];
            if (T & 0x20000) continue;

            Q[23] = Q[22] + rot(T, 14);
            if (Q[23] >> 31) continue;

            Q[24] = Q[23] +
                rot(Q[20] + G(Q[23], Q[22], Q[21]) + t23 + m[4], 20);
            if (!(Q[24] >> 31)) continue;


            Q[25] = Q[24] +
                rot(Q[21] + G(Q[24], Q[23], Q[22]) + t24 + m[9], 5);
            Q[26] = Q[25] +
                rot(Q[22] + G(Q[25], Q[24], Q[23]) + t25 + m[14], 9);
            Q[27] = Q[26] +
                rot(Q[23] + G(Q[26], Q[25], Q[24]) + t26 + m[3], 14);
            Q[28] = Q[27] +
                rot(Q[24] + G(Q[27], Q[26], Q[25]) + t27 + m[8], 20);

            Q[29] = Q[28] +
                rot(Q[25] + G(Q[28], Q[27], Q[26]) + t28 + m[13], 5);
            Q[30] = Q[29] +
                rot(Q[26] + G(Q[29], Q[28], Q[27]) + t29 + m[2], 9);
            Q[31] = Q[30] +
                rot(Q[27] + G(Q[30], Q[29], Q[28]) + t30 + m[7], 14);
            Q[32] = Q[31] +
                rot(Q[28] + G(Q[31], Q[30], Q[29]) + t31 + m[12], 20);

            Q[33] = Q[32] +
                rot(Q[29] + H(Q[32], Q[31], Q[30]) + t32 + m[5], 4);
            Q[34] = Q[33] +
                rot(Q[30] + H(Q[33], Q[32], Q[31]) + t33 + m[8], 11);

            // T_34
            T = Q[31] + H(Q[34], Q[33], Q[32]) + t34 + m[11];
            if (T & 0x8000) continue;

            Q[35] = Q[34] + rot(T, 16);
            Q[36] = Q[35] +
                rot(Q[32] + H(Q[35], Q[34], Q[33]) + t35 + m[14], 23);

            Q[37] = Q[36] +
                rot(Q[33] + H(Q[36], Q[35], Q[34]) + t36 + m[1], 4);
            Q[38] = Q[37] +
                rot(Q[34] + H(Q[37], Q[36], Q[35]) + t37 + m[4], 11);
            Q[39] = Q[38] +
                rot(Q[35] + H(Q[38], Q[37], Q[36]) + t38 + m[7], 16);
            Q[40] = Q[39] +
                rot(Q[36] + H(Q[39], Q[38], Q[37]) + t39 + m[10], 23);

            Q[41] = Q[40] +
                rot(Q[37] + H(Q[40], Q[39], Q[38]) + t40 + m[13], 4);
            Q[42] = Q[41] +
                rot(Q[38] + H(Q[41], Q[40], Q[39]) + t41 + m[0], 11);
            Q[43] = Q[42] +
                rot(Q[39] + H(Q[42], Q[41], Q[40]) + t42 + m[3], 16);
            Q[44] = Q[43] +
                rot(Q[40] + H(Q[43], Q[42], Q[41]) + t43 + m[6], 23);

            Q[45] = Q[44] +
                rot(Q[41] + H(Q[44], Q[43], Q[42]) + t44 + m[9], 4);
            Q[46] = Q[45] +
                rot(Q[42] + H(Q[45], Q[44], Q[43]) + t45 + m[12], 11);
            Q[47] = Q[46] +
                rot(Q[43] + H(Q[46], Q[45], Q[44]) + t46 + m[15], 16);
            Q[48] = Q[47] +
                rot(Q[44] + H(Q[47], Q[46], Q[45]) + t47 + m[2], 23);
            if ((Q[48] ^ Q[46]) & 0x80000000) continue;

            Q[49] = Q[48] +
                rot(Q[45] + I(Q[48], Q[47], Q[46]) + t48 + m[0], 6);
            if ((Q[49] ^ Q[47]) & 0x80000000) continue;

            Q[50] = Q[49] +
                rot(Q[46] + I(Q[49], Q[48], Q[47]) + t49 + m[7], 10);
            if ((~Q[50] ^ Q[46]) & 0x80000000) continue;

            Q[51] = Q[50] +
                rot(Q[47] + I(Q[50], Q[49], Q[48]) + t50 + m[14], 15);
            if ((Q[51] ^ Q[49]) & 0x80000000) continue;

            Q[52] = Q[51] +
                rot(Q[48] + I(Q[51], Q[50], Q[49]) + t51 + m[5], 21);
            if ((Q[52] ^ Q[50]) & 0x80000000) continue;

            Q[53] = Q[52] +
                rot(Q[49] + I(Q[52], Q[51], Q[50]) + t52 + m[12], 6);
            if ((Q[53] ^ Q[51]) & 0x80000000) continue;

            Q[54] = Q[53] +
                rot(Q[50] + I(Q[53], Q[52], Q[51]) + t53 + m[3], 10);
            if ((Q[54] ^ Q[52]) & 0x80000000) continue;

            Q[55] = Q[54] +
                rot(Q[51] + I(Q[54], Q[53], Q[52]) + t54 + m[10], 15);
            if ((Q[55] ^ Q[53]) & 0x80000000) continue;

            Q[56] = Q[55] +
                rot(Q[52] + I(Q[55], Q[54], Q[53]) + t55 + m[1], 21);
            if ((Q[56] ^ Q[54]) & 0x80000000) continue;

            Q[57] = Q[56] +
                rot(Q[53] + I(Q[56], Q[55], Q[54]) + t56 + m[8], 6);
            if ((Q[57] ^ Q[55]) & 0x80000000) continue;

            Q[58] = Q[57] +
                rot(Q[54] + I(Q[57], Q[56], Q[55]) + t57 + m[15], 10);
            if ((Q[58] ^ Q[56]) & 0x80000000) continue;

            Q[59] = Q[58] +
                rot(Q[55] + I(Q[58], Q[57], Q[56]) + t58 + m[6], 15);
            if ((Q[59] ^ Q[57]) & 0x80000000) continue;

            Q[60] = Q[59] +
                rot(Q[56] + I(Q[59], Q[58], Q[57]) + t59 + m[13], 21);
            if ((Q[60] & 0x2000000) || ((~Q[60] ^ Q[58]) & 0x80000000))
                continue;

            Q[61] = Q[60] +
                rot(Q[57] + I(Q[60], Q[59], Q[58]) + t60 + m[4], 6);
            if ((!(Q[61] & 0x2000000)) || ((Q[61] ^ Q[59]) & 0x80000000))
                continue;

            iva = IVA + Q[61];

            T = Q[58] + I(Q[61], Q[60], Q[59]) + t61 + m[11];
            if (!(~T & 0x3f8000)) continue;

            Q[62] = Q[61] + rot(T, 10);
            if ((Q[62] & 0x2000000) || ((Q[62] ^ Q[60]) & 0x80000000))
                continue;

            ivd = IVD + Q[62];
            if (ivd & 0x2000000) continue;

            Q[63] = Q[62] +
                rot(Q[59] + I(Q[62], Q[61], Q[60]) + t62 + m[2], 15);
            if ((Q[63] & 0x2000000) || ((Q[63] ^ Q[61]) & 0x80000000))
                continue;

            ivc = IVC + Q[63];
            if ((!(ivc & 0x2000000)) || (ivc & 0x4000000) ||
                ((ivc ^ ivd) & 0x80000000))
                continue;

            printf(".");

            Q[64] = Q[63] +
                rot(Q[60] + I(Q[63], Q[62], Q[61]) + t63 + m[9], 21);
            ivb = IVB + Q[64];
            if ((ivb & 0x06000020) || ((ivb ^ ivc) & 0x80000000)) continue;

            myIVA = iva; myIVB = ivb; myIVC = ivc; myIVD = ivd;
            ok = 1;
            break;
        }

    } while (!ok);

}



// SECOND BLOCK:

inline void modify_0_13() {
    do {
        Q[1] = random_word();
        Q[1] &= 0xf5fff7df;
        //    Q[1] |= 0x04200040;
        Q[1] |= 0x04200000;
        Q[1] ^= (~Q[1] ^ myIVB) & 0x80000000;

        Q[2] = random_word();
        Q[2] &= 0xfddfffd9;
        //    Q[2] |= 0x0c000840;
        Q[2] |= 0x0c000800;
        //    Q[2] ^= (Q[1]^Q[2])&0xf01f1080;
        Q[2] ^= (Q[1] ^ Q[2]) & 0xf01f10c0;

        T = rotr(Q[2] - Q[1], 12);
        if (!(~T >> 25)) continue;
        m[1] = T - myIVD - F(Q[1], myIVB, myIVC) - t1;

        Q[3] = random_word();
        Q[3] &= 0xbfdfef7f;
        Q[3] |= 0x3e1f0966;
        Q[3] ^= (Q[2] ^ Q[3]) & 0x80000018;

        T = rotr(Q[3] - Q[2], 17);
        if ((T >> 31) || !((~T >> 26) & 0x1f)) continue;
        m[2] = T - myIVC - F(Q[2], Q[1], myIVB) - t2;

        Q[4] = random_word();
        Q[4] &= 0xbbc4e611;
        Q[4] |= 0x3a040010;
        Q[4] ^= (Q[3] ^ Q[4]) & 0x80000601;

        T = rotr(Q[4] - Q[3], 22);
        if (!(T >> 27)) continue;
        m[3] = T - myIVB - F(Q[3], Q[2], Q[1]) - t3;

        Q[5] = random_word();
        Q[5] &= 0xcbefee50;
        Q[5] |= 0x482f0e50;
        Q[5] ^= (~Q[4] ^ Q[5]) & 0x80000000;

        T = rotr(Q[5] - Q[4], 7);
        if ((T >> 31) || !(T & 0x40000000)) continue;
        m[4] = T - Q[1] - F(Q[4], Q[3], Q[2]) - t4;

        Q[6] = random_word();
        Q[6] &= 0xe5eeec56;
        Q[6] |= 0x04220c56;
        Q[6] ^= (Q[5] ^ Q[6]) & 0x80000000;

        T = rotr(Q[6] - Q[5], 12);
        if (!(T >> 30)) continue;
        m[5] = T - Q[2] - F(Q[5], Q[4], Q[3]) - t5;

        Q[7] = random_word();
        Q[7] &= 0xf7cdfe3f;
        Q[7] |= 0x16011e01;
        Q[7] ^= (~Q[6] ^ Q[7]) & 0x80000000;
        Q[7] ^= (Q[6] ^ Q[7]) & 0x1808000;

        T = rotr(Q[7] - Q[6], 17);
        if ((T >> 31) || !(T & 0x7c00)) continue;
        m[6] = T - Q[3] - F(Q[6], Q[5], Q[4]) - t6;

        Q[8] = random_word();
        Q[8] &= 0xe47efffe;
        Q[8] |= 0x043283e0; // Added Q_8[5] = 1 *
        Q[8] ^= (Q[7] ^ Q[8]) & 0x80000002;

        T = rotr(Q[8] - Q[7], 22);
        if (!(~T & 0x3f0) || !(~T >> 27)) continue;
        m[7] = T - Q[4] - F(Q[7], Q[6], Q[5]) - t7;

        Q[9] = random_word();
        Q[9] &= 0xfc7d7ddd; // Added Q_9[5] = 0 *
        Q[9] |= 0x1c0101c1;
        Q[9] ^= (Q[8] ^ Q[9]) & 0x80001000;
        // * so that Q[9]-Q[8] produces a carry into bit 6

        T = rotr(Q[9] - Q[8], 7);
        if (!(T >> 31) || !(~T & 0x7e000000)) continue;
        m[8] = T - Q[5] - F(Q[8], Q[7], Q[6]) - t8;

        Q[10] = random_word();
        Q[10] &= 0xfffbeffc;
        Q[10] |= 0x078383c0;
        // Added Q[10],3 != Q[9],3
        // so correction in step 19 works:
        Q[10] ^= (~Q[9] ^ Q[10]) & 0x8;
        Q[10] ^= (Q[9] ^ Q[10]) & 0x80000000;
        T = rotr(Q[10] - Q[9], 12);
        if (!(T >> 27)) continue;
        m[9] = T - Q[6] - F(Q[9], Q[8], Q[7]) - t9;

        Q[11] = random_word();
        Q[11] &= 0xfffdefff;
        Q[11] |= 0x000583c3;
        Q[11] ^= (Q[10] ^ Q[11]) & 0x80086000;

        T = rotr(Q[11] - Q[10], 17);
        if (!(T >> 27)) continue;
        m[10] = T - Q[7] - F(Q[10], Q[9], Q[8]) - t10;

        Q[12] = random_word();
        Q[12] &= 0xfff81fff;
        Q[12] |= 0x00081080;
        Q[12] ^= (Q[12] ^ Q[11]) & 0xff000000;

        Q[13] = random_word();
        Q[13] &= 0xbfffff7f;
        Q[13] |= 0x3f0fe008;
        Q[13] ^= (~Q[12] ^ Q[13]) & 0x80000000;

        Q[14] = random_word();
        Q[14] &= 0xc0fbffff;
        Q[14] |= 0x400be088;
        Q[14] ^= (Q[13] ^ Q[14]) & 0x80000000;

        T = rotr(Q[14] - Q[13], 12);
        if (!((T >> 12) & 0xff)) continue;
        m[13] = T - Q[10] - F(Q[13], Q[12], Q[11]) - t13;

        m[0] = rotr(Q[1] - myIVB, 7) - myIVA -
            F(myIVB, myIVC, myIVD) - t0;
        m[11] = rotr(Q[12] - Q[11], 22) - Q[8] -
            F(Q[11], Q[10], Q[9]) - t11;
        m[12] = rotr(Q[13] - Q[12], 7) - Q[9] -
            F(Q[12], Q[11], Q[10]) - t12;
        m[13] = rotr(Q[14] - Q[13], 12) - Q[10] -
            F(Q[13], Q[12], Q[11]) - t13;

        break;
    } while (1);
}

inline void checkrest() {
    ctr = 0;
    start_over = 1;
    do {
        ctr++;

        Q[15] = random_word();
        Q[15] &= 0x7dff7ff7;
        Q[15] |= 0x7d000000;

        T = rotr(Q[15] - Q[14], 17);
        if (!(~T >> 30)) continue;

        m[14] = T - Q[11] - F(Q[14], Q[13], Q[12]) - t14;

        Q[16] = random_word();
        Q[16] &= 0x7fffffff;
        Q[16] |= 0x20000000;
        //    Q[16] ^= (Q[15]^Q[16])&0x80000000;

        T = rotr(Q[16] - Q[15], 22);
        if (!(T & 0x380) || !(T >> 26)) continue;

        m[15] = T - Q[12] - F(Q[15], Q[14], Q[13]) - t15;

        changed = 0;
        Q[17] = Q[16] +
            rot(G(Q[16], Q[15], Q[14]) + Q[13] + m[1] + t16, 5);
        if (!bitsequal(Q[17], 3, Q[16])) {
            m[1] += ((Q[2] >> 10) & 1) ? -0x40000000 : 0x40000000;
            Q[2] ^= 0x400;
            Q[17] = Q[16] +
                rot(G(Q[16], Q[15], Q[14]) + Q[13] + m[1] + t16, 5);
            changed = 1;
        }
        if (!bitsequal(Q[17], 15, Q[16])) {
            m[1] += ((Q[2] >> 22) & 1) ? -0x400 : 0x400;
            Q[2] ^= 0x400000;
            Q[17] = Q[16] +
                rot(G(Q[16], Q[15], Q[14]) + Q[13] + m[1] + t16, 5);
            changed = 1;
        }
        if (Q[17] & 0x20000) {
            m[1] += ((Q[2] >> 24) & 1) ? -0x1000 : 0x1000;
            Q[2] ^= 0x1000000;
            Q[17] = Q[16] +
                rot(G(Q[16], Q[15], Q[14]) + Q[13] + m[1] + t16, 5);
            changed = 1;
        }
        if (changed) {
            T = rotr(Q[2] - Q[1], 12);
            if (!(~T >> 25)) return;
            T = rotr(Q[3] - Q[2], 17);
            if ((T >> 31) || !((~T >> 26) & 0x1f)) return;
            m[2] = T - myIVC - F(Q[2], Q[1], myIVB) - t2;
            m[3] = rotr(Q[4] - Q[3], 22) - myIVB -
                F(Q[3], Q[2], Q[1]) - t3;
            m[4] = rotr(Q[5] - Q[4], 7) - Q[1] -
                F(Q[4], Q[3], Q[2]) - t4;
            m[5] = rotr(Q[6] - Q[5], 12) - Q[2] -
                F(Q[5], Q[4], Q[3]) - t5;
        }
        if (Q[17] >> 31) continue;

        if ((Q[17] - Q[16]) >> 29 == 0x7) continue;

        Q[18] = Q[17] +
            rot(G(Q[17], Q[16], Q[15]) + Q[14] + t17 + m[6], 9);
        // Seems impossible to correct:
        if (!(Q[18] & 0x20000)) continue;

        if (!bitsequal(Q[18], 29, Q[17])) {
            m[6] += ((Q[7] >> 5) & 1) ? -0x100000 : 0x100000;
            Q[7] ^= 0x20;
            Q[18] = Q[17] +
                rot(G(Q[17], Q[16], Q[15]) + Q[14] + t17 + m[6], 9);

            T = rotr(Q[7] - Q[6], 17);
            if ((T >> 31) || !(T & 0x7c00)) return;

            T = rotr(Q[8] - Q[7], 22);
            if (!(~T & 0x3f0) || !(~T >> 27)) return;
            m[7] = T - Q[4] - F(Q[7], Q[6], Q[5]) - t7;

            m[8] = rotr(Q[9] - Q[8], 7) - Q[5] -
                F(Q[8], Q[7], Q[6]) - t8;
            m[9] = rotr(Q[10] - Q[9], 12) - Q[6] -
                F(Q[9], Q[8], Q[7]) - t9;
            m[10] = rotr(Q[11] - Q[10], 17) - Q[7] -
                F(Q[10], Q[9], Q[8]) - t10;
        }
        if (Q[18] >> 31) {
            Q[3] ^= 0x400000;

            T = rotr(Q[3] - Q[2], 17);
            if ((T >> 31) || !((~T >> 26) & 0x1f)) return;
            m[2] = T - myIVC - F(Q[2], Q[1], myIVB) - t2;

            T = rotr(Q[4] - Q[3], 22);
            if (!(T >> 27)) return;
            m[3] = T - myIVB - F(Q[3], Q[2], Q[1]) - t3;

            m[4] = rotr(Q[5] - Q[4], 7) - Q[1] -
                F(Q[4], Q[3], Q[2]) - t4;
            m[5] = rotr(Q[6] - Q[5], 12) - Q[2] -
                F(Q[5], Q[4], Q[3]) - t5;
            m[6] = rotr(Q[7] - Q[6], 17) - Q[3] -
                F(Q[6], Q[5], Q[4]) - t6;

            Q[18] = Q[17] +
                rot(G(Q[17], Q[16], Q[15]) + Q[14] + t17 + m[6], 9);
        }

        Q[19] = Q[18] +
            rot(Q[15] + G(Q[18], Q[17], Q[16]) + t18 + m[11], 14);
        if (Q[19] & 0x20000) {
            Q[11] ^= 0x8;
            T = rotr(Q[11] - Q[10], 17);
            if (!(T >> 27)) return;
            m[10] = T - Q[7] - F(Q[10], Q[9], Q[8]) - t10;
            m[11] = rotr(Q[12] - Q[11], 22) - Q[8] -
                F(Q[11], Q[10], Q[9]) - t11;
            m[12] = rotr(Q[13] - Q[12], 7) - Q[9] -
                F(Q[12], Q[11], Q[10]) - t12;
            m[13] = rotr(Q[14] - Q[13], 12) - Q[10] -
                F(Q[13], Q[12], Q[11]) - t13;
            m[14] = rotr(Q[15] - Q[14], 17) - Q[11] -
                F(Q[14], Q[13], Q[12]) - t14;
            Q[19] = Q[18] + rot(Q[15] + G(Q[18], Q[17], Q[16]) +
                t18 + m[11], 14);
        }
        if (Q[19] >> 31) continue;

        // check rest
        T = Q[16] + G(Q[19], Q[18], Q[17]) + t19 + m[0];
        if (!(T >> 29)) continue;
        Q[20] = Q[19] + rot(T, 20);
        if (Q[20] >> 31) continue;

        Q[21] = Q[20] +
            rot(Q[17] + G(Q[20], Q[19], Q[18]) + t20 + m[5], 5);
        if (!bitsequal(Q[21], 17, Q[20]) || Q[21] >> 31) continue;

        Q[22] = Q[21] +
            rot(Q[18] + G(Q[21], Q[20], Q[19]) + t21 + m[10], 9);
        if (Q[22] >> 31) continue;

        T = Q[19] + G(Q[22], Q[21], Q[20]) + t22 + m[15];
        if (T & 0x20000) continue; // p = 1/2

        Q[23] = Q[22] + rot(T, 14);
        if (Q[23] >> 31) continue;

        Q[24] = Q[23] +
            rot(Q[20] + G(Q[23], Q[22], Q[21]) + t23 + m[4], 20);
        if (!(Q[24] >> 31)) continue;

        Q[25] = Q[24] +
            rot(Q[21] + G(Q[24], Q[23], Q[22]) + t24 + m[9], 5);
        Q[26] = Q[25] +
            rot(Q[22] + G(Q[25], Q[24], Q[23]) + t25 + m[14], 9);
        Q[27] = Q[26] +
            rot(Q[23] + G(Q[26], Q[25], Q[24]) + t26 + m[3], 14);
        Q[28] = Q[27] +
            rot(Q[24] + G(Q[27], Q[26], Q[25]) + t27 + m[8], 20);

        Q[29] = Q[28] +
            rot(Q[25] + G(Q[28], Q[27], Q[26]) + t28 + m[13], 5);
        Q[30] = Q[29] +
            rot(Q[26] + G(Q[29], Q[28], Q[27]) + t29 + m[2], 9);
        Q[31] = Q[30] +
            rot(Q[27] + G(Q[30], Q[29], Q[28]) + t30 + m[7], 14);
        Q[32] = Q[31] +
            rot(Q[28] + G(Q[31], Q[30], Q[29]) + t31 + m[12], 20);

        Q[33] = Q[32] +
            rot(Q[29] + H(Q[32], Q[31], Q[30]) + t32 + m[5], 4);
        Q[34] = Q[33] +
            rot(Q[30] + H(Q[33], Q[32], Q[31]) + t33 + m[8], 11);

        // Step 34 T-check
        T = Q[31] + H(Q[34], Q[33], Q[32]) + t34 + m[11];
        if (!(T & 0x8000)) continue; // p = 1/2

        Q[35] = Q[34] + rot(T, 16);
        Q[36] = Q[35] +
            rot(Q[32] + H(Q[35], Q[34], Q[33]) + t35 + m[14], 23);

        Q[37] = Q[36] +
            rot(Q[33] + H(Q[36], Q[35], Q[34]) + t36 + m[1], 4);
        Q[38] = Q[37] +
            rot(Q[34] + H(Q[37], Q[36], Q[35]) + t37 + m[4], 11);
        Q[39] = Q[38] +
            rot(Q[35] + H(Q[38], Q[37], Q[36]) + t38 + m[7], 16);
        Q[40] = Q[39] +
            rot(Q[36] + H(Q[39], Q[38], Q[37]) + t39 + m[10], 23);

        Q[41] = Q[40] +
            rot(Q[37] + H(Q[40], Q[39], Q[38]) + t40 + m[13], 4);
        Q[42] = Q[41] +
            rot(Q[38] + H(Q[41], Q[40], Q[39]) + t41 + m[0], 11);
        Q[43] = Q[42] +
            rot(Q[39] + H(Q[42], Q[41], Q[40]) + t42 + m[3], 16);
        Q[44] = Q[43] +
            rot(Q[40] + H(Q[43], Q[42], Q[41]) + t43 + m[6], 23);

        Q[45] = Q[44] +
            rot(Q[41] + H(Q[44], Q[43], Q[42]) + t44 + m[9], 4);
        Q[46] = Q[45] +
            rot(Q[42] + H(Q[45], Q[44], Q[43]) + t45 + m[12], 11);
        Q[47] = Q[46] +
            rot(Q[43] + H(Q[46], Q[45], Q[44]) + t46 + m[15], 16);
        Q[48] = Q[47] +
            rot(Q[44] + H(Q[47], Q[46], Q[45]) + t47 + m[2], 23);
        if ((Q[48] ^ Q[46]) & 0x80000000) continue;

        Q[49] = Q[48] +
            rot(Q[45] + I(Q[48], Q[47], Q[46]) + t48 + m[0], 6);
        if ((Q[49] ^ Q[47]) & 0x80000000) continue;

        Q[50] = Q[49] +
            rot(Q[46] + I(Q[49], Q[48], Q[47]) + t49 + m[7], 10);
        if ((~Q[50] ^ Q[46]) & 0x80000000) continue;

        Q[51] = Q[50] +
            rot(Q[47] + I(Q[50], Q[49], Q[48]) + t50 + m[14], 15);
        if ((Q[51] ^ Q[49]) & 0x80000000) continue;

        Q[52] = Q[51] +
            rot(Q[48] + I(Q[51], Q[50], Q[49]) + t51 + m[5], 21);
        if ((Q[52] ^ Q[50]) & 0x80000000) continue;

        Q[53] = Q[52] +
            rot(Q[49] + I(Q[52], Q[51], Q[50]) + t52 + m[12], 6);
        if ((Q[53] ^ Q[51]) & 0x80000000) continue;

        Q[54] = Q[53] +
            rot(Q[50] + I(Q[53], Q[52], Q[51]) + t53 + m[3], 10);
        if ((Q[54] ^ Q[52]) & 0x80000000) continue;

        Q[55] = Q[54] +
            rot(Q[51] + I(Q[54], Q[53], Q[52]) + t54 + m[10], 15);
        if ((Q[55] ^ Q[53]) & 0x80000000) continue;

        Q[56] = Q[55] +
            rot(Q[52] + I(Q[55], Q[54], Q[53]) + t55 + m[1], 21);
        if ((Q[56] ^ Q[54]) & 0x80000000) continue;

        Q[57] = Q[56] +
            rot(Q[53] + I(Q[56], Q[55], Q[54]) + t56 + m[8], 6);
        if ((Q[57] ^ Q[55]) & 0x80000000) continue;

        Q[58] = Q[57] +
            rot(Q[54] + I(Q[57], Q[56], Q[55]) + t57 + m[15], 10);
        if ((Q[58] ^ Q[56]) & 0x80000000) continue;

        Q[59] = Q[58] +
            rot(Q[55] + I(Q[58], Q[57], Q[56]) + t58 + m[6], 15);
        if ((Q[59] ^ Q[57]) & 0x80000000) continue;

        Q[60] = Q[59] +
            rot(Q[56] + I(Q[59], Q[58], Q[57]) + t59 + m[13], 21);
        if ((Q[60] & 0x2000000) || (~Q[60] ^ Q[58]) & 0x80000000)
            continue;

        Q[61] = Q[60] +
            rot(Q[57] + I(Q[60], Q[59], Q[58]) + t60 + m[4], 6);
        if ((!(Q[61] & 0x2000000)) || ((Q[61] ^ Q[59]) & 0x80000000))
            continue;

        T = Q[58] + I(Q[61], Q[60], Q[59]) + t61 + m[11];
        if (!(T & 0x3f8000)) continue;

        Q[62] = Q[61] + rot(T, 10);
        if (!(Q[62] & 0x2000000) || ((Q[62] ^ Q[60]) & 0x80000000))
            continue;

        printf(":");
        Q[63] = Q[62] +
            rot(Q[59] + I(Q[62], Q[61], Q[60]) + t62 + m[2], 15);
        if ((Q[63] ^ Q[61]) & 0x80000000) continue;

        if (!(Q[63] & 0x2000000)) {
            T = Q[63] >> 26;
            T2 = Q[61] >> 26;
            if (!T) continue;

            while (!(T & 1)) {
                if (T2 & 1) break;
                T >>= 1; T2 >>= 1;
            }
            if (!(T & 1) || T2 & 1) continue;
        }

        printf("\n");

        start_over = 0;
        break;
    } while (ctr < TRY2);
}

inline void search2() {
    do {
        modify_0_13();
        checkrest();
    } while (start_over);
}

int main(int argc, char* argv[]) {
    X = 777;
    printf("block 1 starts\r\n");
    search1();
    printf("block 1 ends\r\n");
    printf("block 2 starts\r\n");
    search2();
    printf("block 2 ends\r\n");
}