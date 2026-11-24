"""Exact, original-ID H-family replay; all output stays in this new directory.

Mutable primitive rotations are compared against the frozen functional tuple
splay implementation after EVERY original access. No statistical proof claim.
"""
from __future__ import annotations

import bisect
import hashlib
import importlib.util
import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
sys.setrecursionlimit(30000)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
spec = importlib.util.spec_from_file_location("frozen_independent_splay", ROOT / "python/independent/splay.py")
REF = importlib.util.module_from_spec(spec)
spec.loader.exec_module(REF)
START = time.process_time()
TOTAL_ROTATIONS = 0


def weight(label, layer="M"):
    n = label[1] - label[0] + 1
    return int(n == 15) if layer == "15" else int(n >= 3 and (n & (n + 1)) == 0)


class Tree:
    def __init__(self, n):
        self.n = n
        self.root = 1
        self.left = [0] * (n + 1)
        self.right = list(range(1, n + 2))
        self.right[0] = self.right[n] = 0
        self.parent = [0] + [k - 1 for k in range(1, n + 1)]
        self.lo = list(range(n + 1))
        self.hi = [0] + [n] * n
        self.labels = {(k, n) for k in range(1, n + 1)}

    def update(self, x):
        self.lo[x] = self.lo[self.left[x]] if self.left[x] else x
        self.hi[x] = self.hi[self.right[x]] if self.right[x] else x

    def rotate(self, x):
        p = self.parent[x]
        g = self.parent[p]
        old = (self.lo[x], self.hi[x])
        if self.left[p] == x:
            direction = "RIGHT"
            middle = self.right[x]
            self.left[p] = middle
            self.right[x] = p
        else:
            assert self.right[p] == x
            direction = "LEFT"
            middle = self.left[x]
            self.right[p] = middle
            self.left[x] = p
        if middle:
            self.parent[middle] = p
        self.parent[p] = x
        self.parent[x] = g
        if not g:
            self.root = x
        elif self.left[g] == p:
            self.left[g] = x
        else:
            assert self.right[g] == p
            self.right[g] = x
        self.update(p)
        self.update(x)
        new = (self.lo[p], self.hi[p])
        assert old in self.labels and new not in self.labels and old != new
        self.labels.remove(old)
        self.labels.add(new)
        return p, g, direction, old, new

    def depth(self, x):
        d = 0
        while self.parent[x]:
            d += 1
            x = self.parent[x]
        return d

    def tuple(self):
        values = {0: REF.LEAF}
        stack = [(self.root, False)]
        while stack:
            x, ready = stack.pop()
            if not x:
                continue
            if ready:
                values[x] = REF.node(x, values[self.left[x]], values[self.right[x]])
            else:
                stack.extend([(x, True), (self.right[x], False), (self.left[x], False)])
        return values[self.root]

    def validate(self):
        got = set()
        keys = []
        stack = []
        x = self.root
        assert self.parent[x] == 0
        while stack or x:
            if x:
                assert x not in got
                got.add(x)
                if self.left[x]:
                    assert self.parent[self.left[x]] == x
                if self.right[x]:
                    assert self.parent[self.right[x]] == x
                stack.append(x)
                x = self.left[x]
            else:
                x = stack.pop()
                keys.append(x)
                x = self.right[x]
        assert keys == list(range(1, self.n + 1))
        assert len(got) == self.n
        assert self.labels == {(self.lo[k], self.hi[k]) for k in got}


def word(p, q):
    n = (1 << (p + 1)) * (q + 1) + 1
    kept = {n + 1 - (1 << j) for j in range(p + 1)}
    return n, [("prep", "D", x) for x in range(2, n + 1)] + [
        ("descent", "K" if x in kept else "D", x) for x in range(n, 0, -1)
    ] + [("forward", "K", x) for x in range(1, n + 1)] + [
        ("reverse", "K", x) for x in range(n - 1, 0, -1)
    ]


