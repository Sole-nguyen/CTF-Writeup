"""
Deobfuscate and analyze key parts of the VM
"""

code = """
// Version counter - incremented on shape changes
let x = 0;
function f() {
    x = x + 1 | 0;
    if (x === 0) x = 1;
}

// Shape class - stores property map
class o {
    constructor(m) {
        this.id = ++o._i;
        this.m = m;  // Map: property_key -> storage_index
    }
}
o._i = 0;

// Clone shape map
function J(b) {
    const N = new Map();
    for (const [key, value] of b.entries())
        N.set(key, value);
    return N;
}

// Add property to shape
function l(b, N) {
    const map = J(b.m);
    if (!map.has(N))
        map.set(N, map.size);
    return new o(map);
}

// Object class
class v {
    constructor(parent = null) {
        this.p = parent;        // prototype
        this.sh = new o(new Map());  // shape
        this.sl = [];           // storage array
        this.dm = false;        // dictionary mode
        this.d = null;          // dictionary
        this.h = false;         // has been accessed
        this.z = false;         // sealed
    }

    t() { this.h = true; }  // mark accessed
    x() { this.z = true; }  // seal

    o(key, value) {  // set property
        if (this.z) throw "sealed";
        if (this.dm) {
            if (!this.d) this.d = new Map();
            this.d.set(key, value);
            return;
        }
        if (!this.sh.m.has(key))
            this.sh = l(this.sh, key);
        const index = this.sh.m.get(key);
        this.sl[index] = value;
    }

    y(key) {  // has property
        if (this.dm)
            return this.d ? this.d.has(key) : false;
        return this.sh.m.has(key);
    }

    g(key) {  // get property
        if (this.dm)
            return this.d ? this.d.get(key) : undefined;
        if (!this.sh.m.has(key))
            return undefined;
        return this.sl[this.sh.m.get(key)];
    }
}

// SORT handler in VM - opcode 0x70
case 0x70:  // SORT
    check(2);
    {
        const obj_reg = readByte();
        const key = readByte();
        const obj = N[obj_reg];
        if (!(obj instanceof v)) throw "not object";
        Fh(obj, key);  // Call sort function
        break;
    }

// Sort function Fh:
const Fh = (obj, key) => {
    const lookup_result = FG(obj, key);  // Lookup property
    if (!lookup_result.ok) return;
    
    const holder = lookup_result.h;  // Object that has the property
    if (!holder.z) return;  // Must be sealed
    
    if (!holder.dm) {
        holder.dm = true;  // Switch to dictionary mode
        holder.d = new Map();
        
        const arr = [];
        for (const [k, idx] of holder.sh.m.entries()) {
            const val = holder.sl[idx];
            holder.d.set(k, val);
            arr.push([k, val]);
        }
        
        arr.sort((a, b) => a[0] - b[0]);  // Sort by key
        holder.sl = arr.map(x => x[1]);   // Reorder storage!
        
        if (holder.h) f();  // Increment version IF accessed
    }
};

// GETPROPC - cached property access
case 0x21:  // GETPROPC
    {
        const result_reg = readByte();
        const pc = readByte();
        const obj_reg = readByte();
        const key = readByte();
        
        const obj = N[obj_reg];
        if (!(obj instanceof v)) throw "not object";
        
        const cached = Fs(pc, obj, key);  // Try cache
        if (cached) {
            N[result_reg] = cached.fn;
            N[next_reg] = cached.th;
            break;
        }
        
        const lookup = FG(obj, key);
        N[result_reg] = lookup.fn;
        N[next_reg] = obj;
        FZ(pc, obj, key, lookup);  // Update cache
        break;
    }

// Cache lookup Fs:
const Fs = (pc, obj, key) => {
    const cache = this.ic.get(pc);
    if (!cache || cache.m) return null;
    
    const version = x;  // Read current version
    for (const entry of cache.c) {
        if (entry.rs !== obj.sh.id) continue;  // Shape ID must match
        if (entry.k !== key) continue;
        if (entry.v !== version) continue;  // VERSION CHECK!
        
        let holder = obj;
        for (let i = 0; i < entry.d; i++) {
            holder = holder.p;
            if (!(holder instanceof v)) return null;
        }
        
        const value = holder.sl[entry.si];  // Use cached index!
        return { fn: value, th: obj };
    }
    return null;
};
"""

print(code)

print("\n\n=== KEY INSIGHT ===")
print("The SORT function:")
print("1. Switches object to dictionary mode")
print("2. Sorts properties by key")
print("3. Reorders storage array to match sorted order")
print("4. Increments version with f() ONLY if obj.h is true (accessed)")
print()
print("The attack:")
print("1. Access obj.e to cache it and set obj.h = true")
print("2. SORT obj.e - this will:")
print("   - Sort F5's properties")
print("   - Reorder F5.sl storage")
print("   - Increment version because F5.h is true")
print("3. Try to use cache - but version changed!")
print()
print("Wait... let me recheck. Maybe the issue is:")
print("- We cache on F7, not F5")
print("- F7 doesn't have the property directly")
print("- SORT happens on F5 (the holder)")
print("- F7's shape ID doesn't change!")
print("- Version changes, but if cache stores F7's shape...")
print()
print("Let me trace more carefully...")
