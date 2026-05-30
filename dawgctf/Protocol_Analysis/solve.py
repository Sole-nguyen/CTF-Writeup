import os
import re
import requests

BASE_URL = "https://protocols.live"
HEADERS = {"Content-Type": "application/json"}


def init_chal(chal_no):
    res = requests.post(f"{BASE_URL}/model/{chal_no}")
    res.raise_for_status()
    return res.json().get("conn_id")


def send_msg(conn_id, target, content):
    payload = {"conn_id": conn_id, "content": content}
    res = requests.post(f"{BASE_URL}/{target}", json=payload, headers=HEADERS)
    res.raise_for_status()
    return res.json().get("content")


def parse_items(content):
    if not content:
        return []
    return [tuple(part.split(":", 1)) for part in content.split("|") if part]


def get_values(content, key):
    return [value for k, value in parse_items(content) if k == key]


def get_last(content, key):
    values = get_values(content, key)
    return values[-1] if values else None


def util_call(conn_id, endpoint, content):
    res = requests.post(
        f"{BASE_URL}/util/{endpoint}",
        json={"conn_id": conn_id, "content": content},
        headers=HEADERS,
    )
    res.raise_for_status()
    return res.json().get("content")


def gen_asym_key_pair(conn_id):
    content = util_call(conn_id, "gen_asym_key_pair", "none")
    keys = [value for key, value in parse_items(content) if key == "k"]
    return keys[0], keys[1]


def get_cert(conn_id, pub, name):
    content = util_call(conn_id, "get_cert", f"k:{pub}|n:{name}")
    return content.split(":", 1)[1] if content else None


def asym_encrypt(conn_id, pub, text):
    content = util_call(conn_id, "asym_encrypt", f"k:{pub}|t:{text}")
    return content.split(":", 1)[1] if content else None


def asym_decrypt(conn_id, priv, data_hex):
    return util_call(conn_id, "asym_decrypt", f"k:{priv}|d:{data_hex}")


def asym_sign(conn_id, priv, text):
    content = util_call(conn_id, "asym_sign", f"k:{priv}|t:{text}")
    return content.split(":", 1)[1] if content else None


def hash_data(conn_id, data_hex):
    content = util_call(conn_id, "hash_data", f"d:{data_hex}")
    return content.split(":", 1)[1] if content else None


def sym_decrypt(conn_id, key_hex, nonce_hex, data_hex):
    return util_call(conn_id, "sym_decrypt", f"k:{key_hex}|d:{nonce_hex}|d:{data_hex}")


def extract_flag(content):
    if not content:
        return None
    match = re.search(r"DawgCTF\\{[^}]+\\}", content)
    if match:
        return match.group(0)
    t_vals = get_values(content, "t")
    return t_vals[-1] if t_vals else content


def solve_challenge_1():
    print("[*] Challenge 1...")
    cid = init_chal(1)
    msg = "t:Hello|n:bob|t:this is|n:alice|t: give me the flag"
    bob_resp = send_msg(cid, "bob", msg)
    flag = extract_flag(bob_resp)
    print(f"[!] Flag 1: {flag}\n")


def solve_challenge_2():
    print("[*] Challenge 2...")
    cid = init_chal(2)
    msg = "t:Hello|n:bob|t: this is|n:charlie|t: give me the flag"
    bob_resp = send_msg(cid, "bob", msg)
    flag = extract_flag(bob_resp)
    print(f"[!] Flag 2: {flag}\n")


def solve_challenge_3():
    print("[*] Challenge 3...")
    cid = init_chal(3)
    msg = "t:Hello|n:bob|t: this is|n:alice|t: give me the flag"
    bob_resp = send_msg(cid, "bob", msg)
    flag = extract_flag(bob_resp)
    print(f"[!] Flag 3: {flag}\n")


def solve_challenge_4():
    print("[*] Challenge 4...")
    cid = init_chal(4)
    alice_msg = send_msg(cid, "alice", "t:hello")
    key = get_last(alice_msg, "k")
    nonce = get_last(alice_msg, "d")
    bob_resp = send_msg(cid, "bob", alice_msg)
    enc = get_last(bob_resp, "d")
    plain = sym_decrypt(cid, key, nonce, enc)
    flag = extract_flag(plain)
    print(f"[!] Flag 4: {flag}\n")


def solve_challenge_5():
    print("[*] Challenge 5...")
    cid = init_chal(5)
    pub, priv = gen_asym_key_pair(cid)
    msg = (
        "t:Hello|n:bob|t:this is|n:alice|t:send the flag encrypted under this asymetric key"
        f"|k:{pub}"
    )
    bob_resp = send_msg(cid, "bob", msg)
    enc = get_last(bob_resp, "d")
    plain = asym_decrypt(cid, priv, enc)
    flag = extract_flag(plain)
    print(f"[!] Flag 5: {flag}\n")


