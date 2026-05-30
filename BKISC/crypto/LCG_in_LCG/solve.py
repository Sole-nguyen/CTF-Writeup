from z3 import *
from Crypto.Util.number import *

# --- Challenge Parameters ---
p = 109293690254125700593428833253859351747207544427596641988902897826726923108129
leak = [90932320403583933388104590731426350182475714444529235922632654547630050547854, 7419001973708127101952065444933291168381819947297996667304118571827819593833, 67898657390352222099145776514702065237791087004192011316965425093842698547879, 59104346122377345147160947908393133350394990600375907640957883201712863161514, 65791268128235538218159841829641838780085430662646571477813528156670949468574, 30746596701904608663428779065775617660959514980181049138973990539351151163398, 90401086830823038866772268939325153317251259153444707025916388656856331751223, 58272077154494735088853274292736003691073242782827315949821851312399207553921, 2436351101341565181224132398898435947850914144805010798831033314744304065906, 60037930506906075080157529686240388137679026846211607176962484455269373425792, 94603418212790651171053589169233166073715690379203194716340883392985882958728, 40083135504675462463890729594467413366841384941611263958817813623602970950139, 87423735720908548570287620670610997539974220708226253072012896399717805881915, 90068696477808774338018715050496670423314532057245370376629814966590792334138, 85125353608712750771947916413431128173570267602118896397591754906948853457159, 103572197428666464527548288713740517562031762481709127346013361939366060409462, 43369712552829683498588001109740718097054089477610970275193450254188936367127, 93391039302254883112884682942395960326495980261895255005297213996980004965042, 106127175177601840953317451864979451638562623954667122658489723938111108742444, 57117890321834374388608137881909634607470441609846105637468499778163706812815, 108323133963731727447343134032705836190493323038407099159328543077938215447190, 46197978915634272286652335254378306194009148494353844230660614155269659323322, 61275120371350337137606775044861934316845211969342945868270767375887012067459, 105141796923903181156301351545814195231944808346151426835750813084215216036478, 63497969937675382864122605069019472859395334014001110878786173999903860090108, 103978872184469065639739458101313148437273147029754778075306257583387456083595, 88133118544204664892482510421866229283075324748199288179327177640559110484643, 105178940818406923446634762159331510677921686411620687829854838850860667935623, 84382472730499115614151805092165372226815632887388603663091724929767632086870, 46706679512967527627325203221385581068492266844734511449576209129559487807899]
ct = [110, 209, 242, 199, 22, 17, 34, 12, 40, 226, 163, 109, 190, 116, 178, 134, 146, 192, 47, 29, 33, 240, 253, 185, 170, 139, 245, 74, 155, 16, 128, 167, 186, 75, 141, 100]

p_shuffle = 100012367912491304950970537118525513361574730061518925742496715244134368935279
a_shuffle = 94671321777649901144236237096963884182038803186726157270932012072190410389427
b_shuffle = 64123254129311387582805351522310702500911175067175029340692470572851876649363
SIZE = 10

# 1. Map the transitions and group the ones running on the same (a, b) pair
transitions = [(leak[i], leak[i+1]) for i in range(len(leak)-1)]
collinear_groups = []

def are_collinear(p1, p2, p3):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3
    # Cross multiply to avoid modular inversions
    return (y2 - y1) * (x3 - x1) % p == (y3 - y1) * (x2 - x1) % p

used = set()
for i in range(len(transitions)):
    if i in used: continue
    for j in range(i+1, len(transitions)):
        if j in used: continue
        group = [i, j]
        for k in range(j+1, len(transitions)):
            if k in used: continue
            if are_collinear(transitions[i], transitions[j], transitions[k]):
                group.append(k)
        if len(group) >= 3: # Highly certain mappings
            collinear_groups.append(group)
            for x in group: used.add(x)
            break

print(f"[*] Found {len(collinear_groups)} deterministic transition clusters.")

