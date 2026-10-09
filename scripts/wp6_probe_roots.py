"""Probe: root-var columns of SH567 J4 matrix + s0 padding gap minimum."""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def main():
    vm = json.load(open(OUT / "j4_sh567_vmap.json"))["vmap"]
    rkeys = sorted([k for k in vm if k.startswith("('r'")])
    print("[PR] root vars:", rkeys, flush=True)
    Z = np.load(OUT / "j4_sh567_A.npz")
    A = Z["A"].astype(np.int64)
    inv = {i: k for k, i in vm.items()}
    for i in range(A.shape[1]):
        if inv[i].startswith("('r'"):
            col = A[:, i]
            print(f"[PR] {inv[i]} nnz={int((col != 0).sum())} sum={int(col.sum())}", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
