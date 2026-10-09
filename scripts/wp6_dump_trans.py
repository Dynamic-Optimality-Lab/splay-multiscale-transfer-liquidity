"""Dump uniform L/R/NONE lambda-transition tables from j4_padding.json."""
import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine/j4_padding.json"))
for key in sorted(d):
    if "_L" in key or "_R" in key:
        print("=" * 70)
        print(key, "checked=", d[key]["checked"])
        print("--- lambda_changes [slot, lam->lam', count]:")
        for e in d[key]["lambda_changes"]:
            print("   ", e)
        print("--- c_pairs [(c->c'), count]:")
        for e in d[key]["c_pairs"]:
            print("   ", e)
