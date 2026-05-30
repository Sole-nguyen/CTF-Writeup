import numpy as np

# Standard Gaussian Elimination for GF2
def solve_gf2(A, b):
    m, n = A.shape
    row = 0
    pivot_cols = []
    
    for col in range(n):
        if row >= m:
            break
        # Find pivot
        pivot = row + np.argmax(A[row:, col])
        if A[pivot, col] == 0:
            continue
            
        # Swap rows
        A[[row, pivot]] = A[[pivot, row]]
        b[[row, pivot]] = b[[pivot, row]]
        
        # Eliminate other rows
        mask = A[:, col] == 1
        mask[row] = False 
        A[mask] ^= A[row]
        b[mask] ^= b[row]
        
        pivot_cols.append((row, col))
        row += 1
        
    res = np.zeros(n, dtype=np.uint8)
    for r, c in pivot_cols:
        res[c] = b[r]
    return res

# Symbolic implementation of the PRNG logic
class SymGiantLinearRNG:
    def __init__(self, state_size=32):
        self.size = state_size
        self.state = []
        for i in range(self.size):
            word = []
            for j in range(64):
                vec = np.zeros(2048, dtype=np.uint8)
                # Maps bits to the original big-endian seed integer
                bit_idx = 64 * (self.size - 1 - i) + (63 - j)
                vec[bit_idx] = 1
                word.append(vec)
            self.state.append(word)

    def next(self):
        s = self.state
        taps = [0, 1, 3, 7, 13, 22, 28, 31]
        new_val = [np.zeros(2048, dtype=np.uint8) for _ in range(64)]
        
        # Mirror the transformation logic from chall.py
        for i in taps:
            val = s[i]
            shl11 = val[11:] + [np.zeros(2048, dtype=np.uint8)] * 11
            shr7 = [np.zeros(2048, dtype=np.uint8)] * 7 + val[:-7]
            mixed = [v ^ s11 ^ s7 for v, s11, s7 in zip(val, shl11, shr7)]
            rot = (i * 3) % 64
            mixed = mixed[rot:] + mixed[:rot]
            new_val = [nv ^ m for nv, m in zip(new_val, mixed)]
            
        sn = s[-1]
        shr13 = [np.zeros(2048, dtype=np.uint8)] * 13 + sn[:-13]
        shl5 = sn[5:] + [np.zeros(2048, dtype=np.uint8)] * 5
        new_val = [nv ^ s13 ^ s5 for nv, s13, s5 in zip(new_val, shr13, shl5)]
        
        self.state = s[1:] + [new_val]
        
        out = [np.zeros(2048, dtype=np.uint8) for _ in range(64)]
        for i in range(self.size):
            val = self.state[i]
            if i % 2 == 0:
                out = [o ^ v for o, v in zip(out, val)]
            else:
                ror2 = val[-2:] + val[:-2]
                out = [o ^ r for o, r in zip(out, ror2)]
        return out

# Given outputs from output.txt
outputs = [
    11329270341625800450, 14683377949987450496, 11656037499566818711, 14613944493490807838, 
    370532313626579329, 5006729399082841610, 8072429272270319226, 3035866339305997883, 
    8753420467487863273, 15606411394407853524, 5092825474622599933, 6483262783952989294, 
    15380511644426948242, 13769333495965053018, 5620127072433438895, 6809804883045878003, 
    1965081297255415258, 2519823891124920624, 8990634037671460127, 3616252826436676639, 
    1455424466699459058, 2836976688807481485, 11291016575083277338, 1603466311071935653, 
    14629944881049387748, 3844587940332157570, 584252637567556589, 10739738025866331065, 
    11650614949586184265, 1828791347803497022, 9101164617572571488, 16034652114565169975, 
    13629596693592688618, 17837636002790364294, 10619900844581377650, 15079130325914713229, 
    5515526762186744782, 1211604266555550739, 11543408140362566331, 18425294270126030355, 
    2629175584127737886, 6074824578506719227, 6900475985494339491, 3263181255912585281, 
    12421969688110544830, 10785482337735433711, 10286647144557317983, 15284226677373655118, 
    9365502412429803694, 4248763523766770934, 13642948918986007294, 3512868807899248227, 
    14810275182048896102, 1674341743043240380, 28462467602860499, 1060872896572731679, 
    13208674648176077254, 14702937631401007104, 5386638277617718038, 8935128661284199759
]

rng = SymGiantLinearRNG()
A = []
b_vec = []

# Collect enough bits to solve for the 2048 variables
for out_val in outputs:
    sym_out = rng.next()
    for bit_idx in range(64):
        A.append(sym_out[bit_idx])
        b_vec.append((out_val >> (63 - bit_idx)) & 1)

A = np.array(A, dtype=np.uint8)
b_vec = np.array(b_vec, dtype=np.uint8)

solution = solve_gf2(A, b_vec)

# Reconstruct seed_int from bits
recovered_val = 0
for bit in solution:
    recovered_val = (recovered_val << 1) | int(bit)

# Convert to flag
flag_bytes = recovered_val.to_bytes(256, 'big').strip(b'\x00')
print(f"0xfun{{{flag_bytes.decode()}}}")