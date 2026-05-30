"""
Check GETPROPC more carefully
"""

print("GETPROPC runtime code:")
print("""
case u['d']:  // GETPROPC - opcode 0x21
    Fj(0x1bb4+0x18ce+-0x347e);  // Check 4 bytes
    {
        const Fk=FH(),  // result_reg
        FQ=FH(),        // pc_id
        FE=FH(),        // obj_reg
        Fm=FH(),        // key
        FS=N[FE];       // obj value
        
        if(!(FS instanceof v)) throw...;
        
        const Fc=Fs(Fa,FS,Fm);  // Try cache (Fa = current PC)
        if(Fc){
            N[Fk]=Fc['fn'];      // result_reg = value
            N[FQ]=Fc['th'];      // NEXT reg = 'this' (the object!)
            break;
        }
        
        const Fz=FG(FS,Fm);  // Lookup
        N[Fk]=Fz['fn'];      // result_reg = value
        N[FQ]=FS;            // NEXT reg = object
        FZ(Fa,FS,Fm,Fz);     // Update cache
        break;
    }
""")

print("AHA! GETPROPC writes TWO registers:")
print("  N[result_reg] = value")
print("  N[result_reg + 1] = object ('this')")
print()
print("So if I do:")
print("  GETPROPC r2, PC_ID=1, r1, key=10")
print()
print("It actually sets:")
print("  r2 = value")
print("  r3 = r1 (the 'this' object)")
print()
print("This is WRONG in my bytecode!")
print()
print("Let me fix the register allocation...")
