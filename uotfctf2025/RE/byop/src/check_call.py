"""
Check CALL opcode format
"""

print("From validation code:")
print("""
case u['e']:  // CALL - opcode 0x30
    Fi(0xb73+-0x1*-0x1dd4+-0x2943);  // Check 6 bytes
    {
        const FI=FH(),  // result_reg
        Fu=FH(),         // func_reg
        FY=FH(),         // this_reg
        FX=FH();         // argc
        
        if(FX>a['a']) throw...;  // argc <= 8
        Fi(FX);  // Check FX more bytes
        
        for(let Fk=0;Fk<FX;Fk++){
            const arg_reg = FH();
            if(arg_reg>=b['nr']) throw...;
        }
        
        if(FI>=b['nr']||Fu>=b['nr']||FY>=b['nr']) throw...;
        break;
    }
""")

print("Format: [0x30] [result_reg] [func_reg] [this_reg] [argc] [arg0] [arg1] ...")
print()
print("In my code:")
print("  code += p8(0x30) + p8(0x04) + p8(0x02) + p8(0x01) + p8(0x01) + p8(0x03)")
print()
print("This means:")
print("  result_reg = 4")
print("  func_reg = 2")
print("  this_reg = 1")
print("  argc = 1")
print("  arg0 = 3")
print()
print("So: r4 = r2.call(r1, [r3])")
print()
print("But looking at runtime:")
print("""
case u['e']:  // CALL
    {
        const FM=FH(),  // result
        Ff=FH(),        // func
        FK=FH(),        // this
        Fo=FH();        // argc
        
        if(Fo>a['a']) throw...;
        Fj(Fo);
        
        const FJ=N[Ff],  // func value
        Fl=N[FK],        // this value
        Fv=[];
        
        for(let FW=0;FW<Fo;FW++)
            Fv['push'](N[FH()]);  // args
        
        if(!(FJ instanceof g)) throw...;  // Must be function
        
        N[FM]=FJ['c'](Fl,Fv);  // Call: func.call(this, args)
        break;
    }
""")

print("So it calls: func.call(this, [arg0, arg1, ...])")
print()
print("For F1(filename), we want:")
print("  F1.call(???, [filename])")
print()
print("What should 'this' be?")
print("Looking at F1:")
print("""
function F1(b){
    const N=String(b);
    if(t['isAbsolute'](N))return '';
    const FN=t['resolve'](s,N);
    if(!FN['startsWith'](s+t['sep']))return '';
    try{return c(FN);}catch{return '';}
}
""")

print("F1 doesn't use 'this', so it can be anything (null/undefined).")
print("But maybe r1 (F7) is not a valid 'this'?")
print()
print("Let me try with r1 = undefined by using a different register...")
