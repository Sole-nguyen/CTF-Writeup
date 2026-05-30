#!/usr/bin/env python3
"""
UMDCTF - misc/flow - solve.py
Strategy: Attack in LATENT SPACE of RealNVP.

Key insight:
  - If we optimise delta in X-space, large delta pushes x_adv outside the
    learned data manifold, causing log_prob to drop catastrophically.
  - Instead, we optimise in Z-space (Gaussian latent space). Any Z encodes
    to a valid-looking X with high log_prob. We decode Z -> X, then clip to
    the L-inf budget around x_ref. This naturally keeps log_prob reasonable.

Attack loop:
  1. Encode x_ref -> z_ref via flow.forward.
  2. Learn perturbation dz on z_ref. Decode x_adv = flow.inverse(z_ref + dz).
  3. Clip x_adv to L-inf ball around x_ref (done as a soft penalty).
  4. Minimise: -log(p1_purified) + alpha * relu(lp_thresh - log_prob(x_adv))
                                 + gamma * relu(||x_adv - x_ref||_inf - EPS)
"""

import base64
import io
import socket
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from predictor import Predictor
from flow import RealNVP

# ── Challenge constants ───────────────────────────────────────────────────────
EPS          = 0.05
CONF_FLIP    = 0.80
PURIFY_STEPS = 3
PURIFY_ALPHA = 0.55

# ── Attack hyper-parameters ───────────────────────────────────────────────────
LR          = 5e-3
N_STEPS     = 3000
ALPHA       = 10.0   # log-prob penalty weight
GAMMA       = 50.0   # L-inf penalty weight
PRINT_EVERY = 100

HOST = "challs.umdctf.io"
PORT = 30302


# ─────────────────────────────────────────────────────────────────────────────
def load_all():
    x_ref = np.load(HERE / "reference_window.npy").astype(np.float32)
    predictor = Predictor()
    predictor.load_state_dict(torch.load(HERE / "predictor.pt", map_location="cpu"))
    predictor.eval()
    d = torch.load(HERE / "flow.pt", map_location="cpu")
    flow = RealNVP(channels=d["channels"], window=d["window"],
                   n_layers=d["n_layers"], hidden=d["hidden"])
    flow.load_state_dict(d["state_dict"])
    flow.eval()
    return x_ref, predictor, flow, float(d["threshold"])


def purify_diff(x, flow):
    for _ in range(PURIFY_STEPS):
        z, _ = flow.forward(x)
        x = flow.inverse(PURIFY_ALPHA * z)
    return x


def purify_eval(x, flow):
    with torch.no_grad():
        for _ in range(PURIFY_STEPS):
            z, _ = flow.forward(x)
            x = flow.inverse(PURIFY_ALPHA * z)
    return x


def local_check(x_adv_np, x_ref, predictor, flow, lp_thresh):
    sub = x_adv_np.astype(np.float32)
    linf = float(np.max(np.abs(sub - x_ref)))
    print(f"  L-inf    = {linf:.6f}  (limit={EPS})")

    t = torch.from_numpy(sub[None])
    with torch.no_grad():
        lp = float(flow.log_prob(t).item())
    print(f"  log_prob = {lp:.4f}  (thresh={lp_thresh:.4f})")

    with torch.no_grad():
        probs = F.softmax(predictor(purify_eval(t, flow)), dim=1).numpy()[0]
    print(f"  p(cls1)  = {probs[1]:.4f}  (need>={CONF_FLIP})")

    ok = (linf <= EPS + 1e-6) and (lp >= lp_thresh) and (probs[1] >= CONF_FLIP)
    return ok


