set_option warningAsError true

def mem_effecient_mod_exp (b e m c : Nat) : Nat :=
    if e > 0 then
      mem_effecient_mod_exp b (e - 1) m ((b * c) % m)
    else
      c % m

private theorem mod_mod_self (n m : Nat) : n % m % m = n % m := by
  cases m with
  | zero => rfl
  | succ k => exact Nat.mod_eq_of_lt (Nat.mod_lt n (Nat.succ_pos k))

private theorem aux (b e m c : Nat) : mem_effecient_mod_exp b e m c = (b ^ e * c) % m := by
  induction e generalizing c with
  | zero =>
    unfold mem_effecient_mod_exp
    simp
  | succ n ih =>
    unfold mem_effecient_mod_exp
    have h : n + 1 > 0 := Nat.succ_pos n
    simp only [h, ↓reduceIte, Nat.succ_sub_one]
    rw [ih, pow_succ, mul_assoc,
        Nat.mul_mod (b ^ n) ((b * c) % m) m,
        mod_mod_self (b * c) m,
        ← Nat.mul_mod (b ^ n) (b * c) m]

theorem it_works (b e m : Nat) : mem_effecient_mod_exp b e m 1 = (b ^ e) % m := by
  rw [aux, mul_one]