def replay(p, q, save_full=False):
    global TOTAL_ROTATIONS
    if (HERE / "FINAL_MANIFEST.json").exists():
        raise RuntimeError("Sealed run: generate new sources only in a new versioned directory.")
    n, operations = word(p, q)
    A, B = Tree(n), Tree(n)
    a_ref = b_ref = REF.vine(n)
    initial = A.tuple()
    phi = {"M": 0, "15": 0}
    snapshots = []
    events = []
    demands = []
    phase_totals = defaultdict(Counter)
    critical = []
    births = defaultdict(list)
    deaths = defaultdict(list)
    actor_deltas = defaultdict(Counter)

    def primitive(actor, tree, x, op, step, bit, typ, target, phase):
        global TOTAL_ROTATIONS
        before = phi.copy()
        fixed = B if actor == "A" else A
        old = (tree.lo[x], tree.hi[x])
        old_match = old in fixed.labels
        p_old, g_old, direction, removed, created = tree.rotate(x)
        new_match = created in fixed.labels
        if actor == "A":
            delta_psi = int(old_match) - int(new_match)
            changes = {layer: weight(created, layer) * int(new_match) - weight(removed, layer) * int(old_match) for layer in phi}
            assert all(v <= 1 for v in changes.values())
            assert typ == "ZIG" and abs(p_old - x) == 1
            assert all(l == 1 or h == n for l, h in tree.labels)
        else:
            delta_psi = int(not new_match) - int(not old_match)
            assert delta_psi in (0, -1)
            assert removed[0] <= target <= removed[1]
            assert not (created[0] <= target <= created[1])
            changes = {layer: weight(removed, layer) * int(not old_match) - weight(created, layer) * int(not new_match) for layer in phi}
        for layer, change in changes.items():
            phi[layer] += change
            actor_deltas[(phase, actor)][layer] += change
        identifier = [actor, op, step, bit]
        e = {"id": identifier, "type": typ, "direction": direction, "target": target, "promoted": x, "demoted": p_old,
             "external": g_old, "removed": removed, "created": created, "psi_delta": delta_psi,
             "phi_delta": changes, "phi_before": before, "phi_after": phi.copy()}
        if actor == "B":
            deaths[removed].append(len(events))
            births[created].append(len(events))
        events.append(e)
        TOTAL_ROTATIONS += 1
        assert TOTAL_ROTATIONS <= 200000 and time.process_time() - START <= 180
        return e

    def splay(actor, tree, target, op, phase):
        step = 0
        types = []
        local_demands = []
        while tree.parent[target]:
            step += 1
            p_old = tree.parent[target]
            g_old = tree.parent[p_old]
            if not g_old:
                typ = "ZIG"
                primitive(actor, tree, target, op, step, 0, typ, target, phase)
            else:
                frame = (tree.lo[g_old], tree.hi[g_old])
                p_side = "L" if tree.left[g_old] == p_old else "R"
                x_side = "L" if tree.left[p_old] == target else "R"
                typ = p_side + x_side
                phase_boundary = len(events)
                if p_side == x_side:
                    e0 = primitive(actor, tree, p_old, op, step, 0, typ, target, phase)
                    e1 = primitive(actor, tree, target, op, step, 1, typ, target, phase)
                else:
                    e0 = primitive(actor, tree, target, op, step, 0, typ, target, phase)
                    e1 = primitive(actor, tree, target, op, step, 1, typ, target, phase)
                if actor == "B":
                    neutral = e0["psi_delta"] == e1["psi_delta"] == 0
                    inside = frame[0] > 1 and frame[1] < n
                    d = {"id": [op, step], "type": typ, "frame": frame, "neutral": neutral, "interior": inside,
                         "U_int": neutral and inside, "before_first_bit_event": phase_boundary,
                         "created_sizes": [e["created"][1] - e["created"][0] + 1 for e in [e0, e1]]}
                    demands.append(d)
                    local_demands.append(d)
            types.append(typ)
        return types, local_demands

    for op, (phase, mode, target) in enumerate(operations, 1):
        start_phi = phi.copy()
        a_depth = A.depth(target)
        a_begin = len(events)
        a_types, _ = splay("A", A, target, op, phase)
        a_ref, ref_e = REF.trace(a_ref, target)
        assert A.tuple() == a_ref
        assert len(ref_e) == len(a_types) == (a_depth + 1) // 2
        assert A.root == target
        postA_phi = phi.copy()
        b_begin = len(events)
        b_depth = B.depth(target) if mode == "K" else 0
        b_types, ds = splay("B", B, target, op, phase) if mode == "K" else ([], [])
        if mode == "K":
            b_ref, ref_e = REF.trace(b_ref, target)
            assert B.tuple() == b_ref
            assert len(ref_e) == len(b_types) == (b_depth + 1) // 2
        A.validate()
        B.validate()
        b_events = events[b_begin:]
        u = sum(d["U_int"] for d in ds)
        dcount = -sum(e["psi_delta"] for e in b_events)
        row = {"id": op, "phase": phase, "mode": mode, "target": target, "a_depth": a_depth, "a": (a_depth + 1) // 2,
               "b_depth": b_depth, "q_B": b_depth // 2, "z_B": b_depth % 2, "u": u,
               "b0": sum(d["neutral"] for d in ds), "d": dcount, "k": int(b_depth > 0),
               "A_rotations": b_begin - a_begin, "B_rotations": len(b_events), "B_types": b_types,
               "phi_start": start_phi, "phi_postA": postA_phi, "phi_postB": phi.copy(),
               "A_phi_delta": {k: postA_phi[k] - start_phi[k] for k in phi},
               "B_phi_delta": {k: phi[k] - postA_phi[k] for k in phi}}
        for k in ["a", "q_B", "z_B", "u", "d", "k", "A_rotations", "B_rotations"]:
            phase_totals[phase][k] += row[k]
        snapshots.append(row)
        if mode == "K" and phase == "descent":
            critical.append(row)
        if op in {n - 1, 2 * n - 1, 3 * n - 1, 4 * n - 2}:
            for layer in phi:
                direct = -sum(weight(label, layer) for label in B.labels - A.labels)
                assert phi[layer] == direct
    assert A.tuple() == B.tuple() == initial
    assert len(operations) == 4 * n - 2
    assert sum(x["a"] for x in snapshots) == 4 * (n - 1)
    assert phi == {"M": 0, "15": 0}

    # Complete cyclic birth/removal records for every original U demand.
    cycle_length = len(events)
    for demand in demands:
        if not demand["U_int"]:
            continue
        label = tuple(demand["frame"])
        producer_start = next(x for x in range(demand["before_first_bit_event"], -1, -1)
                              if x == 0 or events[x - 1]["id"][1] != demand["id"][0] or events[x - 1]["id"][0] == "A")
        bs = births[label]
        ls = deaths[label]
        assert bs and ls
        bpos = bisect.bisect_left(bs, producer_start) - 1
        gamma = bs[bpos] if bpos >= 0 else bs[-1] - cycle_length
        lpos = bisect.bisect_left(ls, gamma if gamma >= 0 else gamma + cycle_length) - 1
        kappa_base = ls[lpos] if lpos >= 0 else ls[-1] - cycle_length
        kappa = kappa_base if gamma >= 0 else kappa_base - cycle_length
        assert kappa < gamma < producer_start
        demand["Gamma"] = events[gamma % cycle_length]["id"]
        demand["Gamma_lap"] = gamma // cycle_length
        demand["kappa"] = events[kappa % cycle_length]["id"]
        demand["kappa_lap"] = kappa // cycle_length
        demand["full_Pi_absence"] = "Every actual A snapshot is two-vine; this proper interior label never occurs."

    totals = {k: sum(v[k] for v in phase_totals.values()) for k in ["a", "q_B", "z_B", "u", "d", "k", "A_rotations", "B_rotations"]}
    a_growth = {k: max([0] + [e["phi_delta"][k] for e in events if e["id"][0] == "A"]) for k in phi}
    result = {"p": p, "q": q, "N": n, "length": len(operations), "prefix": [], "exact_diagonal_closure": True,
              "totals": totals, "phase_totals": {k: dict(v) for k, v in phase_totals.items()},
              "phase_potential_changes": {f"{ph}:{ac}": dict(c) for (ph, ac), c in actor_deltas.items()},
              "critical": critical, "first_forward_keep1": snapshots[2*n-1], "first_forward_keep3": snapshots[2*n+1],
              "max_A_increase": a_growth, "all_original_accesses_crosschecked": len(operations),
              "original_U_demands_with_full_cyclic_records": sum(d["U_int"] for d in demands)}
    stem = f"H_p{p}_q{q}"
    (HERE / (stem + "_summary.json")).write_text(json.dumps(result, indent=2), encoding="utf-8")
    if save_full:
        witness = {"source": {"p": p, "q": q, "N": n, "initial": "right vine", "prefix": [], "word": operations},
                   "operations": snapshots, "real_rotations": events, "all_B_double_records": demands,
                   "final_pair": "same complete labeled right vine as initial"}
        (HERE / (stem + "_complete_witness.json")).write_text(json.dumps(witness, separators=(",", ":")), encoding="utf-8")
    return result


