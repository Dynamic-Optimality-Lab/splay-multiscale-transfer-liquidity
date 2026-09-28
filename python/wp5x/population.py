"""WP-5X STEP X0: population reconstruction from frozen WP-4 artifacts.

Admits EXACTLY the ranking.json entries with zero dev violations that also
survived screen per screen_results.json. Asserts 6099 or fails closed. The
`promoted`/`dominated` fields are never read as filters (ranking metadata only).
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = 6099


def load_eligible(dev_dir: Path):
    """WP-5X STEP X0: returns canonical ordered list of eligible records."""
    rk = json.loads((dev_dir / "ranking.json").read_text(encoding="utf-8"))
    res = json.loads((dev_dir / "screen_results.json").read_text(encoding="utf-8"))
    elig = []
    for t in rk:
        key = t["key"]
        if t["rank"][0] != 0:
            raise ValueError("ranked entry with dev violations: %s" % key)
        s = res.get(key)
        if s is None or not s["survived"]:
            raise ValueError("ranked entry missing screen survival: %s" % key)
        P, k, C, rho = key.split("|")
        elig.append({"key": key, "P": P, "k": int(k), "C": int(C), "rho": rho,
                     "label": t["label"], "rank": t["rank"]})
    elig.sort(key=lambda e: e["key"])
    if len(elig) != EXPECTED:
        raise ValueError("admitted %d != %d; STOP FAIL-CLOSED" % (len(elig), EXPECTED))
    # WP-5X STEP X0: guard against promoted-filter/dominated-drop mutants.
    pr = json.loads((dev_dir / "promotion.json").read_text(encoding="utf-8"))
    if set(pr["promoted"]) - {e["key"] for e in elig}:
        raise ValueError("promoted key outside eligible set")
    print("[WP-5X][STEP X0] Admitted %d eligible (promoted-field ignored)" % len(elig),
          flush=True)
    return elig


def freeze_identities(elig: list, pred_hash: dict, outdir: Path):
    """WP-5X STEP X0: frozen 30-field identities (same binding as WP-4)."""
    import inspect
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from solver import search as S

    def sha(t: str) -> str:
        return hashlib.sha256(t.encode()).hexdigest()

    import liquidity.multiplicity as MU
    import solver.legality as LG
    import solver.encode as E
    norm_src = inspect.getsource(MU.normalize)
    count = 0
    for e in elig:
        P, k, C, rho_name = e["P"], e["k"], e["C"], e["rho"]
        rho = S.rho_of(rho_name)
        ident = {
            "calculus_id": "LIQ_BRANCH_A_001@C%d" % C, "rule_family_id": "LIQ_BRANCH_A_001",
            "parent_family": "SPLAY-AM-MST-LIQ-v0.4", "branch": "BRANCH_A_UNSIGNED",
            "predicate": P, "predicate_hash": pred_hash[P], "k": k, "C": C,
            "rho_profile": rho_name, "rho_hash": sha("rho_ZIG=%d,rho_DOUBLE=%d" % rho),
            "event_normalization_hash": sha(norm_src),
            "legal_domain_hash": sha(open(ROOT / "python" / "solver" / "legality.py").read()),
            "credit_types": "LATENT/ACTIVE/SPENT",
            "support": "multiset preserved (count-faithful)",
            "scale": "ladder-12", "provenance": "WP-4 synthesis search.py (WP-5X frozen copy)",
            "T7_hash": sha(inspect.getsource(E._sites_nonempty)),
            "T5_rho_hash": sha(inspect.getsource(E.exec_counts)),
            "T6_hash": sha("need=max(y-C*a,0);paid=min(act,need);T6-after-complete-B-trace"),
            "selection_order": "first-eligible ledger order",
            "A_replay_order": "T7->T5 per StepEv", "B_replay_order": "T5 per StepEv",
            "discharge_order": "T6 after complete B trace",
            "required_C_hash": sha("required_C:%d" % C),
            "energy_definition": "E=#LATENT+#ACTIVE (unsigned Branch A)",
            "initialization": "empty ledger, cursor 0",
            "snapshot_convention": "pools pre/post A/B per KEEP",
            "executor_hash": sha(open(ROOT / "python" / "solver" / "encode.py").read()),
            "mapping_version": "v0.4.1", "ontology_version": "v0.4.1",
        }
        e["identity"] = ident
        e["identity_hash"] = sha(json.dumps(ident, sort_keys=True))
        count += 1
    print("[WP-5X][STEP X0] Froze %d identities" % count, flush=True)
    return elig


def population_hash(elig: list) -> str:
    """WP-5X STEP X0: canonical ordered-set hash over exact identities."""
    h = hashlib.sha256()
    for e in elig:
        h.update(json.dumps({"key": e["key"], "identity": e["identity"],
                             "label": e["label"], "rank": e["rank"]},
                            sort_keys=True).encode())
    return h.hexdigest()
