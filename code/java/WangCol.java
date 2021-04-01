import java.util.Scanner;

public class WangCol {
//	Initial IV[0] IV[-1] IV[-2] IV[-3]
	public int A = 0x67452301;
	public int B = 0xefcdab89;
	public int C = 0x98badcfe;
	public int D = 0x10325476;

//	Additional Constant K
	private final int K[] = { 0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613,
			0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
			0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6,
			0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681,
			0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085,
			0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
			0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82,
			0xbd3af235, 0x2ad7d2bb, 0xeb86d391 };

//	Left or Right RLation Functions
	private int RL(int a, int s) {
		return (a << s) | (a >>> (32 - s));
	}

	private int RR(int a, int s) {
		return (a >>> s) | (a << (32 - s));
	}

//	Pseudo Random Generator prg()
//	private int prg() {
//		Random rand = new Random();
//		return rand.nextInt();
//	}
	public int X;

	private int prg() {
		X = (1103515245 * X + 12345) & 0xffffffff;
		return X;
	}

	private boolean msb_equal(int a, int b) {
		return (((~a) ^ (b)) & 0x80000000) != 0;
	}

	private boolean bitsequal(int a, int n, int b) {
		return (((~(a) ^ (b)) >> n) & 1) == 1;
	}

//	Compress Functions F, G, H and I
	private int F(int b, int c, int d) {
		return (b & c) | ((~b) & d);
	}

	private int G(int b, int c, int d) {
		return (d & b) | ((~d) & c);
	}

	private int H(int b, int c, int d) {
		return b ^ c ^ d;
	}

	private int I(int b, int c, int d) {
		return c ^ (b | (~d));
	}

//  convert an integer to a word string
	private static String toHex(int a) {
		String str = Integer.toHexString(a);
		while (str.length() < 8) {
			str = "0" + str;
		}
		return str;
	}

	private int[] x = new int[16]; // message 1 consists of 16 words for block1
	private int[] xx = new int[16]; // message 1 consists of 16 words for block2
	private int[] Hx = new int[16]; // message 2 consists of 16 words for block1
	private int[] Hxx = new int[16]; // message 2 consists of 16 words for block2
	private int A0, B0, C0, D0; // Intermediate hash values of the block1 for message 1
	private int A1, B1, C1, D1; // Intermediate hash values of the block1 for message 2

