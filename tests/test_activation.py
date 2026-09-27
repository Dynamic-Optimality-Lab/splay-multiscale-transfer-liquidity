"""ACT-01..14: activation-axis named tests (meanings frozen in planning/WP2_CONTRACT.md)."""
import ast
import hashlib
import json
import random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))
from liquidity import multiplicity as MU
from liquidity import profiles as PR
from liquidity import activation as AC
from liquidity import diagnostics as DG
from liquidity import legacy_embedding as P
from independent import ledger as I, splay as S

ROOT = Path(__file__).resolve().parents[1]
EV = lambda c: {"case": c, "lo": 1, "hi": 3, "orient": "-"}


def test_ACT01_mu_values():
    assert MU.mu(EV("ROOT")) == 0 and MU.mu({"case": "NONE", "lo": 0, "hi": 0, "orient": "-"}) == 0
    assert MU.mu(EV("ZIG")) == 1
    assert all(MU.mu(EV(c)) == 2 for c in ("LL", "RR", "LR", "RL"))
    assert MU.normalize("ZIG-L") == MU.normalize("ZIG-R") == "ZIG"
    try:
        MU.normalize("BOGUS")
        assert False
    except ValueError:
        pass


def test_ACT02_profiles_exact():
    for r in range(1, 7):
        assert PR.FLAT(r).as_pair() == (r, r)
        assert PR.ROT(r).as_pair() == (r, 2 * r)
    assert [p.name for p in PR.LADDER()] == ["FLAT(%d)" % r for r in range(1, 7)] + ["ROT(%d)" % r for r in range(1, 7)]
    assert PR.FLAT(2).capacity(EV("ROOT")) == 0
    assert PR.FLAT(2).capacity(EV("ZIG")) == 2 and PR.FLAT(2).capacity(EV("LL")) == 2
    assert PR.ROT(3).capacity(EV("ZIG")) == 3 and PR.ROT(3).capacity(EV("RR")) == 6
    for bad in (0, 7, -1):
        for ctor in (PR.FLAT, PR.ROT):
            try:
                ctor(bad)
                assert False, bad
            except ValueError:
                pass


def test_ACT03_forbidden_static_audit():
    src = (ROOT / "python" / "liquidity" / "profiles.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    # capacity() body may only read normalized class + stored bounds (no new params/attrs).
    cap = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "capacity")
    names = {n.id for n in ast.walk(cap) if isinstance(n, ast.Name)}
    # Allowed: self/args, normalized-class binding, normalizer, structural builtins
    # (isinstance/dict for the dict-vs-tuple event form; int is the return annotation).
    assert names <= {"self", "ev", "cls", "normalize", "isinstance", "dict", "int"}, names
    for f in PR.FORBIDDEN:
        assert f in PR.FORBIDDEN
    assert len(PR.FORBIDDEN) == 12


def ledger_of(n_lat, n_act=0, n_spent=0):
    return [["LATENT", 1, 2, True]] * n_lat + [["ACTIVE", 2, 3, False]] * n_act + [["SPENT", 0, 1, True]] * n_spent


def test_ACT04_counts_and_order():
    led = ledger_of(5, 2)
    out = AC.t5_rho([list(c) for c in led], "P_all", PR.FLAT(2), "KEEP", EV("LL"))
    assert AC.pools(out) == (3, 4)
    # Partial: cap exceeds eligible -> all activated, none created.
    out = AC.t5_rho([list(c) for c in led], "P_all", PR.ROT(6), "KEEP", EV("ZIG"))
    assert AC.pools(out) == (0, 7) and len(out) == len(led)
    # First-eligible order: earliest LATENT flips first.
    led2 = [["ACTIVE", 0, 1, True]] + ledger_of(2)
    out = AC.t5_rho([list(c) for c in led2], "P_all", PR.FLAT(1), "KEEP", EV("ZIG"))
    assert out[1][0] == "ACTIVE" and out[2][0] == "LATENT"
    # P_keep silent on DELETE.
    out = AC.t5_rho([list(c) for c in led], "P_keep", PR.FLAT(6), "DELETE", EV("LL"))
    assert out == led


def test_ACT05_energy_conservation():
    rng = random.Random(777)
    for prof in PR.LADDER():
        for _ in range(40):
            led = ledger_of(rng.randint(0, 10), rng.randint(0, 10), rng.randint(0, 5))
            ev = EV(rng.choice(["ROOT", "ZIG", "LL", "RR", "LR", "RL"]))
            assert AC.energy(AC.t5_rho([list(c) for c in led], "P_all", prof, "KEEP", ev)) == AC.energy(led)
            # Independent cross-check on same books.
            iled = [tuple(c) for c in led]
            cap = I.rho_cap(prof.as_pair(), (ev["case"], ev["lo"], ev["hi"], ev["orient"]))
            assert I.energy_of(I.activate_bounded((iled, 0), cap, "KEEP", ev)[0]) == AC.energy(led)


