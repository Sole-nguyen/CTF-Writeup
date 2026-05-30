import idaapi
import idc

print("Extracting all f_X functions...")
print("="*60)

for i in range(75):
    func_name = f"f_{i}"
    func_ea = idaapi.get_name_ea(idaapi.BADADDR, func_name)
    if func_ea != idaapi.BADADDR:
        position = None
        operation = None
        op_value = None
        
        # Scan instructions
        ea = func_ea
        for j in range(20):
            mnem = idc.print_insn_mnem(ea)
            op0 = idc.print_operand(ea, 0)
            op1 = idc.print_operand(ea, 1)
            
            # Find "add rax, XXh"
            if mnem == "add" and "rax" in op0:
                try:
                    position = int(op1.replace("h", ""), 16)
                except:
                    pass
            
            # Find operation on edx
            if mnem in ["add", "sub", "xor"] and "edx" in op0:
                operation = mnem
                try:
                    op_value = int(op1.replace("h", "").replace("FFFFFF", ""), 16) & 0xFF
                except:
                    pass
            
            ea = idc.next_head(ea)
            if ea == idaapi.BADADDR:
                break
        
        if position is not None and operation and op_value is not None:
            # Print inverse operation
            inv_op = "sub" if operation == "add" else "add" if operation == "sub" else "xor"
            print(f"    {position}: ('{inv_op}', 0x{op_value:02X}),  # f_{i}")

print("="*60)
print("Copy the output above and paste into decrypt_ops dictionary!")