	// the first block
	private int block1() {
//		load the initial IHVs
		int IVA = A, IVB = B, IVC = C, IVD = D;
		int tempA, tempB, tempC, tempD;
		int[] Q = new int[65]; // to store the step digest
		int T; // temporary storage
		int ctr; // count the number of trials

//		for loop start
		for (;;) {

			Q[3] = prg();
			Q[3] &= 0xfff7f7bf;

			Q[4] = prg();
			Q[4] &= 0xff7fffbf;
			Q[4] |= 0x00080800;
			Q[4] ^= (Q[3] ^ Q[4]) & 0x77f780;

			Q[5] = prg();
			Q[5] &= 0xfd40003f;
			Q[5] |= 0x08400025;
			Q[5] ^= (Q[4] ^ Q[5]) & 0x80000000;
			if ((RR(Q[5] - Q[4], 7) >> 31) == 0) // msb=1
				continue;

			Q[6] = prg();
			Q[6] &= 0xf77fbc5b;
			Q[6] |= 0x827fbc41;
			Q[6] ^= (Q[5] ^ Q[6]) & 0x7500001a;
			if ((RR(Q[6] - Q[5], 12) & 0x80000) != 0) // 20th=0
				continue;

			Q[7] = 0x03fef820;
			T = RR(Q[7] - Q[6], 17); // T_6
			if ((T & 0x4000) != 0 || ((T >> 10) & 0xf) == 0) // 0 and 1
				continue;
//			x[6] = T - F(Q[6], Q[5], Q[4]) - Q[3] - K[6];

			Q[8] = prg();
			Q[8] &= 0x01f15540;
			Q[8] |= 0x01910540;
//			T = RR(Q[8] - Q[7], 22);
//			x[7] = T - F(Q[7], Q[6], Q[5]) - Q[4] - K[7];

			for (;;) {

				for (;;) {
					Q[9] = prg();
					Q[9] &= 0xfbf07f3d;
					Q[9] |= 0x7b102f3d;
					Q[9] ^= (Q[8] ^ Q[9]) & 0x1000;
					Q[9] ^= (~Q[7] ^ Q[9]) & 0x80000000;
					T = RR(Q[9] - Q[8], 7); // T_8
					if ((T >> 31) == 0 || (T & 0x1000000) == 0) // 1 and 1
						continue;
//					x[8] = T - F(Q[8], Q[7], Q[6]) - Q[5] - K[8];

					Q[10] = prg();
					Q[10] &= 0xff7fde7c;
					Q[10] |= 0x401f9040;
					Q[10] ^= (~Q[9] ^ Q[10]) & 0x80000000;
					T = RR(Q[10] - Q[9], 12); // T_9
					if ((~T >> 27) == 0) // 1
						continue;
//					x[9] = T - F(Q[9], Q[8], Q[7]) - Q[6] - K[9];

					Q[11] = prg();
					Q[11] &= 0xbff1cefc;
					Q[11] |= 0x000180c2;
					Q[11] ^= (Q[10] ^ Q[11]) & 0x80004000;
					T = RR(Q[11] - Q[10], 17); // T_10

					if ((~T & 0x6000) != 0 && (T >> 27) != 0) // 1 and 1
						break;

				} // end for 2

//				x[10] = T - F(Q[10], Q[9], Q[8]) - Q[7] - K[10];

				Q[12] = prg();
				Q[12] &= 0xbff81f7f;
				Q[12] |= 0x00081100;
				Q[12] ^= (Q[11] ^ Q[12]) & 0x83000000;
				T = RR(Q[12] - Q[11], 22); // T_11

				if ((T & 0x300) != 0 && (T >> 24) != 0) // 1 and 1
					break;

			} // end for 1

//			x[11] = T - F(Q[11], Q[10], Q[9]) - Q[8] - K[11];

			Q[13] = prg();
			Q[13] &= 0xfdfffe7f;
			Q[13] |= 0x410fe008;
			Q[13] ^= (Q[12] ^ Q[13]) & 0x80000000;
//			x[12] = RR(Q[13] - Q[12], 7) - F(Q[12], Q[11], Q[10]) - Q[9] - K[12];

			for (;;) {

				Q[14] = prg();
				Q[14] &= 0xdcfbffff;
				Q[14] |= 0x000be188;
				Q[14] ^= (Q[13] ^ Q[14]) & 0x80000000;
//				x[13] = RR(Q[14] - Q[13], 12) - F(Q[13], Q[12], Q[11]) - Q[10] - K[13];

				Q[15] = prg();
				Q[15] &= 0xfdfffff7;
				Q[15] |= 0x21008000;
				T = RR(Q[15] - Q[14], 17);
				if ((T >> 30) == 0) // 1
					continue;
//				x[14] = T - F(Q[14], Q[13], Q[12]) - Q[11] - K[14];

				Q[16] = prg();
				Q[16] |= 0x20000000;
				Q[16] ^= (Q[15] ^ Q[16]) & 0x80000000;

				T = RR(Q[16] - Q[15], 22); // T_15
//				x[15] = T - F(Q[15], Q[14], Q[13]) - Q[12] - K[15];
				if ((T & 0x380) != 0 && (~T >> 26) != 0) // 1 and 1
					break;
			}

			x[6] = RR(Q[7] - Q[6], 17) - F(Q[6], Q[5], Q[4]) - Q[3] - K[6];
			x[11] = RR(Q[12] - Q[11], 22) - F(Q[11], Q[10], Q[9]) - Q[8] - K[11];

			for (ctr = 0; ctr < 0xffff; ctr++) {

				Q[17] = prg();
				Q[17] &= 0xfffdffff;
				Q[17] ^= (Q[16] ^ Q[17]) & 0x80008008;
				Q[18] = Q[17] + RL(G(Q[17], Q[16], Q[15]) + Q[14] + x[6] + K[17], 9);
				Q[19] = Q[18] + RL(G(Q[18], Q[17], Q[16]) + Q[15] + x[11] + K[18], 14);

				if (((Q[18] >> 17) & 1) != 0 && ((Q[17] ^ Q[18]) & 0xa0000000) == 0 && (Q[19] & 0x20000) == 0
						&& ((Q[18] ^ Q[19]) & 0x80000000) == 0)
					break;
			}
			if (ctr > 0xffff)
				continue;

			T = RR(Q[17] - Q[16], 5); // T_16
			if ((T & 0x1000000) != 0) // 0
				continue;
			x[1] = T - G(Q[16], Q[15], Q[14]) - Q[13] - K[16];

			for (Q[20] = Q[19] & 0x80000000; Q[20] != (~Q[19] & 0x80000000); Q[20]++) {

				T = RR(Q[20] - Q[19], 20); // T_19
				if ((T >> 29) == 0) // 1
					continue;
				x[0] = T - G(Q[19], Q[18], Q[17]) - Q[16] - K[19];

				Q[1] = IVB + RL(IVA + F(IVB, IVC, IVD) + K[0] + x[0], 7);
				Q[2] = Q[1] + RL(IVD + F(Q[1], IVB, IVC) + K[1] + x[1], 12);

//				x[2] = RR(Q[3] - Q[2], 17) - F(Q[2], Q[1], IVB) - IVC - K[2];
//				x[3] = RR(Q[4] - Q[3], 22) - F(Q[3], Q[2], Q[1]) - IVB - K[3];
//				x[4] = RR(Q[5] - Q[4], 7) - F(Q[4], Q[3], Q[2]) - Q[1] - K[4];
//				x[5] = RR(Q[6] - Q[5], 12) - F(Q[5], Q[4], Q[3]) - Q[2] - K[5];
//				// x[6] = RR(Q[7] - Q[6], 17) - F(Q[6], Q[5], Q[4]) - Q[3] - K[6];
//				x[7] = RR(Q[8] - Q[7], 22) - F(Q[7], Q[6], Q[5]) - Q[4] - K[7];
//				x[8] = RR(Q[9] - Q[8], 7) - F(Q[8], Q[7], Q[6]) - Q[5] - K[8];
//				x[9] = RR(Q[10] - Q[9], 12) - F(Q[9], Q[8], Q[7]) - Q[6] - K[9];
//				x[10] = RR(Q[11] - Q[10], 17) - F(Q[10], Q[9], Q[8]) - Q[7] - K[10];
//				// x[11] = RR(Q[12] - Q[11], 22) - F(Q[11], Q[10], Q[9]) - Q[8] - K[11];
//				x[12] = RR(Q[13] - Q[12], 7) - F(Q[12], Q[11], Q[10]) - Q[9] - K[12];
//				x[13] = RR(Q[14] - Q[13], 12) - F(Q[13], Q[12], Q[11]) - Q[10] - K[13];
//				x[14] = RR(Q[15] - Q[14], 17) - F(Q[14], Q[13], Q[12]) - Q[11] - K[14];
//				x[15] = RR(Q[16] - Q[15], 22) - F(Q[15], Q[14], Q[13]) - Q[12] - K[15];

				// check rest
				x[5] = RR(Q[6] - Q[5], 12) - F(Q[5], Q[4], Q[3]) - Q[2] - K[5];
				Q[21] = Q[20] + RL(Q[17] + G(Q[20], Q[19], Q[18]) + K[20] + x[5], 5);
				if (!bitsequal(Q[21], 17, Q[20]) || !msb_equal(Q[21], Q[20])) // checked
					continue;

				x[10] = RR(Q[11] - Q[10], 17) - F(Q[10], Q[9], Q[8]) - Q[7] - K[10];
				Q[22] = Q[21] + RL(Q[18] + G(Q[21], Q[20], Q[19]) + K[21] + x[10], 9);
				if (!msb_equal(Q[22], Q[21])) // checked
					continue;

				// T_22
				x[15] = RR(Q[16] - Q[15], 22) - F(Q[15], Q[14], Q[13]) - Q[12] - K[15];
				T = Q[19] + G(Q[22], Q[21], Q[20]) + K[22] + x[15];
				if ((T & 0x20000) != 0) // 0
					continue;

				Q[23] = Q[22] + RL(T, 14);
				if ((Q[23] >> 31) != 0) // 0
					continue;

				x[4] = RR(Q[5] - Q[4], 7) - F(Q[4], Q[3], Q[2]) - Q[1] - K[4];
				Q[24] = Q[23] + RL(Q[20] + G(Q[23], Q[22], Q[21]) + K[23] + x[4], 20);
				if ((Q[24] >> 31) == 0) // 1
					continue;

				x[2] = RR(Q[3] - Q[2], 17) - F(Q[2], Q[1], IVB) - IVC - K[2];
				x[3] = RR(Q[4] - Q[3], 22) - F(Q[3], Q[2], Q[1]) - IVB - K[3];
				x[7] = RR(Q[8] - Q[7], 22) - F(Q[7], Q[6], Q[5]) - Q[4] - K[7];
				x[8] = RR(Q[9] - Q[8], 7) - F(Q[8], Q[7], Q[6]) - Q[5] - K[8];
				x[9] = RR(Q[10] - Q[9], 12) - F(Q[9], Q[8], Q[7]) - Q[6] - K[9];
				x[12] = RR(Q[13] - Q[12], 7) - F(Q[12], Q[11], Q[10]) - Q[9] - K[12];
				x[13] = RR(Q[14] - Q[13], 12) - F(Q[13], Q[12], Q[11]) - Q[10] - K[13];
				x[14] = RR(Q[15] - Q[14], 17) - F(Q[14], Q[13], Q[12]) - Q[11] - K[14];

				Q[25] = Q[24] + RL(Q[21] + G(Q[24], Q[23], Q[22]) + K[24] + x[9], 5);
				Q[26] = Q[25] + RL(Q[22] + G(Q[25], Q[24], Q[23]) + K[25] + x[14], 9);
				Q[27] = Q[26] + RL(Q[23] + G(Q[26], Q[25], Q[24]) + K[26] + x[3], 14);
				Q[28] = Q[27] + RL(Q[24] + G(Q[27], Q[26], Q[25]) + K[27] + x[8], 20);
				Q[29] = Q[28] + RL(Q[25] + G(Q[28], Q[27], Q[26]) + K[28] + x[13], 5);
				Q[30] = Q[29] + RL(Q[26] + G(Q[29], Q[28], Q[27]) + K[29] + x[2], 9);
				Q[31] = Q[30] + RL(Q[27] + G(Q[30], Q[29], Q[28]) + K[30] + x[7], 14);
				Q[32] = Q[31] + RL(Q[28] + G(Q[31], Q[30], Q[29]) + K[31] + x[12], 20);
				Q[33] = Q[32] + RL(Q[29] + H(Q[32], Q[31], Q[30]) + K[32] + x[5], 4);
				Q[34] = Q[33] + RL(Q[30] + H(Q[33], Q[32], Q[31]) + K[33] + x[8], 11);

				// T_34
				T = Q[31] + H(Q[34], Q[33], Q[32]) + K[34] + x[11];
				if ((T & 0x8000) != 0) // 0
					continue;

				Q[35] = Q[34] + RL(T, 16);
				Q[36] = Q[35] + RL(Q[32] + H(Q[35], Q[34], Q[33]) + K[35] + x[14], 23);

				Q[37] = Q[36] + RL(Q[33] + H(Q[36], Q[35], Q[34]) + K[36] + x[1], 4);
				Q[38] = Q[37] + RL(Q[34] + H(Q[37], Q[36], Q[35]) + K[37] + x[4], 11);
				Q[39] = Q[38] + RL(Q[35] + H(Q[38], Q[37], Q[36]) + K[38] + x[7], 16);
				Q[40] = Q[39] + RL(Q[36] + H(Q[39], Q[38], Q[37]) + K[39] + x[10], 23);

				Q[41] = Q[40] + RL(Q[37] + H(Q[40], Q[39], Q[38]) + K[40] + x[13], 4);
				Q[42] = Q[41] + RL(Q[38] + H(Q[41], Q[40], Q[39]) + K[41] + x[0], 11);
				Q[43] = Q[42] + RL(Q[39] + H(Q[42], Q[41], Q[40]) + K[42] + x[3], 16);
				Q[44] = Q[43] + RL(Q[40] + H(Q[43], Q[42], Q[41]) + K[43] + x[6], 23);

				Q[45] = Q[44] + RL(Q[41] + H(Q[44], Q[43], Q[42]) + K[44] + x[9], 4);
				Q[46] = Q[45] + RL(Q[42] + H(Q[45], Q[44], Q[43]) + K[45] + x[12], 11);
				Q[47] = Q[46] + RL(Q[43] + H(Q[46], Q[45], Q[44]) + K[46] + x[15], 16);
				Q[48] = Q[47] + RL(Q[44] + H(Q[47], Q[46], Q[45]) + K[47] + x[2], 23);
				if (((Q[48] ^ Q[46]) & 0x80000000) != 0)
					continue;

				Q[49] = Q[48] + RL(Q[45] + I(Q[48], Q[47], Q[46]) + K[48] + x[0], 6);
				if (((Q[49] ^ Q[47]) & 0x80000000) != 0) // 0
					continue;

				Q[50] = Q[49] + RL(Q[46] + I(Q[49], Q[48], Q[47]) + K[49] + x[7], 10);
				if (((~Q[50] ^ Q[46]) & 0x80000000) != 0) // 0
					continue;

				Q[51] = Q[50] + RL(Q[47] + I(Q[50], Q[49], Q[48]) + K[50] + x[14], 15);
				if (((Q[51] ^ Q[49]) & 0x80000000) != 0) // 0
					continue;

				Q[52] = Q[51] + RL(Q[48] + I(Q[51], Q[50], Q[49]) + K[51] + x[5], 21);
				if (((Q[52] ^ Q[50]) & 0x80000000) != 0) // 0
					continue;

				Q[53] = Q[52] + RL(Q[49] + I(Q[52], Q[51], Q[50]) + K[52] + x[12], 6);
				if (((Q[53] ^ Q[51]) & 0x80000000) != 0) // 0
					continue;

				Q[54] = Q[53] + RL(Q[50] + I(Q[53], Q[52], Q[51]) + K[53] + x[3], 10);
				if (((Q[54] ^ Q[52]) & 0x80000000) != 0) // 0
					continue;

				Q[55] = Q[54] + RL(Q[51] + I(Q[54], Q[53], Q[52]) + K[54] + x[10], 15);
				if (((Q[55] ^ Q[53]) & 0x80000000) != 0) // 0
					continue;

				Q[56] = Q[55] + RL(Q[52] + I(Q[55], Q[54], Q[53]) + K[55] + x[1], 21);
				if (((Q[56] ^ Q[54]) & 0x80000000) != 0) // 0
					continue;

				Q[57] = Q[56] + RL(Q[53] + I(Q[56], Q[55], Q[54]) + K[56] + x[8], 6);
				if (((Q[57] ^ Q[55]) & 0x80000000) != 0) // 0
					continue;

				Q[58] = Q[57] + RL(Q[54] + I(Q[57], Q[56], Q[55]) + K[57] + x[15], 10);
				if (((Q[58] ^ Q[56]) & 0x80000000) != 0) // 0
					continue;

				Q[59] = Q[58] + RL(Q[55] + I(Q[58], Q[57], Q[56]) + K[58] + x[6], 15);
				if (((Q[59] ^ Q[57]) & 0x80000000) != 0) // 0
					continue;

				Q[60] = Q[59] + RL(Q[56] + I(Q[59], Q[58], Q[57]) + K[59] + x[13], 21);
				if ((Q[60] & 0x2000000) != 0 || ((~Q[60] ^ Q[58]) & 0x80000000) != 0) // 0 and 0
					continue;

				Q[61] = Q[60] + RL(Q[57] + I(Q[60], Q[59], Q[58]) + K[60] + x[4], 6);
				if ((Q[61] & 0x2000000) == 0 || ((Q[61] ^ Q[59]) & 0x80000000) != 0) // 1 and 0
					continue;

				tempA = IVA + Q[61];

				T = Q[58] + I(Q[61], Q[60], Q[59]) + K[61] + x[11];
				if ((~T & 0x3f8000) == 0) // 1
					continue;

				Q[62] = Q[61] + RL(T, 10);
				if ((Q[62] & 0x2000000) != 0 || ((Q[62] ^ Q[60]) & 0x80000000) != 0) // 0 and 0
					continue;

				tempD = IVD + Q[62];
				if ((tempD & 0x2000000) != 0) // 0
					continue;

				Q[63] = Q[62] + RL(Q[59] + I(Q[62], Q[61], Q[60]) + K[62] + x[2], 15);
				if ((Q[63] & 0x2000000) != 0 || ((Q[63] ^ Q[61]) & 0x80000000) != 0) // 0 and 0
					continue;

				tempC = IVC + Q[63];
				if ((tempC & 0x2000000) == 0 || (tempC & 0x4000000) != 0 || ((tempC ^ tempD) & 0x80000000) != 0) // 1
																													// and
																													// 0
																													// and
																													// 0
					continue;

				System.out.print("> ");

				Q[64] = Q[63] + RL(Q[60] + I(Q[63], Q[62], Q[61]) + K[63] + x[9], 21);
				tempB = IVB + Q[64];
				if ((tempB & 0x06000020) != 0 || ((tempB ^ tempC) & 0x80000000) != 0) // 0 and 0
					continue;

				A0 = tempA;
				B0 = tempB;
				C0 = tempC;
				D0 = tempD;

				return 1;
			} // end branch for

		} // end main for

	} // end block 1

