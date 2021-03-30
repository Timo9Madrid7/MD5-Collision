import numpy as np


def inverse(nu):
    if type(nu) == int:
        if nu == 1:
            return 0
        else:
            return 1
    else:
        if nu == '1':
            return '0'
        else:
            return '1'


def int32Control(x: int):
    """
    overflow control
    """
    if x > 2147483647:
        return -2147483648 + (x - 0x7fffffff) - 1
    elif x < -2147483648:
        return 2147483647 - (-2147483648 - x) + 1
    else:
        return x


def trans_10_to_2(n):
    n = int32Control(n)
    n = n & 0xffffffff
    output = bin(n)[2:]
    while len(output) != 32:
        output = '0' + output
    return list(output)


def trans_10_to_16(n):
    n = int32Control(n)
    n = n & 0xffffffff
    return hex(n)[2:]


def trans_32_16_to_10(x):
    # hex = "8aa04030"
    x = '0' * (32 - len(bin(int(x, 16))[2:])) + bin(int(x, 16))[2:]
    head = x[0]
    body = x[1:]
    if head == '1':
        y = -2 ** 31 + int(body, 2)
    else:
        y = int(body, 2)
    return int32Control(y)


def trans_32_16_to_2(x):
    return trans_10_to_2(trans_32_16_to_10(x))


def trans_2_to_10(bin_list):
    bit_num = ''
    n = 0
    if bin_list[0] == '0':
        bin_list = bin_list[1:]
        while n < len(bin_list):
            bit_num += str(bin_list[n])
            n += 1
        bit_int = int(bit_num, 2)
    else:
        bin_list = bin_list[1:]
        while n < len(bin_list):
            bit_num += str(bin_list[n])
            n += 1
        bit_int = -2 ** 31 + int(bit_num, 2)
    return int32Control(bit_int)


def trans_2_to_16(bin_list):
    return trans_10_to_16((trans_2_to_10(bin_list)))


def rl(input_int, rc):
    bin_list = trans_10_to_2(input_int)
    bin_list = bin_list[rc % len(bin_list):] + bin_list[:rc % len(bin_list)]
    return trans_2_to_10(bin_list)


#
def rr(input_int, rc):
    bin_list = trans_10_to_2(input_int)
    bin_list = bin_list[-(rc % len(bin_list)):] + bin_list[:-(rc % len(bin_list))]
    # print(bin_list)
    return trans_2_to_10(bin_list)


def RC(t7: int):
    assert (t7 < 64)
    if t7 >= 0 and t7 < 16:
        if t7 % 4 == 0:
            return 7
        elif t7 % 4 == 1:
            return 12
        elif t7 % 4 == 2:
            return 17
        else:
            return 22
    elif t7 >= 16 and t7 < 32:
        if t7 % 4 == 0:
            return 5
        elif t7 % 4 == 1:
            return 9
        elif t7 % 4 == 2:
            return 14
        else:
            return 20
    elif t7 >= 32 and t7 < 48:
        if t7 % 4 == 0:
            return 4
        elif t7 % 4 == 1:
            return 11
        elif t7 % 4 == 2:
            return 16
        else:
            return 23
    else:
        if t7 % 4 == 0:
            return 6
        elif t7 % 4 == 1:
            return 10
        elif t7 % 4 == 2:
            return 15
        else:
            return 21


def Ft(X, Y, Z, t6: int):
    """
    return the output from the non-linear function
    """
    assert (t6 < 64)
    if 0 <= t6 < 16:
        return int32Control((X & Y) ^ ((~X) & Z))
    elif 16 <= t6 < 32:
        return int32Control((Z & X) ^ ((~Z) & Y))
    elif 32 <= t6 < 48:
        return int32Control(X ^ Y ^ Z)
    else:
        return int32Control(Y ^ (X | (~Z)))


def compress_2_to_string(compress_input):
    input1 = compress_input
    for i in range(len(input1)):
        input1[i] = str(input1[i])
    return input1


def gen_require_bit(x_1: str, n_1, n_2, q_2_block):
    if x_1 == '0':
        return '0'
    elif x_1 == '1':
        return '1'
    elif x_1 == '.':
        return str(np.random.randint(0, 2))
    elif x_1 == '!':
        return inverse(q_2_block[n_1-2][n_2])
    else:
        return q_2_block[n_1-2][n_2]


def gen_random_1(Q_block_2_in):
    Q_block_1_list = []
    for i in range(32):
        Q_block_1_list.append(str(np.random.randint(0, 2)))
    for i in [0, 1, 2, 3, 11, 12, 13, 14, 19, 24]:
        Q_block_1_list[i] = Q_block_2_in[1][i]
    for i in [5, 10, 25]:
        Q_block_1_list[i] = '1'
    for i in [4, 6, 15, 20, 26]:
        Q_block_1_list[i] = '0'
    return Q_block_1_list


