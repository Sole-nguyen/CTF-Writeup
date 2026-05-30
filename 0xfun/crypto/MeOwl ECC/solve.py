#!/usr/bin/env python3
from sage.all import *
import hashlib
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes

# Curve parameters
p = 1070960903638793793346073212977144745230649115077006408609822474051879875814028659881855169
a = 0
b = 19

# Points
Px = 850194424131363838588909772639181716366575918001556629491986206564277588835368712774900915
Py = 749509706400667976882772182663506383952119723848300900481860146956631278026417920626334886

Qx = 54250358642669756154015134950152636682437522715786363311759940981383592083045988845753867
Qy = 324772290891069325219931358863917293864610371020855881775477694333357303867104131696431188

aes_iv = "7d0e47bb8d111b626f0e17be5a761a14"
des_iv = "86fd0c44751700d4"
ciphertext = bytes.fromhex(
    "7d34910bca6f505e638ed22f412dbf1b50d03243b739de0090d07fb097ec0a2c"
    "a19158949f32e39cd84adea33d2229556f635237088316d2"
)

# Check if this is an anomalous curve (vulnerable to Smart's attack)
E = EllipticCurve(GF(p), [a, b])
order = E.order()

print(f"Prime p:        {p}")
print(f"Curve order:    {order}")
print(f"p == order:     {p == order}")
print()

def smart_attack(P, Q, p):
    """Manual Smart's attack implementation for anomalous curves"""
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ZZ(t) + randint(0, p) * p for t in E.a_invariants()])
    
    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break
    
    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break
    
    p_times_P = p * P_Qp
    p_times_Q = p * Q_Qp
    
    x_P, y_P = p_times_P.xy()
    x_Q, y_Q = p_times_Q.xy()
    
    phi_P = -(x_P / y_P)
    phi_Q = -(x_Q / y_Q)
    
    k = phi_Q / phi_P
    return ZZ(k)

if p == order:
    print("🚨 VULNERABLE! This is an anomalous curve - Smart's attack applies!")
    print()
    
    P = E(Px, Py)
    Q = E(Qx, Qy)
    
    print("Applying Smart's attack (fast implementation)...")
    d = smart_attack(P, Q, p)
    print(f"Recovered d = {d}")
    print()
    
    # Decrypt the flag
    k = long_to_bytes(int(d))
    aes_key = hashlib.sha256(k + b"MeOwl::AES").digest()[:16]
    des_key = hashlib.sha256(k + b"MeOwl::DES").digest()[:8]
    
    c_des = DES.new(des_key, DES.MODE_CBC, iv=bytes.fromhex(des_iv)).decrypt(ciphertext)
    flag = AES.new(aes_key, AES.MODE_CBC, iv=bytes.fromhex(aes_iv)).decrypt(unpad(c_des, 8))
    
    print(f"Flag: {flag.decode()}")
else:
    print("Curve order ≠ p, Smart's attack does not directly apply.")
