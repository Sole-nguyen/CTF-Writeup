# -*- coding: utf-8 -*-
"""
Since simple operations don't work, let's try using angr for symbolic execution
to solve the constraints
"""

try:
    import angr
    import claripy
except ImportError:
    print("angr not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "angr"])
    import angr
    import claripy

# Load the binary
binary_path = "checker_unpacked"
proj = angr.Project(binary_path, auto_load_libs=False)

# Create a symbolic input of 42 bytes (flag length)
flag_chars = [claripy.BVS(f'flag_{i}', 8) for i in range(42)]
flag = claripy.Concat(*flag_chars)

# Set up initial state
state = proj.factory.entry_state(
    stdin=angr.storage.SimFile('/dev/stdin', content=flag, size=42)
)

# Add constraints that input should be printable ASCII
for i, c in enumerate(flag_chars):
    state.solver.add(c >= 0x20)
    state.solver.add(c <= 0x7e)

# Add constraint for flag format
state.solver.add(flag_chars[0] == ord('u'))
state.solver.add(flag_chars[1] == ord('o'))
state.solver.add(flag_chars[2] == ord('f'))
state.solver.add(flag_chars[3] == ord('t'))
state.solver.add(flag_chars[4] == ord('c'))
state.solver.add(flag_chars[5] == ord('t'))
state.solver.add(flag_chars[6] == ord('f'))
state.solver.add(flag_chars[7] == ord('{'))
state.solver.add(flag_chars[41] == ord('}'))

# Create simulation manager
simgr = proj.factory.simulation_manager(state)

# Look for the "Yes" string address (we know it's after the encrypted data)
# Based on xxd output, "Yes" is at around 0x41040

# Find paths to success (printing "Yes")
print("Starting symbolic execution...")
simgr.explore(find=lambda s: b"Yes" in s.posix.dumps(1))

if simgr.found:
    solution_state = simgr.found[0]
    flag_solution = solution_state.posix.dumps(0)
    print(f"\n*** FLAG FOUND ***")
    print(flag_solution.decode())
else:
    print("No solution found")
    if simgr.errored:
        print(f"Errors: {len(simgr.errored)}")
    if simgr.deadended:
        print(f"Dead ends: {len(simgr.deadended)}")