def block_2_step_1(block_1_0_bin):
    Q_2 = []
    Q_2_1 = []
    for i in range(32):
        Q_2_1.append(str(np.random.randint(0, 2)))
    Q_2_1[0] = inverse(block_1_0_bin[0])
    Q_2.append(Q_2_1)
    Q_2_2 = '^^^^110...0^^^^01..^1...^10..00.'
    Q_2_2_list = []
    for i in range(len(Q_2_2)):
        Q_2_2_list.append(gen_require_bit(Q_2_2[i], 2, i, Q_2))
    Q_2.append(Q_2_2_list)
    Q_2_3 = '^011111...0111110..01..1011^^11.'
    Q_2_3_list = []
    for i in range(len(Q_2_3)):
        Q_2_3_list.append(gen_require_bit(Q_2_3[i], 3, i, Q_2))
    Q_2.append(Q_2_3_list)
    Q_2_4 = '^011101...000100...00^^00001000^'
    Q_2_4_list = []
    for i in range(len(Q_2_4)):
        Q_2_4_list.append(gen_require_bit(Q_2_4[i], 4, i, Q_2))
    Q_2.append(Q_2_4_list)
    Q_2_5 = '!10010....101111...0111001010000'
    Q_2_5_list = []
    for i in range(len(Q_2_5)):
        Q_2_5_list.append(gen_require_bit(Q_2_5[i], 5, i, Q_2))
    Q_2.append(Q_2_5_list)
    Q_2_6 = '^..0010.1.10..1011.0110001010110'
    Q_2_6_list = []
    for i in range(len(Q_2_6)):
        Q_2_6_list.append(gen_require_bit(Q_2_6[i], 6, i, Q_2))
    Q_2.append(Q_2_6_list)
    Q_2_7 = '!..1011^1.00..0110.1111000.....1'
    Q_2_7_list = []
    for i in range(len(Q_2_7)):
        Q_2_7_list.append(gen_require_bit(Q_2_7[i], 7, i, Q_2))
    Q_2.append(Q_2_7_list)
    Q_2_8 = '^..001000.11..101.....11111...^0'
    Q_2_8_list = []
    for i in range(len(Q_2_8)):
        Q_2_8_list.append(gen_require_bit(Q_2_8[i], 8, i, Q_2))
    Q_2.append(Q_2_8_list)
    Q_2_9 = '^..111000.....010..^..01110...01'
    Q_2_9_list = []
    for i in range(len(Q_2_9)):
        Q_2_9_list.append(gen_require_bit(Q_2_9[i], 9, i, Q_2))
    Q_2.append(Q_2_9_list)
    Q_2_10 = '^....1111...101111001.1111....00'
    Q_2_10_list = []
    for i in range(len(Q_2_10)):
        Q_2_10_list.append(gen_require_bit(Q_2_10[i], 10, i, Q_2))
    Q_2.append(Q_2_10_list)
    Q_2_11 = '^..00.......110111000.11110...11'
    Q_2_11_list = []
    for i in range(len(Q_2_11)):
        Q_2_11_list.append(gen_require_bit(Q_2_11[i], 11, i, Q_2))
    Q_2.append(Q_2_11_list)
    Q_2_12 = '^^^00^^^....10000001....1.......'
    Q_2_12_list = []
    for i in range(len(Q_2_12)):
        Q_2_12_list.append(gen_require_bit(Q_2_12[i], 12, i, Q_2))
    Q_2.append(Q_2_12_list)
    Q_2_13 = '!01111110...1111111.....0...1...'
    Q_2_13_list = []
    for i in range(len(Q_2_13)):
        Q_2_13_list.append(gen_require_bit(Q_2_13[i], 13, i, Q_2))
    Q_2.append(Q_2_13_list)
    Q_2_14 = '^10000001...1011111.....1...1...'
    Q_2_14_list = []
    for i in range(len(Q_2_14)):
        Q_2_14_list.append(gen_require_bit(Q_2_14[i], 14, i, Q_2))
    Q_2.append(Q_2_14_list)
    Q_2_15 = '01111101........00..........0...'
    Q_2_15_list = []
    for i in range(len(Q_2_15)):
        Q_2_15_list.append(gen_require_bit(Q_2_15[i], 15, i, Q_2))
    Q_2.append(Q_2_15_list)
    Q_2_16 = '0.10..........!.................'
    Q_2_16_list = []
    for i in range(len(Q_2_16)):
        Q_2_16_list.append(gen_require_bit(Q_2_16[i], 16, i, Q_2))
    Q_2.append(Q_2_16_list)
    return Q_2


#
#
def step_1():
    # print('----------------------------------------------------------------------------------')
    Q_out = []
    Q_1 = []
    Q_2 = []
    # Q_3 = []
    # Q_4 = []
    for i in range(32):
        Q_1.append(str(np.random.randint(0, 2)))
    Q_out.append(Q_1)
    for i in range(32):
        Q_2.append(str(np.random.randint(0, 2)))
    Q_out.append(Q_2)
    Q_3 = '............0.......0....0......'
    Q_3_list = []
    for i in range(len(Q_3)):
        Q_3_list.append(gen_require_bit(Q_3[i], 3, i, Q_out))
    Q_out.append(Q_3_list)
    Q_4 = '1.......0^^^1^^^^^^^1^^^^011....'
    Q_4_list = []
    for i in range(len(Q_4)):
        Q_4_list.append(gen_require_bit(Q_4[i], 4, i, Q_out))
    Q_out.append(Q_4_list)
    Q_5 = '1000100.01..0000000000000010.1.1'
    Q_5_list = []
    for i in range(len(Q_5)):
        Q_5_list.append(gen_require_bit(Q_5[i], 5, i, Q_out))
    Q_out.append(Q_5_list)
    Q_6 = '0000001^01111111101111000100^0^1'
    Q_6_list = []
    for i in range(len(Q_6)):
        Q_6_list.append(gen_require_bit(Q_6[i], 6, i, Q_out))
    Q_out.append(Q_6_list)
    Q_7 = '00000011111111101111100000100000'
    Q_7_list = []
    for i in range(len(Q_7)):
        Q_7_list.append(gen_require_bit(Q_7[i], 7, i, Q_out))
    Q_out.append(Q_7_list)
    Q_8 = '000000011..100010.0.010101000000'
    Q_8_list = []
    for i in range(len(Q_8)):
        Q_8_list.append(gen_require_bit(Q_8[i], 8, i, Q_out))
    Q_out.append(Q_8_list)
    Q_9 = '11111011...100000.1^111100111101'
    Q_9_list = []
    for i in range(len(Q_9)):
        Q_9_list.append(gen_require_bit(Q_9[i], 9, i, Q_out))
    Q_out.append(Q_9_list)
    Q_10 = '0111....0..111111101...001....00'
    Q_10_list = []
    for i in range(len(Q_10)):
        Q_10_list.append(gen_require_bit(Q_10[i], 10, i, Q_out))
    Q_out.append(Q_10_list)
    Q_11 = '001000001...00011100000011000010'
    Q_11_list = []
    for i in range(len(Q_11)):
        Q_11_list.append(gen_require_bit(Q_11[i], 11, i, Q_out))
    Q_out.append(Q_11_list)
    Q_12 = '000...00....10000001...10.......'
    Q_12_list = []
    for i in range(len(Q_12)):
        Q_12_list.append(gen_require_bit(Q_12[i], 12, i, Q_out))
    Q_out.append(Q_12_list)
    Q_13 = '01....01....1111111....00...1...'
    Q_13_list = []
    for i in range(len(Q_13)):
        Q_13_list.append(gen_require_bit(Q_13[i], 13, i, Q_out))
    Q_out.append(Q_13_list)
    Q_14 = '0.0...00....1011111....11...1...'
    Q_14_list = []
    for i in range(len(Q_14)):
        Q_14_list.append(gen_require_bit(Q_14[i], 14, i, Q_out))
    Q_out.append(Q_14_list)
    Q_15 = '0.1...01.......01...........0...'
    Q_15_list = []
    for i in range(len(Q_15)):
        Q_15_list.append(gen_require_bit(Q_15[i], 15, i, Q_out))
    Q_out.append(Q_15_list)
    Q_16 = '0!1...........!.................'
    Q_16_list = []
    for i in range(len(Q_16)):
        Q_16_list.append(gen_require_bit(Q_16[i], 16, i, Q_out))
    Q_out.append(Q_16_list)
    # for i in range(32):
    #     if i in [12, 20, 25]:
    #         Q_3.append(0)
    #     else:
    #         Q_3.append(np.random.randint(0, 2))
    # for i in range(32):
    #     if i in [0, 12, 20, 26, 27]:
    #         Q_4.append(1)
    #     else:
    #         if i in [8, 25]:
    #             Q_4.append(0)
    #         else:
    #             Q_4.append(np.random.randint(0, 2))
    # Q_4[9:12] = Q_3[9:12].copy()
    # Q_4[13:20] = Q_3[13:20].copy()
    # Q_4[21:25] = Q_3[21:25].copy()
    # Q_5 = [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    # for i in [7, 10, 11, 28, 30]:
    #     Q_5[i] = np.random.randint(0, 2)
    # Q_6 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
    # for i in [7, 28, 30]:
    #     Q_6[i] = Q_5[i]
    # Q_7 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    # Q_8 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    # for i in [9, 10, 17, 19]:
    #     Q_8[i] = np.random.randint(0, 2)
    # Q_9 = [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1]
    # for i in [8, 9, 10, 17]:
    #     Q_9[i] = np.random.randint(0, 2)
    # Q_9[19] = Q_8[19]
    # Q_10 = [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    # for i in [4, 5, 6, 7, 9, 10, 20, 21, 22, 26, 27, 28, 29]:
    #     Q_10[i] = np.random.randint(0, 2)
    # Q_11 = [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0]
    # for i in [9, 10, 11]:
    #     Q_11[i] = np.random.randint(0, 2)
    # Q_12 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    # for i in [3, 4, 5, 8, 9, 10, 11, 20, 21, 22, 25, 26, 27, 28, 29, 30, 31]:
    #     Q_12[i] = np.random.randint(0, 2)
    # Q_13 = [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    # for i in [2, 3, 4, 5, 8, 9, 10, 11, 19, 20, 21, 22, 25, 26, 27, 29, 30, 31]:
    #     Q_13[i] = np.random.randint(0, 2)
    # Q_14 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0]
    # for i in [1, 3, 4, 5, 8, 9, 10, 11, 19, 20, 21, 22, 25, 26, 27, 29, 30, 31]:
    #     Q_14[i] = np.random.randint(0, 2)
    # Q_15 = []
    # for i in range(32):
    #     if i in [0, 6, 15, 28]:
    #         Q_15.append(0)
    #     else:
    #         if i in [2, 7, 16]:
    #             Q_15.append(1)
    #         else:
    #             Q_15.append(np.random.randint(0, 2))
    # # print(Q_15)
    # Q_16 = []
    # for i in range(32):
    #     if i == 0:
    #         Q_16.append(0)
    #     else:
    #         if i == 2:
    #             Q_16.append(1)
    #         else:
    #             if i in [1, 14]:
    #                 # print(Q_15[i])
    #                 # print(inverse(Q_15[i]))
    #                 Q_16.append(inverse(Q_15[i]))
    #             else:
    #                 Q_16.append(np.random.randint(0, 2))
    # print(Q_15)
    # Q = [Q_1, Q_2, Q_3, Q_4, Q_5, Q_6, Q_7, Q_8, Q_9, Q_10, Q_11, Q_12, Q_13, Q_14, Q_15, Q_16]
    # for small in Q:
    #     small = compress_2_to_string(small)
    return Q_out