	// the second block
	private int block2() {
//		load the initial IHVs
		int IVA = A0, IVB = B0, IVC = C0, IVD = D0;
		int[] Q = new int[65]; // to store the step digest
		int T, T2, changed; // temporary flag storage

		for (;;) {

			for (;;) {
				Q[1] = prg();
				Q[1] &= 0xf5fff7df;
				// Q[1] |= 0x04200040;
				Q[1] |= 0x04200000;
				Q[1] ^= (~Q[1] ^ B0) & 0x80000000;

				Q[2] = prg();
				Q[2] &= 0xfddfffd9;
				// Q[2] |= 0x0c000840;
				Q[2] |= 0x0c000800;
				// Q[2] ^= (Q[1]^Q[2])&0xf01f1080;
				Q[2] ^= (Q[1] ^ Q[2]) & 0xf01f10c0;

				T = RR(Q[2] - Q[1], 12);
				if ((~T >> 25) == 0)
					continue;
//				xx[1] = T - D0 - F(Q[1], B0, C0) - K[1];

				Q[3] = prg();
				Q[3] &= 0xbfdfef7f;
				Q[3] |= 0x3e1f0966;
				Q[3] ^= (Q[2] ^ Q[3]) & 0x80000018;

				T = RR(Q[3] - Q[2], 17);
				if ((T >> 31) != 0 || ((~T >> 26) & 0x1f) == 0)
					continue;
//				xx[2] = T - C0 - F(Q[2], Q[1], B0) - K[2];

				Q[4] = prg();
				Q[4] &= 0xbbc4e611;
				Q[4] |= 0x3a040010;
				Q[4] ^= (Q[3] ^ Q[4]) & 0x80000601;

				T = RR(Q[4] - Q[3], 22);
				if ((T >> 27) == 0)
					continue;
//				xx[3] = T - B0 - F(Q[3], Q[2], Q[1]) - K[3];

				Q[5] = prg();
				Q[5] &= 0xcbefee50;
				Q[5] |= 0x482f0e50;
				Q[5] ^= (~Q[4] ^ Q[5]) & 0x80000000;

				T = RR(Q[5] - Q[4], 7);
				if ((T >> 31) != 0 || (T & 0x40000000) == 0)
					continue;
//				xx[4] = T - Q[1] - F(Q[4], Q[3], Q[2]) - K[4];

				Q[6] = prg();
				Q[6] &= 0xe5eeec56;
				Q[6] |= 0x04220c56;
				Q[6] ^= (Q[5] ^ Q[6]) & 0x80000000;

				T = RR(Q[6] - Q[5], 12);
				if ((T >> 30) == 0)
					continue;
//				xx[5] = T - Q[2] - F(Q[5], Q[4], Q[3]) - K[5];

				Q[7] = prg();
				Q[7] &= 0xf7cdfe3f;
				Q[7] |= 0x16011e01;
				Q[7] ^= (~Q[6] ^ Q[7]) & 0x80000000;
				Q[7] ^= (Q[6] ^ Q[7]) & 0x1808000;

				T = RR(Q[7] - Q[6], 17);
				if ((T >> 31) != 0 || (T & 0x7c00) == 0)
					continue;
//				xx[6] = T - Q[3] - F(Q[6], Q[5], Q[4]) - K[6];

				Q[8] = prg();
				Q[8] &= 0xe47efffe;
				Q[8] |= 0x043283e0; // Added Q_8[5] = 1 *
				Q[8] ^= (Q[7] ^ Q[8]) & 0x80000002;

				T = RR(Q[8] - Q[7], 22);
				if ((~T & 0x3f0) == 0 || (~T >> 27) == 0)
					continue;
//				xx[7] = T - Q[4] - F(Q[7], Q[6], Q[5]) - K[7];

				Q[9] = prg();
				Q[9] &= 0xfc7d7ddd; // Added Q_9[5] = 0 *
				Q[9] |= 0x1c0101c1;
				Q[9] ^= (Q[8] ^ Q[9]) & 0x80001000;
				// * so that Q[9]-Q[8] produces a carry into bit 6

				T = RR(Q[9] - Q[8], 7);
				if ((T >> 31) == 0 || (~T & 0x7e000000) == 0)
					continue;
//				xx[8] = T - Q[5] - F(Q[8], Q[7], Q[6]) - K[8];

				Q[10] = prg();
				Q[10] &= 0xfffbeffc;
				Q[10] |= 0x078383c0;
				// Added Q[10],3 != Q[9],3
				// so correction in step 19 works:
				Q[10] ^= (~Q[9] ^ Q[10]) & 0x8;
				Q[10] ^= (Q[9] ^ Q[10]) & 0x80000000;
				T = RR(Q[10] - Q[9], 12);
				if ((T >> 27) == 0)
					continue;
//				xx[9] = T - Q[6] - F(Q[9], Q[8], Q[7]) - K[9];

				Q[11] = prg();
				Q[11] &= 0xfffdefff;
				Q[11] |= 0x000583c3;
				Q[11] ^= (Q[10] ^ Q[11]) & 0x80086000;

				T = RR(Q[11] - Q[10], 17);
				if ((T >> 27) == 0)
					continue;
//				xx[10] = T - Q[7] - F(Q[10], Q[9], Q[8]) - K[10];

				Q[12] = prg();
				Q[12] &= 0xfff81fff;
				Q[12] |= 0x00081080;
				Q[12] ^= (Q[12] ^ Q[11]) & 0xff000000;

				Q[13] = prg();
				Q[13] &= 0xbfffff7f;
				Q[13] |= 0x3f0fe008;
				Q[13] ^= (~Q[12] ^ Q[13]) & 0x80000000;

				Q[14] = prg();
				Q[14] &= 0xc0fbffff;
				Q[14] |= 0x400be088;
				Q[14] ^= (Q[13] ^ Q[14]) & 0x80000000;

				T = RR(Q[14] - Q[13], 12);
				if (((T >> 12) & 0xff) == 0)
					continue;
//				xx[13] = T - Q[10] - F(Q[13], Q[12], Q[11]) - K[13];
//
//				xx[0] = RR(Q[1] - B0, 7) - IVA - F(IVB, IVC, IVD) - K[0];
//				xx[11] = RR(Q[12] - Q[11], 22) - Q[8] - F(Q[11], Q[10], Q[9]) - K[11];
//				xx[12] = RR(Q[13] - Q[12], 7) - Q[9] - F(Q[12], Q[11], Q[10]) - K[12];
//				xx[13] = RR(Q[14] - Q[13], 12) - Q[10] - F(Q[13], Q[12], Q[11]) - K[13];

				break;
			}
			/*---------------------------------------------------------------------------------------------------*/
			for (int i = 0; i < 0x10000; i++) {

				Q[15] = prg();
				Q[15] &= 0x7dff7ff7;
				Q[15] |= 0x7d000000;

				T = RR(Q[15] - Q[14], 17);
				if ((~T >> 30) == 0)
					continue;
//				xx[14] = T - Q[11] - F(Q[14], Q[13], Q[12]) - K[14];

				Q[16] = prg();
				Q[16] &= 0x7fffffff;
				Q[16] |= 0x20000000;
				// Q[16] ^= (Q[15]^Q[16])&0x80000000;

				T = RR(Q[16] - Q[15], 22);
				if ((T & 0x380) == 0 || (T >> 26) == 0)
					continue;
//				xx[15] = T - Q[12] - F(Q[15], Q[14], Q[13]) - K[15];

				xx[1] = RR(Q[2] - Q[1], 12) - D0 - F(Q[1], B0, C0) - K[1];

				changed = 0;
				Q[17] = Q[16] + RL(G(Q[16], Q[15], Q[14]) + Q[13] + xx[1] + K[16], 5);

				if (!bitsequal(Q[17], 3, Q[16])) {
					xx[1] += (((Q[2] >> 10) & 1) != 0) ? -0x40000000 : 0x40000000;
					Q[2] ^= 0x400;
					Q[17] = Q[16] + RL(G(Q[16], Q[15], Q[14]) + Q[13] + xx[1] + K[16], 5);
					changed = 1;
				}
				if (!bitsequal(Q[17], 15, Q[16])) {
					xx[1] += (((Q[2] >> 22) & 1) != 0) ? -0x400 : 0x400;
					Q[2] ^= 0x400000;
					Q[17] = Q[16] + RL(G(Q[16], Q[15], Q[14]) + Q[13] + xx[1] + K[16], 5);
					changed = 1;
				}
				if ((Q[17] & 0x20000) != 0) {
					xx[1] += (((Q[2] >> 24) & 1) != 0) ? -0x1000 : 0x1000;
					Q[2] ^= 0x1000000;
					Q[17] = Q[16] + RL(G(Q[16], Q[15], Q[14]) + Q[13] + xx[1] + K[16], 5);
					changed = 1;
				}
				if (changed != 0) {
					T = RR(Q[2] - Q[1], 12);
					if ((~T >> 25) == 0)
						break;
					T = RR(Q[3] - Q[2], 17);
					if ((T >> 31) != 0 || ((~T >> 26) & 0x1f) == 0)
						break;
					xx[2] = T - C0 - F(Q[2], Q[1], B0) - K[2];
					xx[3] = RR(Q[4] - Q[3], 22) - B0 - F(Q[3], Q[2], Q[1]) - K[3];
					xx[4] = RR(Q[5] - Q[4], 7) - Q[1] - F(Q[4], Q[3], Q[2]) - K[4];
					xx[5] = RR(Q[6] - Q[5], 12) - Q[2] - F(Q[5], Q[4], Q[3]) - K[5];
				}

				if (Q[17] >> 31 != 0)
					continue;

				if ((Q[17] - Q[16]) >> 29 == 0x7)
					continue;

				xx[6] = RR(Q[7] - Q[6], 17) - Q[3] - F(Q[6], Q[5], Q[4]) - K[6];
				Q[18] = Q[17] + RL(G(Q[17], Q[16], Q[15]) + Q[14] + K[17] + xx[6], 9);
				// Seems impossible to correct:
				if ((Q[18] & 0x20000) == 0)
					continue;

				if (!bitsequal(Q[18], 29, Q[17])) {
					xx[6] += (((Q[7] >> 5) & 1) != 0) ? -0x100000 : 0x100000;
					Q[7] ^= 0x20;
					Q[18] = Q[17] + RL(G(Q[17], Q[16], Q[15]) + Q[14] + K[17] + xx[6], 9);

					T = RR(Q[7] - Q[6], 17);
					if ((T >> 31) != 0 || (T & 0x7c00) == 0)
						break;

					T = RR(Q[8] - Q[7], 22);
					if ((~T & 0x3f0) == 0 || (~T >> 27) == 0)
						break;
					xx[7] = T - Q[4] - F(Q[7], Q[6], Q[5]) - K[7];

					xx[8] = RR(Q[9] - Q[8], 7) - Q[5] - F(Q[8], Q[7], Q[6]) - K[8];
					xx[9] = RR(Q[10] - Q[9], 12) - Q[6] - F(Q[9], Q[8], Q[7]) - K[9];
					xx[10] = RR(Q[11] - Q[10], 17) - Q[7] - F(Q[10], Q[9], Q[8]) - K[10];
				}

				if (Q[18] >> 31 != 0) {
					Q[3] ^= 0x400000;

					T = RR(Q[3] - Q[2], 17);
					if ((T >> 31) != 0 || ((~T >> 26) & 0x1f) == 0)
						break;
					xx[2] = T - C0 - F(Q[2], Q[1], B0) - K[2];

					T = RR(Q[4] - Q[3], 22);
					if ((T >> 27) == 0)
						break;
					xx[3] = T - B0 - F(Q[3], Q[2], Q[1]) - K[3];

					xx[4] = RR(Q[5] - Q[4], 7) - Q[1] - F(Q[4], Q[3], Q[2]) - K[4];
					xx[5] = RR(Q[6] - Q[5], 12) - Q[2] - F(Q[5], Q[4], Q[3]) - K[5];
					xx[6] = RR(Q[7] - Q[6], 17) - Q[3] - F(Q[6], Q[5], Q[4]) - K[6];

					Q[18] = Q[17] + RL(G(Q[17], Q[16], Q[15]) + Q[14] + K[17] + xx[6], 9);
				}

				xx[11] = RR(Q[12] - Q[11], 22) - Q[8] - F(Q[11], Q[10], Q[9]) - K[11];
				Q[19] = Q[18] + RL(Q[15] + G(Q[18], Q[17], Q[16]) + K[18] + xx[11], 14);

				if ((Q[19] & 0x20000) != 0) {
					Q[11] ^= 0x8;
					T = RR(Q[11] - Q[10], 17);
					if ((T >> 27) == 0)
						break;
					xx[10] = T - Q[7] - F(Q[10], Q[9], Q[8]) - K[10];
					xx[11] = RR(Q[12] - Q[11], 22) - Q[8] - F(Q[11], Q[10], Q[9]) - K[11];
					xx[12] = RR(Q[13] - Q[12], 7) - Q[9] - F(Q[12], Q[11], Q[10]) - K[12];
					xx[13] = RR(Q[14] - Q[13], 12) - Q[10] - F(Q[13], Q[12], Q[11]) - K[13];
					xx[14] = RR(Q[15] - Q[14], 17) - Q[11] - F(Q[14], Q[13], Q[12]) - K[14];
					Q[19] = Q[18] + RL(Q[15] + G(Q[18], Q[17], Q[16]) + K[18] + xx[11], 14);
				}

				if ((Q[19] >> 31) != 0)
					continue;

				// check rest
				xx[0] = RR(Q[1] - B0, 7) - IVA - F(IVB, IVC, IVD) - K[0];
				T = Q[16] + G(Q[19], Q[18], Q[17]) + K[19] + xx[0];
				if ((T >> 29) == 0)
					continue;
				Q[20] = Q[19] + RL(T, 20);
				if (Q[20] >> 31 != 0)
					continue;

				xx[5] = RR(Q[6] - Q[5], 12) - Q[2] - F(Q[5], Q[4], Q[3]) - K[5];
				Q[21] = Q[20] + RL(Q[17] + G(Q[20], Q[19], Q[18]) + K[20] + xx[5], 5);
				if (!bitsequal(Q[21], 17, Q[20]) || Q[21] >> 31 != 0)
					continue;

				xx[10] = RR(Q[11] - Q[10], 17) - Q[7] - F(Q[10], Q[9], Q[8]) - K[10];
				Q[22] = Q[21] + RL(Q[18] + G(Q[21], Q[20], Q[19]) + K[21] + xx[10], 9);
				if (Q[22] >> 31 != 0)
					continue;

				xx[15] = RR(Q[16] - Q[15], 22) - Q[12] - F(Q[15], Q[14], Q[13]) - K[15];
				T = Q[19] + G(Q[22], Q[21], Q[20]) + K[22] + xx[15];
				if ((T & 0x20000) != 0)
					continue; // p = 1/2

				Q[23] = Q[22] + RL(T, 14);
				if (Q[23] >> 31 != 0)
					continue;

				xx[4] = RR(Q[5] - Q[4], 7) - Q[1] - F(Q[4], Q[3], Q[2]) - K[4];
				Q[24] = Q[23] + RL(Q[20] + G(Q[23], Q[22], Q[21]) + K[23] + xx[4], 20);
				if ((Q[24] >> 31) == 0)
					continue;

				xx[2] = RR(Q[3] - Q[2], 17) - C0 - F(Q[2], Q[1], B0) - K[2];
				xx[3] = RR(Q[4] - Q[3], 22) - B0 - F(Q[3], Q[2], Q[1]) - K[3];
				xx[7] = RR(Q[8] - Q[7], 22) - Q[4] - F(Q[7], Q[6], Q[5]) - K[7];
				xx[8] = RR(Q[9] - Q[8], 7) - Q[5] - F(Q[8], Q[7], Q[6]) - K[8];
				xx[9] = RR(Q[10] - Q[9], 12) - Q[6] - F(Q[9], Q[8], Q[7]) - K[9];
				xx[12] = RR(Q[13] - Q[12], 7) - Q[9] - F(Q[12], Q[11], Q[10]) - K[12];
				xx[13] = RR(Q[14] - Q[13], 12) - Q[10] - F(Q[13], Q[12], Q[11]) - K[13];
				xx[14] = RR(Q[15] - Q[14], 17) - Q[11] - F(Q[14], Q[13], Q[12]) - K[14];

				Q[25] = Q[24] + RL(Q[21] + G(Q[24], Q[23], Q[22]) + K[24] + xx[9], 5);
				Q[26] = Q[25] + RL(Q[22] + G(Q[25], Q[24], Q[23]) + K[25] + xx[14], 9);
				Q[27] = Q[26] + RL(Q[23] + G(Q[26], Q[25], Q[24]) + K[26] + xx[3], 14);
				Q[28] = Q[27] + RL(Q[24] + G(Q[27], Q[26], Q[25]) + K[27] + xx[8], 20);
				Q[29] = Q[28] + RL(Q[25] + G(Q[28], Q[27], Q[26]) + K[28] + xx[13], 5);
				Q[30] = Q[29] + RL(Q[26] + G(Q[29], Q[28], Q[27]) + K[29] + xx[2], 9);
				Q[31] = Q[30] + RL(Q[27] + G(Q[30], Q[29], Q[28]) + K[30] + xx[7], 14);
				Q[32] = Q[31] + RL(Q[28] + G(Q[31], Q[30], Q[29]) + K[31] + xx[12], 20);
				Q[33] = Q[32] + RL(Q[29] + H(Q[32], Q[31], Q[30]) + K[32] + xx[5], 4);
				Q[34] = Q[33] + RL(Q[30] + H(Q[33], Q[32], Q[31]) + K[33] + xx[8], 11);

				// Step 34 T-check
				T = Q[31] + H(Q[34], Q[33], Q[32]) + K[34] + xx[11];
				if ((T & 0x8000) == 0)
					continue; // p = 1/2

				Q[35] = Q[34] + RL(T, 16);
				Q[36] = Q[35] + RL(Q[32] + H(Q[35], Q[34], Q[33]) + K[35] + xx[14], 23);

				Q[37] = Q[36] + RL(Q[33] + H(Q[36], Q[35], Q[34]) + K[36] + xx[1], 4);
				Q[38] = Q[37] + RL(Q[34] + H(Q[37], Q[36], Q[35]) + K[37] + xx[4], 11);
				Q[39] = Q[38] + RL(Q[35] + H(Q[38], Q[37], Q[36]) + K[38] + xx[7], 16);
				Q[40] = Q[39] + RL(Q[36] + H(Q[39], Q[38], Q[37]) + K[39] + xx[10], 23);

				Q[41] = Q[40] + RL(Q[37] + H(Q[40], Q[39], Q[38]) + K[40] + xx[13], 4);
				Q[42] = Q[41] + RL(Q[38] + H(Q[41], Q[40], Q[39]) + K[41] + xx[0], 11);
				Q[43] = Q[42] + RL(Q[39] + H(Q[42], Q[41], Q[40]) + K[42] + xx[3], 16);
				Q[44] = Q[43] + RL(Q[40] + H(Q[43], Q[42], Q[41]) + K[43] + xx[6], 23);

				Q[45] = Q[44] + RL(Q[41] + H(Q[44], Q[43], Q[42]) + K[44] + xx[9], 4);
				Q[46] = Q[45] + RL(Q[42] + H(Q[45], Q[44], Q[43]) + K[45] + xx[12], 11);
				Q[47] = Q[46] + RL(Q[43] + H(Q[46], Q[45], Q[44]) + K[46] + xx[15], 16);
				Q[48] = Q[47] + RL(Q[44] + H(Q[47], Q[46], Q[45]) + K[47] + xx[2], 23);
				if (((Q[48] ^ Q[46]) & 0x80000000) != 0)
					continue;

				Q[49] = Q[48] + RL(Q[45] + I(Q[48], Q[47], Q[46]) + K[48] + xx[0], 6);
				if (((Q[49] ^ Q[47]) & 0x80000000) != 0)
					continue;

				Q[50] = Q[49] + RL(Q[46] + I(Q[49], Q[48], Q[47]) + K[49] + xx[7], 10);
				if (((~Q[50] ^ Q[46]) & 0x80000000) != 0)
					continue;

				Q[51] = Q[50] + RL(Q[47] + I(Q[50], Q[49], Q[48]) + K[50] + xx[14], 15);
				if (((Q[51] ^ Q[49]) & 0x80000000) != 0)
					continue;

				Q[52] = Q[51] + RL(Q[48] + I(Q[51], Q[50], Q[49]) + K[51] + xx[5], 21);
				if (((Q[52] ^ Q[50]) & 0x80000000) != 0)
					continue;

				Q[53] = Q[52] + RL(Q[49] + I(Q[52], Q[51], Q[50]) + K[52] + xx[12], 6);
				if (((Q[53] ^ Q[51]) & 0x80000000) != 0)
					continue;

				Q[54] = Q[53] + RL(Q[50] + I(Q[53], Q[52], Q[51]) + K[53] + xx[3], 10);
				if (((Q[54] ^ Q[52]) & 0x80000000) != 0)
					continue;

				Q[55] = Q[54] + RL(Q[51] + I(Q[54], Q[53], Q[52]) + K[54] + xx[10], 15);
				if (((Q[55] ^ Q[53]) & 0x80000000) != 0)
					continue;

				Q[56] = Q[55] + RL(Q[52] + I(Q[55], Q[54], Q[53]) + K[55] + xx[1], 21);
				if (((Q[56] ^ Q[54]) & 0x80000000) != 0)
					continue;

				Q[57] = Q[56] + RL(Q[53] + I(Q[56], Q[55], Q[54]) + K[56] + xx[8], 6);
				if (((Q[57] ^ Q[55]) & 0x80000000) != 0)
					continue;

				Q[58] = Q[57] + RL(Q[54] + I(Q[57], Q[56], Q[55]) + K[57] + xx[15], 10);
				if (((Q[58] ^ Q[56]) & 0x80000000) != 0)
					continue;

				Q[59] = Q[58] + RL(Q[55] + I(Q[58], Q[57], Q[56]) + K[58] + xx[6], 15);
				if (((Q[59] ^ Q[57]) & 0x80000000) != 0)
					continue;

				Q[60] = Q[59] + RL(Q[56] + I(Q[59], Q[58], Q[57]) + K[59] + xx[13], 21);
				if ((Q[60] & 0x2000000) != 0 || ((~Q[60] ^ Q[58]) & 0x80000000) != 0)
					continue;

				Q[61] = Q[60] + RL(Q[57] + I(Q[60], Q[59], Q[58]) + K[60] + xx[4], 6);
				if (((Q[61] & 0x2000000)) == 0 || ((Q[61] ^ Q[59]) & 0x80000000) != 0)
					continue;

				T = Q[58] + I(Q[61], Q[60], Q[59]) + K[61] + xx[11];
				if ((T & 0x3f8000) == 0)
					continue;

				Q[62] = Q[61] + RL(T, 10);
				if ((Q[62] & 0x2000000) == 0 || ((Q[62] ^ Q[60]) & 0x80000000) != 0)
					continue;

				System.out.print(">> ");

				Q[63] = Q[62] + RL(Q[59] + I(Q[62], Q[61], Q[60]) + K[62] + xx[2], 15);
				if (((Q[63] ^ Q[61]) & 0x80000000) != 0)
					continue;

				if ((Q[63] & 0x2000000) == 0) {
					T = Q[63] >> 26;
					T2 = Q[61] >> 26;
					if (T == 0)
						continue;

					while ((T & 1) == 0) {
						if ((T2 & 1) != 0)
							break;
						T >>= 1;
						T2 >>= 1;
					}
					if ((T & 1) == 0 || (T2 & 1) != 0)
						continue;
				}
				Q[64] = Q[63] + RL(Q[60] + I(Q[63], Q[62], Q[61]) + K[63] + xx[9], 21);

				A1 = IVA + Q[61];
				D1 = IVD + Q[62];
				C1 = IVC + Q[63];
				B1 = IVB + Q[64];

				for (int j = 0; j < 16; j++) {
					Hx[j] = x[j];
					Hxx[j] = xx[j];
				}
				Hx[4] = x[4] + 0x80000000;
				Hx[11] = x[11] + 0x00008000;
				Hx[14] = x[14] + 0x80000000;
				Hxx[4] = xx[4] - 0x80000000;
				Hxx[11] = xx[11] - 0x00008000;
				Hxx[14] = xx[14] - 0x80000000;

				return 1;
			}

		}

	}