# 2. Reconstruct the PRNG mapping sequence via Z3 
solver = Solver()
S1 = Int('S1')
solver.add(S1 >= 0, S1 < p_shuffle)

# Simulate states
S_vals = [S1]
for i in range(1, len(leak) + len(ct) + 2):
    S_vals.append((a_shuffle * S_vals[-1] + b_shuffle) % p_shuffle)

# The C_vals represent the index arrays returned via % SIZE
C_vals = [S % SIZE for S in S_vals]

# Constrain Z3 perfectly: points in known groups MUST share the same modulus
for group in collinear_groups:
    first = group[0]
    for other in group[1:]:
        solver.add(C_vals[first] == C_vals[other])

# Different known groups must resolve to independent indices 
for i in range(len(collinear_groups)):
    for j in range(i+1, len(collinear_groups)):
        solver.add(C_vals[collinear_groups[i][0]] != C_vals[collinear_groups[j][0]])

# Prevent Z3 from falsely grouping un-aligned 3+ triplets
known_triplets = set()
for group in collinear_groups:
    for i in range(len(group)):
        for j in range(i+1, len(group)):
            for k in range(j+1, len(group)):
                known_triplets.add(tuple(sorted([group[i], group[j], group[k]])))

for i in range(len(transitions)):
    for j in range(i+1, len(transitions)):
        for k in range(j+1, len(transitions)):
            if tuple(sorted([i, j, k])) not in known_triplets:
                solver.add(Not(And(C_vals[i] == C_vals[j], C_vals[j] == C_vals[k])))

print("[*] Launching Z3 Solver to reconstruct internal seed...")

# 3. Discover seed_shuffle, infer missing groups & decipher ciphertext
while solver.check() == sat:
    model = solver.model()
    s1_val = model[S1].as_long()
    
    sim_S = s1_val
    sim_C = []
    for _ in range(len(leak) + len(ct) + 2):
        sim_C.append(sim_S % SIZE)
        sim_S = (a_shuffle * sim_S + b_shuffle) % p_shuffle
        
    recovered_ab = {}
    
    # Process definitively clustered arrays
    for group in collinear_groups:
        i, j = group[0], group[1]
        x1, y1 = transitions[i]
        x2, y2 = transitions[j]
        dx = (x1 - x2) % p
        dy = (y1 - y2) % p
        a = (dy * pow(dx, -1, p)) % p
        b = (y1 - a * x1) % p
        recovered_ab[sim_C[i]] = (a, b)
        
    # Process leftover size-2 arrays resolved natively by Z3 constraints
    for c_val in range(SIZE):
        if c_val in recovered_ab: continue
        indices = [i for i in range(len(transitions)) if sim_C[i] == c_val]
        if len(indices) >= 2:
            i, j = indices[0], indices[1]
            x1, y1 = transitions[i]
            x2, y2 = transitions[j]
            dx = (x1 - x2) % p
            if dx == 0: continue
            dy = (y1 - y2) % p
            a = (dy * pow(dx, -1, p)) % p
            b = (y1 - a * x1) % p
            recovered_ab[c_val] = (a, b)
            
    current_s = leak[-1]
    flag = bytearray()
    valid_decryption = True
    
    for i in range(len(ct)):
        c_val = sim_C[len(leak) - 1 + i] 
        if c_val not in recovered_ab:
            valid_decryption = False
            break
        a, b = recovered_ab[c_val]
        current_s = (a * current_s + b) % p
        char = (current_s & 0xFF) ^ ct[i]
        flag.append(char)
        
    if valid_decryption:
        flag_str = flag.decode(errors='ignore')
        if "BKISC{" in flag_str:
            print(f"\n[+] Exploit Successful!")
            print(f"[+] Flag: {flag_str}")
            break
            
    # Re-loop to iterate constraints if we triggered a mathematically sound but textually false model
    solver.add(S1 != s1_val)