#
#
def AC(t5: int):
    """
    return the decimal Addition Constant ACt for each step
    """
    assert (t5 < 64)
    from math import sin
    return int32Control(int(2 ** 32 * abs(sin(1 + t5))))


#
#
def get_message(t1, q__3, q__2, q__1, q, q_1):
    message1 = rr(q_1 - q, RC(t1)) - Ft(q, q__1, q__2, t1) - q__3 - AC(t1)
    if type(message1) != int:
        print('type error')
    else:
        pass
    return int32Control(message1)


def gen_random_17(Q_17_in):
    Q_17 = '0!............0.^...........^...'
    Q_17_list = []
    for i in range(len(Q_17)):
        Q_17_list.append(gen_require_bit(Q_17[i], 17, i, Q_17_in))
    return Q_17_list
    # Q_17 = []
    # for i in range(32):
    #     Q_17.append(str(np.random.randint(0, 2)))
    # for i in [0, 14]:
    #     Q_17[i] = '0'
    # Q_17[1] = inverse(Q_17_in[15][1])
    # for i in [16, 28]:
    #     Q_17[i] = Q_17_in[15][i]
    # return Q_17


def gen_random_9_and_10(q_9_10):
    Q_9 = '11111011...100000.1^111100111101'
    Q_9_list = []
    for i in range(len(Q_9)):
        Q_9_list.append(gen_require_bit(Q_9[i], 9, i, q_9_10))
    Q_10 = '0111....0..111111101...001....00'
    Q_10_list = []
    for i in range(len(Q_10)):
        Q_10_list.append(gen_require_bit(Q_10[i], 10, i, q_9_10))
    return Q_9_list, Q_10_list
    # Q_9 = ['1', '1', '1', '1', '1', '0', '1', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1', '0', '1', '1',
    #        '1', '1', '0', '0', '1', '1', '1', '1', '0', '1']
    # for i in [8, 9, 10, 17]:
    #     Q_9[i] = str(np.random.randint(0, 2))
    # Q_9[19] = q_9_10[7][19]
    # Q_10 = ['0', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '0',
    #         '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0']
    # for i in [4, 5, 6, 7, 9, 10, 20, 21, 22, 26, 27, 28, 29]:
    #     Q_10[i] = str(np.random.randint(0, 2))
    # return Q_9, Q_10


def gen_random_block2_9_and_10(q_block2_9_10):
    Q_9_block_2 = '^..111000.....010..^..01110...01'
    Q_10_block_2 = '^....1111...101111001.1111....00'
    Q_9_block_2_list = []
    for i in range(len(Q_9_block_2)):
        Q_9_block_2_list.append(gen_require_bit(Q_9_block_2[i], 9, i, q_block2_9_10))
    Q_10_block_2_list = []
    for i in range(len(Q_10_block_2)):
        Q_10_block_2_list.append(gen_require_bit(Q_10_block_2[i], 10, i, q_block2_9_10))
    return Q_9_block_2_list, Q_10_block_2_list




def Wt(message2, t2):
    """
    return the word for each step
    """
    m_list = message2
    if 0 <= t2 < 16: return trans_32_16_to_10(m_list[t2])
    if 16 <= t2 < 32: return trans_32_16_to_10(m_list[(1 + 5 * t2) % 16])
    if 32 <= t2 < 48: return trans_32_16_to_10(m_list[(5 + 3 * t2) % 16])
    if 48 <= t2 < 64: return trans_32_16_to_10(m_list[(7 * t2) % 16])


def get_Q_next(t3, q__3, q__2, q__1, q, message3):
    if type((Ft(q, q__1, q__2, t3) + q__3 + AC(t3) + Wt(message3, t3))) != int:
        print('type error 2')
    else:
        pass
    Q_next = q + rl((Ft(q, q__1, q__2, t3) + q__3 + AC(t3) + Wt(message3, t3)), RC(t3))
    if type(Q_next) != int:
        print('type error')
    else:
        pass
    # print(trans_10_to_16(Wt(message3, t3)))
    return int32Control(Q_next)


def get_T(t4, q__3, q__2, q__1, q, message4):
    T = Ft(q, q__1, q__2, t4) + q__3 + AC(t4) + Wt(message4, t4)
    return int32Control(T)