def main():
    results = []
    for q in [1, 2, 3, 4, 7, 8, 16, 32]:
        result = replay(3, q, save_full=q in {1, 3, 7})
        assert result["critical"][0]["B_phi_delta"]["M"] == int(math.log2(result["N"])) - 1
        assert result["critical"][3]["B_phi_delta"] == {"M": -q, "15": -q}
        results.append(result)
    for p in [1, 2, 3, 4, 5, 6]:
        result = replay(p, 5, save_full=p in {3, 5})
        row = result["first_forward_keep3"]
        assert row["u"] == (p + 1) // 2
        assert row["d"] == 2 + int(p % 2 == 0)
        assert row["B_phi_delta"]["M"] == p
        results.append(result)
    overview = {"sources": [{"p": r["p"], "q": r["q"], "N": r["N"], "totals": r["totals"]} for r in results],
                "complete_original_sources": len(results), "crosschecked_original_accesses": sum(r["length"] for r in results),
                "real_rotations": TOTAL_ROTATIONS, "cpu_seconds": time.process_time() - START,
                "claims": "Exact finite replay validation only. Parametric source theorems require the separate symbolic proof.",
                "independence": "New primitive mutable implementation vs frozen functional whole-access implementation; same agent, not external certification."}
    (HERE / "REPLAY_OVERVIEW.json").write_text(json.dumps(overview, indent=2), encoding="utf-8")
    print(json.dumps(overview, indent=2))


if __name__ == "__main__":
    main()
