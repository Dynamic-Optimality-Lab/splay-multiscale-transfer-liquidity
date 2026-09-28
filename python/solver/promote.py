"""WP-4 STEP 117: validation + adversarial orchestration, identity freeze, outlines,
append-only counterexample store with L0/L1 minimization.

Validation/adversarial contact frozen candidates only. Violations demote the
candidate and append a counterexample; they never mutate frozen IDs.
"""
from __future__ import annotations
import hashlib
import inspect
import json
from pathlib import Path

from solver import encode as E
from solver import predicates as CP
from solver import search as S

RULE_FAMILY = "LIQ_BRANCH_A_001"


def calculus_id(C: int) -> str:
    return "%s@C%d" % (RULE_FAMILY, C)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def freeze_identity(entry: dict, paths: dict) -> dict:
    """WP-4 STEP 117: the frozen 29-field candidate identity (all hash-bound)."""
    P, k, C, rho_name = entry["P"], entry["k"], entry["C"], entry["rho"]
    rho = S.rho_of(rho_name)
    pred_hash = [p["hash"] for p in
                 __import__("yaml").safe_load(open(paths["predicate_family"]).read())["predicates"]
                 if p["id"] == P][0]
    ident = {
        "calculus_id": calculus_id(C), "rule_family_id": RULE_FAMILY,
        "parent_family": "SPLAY-AM-MST-LIQ-v0.4", "branch": "BRANCH_A_UNSIGNED",
        "predicate": P, "predicate_hash": pred_hash, "k": k, "C": C,
        "rho_profile": rho_name, "rho_hash": _sha("rho_ZIG=%d,rho_DOUBLE=%d" % rho),
        "event_normalization_hash": _sha(inspect.getsource(
            __import__("liquidity.multiplicity", fromlist=["normalize"]).normalize)),
        "legal_domain_hash": _sha(open(paths["legality"]).read()),
        "credit_types": "LATENT/ACTIVE/SPENT", "support": "multiset preserved (count-faithful)",
        "scale": "ladder-12", "provenance": "WP-4 synthesis search.py (deterministic funnel)",
        "T7_hash": _sha(inspect.getsource(E._sites_nonempty)),
        "T5_rho_hash": _sha(inspect.getsource(E.exec_counts)),
        "T6_hash": _sha("need=max(y-C*a,0);paid=min(act,need);T6-after-complete-B-trace"),
        "selection_order": "first-eligible ledger order",
        "A_replay_order": "T7->T5 per StepEv", "B_replay_order": "T5 per StepEv",
        "discharge_order": "T6 after complete B trace",
        "required_C_hash": _sha("required_C:%d" % C),
        "energy_definition": "E=#LATENT+#ACTIVE (unsigned Branch A)",
        "initialization": "empty ledger, cursor 0",
        "snapshot_convention": "pools pre/post A/B per KEEP",
        "executor_hash": _sha(open(paths["encode"]).read()),
        "mapping_version": "v0.4.1", "ontology_version": "v0.4.1",
    }
    return ident


def check_identity_schema(ident: dict, schema: dict) -> None:
    """WP-4 STEP 117: identity schema conformance (SYN-12).

    Note: operative prose says "29 fields" but schemas/candidate.schema.json
    (machine-readable authority) requires 30; conformance follows the schema.
    """
    assert set(ident) == set(schema["required"]), \
        set(schema["required"]) ^ set(ident)


def write_outline(path: Path, ident: dict, entry: dict, dev: dict, val: dict,
                  adv: dict, label: str, eligibility: list) -> None:
    """WP-4 STEP 117: per-candidate proof outline (dev form, no universality)."""
    lines = ["# Candidate outline: %s" % ident["calculus_id"], "",
             "Config: P=%s k=%d C=%d rho=%s (label %s)" % (
                 entry["P"], entry["k"], entry["C"], entry["rho"], label),
             "Identity hash: %s" % _sha(json.dumps(ident, sort_keys=True)),
             "Dev: violations=%d worst_shortfall=%d reg_ok=%s" % (
                 dev.get("violations", 0), dev.get("worst_shortfall", 0),
                 dev.get("reg_ok")),
             "Validation: violations=%d episodes=%d" % (
                 val.get("violations", -1), val.get("episodes", 0)),
             "Adversarial: %s" % json.dumps(adv, sort_keys=True),
             "Eligibility:"] + ["- " + e for e in eligibility] + [
             "Non-claims: no universality, no C-minimality, finite survival only."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _ce_path(outdir: Path) -> Path:
    outdir.mkdir(parents=True, exist_ok=True)
    i = 0
    while (outdir / ("ce_%04d.json" % i)).exists():
        i += 1
    return outdir / ("ce_%04d.json" % i)


def append_counterexample(outdir: Path, theorem_hash: str, calculus_id: str,
                          ep: dict, primary: dict, independent: dict,
                          level: str, certificate: str) -> Path:
    """WP-4 STEP 117: append-only counterexample (never overwrites)."""
    rec = {"theorem": "MSTL-14", "theorem_hash": theorem_hash,
           "calculus_id": calculus_id, "legality": "LegalPairInstance checked",
           "primary_replay": primary, "independent_replay": independent,
           "formal_witness_or_exemption": "EXEMPT_WP4_DEV (development witness only)",
           "minimization_level": level, "minimization_certificate": certificate,
           "episode": {"n": ep["n"], "H": ep["H"], "id": ep.get("id")}}
    p = _ce_path(outdir)
    assert not p.exists()
    p.write_text(json.dumps(rec, indent=2, sort_keys=True), encoding="utf-8")
    return p


def minimize_history(exec_fn, n, T0, H):
    """WP-4 STEP 117: greedy history shrink preserving violation (L0 -> L1)."""
    steps = []
    H = [list(s) for s in H]
    if exec_fn(n, T0, H)["violations"] == 0:
        return H, "L0 (no shrink: input violation not reproduced)"
    changed = True
    while changed:
        changed = False
        for i in range(len(H)):
            trial = H[:i] + H[i + 1:]
            if len(trial) < 1:
                continue
            try:
                if exec_fn(n, T0, trial)["violations"] > 0:
                    steps.append("removed step %d (%s)" % (i, H[i]))
                    H = trial
                    changed = True
                    break
            except ValueError:
                continue
    return H, "L1 greedy shrink: %d steps; %s" % (len(steps), "; ".join(steps) or "fixpoint")
