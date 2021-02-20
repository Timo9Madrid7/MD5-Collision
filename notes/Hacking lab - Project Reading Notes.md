# Hacking lab - Project Reading Notes
> notes retrieved from [PhD-Thesis-Marc-Stevens-Attacks-on-Hash-Functions-and-Applications.pdf](https://www.cwi.nl/system/files/PhD-Thesis-Marc-Stevens-Attacks-on-Hash-Functions-and-Applications.pdf)

## Introduction

### Hash functions
- *one-way functions*: A one-way function maps a huge (possibly infinite) domain (e.g., of all possible messages) to some (possibly infinite) range (e.g., all bit strings of length 256)
- the usage of Hash: Signing a large message directly with a public-key crypto system is slow and leads to a signature as large as the message. Reducing a large message to a small hash using a hash function and signing the hash is a lot faster and leads to small fixed-size signatures
- Finding a *collision*: Finding two different documents M and M′ that have the same hash. Since if either M or M′ is signed, then the corresponding signature is also valid for the other document, resulting in a successful forgery.
    - General attacks: A hash function is called broken when there exists a known explicit attack that is faster than the general attack for a security property.
    - *Birthday Paradox*: *The birthday paradox is the counter-intuitive principle that for groups of as few as 23 persons there is already a chance of about one half of finding two persons with the same birthday*.To find collisions, one can do a lot better with a general attack based on the birthday paradox. For a given hash function with output size of N bits, this general algorithm succeeds after approximately $\sqrt{\pi/2}\cdot2^{\frac{N}{2}}$
- *Compression function* to Hash function: The compression function is then repeatedly used in some mode of operation to process the entire message. The well known Merkle-Damgård construction (named after the authors of the independent papers [Mer89, Dam89] published in 1989) describes exactly how to construct a hash function based on a general compression function in an iterative structure.
- *Differential cryptanalysis*: By analyzing how differences between those two evaluations caused by message differences propagate throughout the computation of hash function, one can try to control those differences and try to build an efficient attack.
- Big Endian vs. Little Endian Word: 
    - Big Endian: $(b_{31}, ..., b_{0})$
    - Little Endian: $(b_7b_6 ... b_1b_0 b_{15}b_{14} ... b_9b_8 b_{23}b_{22} ... b_{17}b_{16} b_{31}b_{30} ... b_{25}b_{24})$
- MD5 Overview:
    - the structure of "Step Function of MD5’s Compression Function"
    ![MD5_oneStep.png](https://raw.githubusercontent.com/Timo9Madrid7/MD5_Collision/TimoMD5/images/MD5_oneStep.png)
    - Padding: Pad the message: first append a ‘1’-bit, next append the least number of ‘0’-bits to make the resulting bit length equivalent to 448 modulo 512, and finally append the bit length of the original unpadded message M as a 64-bit **little-endian integer**. **if the original messaage is 448 bits length mod 512, it is also necessary to pad **.
    - Partitioning: Partition the padded message Mc into N consecutive 512-bit blocks
    - Processing: The general process is shown in the above diagram.
        - The word of message $m_i$:
            $$W_t=\begin{cases}
            m_t & \text{for 0 $\leq$ t < 16,}\\
            m_{(1+5t)\ mod\ 16} & \text{for 16 $\leq$ t < 32,}\\
            m_{(5+3t)\ mod\ 16} & \text{for 32 $\leq$ t < 48,}\\
            m_{(7t)\ mod\ 16} & \text{for 48 $\leq$ t < 64.}
            \end{cases}$$
        - The addition constant $K_i$:
            $$AC_t = int(2^{32}|sin(t+1)|), \text{ 0 $\leq$ t < 64}$$
        - The non-linear function $F$ depends on the round:
            $$f_t(X,Y,Z)=\begin{cases}
            (X \land Y ) \oplus (\bar{X} \land Z) & \text{for 0 $\leq$ t < 16,}\\
            (Z \land X ) \oplus (\bar{Z} \land Y) & \text{for 16 $\leq$ t < 32,}\\
            X \oplus Y \oplus Z & \text{for 32 $\leq$ t < 48,}\\
            Y \oplus (X \lor \bar{Z}) & \text{for 48 $\leq$ t < 64.}
            \end{cases}$$
        - The rotation constant $<<<_s$:
            $$(RC_t, RC_{t+1}, RC_{t+2}, RC_{t+3})=\begin{cases}
            (7, 12, 17, 22) & \text{for t = 0, 4, 8, 12,}\\
            (5, 9, 14, 20)  & \text{for t = 16, 20, 24, 28,}\\
            (4, 11, 16, 23) & \text{for t = 32, 36, 40, 44,}\\
            (6, 10, 15, 21) & \text{for t = 48, 52, 56, 60.}
            \end{cases}$$
        - Algorithm:
            1. Initialization:
            $$
            (a,b,c,d) = (67452301_{16}, efcdab89_{16}, 98badcfe_{16}, 10325476_{16})\\
            (Q_0, Q_{-1}, Q_{-2}, Q_{-3}) = (b,c,d,a) \\
            $$
            1. Loop for a block:
            $$
            F_t = f_t(Q_t, Q_{t-1}, Q_{t-2})\\
            T_t = F_t + Q_{t-3} + AC_t + W_t\\
            R_t = RL(T_t, RC_t)\\
            Q_{t+1} = Q_t + R_t\\
            $$
            1. After finishing all the blocks:
            The resulting state words are added to the input **intermediate hash value** and returned as output     
    - Output: The resulting hash value is the last intermediate hash value, expressed as the concatenation of the hexadecimal byte strings of the four words, converted back from their little-endian representation.




### MD5 collision attack by Wang et al.






## Contributions


### Our contributions


### Chosen-prefix collision abuse scenarios


### Differential cryptanalysis and paths


### MD5


### Detecting collision attacks


## Appendices