	public static void main(String[] args) {
		WangCol t = new WangCol();
//		t.X = 8888;

//		t.block1();
//		t.block2();
//		System.out.println("\r\n" + t.A0 + " " + t.B0 + " " + t.C0 + " " + t.D0);
//		System.out.println("\r\n" + t.A1 + " " + t.B1 + " " + t.C1 + " " + t.D1);

		Scanner scanner = new Scanner(System.in);
		char IV_flag;

		System.out.print("Do you want to change the initial IHV? [y/n]: ");
		IV_flag = scanner.next().charAt(0);

		if (IV_flag == 'y') {
			System.out.print("Input a new initial IV_0: ");
			t.A = scanner.nextInt();
			System.out.print("Input a new initial IV_1: ");
			t.B = scanner.nextInt();
			System.out.print("Input a new initial IV_2: ");
			t.C = scanner.nextInt();
			System.out.print("Input a new initial IV_3: ");
			t.D = scanner.nextInt();
		} else {
			System.out.print("It will use the default IHVs: ");
			System.out.print(Integer.toHexString(t.A) + " " + Integer.toHexString(t.B) + " " + Integer.toHexString(t.C)
					+ " " + Integer.toHexString(t.D));
		}

		System.out.println();
		System.out.print("Input an integer as the random seed: ");
		t.X = scanner.nextInt();
		System.out.println();

		scanner.close();

		System.out.println("Block 1 Started");
		long blockStart = System.currentTimeMillis();
		t.block1();
		long blockEnd = System.currentTimeMillis();
		long Timer1 = blockEnd - blockStart;
		System.out.println("\r\nBlock 1 Finished");
		System.out.println("Time for the first block:" + Timer1 / 1000 + "sec");

		System.out.println("Block 2 Started");
		blockStart = System.currentTimeMillis();
		t.block2();
		blockEnd = System.currentTimeMillis();
		long Timer2 = blockEnd - blockStart;
		System.out.println("\r\nBlock 2 Finished");
		System.out.println("Time for the second block:" + Timer2 / 1000 + "sec");

		System.out.println("Total Time:" + (Timer1 + Timer2) / 1000 + "sec");

		String message1 = "";
		String message2 = "";
		String hash = toHex(t.A1) + toHex(t.B1) + toHex(t.C1) + toHex(t.D1);
		for (int i = 0; i < 32; i++) {
			if (i < 16) {
				message1 += "0x" + toHex((t.x[i])) + "\t";
				message2 += "0x" + toHex((t.Hx[i])) + "\t";
			} else {
				message1 += "0x" + toHex((t.xx[i - 16])) + "\t";
				message2 += "0x" + toHex((t.Hxx[i - 16])) + "\t";
			}
			if ((i + 1) % 4 == 0) {
				message1 += "\r\n";
				message2 += "\r\n";
			}
		}

		System.out.println("\n----------------------Collision Found!----------------------\n");

		System.out.println("M1:\n" + message1);
		System.out.println("M2:\n" + message2);
		System.out.println("Hash:\n" + hash);

	}

}
