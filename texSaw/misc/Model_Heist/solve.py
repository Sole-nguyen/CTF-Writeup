#!/usr/bin/env python3
import re
import numpy as np
import h5py


def extract_flag(model_path: str = "model.h5") -> str:
    # The challenge hides ASCII directly in secret_layer kernel values * 1000.
    ds_path = "model_weights/secret_layer/sequential/secret_layer/kernel"
    with h5py.File(model_path, "r") as f:
        kernel = f[ds_path][()]

    ints = np.round(kernel.ravel() * 1000).astype(int)
    text = "".join(chr(v) if 32 <= v < 127 else "?" for v in ints)

    m = re.search(r"texsaw\{[^}]+\}", text)
    if not m:
        raise RuntimeError("Flag not found")
    return m.group(0)


if __name__ == "__main__":
    print(extract_flag("model.h5"))