# block one #
while True:
    Q = []
    message = []
    Q = step_1().copy()
    # for i in Q:
    #     print(i)
    # print(Q[14][1])
    # print(Q[14][14])
    # print(Q[15][1])
    # print(Q[15][14])
    Q_ten = []
    for i in range(16):
        Q_ten.append(trans_2_to_10(Q[i]))
    Q0 = '0x67452301'  # -------------a-----------------Q-3-------------------#
    Q1 = '0xefcdab89'  # -------------b-----------------Q_0-------------------#
    Q2 = '0x98badcfe'  # -------------c-----------------Q-1-------------------#
    Q3 = '0x10325476'  # -------------d-----------------Q-2-------------------#
    Q0_dec = trans_32_16_to_10((Q0[2:]))
    Q1_dec = trans_32_16_to_10((Q1[2:]))
    Q2_dec = trans_32_16_to_10((Q2[2:]))
    Q3_dec = trans_32_16_to_10((Q3[2:]))
    m_0 = get_message(0, Q0_dec, Q3_dec, Q2_dec, Q1_dec, Q_ten[0])
    message.append(trans_10_to_16(m_0))
    for i in range(5):
        message.append('ffffffff')
    for t in range(10):
        m = get_message(6 + t, Q_ten[2 + t], Q_ten[3 + t], Q_ten[4 + t], Q_ten[5 + t], Q_ten[6 + t])
        message.append(trans_10_to_16(m))
    # for i in message:
    #     print(i)
    #     print(trans_32_16_to_2(i))
    for i in range(48):
        # Q.append(['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'])
        Q_ten.append(0)
        counter = 0
    while counter < 100:
        counter = counter + 1
        q_17 = gen_random_17(Q)
        q_17 = trans_2_to_10(q_17)
        Q_ten[16] = q_17
        q_17_bin = trans_10_to_2(Q_ten[16])
        if q_17_bin[0] != '0' or q_17_bin[1] == Q[15][1] or q_17_bin[14] != '0' or q_17_bin[16] != Q[15][16] or \
                q_17_bin[28] != Q[15][28]:
            # print('step one failed')
            continue
        else:
            pass
        Q_ten[17] = get_Q_next(17, Q_ten[13], Q_ten[14], Q_ten[15], Q_ten[16], message)
        q_18_bin = trans_10_to_2(Q_ten[17])
        if q_18_bin[0] != '0' or q_18_bin[2] != q_17_bin[2] or q_18_bin[14] != '1':
            # print('step two failed')
            continue
        else:
            pass
        Q_ten[18] = get_Q_next(18, Q_ten[14], Q_ten[15], Q_ten[16], Q_ten[17], message)
        q_19_bin = trans_10_to_2(Q_ten[18])
        if q_19_bin[0] != '0' or q_19_bin[14] != '0':
            # print('step three failed')
            continue
        else:
            pass
        Q_ten[19] = get_Q_next(19, Q_ten[15], Q_ten[16], Q_ten[17], Q_ten[18], message)
        q_20_bin = trans_10_to_2(Q_ten[19])
        if q_20_bin[0] != '0' or q_20_bin[13] == q_19_bin[13]:
            # print('step four failed')
            continue
        else:
            pass
        m_1 = get_message(16, Q_ten[12], Q_ten[13], Q_ten[14], Q_ten[15], q_17)
        message[1] = trans_10_to_16(m_1)
        Q_ten[1] = get_Q_next(1, Q3_dec, Q2_dec, Q1_dec, Q_ten[0], message)
        m_2 = get_message(2, Q2_dec, Q1_dec, Q_ten[0], Q_ten[1], Q_ten[2])
        message[2] = trans_10_to_16(m_2)
        m_3 = get_message(3, Q1_dec, Q_ten[0], Q_ten[1], Q_ten[2], Q_ten[3])
        message[3] = trans_10_to_16(m_3)
        m_4 = get_message(4, Q_ten[0], Q_ten[1], Q_ten[2], Q_ten[3], Q_ten[4])
        message[4] = trans_10_to_16(m_4)
        m_5 = get_message(5, Q_ten[1], Q_ten[2], Q_ten[3], Q_ten[4], Q_ten[5])
        message[5] = trans_10_to_16(m_5)
        Q_ten[20] = get_Q_next(20, Q_ten[16], Q_ten[17], Q_ten[18], Q_ten[19], message)
        q_21_bin = trans_10_to_2(Q_ten[20])
        if q_21_bin[0] != '0' or q_21_bin[14] != q_20_bin[14]:
            # print('step five failed')
            continue
        else:
            counter = 0
            break
    if counter != 0:
        continue
    else:
        pass
    last_new_qs_60_bin = []
    timer2 = 0
    while timer2 < 1000:
        timer2 = timer2 + 1
        while True:
            new_q_9, new_q_10 = gen_random_9_and_10(Q)
            new_q_9 = trans_2_to_10(new_q_9)
            new_q_10 = trans_2_to_10(new_q_10)
            new_m_11 = get_message(11, Q_ten[7], new_q_9, new_q_10, Q_ten[10], Q_ten[11])
            if trans_10_to_16(new_m_11) != message[11]:
                # print('one Q9 Q10 failed, try another one')
                continue
            else:
                break
        new_qs = Q_ten.copy()
        new_qs[8] = new_q_9
        new_qs[9] = new_q_10
        new_message = message.copy()
        for i in [8, 9, 10, 11, 12, 13]:
            # print(type((get_message(i, new_qs[i - 4], new_qs[i - 3], new_qs[i - 2], new_qs[i - 1], new_qs[i]))))
            new_message[i] = trans_10_to_16(
                get_message(i, new_qs[i - 4], new_qs[i - 3], new_qs[i - 2], new_qs[i - 1], new_qs[i]))
        # print(new_qs)
        # print(new_message)
        new_qs[21] = get_Q_next(21, new_qs[17], new_qs[18], new_qs[19], new_qs[20], new_message)
        new_qs_21_bin = trans_10_to_2(new_qs[21])
        if new_qs_21_bin[0] != '0':
            # print(new_qs_21_bin)
            # print('22 unsatisfied')
            continue
        else:
            pass
        T_22_block_1 = get_T(22, new_qs[18], new_qs[19], new_qs[20], new_qs[21], new_message)
        T_22_block_1_bin = trans_10_to_2(T_22_block_1)
        if T_22_block_1_bin[14] != '0':
            # print('T_22 unsatisfied')
            continue
        else:
            pass
        new_qs[22] = get_Q_next(22, new_qs[18], new_qs[19], new_qs[20], new_qs[21], new_message)
        new_qs_22_bin = trans_10_to_2(new_qs[22])
        if new_qs_22_bin[0] != '0':
            # print('23 unsatisfied')
            continue
        else:
            pass
        new_qs[23] = get_Q_next(23, new_qs[19], new_qs[20], new_qs[21], new_qs[22], new_message)
        new_qs_23_bin = trans_10_to_2(new_qs[23])
        if new_qs_23_bin[0] != '1':
            # print(new_qs_23_bin)
            # print('24 unsatisfied')
            continue
        else:
            pass
        for i in range(21):
            new_qs[24 + i] = get_Q_next(24 + i, new_qs[20 + i], new_qs[21 + i], new_qs[22 + i], new_qs[23 + i],
                                        new_message)
        T_34_block_1 = get_T(34, new_qs[30], new_qs[31], new_qs[32], new_qs[33], new_message)
        T_34_block_1_bin = trans_10_to_2(T_34_block_1)
        if T_34_block_1_bin[16] != '0':
            # print('T_34 unsatisfied')
            continue
        else:
            pass
        new_qs[45] = get_Q_next(45, new_qs[41], new_qs[42], new_qs[43], new_qs[44], new_message)
        new_qs_45_bin = trans_10_to_2(new_qs[45])
        new_qs[46] = get_Q_next(46, new_qs[42], new_qs[43], new_qs[44], new_qs[45], new_message)
        new_qs_46_bin = trans_10_to_2(new_qs[46])
        new_qs[47] = get_Q_next(47, new_qs[43], new_qs[44], new_qs[45], new_qs[46], new_message)
        new_qs_47_bin = trans_10_to_2(new_qs[47])
        if new_qs_47_bin[0] != new_qs_45_bin[0]:
            # print(new_qs_45_bin)
            # print(new_qs_47_bin)
            # print('48 unsatisfied')
            continue
        else:
            pass
        new_qs[48] = get_Q_next(48, new_qs[44], new_qs[45], new_qs[46], new_qs[47], new_message)
        new_qs_48_bin = trans_10_to_2(new_qs[48])
        if new_qs_48_bin[0] != new_qs_46_bin[0]:
            # print(new_qs_46_bin)
            # print(new_qs_48_bin)
            # print('49 unsatisfied')
            continue
        else:
            pass
        new_qs[49] = get_Q_next(49, new_qs[45], new_qs[46], new_qs[47], new_qs[48], new_message)
        new_qs_49_bin = trans_10_to_2(new_qs[49])
        if new_qs_49_bin[0] == new_qs_45_bin[0]:
            # print(new_qs_45_bin)
            # print(new_qs_49_bin)
            # print('50 unsatisfied')
            continue
        else:
            pass
        new_qs[50] = get_Q_next(50, new_qs[46], new_qs[47], new_qs[48], new_qs[49], new_message)
        new_qs_50_bin = trans_10_to_2(new_qs[50])
        if new_qs_50_bin[0] != new_qs_48_bin[0]:
            # print(new_qs_48_bin)
            # print(new_qs_50_bin)
            # print('51 unsatisfied')
            continue
        else:
            pass
        new_qs[51] = get_Q_next(51, new_qs[47], new_qs[48], new_qs[49], new_qs[50], new_message)
        new_qs_51_bin = trans_10_to_2(new_qs[51])
        if new_qs_51_bin[0] != new_qs_49_bin[0]:
            # print(new_qs_49_bin)
            # print(new_qs_51_bin)
            # print('52 unsatisfied')
            continue
        else:
            pass
        new_qs[52] = get_Q_next(52, new_qs[48], new_qs[49], new_qs[50], new_qs[51], new_message)
        new_qs_52_bin = trans_10_to_2(new_qs[52])
        if new_qs_52_bin[0] != new_qs_50_bin[0]:
            # print(new_qs_50_bin)
            # print(new_qs_52_bin)
            # print('53 unsatisfied')
            continue
        else:
            pass
        new_qs[53] = get_Q_next(53, new_qs[49], new_qs[50], new_qs[51], new_qs[52], new_message)
        new_qs_53_bin = trans_10_to_2(new_qs[53])
        if new_qs_53_bin[0] != new_qs_51_bin[0]:
            # print(new_qs_51_bin)
            # print(new_qs_53_bin)
            # print('54 unsatisfied')
            continue
        else:
            pass
        new_qs[54] = get_Q_next(54, new_qs[50], new_qs[51], new_qs[52], new_qs[53], new_message)
        new_qs_54_bin = trans_10_to_2(new_qs[54])
        if new_qs_54_bin[0] != new_qs_52_bin[0]:
            # print(new_qs_52_bin)
            # print(new_qs_54_bin)
            # print('55 unsatisfied')
            continue
        else:
            pass
        new_qs[55] = get_Q_next(55, new_qs[51], new_qs[52], new_qs[53], new_qs[54], new_message)
        new_qs_55_bin = trans_10_to_2(new_qs[55])
        if new_qs_55_bin[0] != new_qs_53_bin[0]:
            # print(new_qs_53_bin)
            # print(new_qs_55_bin)
            # print('56 unsatisfied')
            continue
        else:
            pass
        new_qs[56] = get_Q_next(56, new_qs[52], new_qs[53], new_qs[54], new_qs[55], new_message)
        new_qs_56_bin = trans_10_to_2(new_qs[56])
        # print(new_qs[56])
        if new_qs_56_bin[0] != new_qs_54_bin[0]:
            # print(new_qs_54_bin)
            # print(new_qs_56_bin)
            # print('57 unsatisfied')
            continue
        else:
            # print(new_qs[56])
            pass
        new_qs[57] = get_Q_next(57, new_qs[53], new_qs[54], new_qs[55], new_qs[56], new_message)
        new_qs_57_bin = trans_10_to_2(new_qs[57])
        if new_qs_57_bin[0] != new_qs_55_bin[0]:
            # print('58 unsatisfied')
            continue
        else:
            # print(new_qs[57])
            pass
        new_qs[58] = get_Q_next(58, new_qs[54], new_qs[55], new_qs[56], new_qs[57], new_message)
        new_qs_58_bin = trans_10_to_2(new_qs[58])
        if new_qs_58_bin[0] != new_qs_56_bin[0]:
            # print('59 unsatisfied')
            continue
        else:
            # print(new_qs[58])
            pass
        new_qs[59] = get_Q_next(59, new_qs[55], new_qs[56], new_qs[57], new_qs[58], new_message)
        new_qs_59_bin = trans_10_to_2(new_qs[59])
        if new_qs_59_bin[0] != new_qs_47_bin[0]:
            # print('60 unsatisfied')
            continue
        else:
            # print(new_qs[59])
            pass
        new_qs[60] = get_Q_next(60, new_qs[56], new_qs[57], new_qs[58], new_qs[59], new_message)
        new_qs_60_bin = trans_10_to_2(new_qs[60])
        if new_qs_60_bin[0] != new_qs_58_bin[0]:
            # print(new_qs[60])
            print('61 unsatisfied')
            continue
        else:
            # print(new_qs[60])
            pass
        new_qs[61] = get_Q_next(61, new_qs[57], new_qs[58], new_qs[59], new_qs[60], new_message)
        new_qs_61_bin = trans_10_to_2(new_qs[61])
        if new_qs_61_bin[0] != new_qs_59_bin[0]:
            print('62 unsatisfied')
            continue
        else:
            pass
        new_qs[62] = get_Q_next(62, new_qs[58], new_qs[59], new_qs[60], new_qs[61], new_message)
        new_qs_62_bin = trans_10_to_2(new_qs[62])
        if new_qs_62_bin[0] != new_qs_60_bin[0]:
            print('63 unsatisfied')
            continue
        else:
            pass
        print('all satisfied')
        # print(new_qs[59])
        # print(new_qs[60])
        # print(new_qs[61])
        # print(new_qs[62])
        # print(new_message)
        new_qs[63] = get_Q_next(63, new_qs[59], new_qs[60], new_qs[61], new_qs[62], new_message)
        # for i in new_qs:
        #     print(trans_10_to_2(i))
        out_block_0_a = int32Control(Q0_dec + new_qs[60])
        out_block_0_b = int32Control(Q1_dec + new_qs[63])
        out_block_0_c = int32Control(Q2_dec + new_qs[62])
        out_block_0_d = int32Control(Q3_dec + new_qs[61])
        Q_block_1_0 = out_block_0_b
        Q_block_1__1 = out_block_0_c
        Q_block_1__2 = out_block_0_d
        Q_block_1__3 = out_block_0_a
        Q_block_1__3_bin = trans_10_to_2(Q_block_1__3)
        Q_block_1__2_bin = trans_10_to_2(Q_block_1__2)
        if Q_block_1__2_bin[6] != '0':
            print(Q_block_1__2_bin)
            print('step 1 for block 1 failed')
            # timer2 = 0
            continue
        else:
            print(Q_block_1__2_bin)
            print('step 1 for block 1 satisfied')
            pass
        Q_block_1__1_bin = trans_10_to_2(Q_block_1__1)
        if Q_block_1__1_bin[0] != Q_block_1__2_bin[0] or Q_block_1__1_bin[5] != '0' or Q_block_1__1_bin[6] != '1':
            print(Q_block_1__1_bin)
            print('step 2 for block 1 failed')
            # timer2 = 0
            continue
        else:
            print(Q_block_1__1_bin)
            print('step 2 for block 1 satisfied')
            pass
        Q_block_1_0_bin = trans_10_to_2(Q_block_1_0)
        if Q_block_1_0_bin[0] != Q_block_1__1_bin[0] or Q_block_1_0_bin[5] != '0' or Q_block_1_0_bin[6] != '0' or \
                Q_block_1_0_bin[26] != '0':
            print(Q_block_1_0_bin)
            print('step 3 for block 1 failed')
            continue
        else:
            hash_block_1 = trans_10_to_16(out_block_0_a) + trans_10_to_16(out_block_0_b) + trans_10_to_16(
                out_block_0_c) + trans_10_to_16(out_block_0_d)
            print('step 3 for block 1 satisfied')
            print('block 0 found')
            print(new_message)
            print(Q_block_1__3_bin)
            print(Q_block_1__2_bin)
            print(Q_block_1__1_bin)
            print(Q_block_1_0_bin)
            timer2 = 0
            break
    if timer2 != 0:
        continue
    else:
        break