def solve_challenge_6():
    print("[*] Challenge 6...")
    cid = init_chal(6)
    bob_first = send_msg(cid, "bob", "t:hello")
    pub_b = get_last(bob_first, "k")
    pub_x, priv_x = gen_asym_key_pair(cid)
    name = "mallory"
    cert_x = get_cert(cid, pub_x, name)
    alice_enc = send_msg(cid, "alice", f"k:{pub_x}|n:{name}|d:{cert_x}")
    enc_x = get_last(alice_enc, "d")
    plain = asym_decrypt(cid, priv_x, enc_x)
    n_a = get_values(plain, "d")[0]
    enc_b = asym_encrypt(cid, pub_b, plain)
    bob_resp = send_msg(cid, "bob", f"d:{enc_b}")
    alice_resp = send_msg(cid, "alice", bob_resp)
    enc_x2 = get_last(alice_resp, "d")
    n_b_plain = asym_decrypt(cid, priv_x, enc_x2)
    n_b = get_last(n_b_plain, "d")
    enc_nb = asym_encrypt(cid, pub_b, f"d:{n_b}")
    flag_msg = send_msg(cid, "bob", f"d:{enc_nb}")
    flag_ct = get_last(flag_msg, "d")
    key = hash_data(cid, n_a + n_b)
    nonce = key[:24]
    plain_flag = sym_decrypt(cid, key, nonce, flag_ct)
    flag = extract_flag(plain_flag)
    print(f"[!] Flag 6: {flag}\n")


def solve_challenge_7():
    print("[*] Challenge 7...")
    cid = init_chal(7)
    alice_msg = send_msg(cid, "alice", "t:hello")
    n_a = get_last(alice_msg, "d")
    bob_resp = send_msg(cid, "bob", alice_msg)
    n_b = get_values(bob_resp, "d")[1]
    pub_x, priv_x = gen_asym_key_pair(cid)
    name = "mallory"
    cert_x = get_cert(cid, pub_x, name)
    sig_text = f"n:{name}|d:{n_b}|d:{n_a}"
    sig_x = asym_sign(cid, priv_x, sig_text)
    alice_resp = send_msg(
        cid,
        "alice",
        f"k:{pub_x}|n:{name}|d:{cert_x}|d:{n_b}|d:{sig_x}",
    )
    bob_final = send_msg(cid, "bob", alice_resp)
    flag = extract_flag(bob_final)
    print(f"[!] Flag 7: {flag}\n")


def solve_challenge_8():
    print("[*] Challenge 8...")
    cid = init_chal(8)
    send_msg(cid, "bob", "t:hello")
    pub_x, priv_x = gen_asym_key_pair(cid)
    name = "mallory"
    cert_x = get_cert(cid, pub_x, name)
    n_x1 = os.urandom(32).hex()
    bob_resp = send_msg(cid, "bob", f"k:{pub_x}|n:{name}|d:{cert_x}|d:{n_x1}")
    n_b = get_values(bob_resp, "d")[0]
    n_x2 = os.urandom(32).hex()
    sig_text = f"n:bob|d:{n_b}|d:{n_x2}"
    sig_x = asym_sign(cid, priv_x, sig_text)
    bob_final = send_msg(cid, "bob", f"d:{n_x2}|d:{sig_x}")
    flag = extract_flag(bob_final)
    if not flag:
        raise RuntimeError("Challenge 8 did not return a flag.")
    print(f"[!] Flag 8: {flag}\n")


def solve_challenge_9():
    print("[*] Challenge 9...")
    cid = init_chal(9)
    alice_msg = send_msg(cid, "alice", "t:hello")
    bob_resp = send_msg(cid, "bob", alice_msg)
    pub_b = get_last(bob_resp, "k")
    cert_b = get_values(bob_resp, "d")[0]
    outer_ct = get_values(bob_resp, "d")[1]
    oracle_req = f"k:{pub_b}|n:bob|d:{cert_b}|d:{outer_ct}|n:alice"
    oracle_resp = send_msg(cid, "alice", oracle_req)
    if not oracle_resp:
        raise RuntimeError("Challenge 9 oracle rejected the request.")
    # Oracle response is encrypted under Bob's public key. A private-key bypass is needed here.
    raise RuntimeError("Challenge 9 requires bypassing Bob's key; not implemented.")


if __name__ == "__main__":
    solve_challenge_1()
    solve_challenge_2()
    solve_challenge_3()
    solve_challenge_4()
    solve_challenge_5()
    solve_challenge_6()
    solve_challenge_7()
    solve_challenge_8()
    solve_challenge_9()
