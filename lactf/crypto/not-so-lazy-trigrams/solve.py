ct = "zjlel{heqmz_dgk_tevr_tk_vnnds_c_imcqaeyde_ug_byndu_e_jjaogy_rqqnisoqe_cwtnamd}"
# We know z is stream 0.
# Let's print index, char, stream for the whole string.
idx = 0
for c in ct:
    if c.isalpha():
        print(f"'{c}' : {idx % 3}")
        idx += 1
    else:
        print(f"'{c}' : SKIP")