# block 2 #
Q_block_1__3 = trans_2_to_10(Q_block_1__3_bin)
Q_block_1__2 = trans_2_to_10(Q_block_1__2_bin)
Q_block_1__1 = trans_2_to_10(Q_block_1__1_bin)
Q_block_1_0 = trans_2_to_10(Q_block_1_0_bin)
while True:
    Q_block_2 = []
    Q_block_2 = block_2_step_1(Q_block_1_0_bin).copy()
    Q_block_2_ten = []
    for i in Q_block_2:
        Q_block_2_ten.append(trans_2_to_10(i))
    message_block_2 = []
    for i in range(5):
        message_block_2.append('ffffffff')
    for t in range(11):
        m = get_message(5 + t, Q_block_2_ten[1 + t], Q_block_2_ten[2 + t], Q_block_2_ten[3 + t], Q_block_2_ten[4 + t], Q_block_2_ten[5 + t])
        message_block_2.append(trans_10_to_16(m))
    for i in range(48):
        Q_block_2_ten.append(0)
    counter3 = 0
    while counter3 < 100:
        counter3 = counter3 + 1
        Q_block_2[0] = gen_random_1(Q_block_2)
        Q_block_2_ten[0] = trans_2_to_10(Q_block_2[0])
        m_block_2_0 = get_message(0, Q_block_1__3, Q_block_1__2, Q_block_1__1, Q_block_1_0, Q_block_2_ten[0])
        message_block_2[0] = trans_10_to_16(m_block_2_0)
        m_block_2_1 = get_message(1, Q_block_1__2, Q_block_1__1, Q_block_1_0, Q_block_2_ten[0], Q_block_2_ten[1])
        message_block_2[1] = trans_10_to_16(m_block_2_1)
        m_block_2_2 = get_message(2, Q_block_1__1, Q_block_1_0, Q_block_2_ten[0], Q_block_2_ten[1], Q_block_2_ten[2])
        message_block_2[2] = trans_10_to_16(m_block_2_2)
        m_block_2_3 = get_message(3, Q_block_1_0, Q_block_2_ten[0], Q_block_2_ten[1], Q_block_2_ten[2], Q_block_2_ten[3])
        message_block_2[3] = trans_10_to_16(m_block_2_3)
        m_block_2_4 = get_message(4,  Q_block_2_ten[0], Q_block_2_ten[1], Q_block_2_ten[2], Q_block_2_ten[3], Q_block_2_ten[4])
        message_block_2[4] = trans_10_to_16(m_block_2_4)
        Q_block_2_ten[16] = get_Q_next(16, Q_block_2_ten[12], Q_block_2_ten[13], Q_block_2_ten[14], Q_block_2_ten[15], message_block_2)
        Q_block_2_17 = trans_10_to_2(Q_block_2_ten[16])
        if Q_block_2_17[0] != '0' or Q_block_2_17[1] == Q_block_2[15][1] or Q_block_2_17[14] != '0' or Q_block_2_17[16] != Q_block_2[15][16] or Q_block_2_17[28] != Q_block_2[15][28]:
            # print('step one failed')
            continue
        else:
            pass
        Q_block_2_ten[17] = get_Q_next(17, Q_block_2_ten[13], Q_block_2_ten[14], Q_block_2_ten[15], Q_block_2_ten[16], message_block_2)
        Q_block_2_18 = trans_10_to_2(Q_block_2_ten[17])
        if Q_block_2_18[0] != '0' or Q_block_2_18[2] != Q_block_2_17[2] or Q_block_2_18[14] != '1':
            # print('step three failed')
            continue
        else:
            pass
        Q_block_2_ten[18] = get_Q_next(18, Q_block_2_ten[14], Q_block_2_ten[15], Q_block_2_ten[16], Q_block_2_ten[17], message_block_2)
        Q_block_2_19 = trans_10_to_2(Q_block_2_ten[18])
        if Q_block_2_19[0] != '0' or Q_block_2_19[14] != '0':
            # print('step four failed')
            continue
        else:
            pass
        Q_block_2_ten[19] = get_Q_next(19, Q_block_2_ten[15], Q_block_2_ten[16], Q_block_2_ten[17], Q_block_2_ten[18], message_block_2)
        Q_block_2_20 = trans_10_to_2(Q_block_2_ten[19])
        if Q_block_2_20[0] != '0' or Q_block_2_20[13] == Q_block_2_19[13]:
            # print('step five failed')
            continue
        else:
            pass
        Q_block_2_ten[20] = get_Q_next(20, Q_block_2_ten[16], Q_block_2_ten[17], Q_block_2_ten[18], Q_block_2_ten[19], message_block_2)
        Q_block_2_21 = trans_10_to_2(Q_block_2_ten[20])
        if Q_block_2_21[0] != '0' or Q_block_2_21[14] != Q_block_2_20[14]:
            # print('step six failed')
            continue
        else:
            pass
        # for i in Q_block_2_ten:
        #     print(trans_10_to_2(i))
        counter3 = 0
        break
    if counter3 != 0:
        continue
    else:
        pass
    counter4 = 0
    while counter4 < 1000:
        counter4 = counter4 + 1
        while True:
            # new_q_9 = Q_block_2[8]
            # new_q_10 = Q_block_2[9]
            new_q_9, new_q_10 = gen_random_block2_9_and_10(Q_block_2)
            new_q_9_ten = trans_2_to_10(new_q_9)
            new_q_10_ten = trans_2_to_10(new_q_10)
            m_block_2_new_11 = get_message(11, Q_block_2_ten[7], new_q_9_ten, new_q_10_ten, Q_block_2_ten[10], Q_block_2_ten[11])
            m_block_2_new_11 = trans_10_to_16(m_block_2_new_11)
            # print(Q_block_2[8])
            # print(Q_block_2[9])
            # print(new_q_9)
            # print(new_q_10)
            # print(message_block_2[11])
            # print(m_block_2_new_11)
            if m_block_2_new_11 != message_block_2[11]:
                # print('one Q9 and Q10 failed, try another pair')
                continue
            else:
                Q_block_2_ten[8] = new_q_9_ten
                Q_block_2_ten[9] = new_q_10_ten
                break
        for i in [8, 9, 10, 12, 13]:
            message_block_2[i] = trans_10_to_16(get_message(i, Q_block_2_ten[i-4], Q_block_2_ten[i-3], Q_block_2_ten[i-2], Q_block_2_ten[i-1], Q_block_2_ten[i]))
        Q_block_2_ten[21] = get_Q_next(21, Q_block_2_ten[17], Q_block_2_ten[18], Q_block_2_ten[19], Q_block_2_ten[20], message_block_2)
        Q_block_2_22_bin = trans_10_to_2(Q_block_2_ten[21])
        if Q_block_2_22_bin[0] != '0':
            # print('22 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[22] = get_Q_next(22, Q_block_2_ten[18], Q_block_2_ten[19], Q_block_2_ten[20], Q_block_2_ten[21], message_block_2)
        Q_block_2_23_bin = trans_10_to_2(Q_block_2_ten[22])
        if Q_block_2_23_bin[0] != '0':
            # print('23 unsatisfied')
            continue
        else:
            pass
        T_22 = get_T(22, Q_block_2_ten[18], Q_block_2_ten[19], Q_block_2_ten[20], Q_block_2_ten[21], message_block_2)
        T_22_bin = trans_10_to_2(T_22)
        if T_22_bin[14] != '0':
            print('T_22 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[23] = get_Q_next(23, Q_block_2_ten[19], Q_block_2_ten[20], Q_block_2_ten[21], Q_block_2_ten[22], message_block_2)
        Q_block_2_24_bin = trans_10_to_2(Q_block_2_ten[23])
        if Q_block_2_24_bin[0] != '1':
            # print(new_qs_23_bin)
            # print('24 unsatisfied')
            continue
        else:
            pass
        for i in range(21):
            Q_block_2_ten[24 + i] = get_Q_next(24 + i, Q_block_2_ten[20 + i], Q_block_2_ten[21 + i], Q_block_2_ten[22 + i], Q_block_2_ten[23 + i],
                                        message_block_2)
        T_34 = get_T(34, Q_block_2_ten[30], Q_block_2_ten[31], Q_block_2_ten[32], Q_block_2_ten[33], message_block_2)
        T_34_bin = trans_10_to_2(T_34)
        if T_34_bin[16] != '0':
            print('T_34 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[45] = get_Q_next(45, Q_block_2_ten[41], Q_block_2_ten[42], Q_block_2_ten[43], Q_block_2_ten[44], message_block_2)
        Q_block_2_46_bin = trans_10_to_2(Q_block_2_ten[45])
        Q_block_2_ten[46] = get_Q_next(46, Q_block_2_ten[42], Q_block_2_ten[43], Q_block_2_ten[44], Q_block_2_ten[45], message_block_2)
        Q_block_2_47_bin = trans_10_to_2(Q_block_2_ten[46])
        Q_block_2_ten[47] = get_Q_next(47, Q_block_2_ten[43], Q_block_2_ten[44], Q_block_2_ten[45], Q_block_2_ten[46], message_block_2)
        Q_block_2_48_bin = trans_10_to_2(Q_block_2_ten[47])
        if Q_block_2_48_bin[0] != Q_block_2_46_bin[0]:
            # print(new_qs_45_bin)
            # print(new_qs_47_bin)
            print('48 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[48] = get_Q_next(48, Q_block_2_ten[44], Q_block_2_ten[45], Q_block_2_ten[46], Q_block_2_ten[47], message_block_2)
        Q_block_2_49_bin = trans_10_to_2(Q_block_2_ten[48])
        if Q_block_2_49_bin[0] != Q_block_2_47_bin[0]:
            # print(new_qs_46_bin)
            # print(new_qs_48_bin)
            # print('49 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[49] = get_Q_next(49, Q_block_2_ten[45], Q_block_2_ten[46], Q_block_2_ten[47], Q_block_2_ten[48], message_block_2)
        Q_block_2_50_bin = trans_10_to_2(Q_block_2_ten[49])
        if Q_block_2_50_bin[0] == Q_block_2_48_bin[0]:
            # print(new_qs_45_bin)
            # print(new_qs_49_bin)
            # print('50 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[50] = get_Q_next(50, Q_block_2_ten[46], Q_block_2_ten[47], Q_block_2_ten[48], Q_block_2_ten[49], message_block_2)
        Q_block_2_51_bin = trans_10_to_2(Q_block_2_ten[50])
        if Q_block_2_51_bin[0] != Q_block_2_49_bin[0]:
            # print(new_qs_48_bin)
            # print(new_qs_50_bin)
            # print('51 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[51] = get_Q_next(51, Q_block_2_ten[47], Q_block_2_ten[48], Q_block_2_ten[49], Q_block_2_ten[50], message_block_2)
        Q_block_2_52_bin = trans_10_to_2(Q_block_2_ten[51])
        if Q_block_2_52_bin[0] != Q_block_2_50_bin[0]:
            # print(new_qs_49_bin)
            # print(new_qs_51_bin)
            # print('52 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[52] = get_Q_next(52, Q_block_2_ten[48], Q_block_2_ten[49], Q_block_2_ten[50], Q_block_2_ten[51], message_block_2)
        Q_block_2_53_bin = trans_10_to_2(Q_block_2_ten[52])
        if Q_block_2_53_bin[0] != Q_block_2_51_bin[0]:
            # print(new_qs_50_bin)
            # print(new_qs_52_bin)
            # print('53 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[53] = get_Q_next(53, Q_block_2_ten[49], Q_block_2_ten[50], Q_block_2_ten[51], Q_block_2_ten[52], message_block_2)
        Q_block_2_54_bin = trans_10_to_2(Q_block_2_ten[53])
        if Q_block_2_54_bin[0] != Q_block_2_52_bin[0]:
            # print(new_qs_51_bin)
            # print(new_qs_53_bin)
            # print('54 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[54] = get_Q_next(54, Q_block_2_ten[50], Q_block_2_ten[51], Q_block_2_ten[52], Q_block_2_ten[53], message_block_2)
        Q_block_2_55_bin = trans_10_to_2(Q_block_2_ten[54])
        if Q_block_2_55_bin[0] != Q_block_2_53_bin[0]:
            # print(new_qs_52_bin)
            # print(new_qs_54_bin)
            # print('55 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[55] = get_Q_next(55, Q_block_2_ten[51], Q_block_2_ten[52], Q_block_2_ten[53], Q_block_2_ten[54], message_block_2)
        Q_block_2_56_bin = trans_10_to_2(Q_block_2_ten[55])
        if Q_block_2_56_bin[0] != Q_block_2_54_bin[0]:
            # print(new_qs_53_bin)
            # print(new_qs_55_bin)
            # print('56 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[56] = get_Q_next(56, Q_block_2_ten[52], Q_block_2_ten[53], Q_block_2_ten[54], Q_block_2_ten[55], message_block_2)
        Q_block_2_57_bin = trans_10_to_2(Q_block_2_ten[56])
        # print(new_qs[56])
        if Q_block_2_57_bin[0] != Q_block_2_55_bin[0]:
            # print(new_qs_54_bin)
            # print(new_qs_56_bin)
            # print('57 unsatisfied')
            continue
        else:
            # print(new_qs[56])
            pass
        Q_block_2_ten[57] = get_Q_next(57, Q_block_2_ten[53], Q_block_2_ten[54], Q_block_2_ten[55], Q_block_2_ten[56], message_block_2)
        Q_block_2_58_bin = trans_10_to_2(Q_block_2_ten[57])
        if Q_block_2_58_bin[0] != Q_block_2_56_bin[0]:
            # print('58 unsatisfied')
            continue
        else:
            # print(new_qs[57])
            pass
        Q_block_2_ten[58] = get_Q_next(58, Q_block_2_ten[54], Q_block_2_ten[55], Q_block_2_ten[56], Q_block_2_ten[57], message_block_2)
        Q_block_2_59_bin = trans_10_to_2(Q_block_2_ten[58])
        if Q_block_2_59_bin[0] != Q_block_2_57_bin[0]:
            # print('59 unsatisfied')
            continue
        else:
            # print(new_qs[58])
            pass
        Q_block_2_ten[59] = get_Q_next(59, Q_block_2_ten[55], Q_block_2_ten[56], Q_block_2_ten[57], Q_block_2_ten[58], message_block_2)
        Q_block_2_60_bin = trans_10_to_2(Q_block_2_ten[59])
        if Q_block_2_60_bin[0] != Q_block_2_48_bin[0]:
            # print('60 unsatisfied')
            continue
        else:
            # print(new_qs[59])
            pass
        Q_block_2_ten[60] = get_Q_next(60, Q_block_2_ten[56], Q_block_2_ten[57], Q_block_2_ten[58], Q_block_2_ten[59], message_block_2)
        Q_block_2_61_bin = trans_10_to_2(Q_block_2_ten[60])
        if Q_block_2_61_bin[0] != Q_block_2_59_bin[0]:
            # print(new_qs[60])
            print('61 unsatisfied')
            continue
        else:
            # print(new_qs[60])
            pass
        Q_block_2_ten[61] = get_Q_next(61, Q_block_2_ten[57], Q_block_2_ten[58], Q_block_2_ten[59], Q_block_2_ten[60], message_block_2)
        Q_block_2_62_bin = trans_10_to_2(Q_block_2_ten[61])
        if Q_block_2_62_bin[0] != Q_block_2_60_bin[0]:
            print('62 unsatisfied')
            continue
        else:
            pass
        Q_block_2_ten[62] = get_Q_next(62, Q_block_2_ten[58], Q_block_2_ten[59], Q_block_2_ten[60], Q_block_2_ten[61], message_block_2)
        Q_block_2_63_bin = trans_10_to_2(Q_block_2_ten[62])
        if Q_block_2_63_bin[0] != Q_block_2_61_bin[0]:
            print('63 unsatisfied')
            continue
        else:
            pass
        print('all satisfied')
        # print(new_qs[59])
        # print(new_qs[60])
        # print(new_qs[61])
        # print(new_qs[62])
        # print(new_message)
        Q_block_2_ten[63] = get_Q_next(63, Q_block_2_ten[59], Q_block_2_ten[60], Q_block_2_ten[61], Q_block_2_ten[62], message_block_2)
        print('----------------------------------------------------------------------------------------')
        print(message_block_2)
        out_block_2_a = int32Control(Q_block_1_0 + Q_block_2_ten[60])
        out_block_2_b = int32Control(Q_block_1__1 + Q_block_2_ten[63])
        out_block_2_c = int32Control(Q_block_1__2 + Q_block_2_ten[62])
        out_block_2_d = int32Control(Q_block_1__3 + Q_block_2_ten[61])
        print('----------------------------------------------------------------------------------------')
        for i in Q_block_2_ten:
            print(trans_10_to_2(i))
        print('----------------------------------------------------------------------------------------')
        hash_block_2 = trans_10_to_16(out_block_2_a) + trans_10_to_16(out_block_2_b) + trans_10_to_16(out_block_2_c) + trans_10_to_16(out_block_2_d)
        counter4 = 0
        break
    if counter4 != 0:
        continue
    else:
        break
print('message for block 1:')
print(new_message)
print('hash value:' + hash_block_1)
print('message for block 2:')
print(message_block_2)
print('hash value:' + hash_block_2)















