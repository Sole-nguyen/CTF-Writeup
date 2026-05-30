#!/usr/bin/env python3
import angr
import claripy

def solve():
    print("[*] Khởi tạo angr project (Advanced Bypass Mode)...")
    # Tắt load libs để chạy mượt mà, vì chúng ta sẽ bypass các hàm standard
    project = angr.Project('./black_ledger', main_opts={'base_addr': 0x400000}, auto_load_libs=False)

    # 1. Tạo 32 bytes symbolic vector cho flag
    flag_chars = [claripy.BVS(f'c_{i}', 8) for i in range(32)]
    flag = claripy.Concat(*flag_chars)

    # 2. Bắt đầu ngay tại đoạn code chuẩn bị chạy thuật toán mã hóa (bỏ qua fgets và check fake string)
    START_ADDR = 0x40085C
    state = project.factory.blank_state(addr=START_ADDR)
    
    # 3. Khởi tạo bộ nhớ và thanh ghi
    sp = 0x800000
    state.regs.sp = sp
    
    # Dựa vào disassembly: ADD X20, SP, #0x150-0xA0 => X20 = SP + 0xB0
    # Buffer chứa 32 ký tự nhập vào nằm tại SP + 0xB0, kéo dài đến SP + 0xCF
    state.memory.store(sp + 0xB0, flag)
    
    # X19 được dùng làm base pointer trỏ tới bảng tra cứu ROM (unk_4010E0)
    state.regs.x19 = 0x4010E0
    
    # 4. Ràng buộc ký tự in được (loại bỏ ký tự rác giúp giải cực nhanh)
    for c in flag_chars:
        state.solver.add(c >= 0x20)
        state.solver.add(c <= 0x7e)

    simgr = project.factory.simulation_manager(state)

    # 5. Điểm dừng: Bỏ qua khối so sánh NEON (vì angr hay lỗi lệnh SIMD).
    # Tại 0x400B54, mọi phép mã hóa từ Custom VM đã hoàn tất và được ghi xuống Stack.
    TARGET_ADDR = 0x400B54
    
    print("[*] Đang chạy Symbolic Execution qua Custom VM (sẽ mất khoảng 30s-1p)...")
    simgr.explore(find=TARGET_ADDR)

    if simgr.found:
        print("[+] Đã qua vòng lặp VM! Bắt đầu trích xuất và đối chiếu bộ nhớ...")
        found_state = simgr.found[0]
        
        # 6. Trích xuất 3 block kết quả (mỗi block 16 bytes) từ Stack
        # var_F0 = SP + 0x150 - 0xF0 = SP + 0x60
        # var_C0 = SP + 0x150 - 0xC0 = SP + 0x90
        # var_B0 = SP + 0x150 - 0xB0 = SP + 0xA0
        
        # Để tránh lỗi Little/Big Endian của ARM, ta ép solver so sánh trực tiếp từng byte một
        for i in range(16):
            # Check khối var_F0 với xmmword_402710
            res_f0 = found_state.memory.load(sp + 0x60 + i, 1)
            exp_f0 = found_state.memory.load(0x402710 + i, 1)
            found_state.solver.add(res_f0 == exp_f0)

            # Check khối var_C0 với xmmword_402720
            res_c0 = found_state.memory.load(sp + 0x90 + i, 1)
            exp_c0 = found_state.memory.load(0x402720 + i, 1)
            found_state.solver.add(res_c0 == exp_c0)

            # Check khối var_B0 với xmmword_402730
            res_b0 = found_state.memory.load(sp + 0xA0 + i, 1)
            exp_b0 = found_state.memory.load(0x402730 + i, 1)
            found_state.solver.add(res_b0 == exp_b0)
        
        print("[*] Đang giải mã chuỗi gốc (Z3 Solver)...")
        if found_state.satisfiable():
            solution = found_state.solver.eval(flag, cast_to=bytes)
            course = solution.decode('utf-8', errors='ignore')
            print("\n" + "="*60)
            print(f"[+] TÌM THẤY 32-RUNE COURSE: {course}")
            print(f"[+] FLAG: RITSEC{{{course}}}")
            print("="*60 + "\n")
        else:
            print("[-] Không thể giải phương trình. Ràng buộc bị mâu thuẫn toán học.")
    else:
        print("[-] Không đến được đích. Hãy kiểm tra lại control flow.")

if __name__ == '__main__':
    solve()