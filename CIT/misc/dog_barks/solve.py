import numpy as np
from scipy.io import wavfile

def decode_barks_binary(filepath):
    sample_rate, data = wavfile.read(filepath)
    # Chuyển về Mono nếu là file âm thanh Stereo
    if len(data.shape) > 1:
        data = data.mean(axis=1)
        
    data = np.abs(data)
    
    # 1. Tìm đường bao (Envelope) để lấy đỉnh của từng tiếng sủa (Khung 50ms)
    window = int(sample_rate * 0.05)
    frames = len(data) // window
    reshaped = data[:frames * window].reshape(frames, window)
    envelopes = np.max(reshaped, axis=1)
    
    # 2. Lọc bỏ các khoảng lặng, chỉ giữ lại các "cục" âm thanh
    thresh = np.max(envelopes) * 0.1
    is_sound = envelopes > thresh
    
    changes = np.where(is_sound[:-1] != is_sound[1:])[0]
    changes = np.insert(changes, 0, 0)
    changes = np.append(changes, len(envelopes) - 1)
    
    peaks = []
    for i in range(len(changes) - 1):
        if is_sound[changes[i] + 1]:
            # Lấy mức biên độ cao nhất của tiếng sủa này
            peak = np.max(envelopes[changes[i]:changes[i+1]])
            peaks.append(peak)
            
    if not peaks:
        return "Lỗi: Không tìm thấy tiếng sủa."
        
    # 3. Phân loại Sủa To và Sủa Nhỏ dựa trên mức trung bình cộng
    mid_point = np.mean([np.min(peaks), np.max(peaks)])
    
    binary_str = ""
    for p in peaks:
        binary_str += "1" if p > mid_point else "0"
        
    print(f"[*] Đã bắt được tổng cộng: {len(peaks)} tiếng sủa (bits)")
    print(f"[*] Chuỗi Binary thô: {binary_str}")
    
    # 4. Giải mã Binary thành Text ASCII (8 bit = 1 ký tự)
    # Cắt bỏ các bit lẻ ở cuối nếu không gom đủ 8 bit
    clean_bin = binary_str[:len(binary_str) - (len(binary_str) % 8)]
    
    flag_normal = ""
    flag_inverted = ""
    
    for i in range(0, len(clean_bin), 8):
        byte = clean_bin[i:i+8]
        # Dịch mã xuôi
        flag_normal += chr(int(byte, 2))
        
        # Dịch mã ngược (Trường hợp Sủa To = 0, Sủa Nhỏ = 1)
        inv_byte = "".join(['1' if b == '0' else '0' for b in byte])
        flag_inverted += chr(int(inv_byte, 2))
        
    print("-" * 30)
    print(f"[+] Flag Option 1 (To=1, Nhỏ=0): {flag_normal}")
    print(f"[+] Flag Option 2 (To=0, Nhỏ=1): {flag_inverted}")

if __name__ == "__main__":
    decode_barks_binary("challenge.wav")
