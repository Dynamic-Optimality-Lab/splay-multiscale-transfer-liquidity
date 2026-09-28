"""H5 holdout safeguards: prereg inheritance, candidate-blindness, firewall.

Runnable BEFORE any H5 randomness exists (no seed/bank required). Fail-closed
mutants for the H5 design/freeze stage.
"""
from __future__ import annotations
import ast
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "v04"


def _h4l():
    return yaml.safe_load(open(ROOT / "prereg" / "h4l_holdout.yaml").read())


def _h5():
    return yaml.safe_load(open(ROOT / "prereg" / "h5_holdout.yaml").read())


def test_h5_01_prereg_same_distribution():
    h4, h5 = _h4l(), _h5()
    assert h5["bank_id"] == "H5-R1"
    assert h5["sizes"] == h4["sizes"] == [18, 26, 34, 46, 58, 74, 98]
    assert h5["per_size"] == h4["per_size"] == 10000
    assert h5["total"] == h4["total"] == 70000
    assert h5["strata"] == h4["strata"] and len(h5["strata"]) == 12
    assert h5["quota"] == h4["quota"]
    assert h5["history_length_law"] == h4["history_length_law"]
    assert h5["tree_shape_law"] == h4["tree_shape_law"]
    assert h5["rng"] == h4["rng"]
    assert h5["dedup"] == h4["dedup"]
    assert h5["legality"] == h4["legality"]
    assert h5["serialization"] == h4["serialization"]
    assert h5["ordering"] == h4["ordering"]
    assert "no K0-K6 outcome used to tune generation" in h5["design"]


def test_h5_02_generator_inherits_frozen_semantics():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h4l_generate as H4L
    from holdout import h5_generate as H5
    assert H5.SIZES == H4L.SIZES
    assert H5.PER_SIZE == H4L.PER_SIZE
    assert H5.STRATA == H4L.STRATA
    assert H5.QUOTA == H4L.QUOTA
    assert (H5.HIST_MIN, H5.HIST_MAX) == (H4L.HIST_MIN, H4L.HIST_MAX)
    assert H5.SHAPE_MIX == {k: tuple(v) for k, v in H4L.SHAPE_MIX.items()}
    assert H5.ZSTD_LEVEL == 3
    assert H5.DOMAIN != "h4l", "H5 stream domain must differ from H4L"


def test_h5_03_generator_candidate_blind():
    src = Path(ROOT / "python" / "holdout" / "h5_generate.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
    allowed = {"__future__", "hashlib", "json", "pathlib", "holdout",
                 "holdout.h4l_generate"}
    assert imports <= allowed, "H5 generator imports forbidden modules: %s" % (imports - allowed,)
    # Token scan over code excluding the module docstring (which states the
    # prohibition itself): drop lines spanned by the first statement.
    lines = src.splitlines(keepends=True)
    first = tree.body[0]
    code_only = "".join(lines[:first.lineno - 1] + lines[first.end_lineno:])
    low = code_only.lower()
    for token in ("specialized_survivors", "phase_diagram", "wp5x_k6c2", "solver",
                  "cleanroom", "independent", "adversary"):
        assert token not in low, "H5 generator references forbidden namespace: %s" % token


def test_h5_04_seal_candidate_blind():
    src = Path(ROOT / "scripts" / "seal_h5.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module or "")
    for bad in ("solver", "cleanroom", "independent", "adversary"):
        assert not any(bad in i for i in imports), "seal imports evaluator: %s" % bad
    assert "specialized_survivors" not in src
    assert "wp5x_k6c2" not in src


def test_h5_05_episode_schema_identical_to_h4l():
    """A tiny H5 bank (same code path, small sizes/quotas) must pass H4L episode audit."""
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_generate as H5
    from holdout import h4l_verify as HV
    bank = H5.generate_bank(b"\x42" * 32, sizes=[18],
                            quotas={s: 2 for s in H5.STRATA})
    n_eps = sum(len(v) for v in bank.values())
    assert n_eps == 2 * len(H5.STRATA)
    for eps in bank.values():
        for ep in eps:
            HV.check_episode(ep)
            assert 2 <= len(ep["H"]) <= 8


def test_h5_06_determinism_and_domain_separation():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h4l_generate as H4L
    from holdout import h5_generate as H5
    seed = b"\x07" * 32
    a = H5.generate_bank(seed, sizes=[18], quotas={s: 3 for s in H5.STRATA})
    b = H5.generate_bank(seed, sizes=[18], quotas={s: 3 for s in H5.STRATA})
    ida = sorted(e["hash"] for eps in a.values() for e in eps)
    idb = sorted(e["hash"] for eps in b.values() for e in eps)
    assert ida == idb, "same seed must replay identically"
    h4 = H4L.generate_bank(seed, sizes=[18],
                           quotas={s: 3 for s in H4L.STRATA})
    idh = {e["hash"] for eps in h4.values() for e in eps}
    assert not (set(ida) & idh), "H5 bytes must differ from H4L even under same seed"


def test_h5_07_firewall_lifecycle_and_single_unlock():
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        real = FW.STATE_FILE
        FW.STATE_FILE = Path(td) / "fw.json"
        try:
            assert FW.read_state()["state"] == "EMPTY"
            with pytest.raises(FW.FirewallError):
                FW.transition("BANK_GENERATED_SECRET")
            FW.transition("GENERATOR_FROZEN")
            with pytest.raises(FW.FirewallError):
                FW.guard_bank_read()
            FW.transition("BANK_GENERATED_SECRET")
            FW.transition("COMMITMENT_PUBLISHED")
            FW.transition("CANDIDATE_SET_BOUND")
            FW.transition("REVEALED_ONCE")
            FW.guard_bank_read()
            with pytest.raises(FW.FirewallError):
                FW.transition("REVEALED_ONCE")
            with pytest.raises(FW.FirewallError):
                FW.reveal()
            FW.transition("CONSUMED")
        finally:
            FW.STATE_FILE = real


def test_h5_08_no_h5_bytes_before_freeze():
    # Pre-generation: no commitment, firewall at EMPTY/GENERATOR_FROZEN.
    # Post-generation: firewall log must show GENERATOR_FROZEN first (i.e. the
    # pushed freeze preceded all bank bytes) and unlocks <= 1.
    import sys
    sys.path.insert(0, str(ROOT / "python"))
    from holdout import h5_firewall as FW
    st = FW.read_state()
    if not (ART / "h5" / "h5_commitment.json").exists():
        assert st["state"] in ("EMPTY", "GENERATOR_FROZEN")
        assert st["unlocks"] == 0
        return
    order = [e["to"] for e in st["log"]]
    assert order[0] == "GENERATOR_FROZEN", "bank bytes predate generator freeze"
    assert st["unlocks"] <= 1


def test_h5_09_k6_binding_constants():
    k6 = json.loads((ART / "wp5x_k6c2" / "specialized_survivors.json").read_text(encoding="utf-8"))
    assert k6["count"] == 63
    assert k6["survivor_set_hash"] == "9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748"
    h5 = _h5()
    assert h5["candidate_binding"]["survivor_set_hash"] == k6["survivor_set_hash"]
    assert h5["candidate_binding"]["count"] == 63