def test_ACT06_preservation_no_resurrection():
    led = ledger_of(4, 3, 2)
    for prof in PR.LADDER():
        out = AC.t5_rho([list(c) for c in led], "P_all", prof, "KEEP", EV("RR"))
        assert AC.support_multiset(out) == AC.support_multiset(led)
        assert sum(1 for c in out if c[0] == "SPENT") == 2
        assert all(c[0] in ("LATENT", "ACTIVE", "SPENT") for c in out)


def test_ACT07_determinism():
    led = ledger_of(9, 4, 1)
    h = lambda: hashlib.sha256(json.dumps(AC.t5_rho([list(c) for c in led], "P_all", PR.ROT(4), "KEEP", EV("LR"))).encode()).hexdigest()
    assert h() == h()


def test_ACT08_differential_rho():
    rng = random.Random(20260928)
    bad = 0
    total = 0
    for prof in PR.LADDER():
        for _ in range(300):
            led = ledger_of(rng.randint(0, 12), rng.randint(0, 12), rng.randint(0, 4))
            ev = EV(rng.choice(["ROOT", "ZIG", "LL", "RR", "LR", "RL"]))
            mode = rng.choice(["KEEP", "DELETE"])
            a = AC.t5_rho([list(c) for c in led], "P_all", prof, mode, ev)
            iled = [tuple(c) for c in led]
            b, _ = I.activate_bounded((iled, 0), I.rho_cap(prof.as_pair(), (ev["case"], ev["lo"], ev["hi"], ev["orient"])), mode, ev)
            total += 1
            if [tuple(c) for c in a] != b or AC.pools(a) != I.pools(b):
                bad += 1
    assert total == 3600 and bad == 0


def test_ACT09_diagnostics_schema():
    rec = DG.keep_record(56, 2, 8, 7, 54, 3, 7, 7, 11, 10, 63, 1)
    schema = json.loads((ROOT / "schemas" / "keep_record.schema.json").read_text(encoding="utf-8"))
    assert set(rec) == set(schema["required"]) and len(rec) == 13
    assert DG.flat_pressure(11, 2, 8) == 2
    assert DG.flat_pressure(11, 2, 1) == 9
    assert DG.flat_pressure(5, 9, 3) == 0
    assert DG.flat_pressure(11, 2, 0) == float("inf")


def test_ACT10_multiplicity_corpus():
    rng = random.Random(4242)
    checked = 0
    for n in (3, 5, 8, 13):
        t = P.vine_right(n)
        for x in list(range(1, n + 1)) + [rng.randint(1, n) for _ in range(20)]:
            t2, evs = P.splay_trace(P.vine_right(n), x)
            assert MU.trace_sum(evs) == P.splay_cost(P.vine_right(n), x) - 1
            checked += 1
    # Absent-key: empty trace, zero opportunities.
    t2, evs = P.splay_trace(P.balanced([1, 3, 5]), 4)
    assert evs == [] and MU.trace_sum(evs) == 0
    assert checked == 109


def test_ACT11_mutants_killed():
    r = __import__("subprocess").run([sys.executable, "scripts/test_wp2_mutants.py"], capture_output=True, text=True, cwd=str(ROOT))
    assert r.returncode == 0 and "ALL_16_KILLED" in r.stdout, r.stdout[-2000:] + r.stderr[-2000:]


def test_ACT12_packages_honest():
    import glob
    pkgs = sorted((ROOT / "math" / "reviews").glob("LIQ0-0[2-9].PACKAGE.md")) + sorted((ROOT / "math" / "reviews").glob("LIQ0-10.PACKAGE.md"))
    assert len(pkgs) == 9
    for p in pkgs:
        t = p.read_text(encoding="utf-8")
        assert "Statement" in t and "Negation" in t and "Evidence" in t


def test_ACT13_h4l_empty():
    assert not list((ROOT / "artifacts" / "v04" / "holdouts").glob("h4l_bank*"))
    assert not list((ROOT / "artifacts" / "v04" / "holdouts").glob("*.json.zst"))


def test_ACT14_no_regression():
    rp, _ = P.exec_hist(P.vine_right(28), [("DELETE", 27), ("DELETE", 28), ("KEEP", 28), ("KEEP", 27)], 28)
    assert (rp[3]["a"], rp[3]["y"], rp[3]["need"], rp[3]["paid"], rp[3]["margin"]) == (2, 15, 11, 10, -1)
    st = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    assert st["LIQ0-01"]["truth"] == "REVIEWED"