# ─────────────────────────────────────────────────────────────────────────────
def attack_in_latent_space(x_ref, predictor, flow, lp_thresh):
    """
    Optimise dz in latent space.
    x_adv = clip(flow.inverse(z_ref + dz), x_ref-EPS, x_ref+EPS)
    """
    x_ref_t = torch.from_numpy(x_ref)         # (5, 64)
    x_ref_b = x_ref_t.unsqueeze(0)            # (1, 5, 64)

    # Encode x_ref -> z_ref
    with torch.no_grad():
        z_ref, _ = flow.forward(x_ref_b)      # (1, 320)
    print(f"  z_ref  : shape={z_ref.shape}, mean={z_ref.mean():.4f}, std={z_ref.std():.4f}")

    # Learnable perturbation in Z space
    dz = torch.zeros_like(z_ref, requires_grad=True)
    optimiser = torch.optim.Adam([dz], lr=LR)

    best_p1    = -1.0
    best_x_adv = None

    print(f"\n[*] Latent-space PGD: {N_STEPS} steps, LR={LR}, ALPHA={ALPHA}, GAMMA={GAMMA}\n")

    for step in range(1, N_STEPS + 1):
        optimiser.zero_grad()

        # Decode perturbed latent -> x_adv, then hard-clip to L-inf ball
        x_decoded = flow.inverse(z_ref + dz)          # (1, 5, 64) — with grad
        x_adv     = torch.clamp(x_decoded,
                                x_ref_b - EPS,
                                x_ref_b + EPS)         # stays on manifold AND in budget

        # Purify and classify
        x_pur  = purify_diff(x_adv, flow)
        logits = predictor(x_pur)
        log_p1 = F.log_softmax(logits, dim=1)[0, 1]
        loss_cls = -log_p1

        # Penalty: keep flow log-prob high
        lp = flow.log_prob(x_adv)[0]
        loss_lp = ALPHA * F.relu(torch.tensor(lp_thresh, dtype=torch.float32) - lp)

        # Penalty: soft L-inf constraint (should be near 0 after clamping)
        linf_viol = F.relu((x_decoded - x_ref_b).abs() - EPS).max()
        loss_linf = GAMMA * linf_viol

        loss = loss_cls + loss_lp + loss_linf
        loss.backward()
        optimiser.step()

        # Evaluate (no grad)
        with torch.no_grad():
            p1    = F.softmax(logits, dim=1)[0, 1].item()
            lp_v  = lp.item()
            linf_v = float((x_adv - x_ref_b).abs().max().item())

        if p1 > best_p1 and lp_v >= lp_thresh and linf_v <= EPS + 1e-6:
            best_p1    = p1
            best_x_adv = x_adv.detach().squeeze(0).numpy().copy()

        if step % PRINT_EVERY == 0:
            print(f"  step {step:4d}/{N_STEPS} | loss={loss.item():.3f} "
                  f"| p1={p1:.4f} | lp={lp_v:.1f} | linf={linf_v:.5f}")

        if best_p1 >= CONF_FLIP:
            if step % PRINT_EVERY == 0 or step <= 5:
                print(f"  [*] Candidate found! best_p1={best_p1:.4f}")
            # Keep going to improve
            if best_p1 >= 0.95 and step > 200:
                print(f"\n[+] High-confidence candidate at step {step}, stopping.")
                break

    print(f"\n[*] Best p1 (satisfying all constraints): {best_p1:.4f}")

    if best_x_adv is None:
        print("[!] No valid candidate found. Returning best clipped x_adv from last step.")
        with torch.no_grad():
            x_decoded = flow.inverse(z_ref + dz)
            best_x_adv = torch.clamp(x_decoded, x_ref_b - EPS, x_ref_b + EPS)
            best_x_adv = best_x_adv.squeeze(0).numpy()

    return best_x_adv


# ─────────────────────────────────────────────────────────────────────────────
def encode_submission(arr):
    buf = io.BytesIO()
    np.save(buf, arr.astype(np.float32))
    return base64.b64encode(buf.getvalue()).decode()


def submit_to_server(b64):
    print(f"\n[*] Connecting to {HOST}:{PORT} ...")
    with socket.create_connection((HOST, PORT), timeout=30) as sock:
        f = sock.makefile("rb")
        banner = b""
        while b"> " not in banner:
            c = f.read(1)
            if not c:
                break
            banner += c
        print("[server]", banner.decode(errors="replace").strip())
        sock.sendall((b64 + "\n").encode())
        print(f"[*] Sent {len(b64)} chars.")
        resp = b""
        try:
            while True:
                c = f.read(1)
                if not c:
                    break
                resp += c
        except Exception:
            pass
    resp_str = resp.decode(errors="replace").strip()
    print("\n[server]\n" + resp_str)
    return resp_str


# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  UMDCTF misc/flow  -  Latent-Space Adversarial Attack")
    print("=" * 60)

    print("\n[*] Loading models ...")
    x_ref, predictor, flow, lp_thresh = load_all()
    print(f"    x_ref     : {x_ref.shape} {x_ref.dtype}")
    print(f"    lp_thresh : {lp_thresh:.4f}")

    t0 = torch.from_numpy(x_ref[None])
    with torch.no_grad():
        lp0 = flow.log_prob(t0).item()
        p0  = F.softmax(predictor(t0), dim=1).numpy()[0]
    print(f"    baseline  : log_prob={lp0:.2f}  p0={p0[0]:.4f}  p1={p0[1]:.4f}")

    x_adv = attack_in_latent_space(x_ref, predictor, flow, lp_thresh)

    print("\n[*] Local verification:")
    ok = local_check(x_adv, x_ref, predictor, flow, lp_thresh)

    if ok:
        print("  [OK] All checks passed. Submitting ...")
    else:
        print("  [FAIL] Some checks failed. Submit anyway? [y/N]: ", end="", flush=True)
        if input().strip().lower() != "y":
            sys.exit(1)

    b64 = encode_submission(x_adv)
    resp = submit_to_server(b64)

    if "UMDCTF{" in resp:
        s = resp.index("UMDCTF{")
        e = resp.index("}", s) + 1
        print(f"\n{'='*60}")
        print(f"  FLAG: {resp[s:e]}")
        print(f"{'='*60}")
    else:
        print("\n[!] Flag not found in server response.")


if __name__ == "__main__":
    main()
