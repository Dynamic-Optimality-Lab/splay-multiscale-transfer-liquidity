"""Original paired trees and the FROZEN H=5 bank; no early failure exit.

Only standard-library dependencies. All physical keys, including never-accessed
keys, are retained. A DELETE splays A and removes no vertex.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
POLICY = "selected_H5_target_middle2_external_grandparent_parent_middle1"
H = 5


def read(path):
    path = Path(path)
    with (gzip.open(path, "rt", encoding="utf-8") if path.suffix == ".gz"
          else path.open(encoding="utf-8")) as stream:
        return json.load(stream)


def write(path, value):
    path = Path(path)
    path = (path if path.is_absolute() else HERE / path).resolve()
    assert path.is_relative_to(HERE), "All artifacts stay inside this checkpoint."
    assert not (HERE / "FINAL_MANIFEST.json").exists(), "Sealed checkpoint."
    assert not path.exists(), "Never overwrite a research artifact."
    path.parent.mkdir(parents=True, exist_ok=True)
    with (gzip.open(path, "wt", encoding="utf-8") if path.suffix == ".gz"
          else path.open("w", encoding="utf-8")) as stream:
        json.dump(value, stream, separators=(",", ":") if path.suffix == ".gz" else None,
                  indent=None if path.suffix == ".gz" else 2)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


class Tree:
    """Dense rank arrays internally; event labels remain actual original keys."""
    def __init__(self, state, keys):
        self.keys = list(keys)
        self.index = {key: i + 1 for i, key in enumerate(keys)}
        assert set(map(int, state["children"])) == set(keys)
        n = len(keys)
        self.child = [[0, 0] for _ in range(n + 1)]
        self.parent = [0] * (n + 1)
        self.root = self.index[state["root"]]
        for key in keys:
            v = self.index[key]
            for side, child in enumerate(state["children"][str(key)]):
                if child is not None:
                    c = self.index[child]
                    assert not self.parent[c]
                    self.child[v][side] = c
                    self.parent[c] = v
        assert self.parent[self.root] == 0
        seen = set()
        stack = [(self.root, 0, n + 1)]
        while stack:
            v, lo, hi = stack.pop()
            assert lo < v < hi and v not in seen
            seen.add(v)
            l, r = self.child[v]
            if l:
                stack.append((l, lo, v))
            if r:
                stack.append((r, v, hi))
        assert len(seen) == n

    def label(self, v):
        return self.keys[v - 1] if v else None

    def owner(self, v):
        assert v
        return (v - 1) // 5

    def flat(self):
        return tuple([self.root] + [c for row in self.child[1:] for c in row])

    def state(self):
        return {"root": self.label(self.root), "children": {
            str(key): [self.label(c) for c in self.child[i + 1]]
            for i, key in enumerate(self.keys)}}

    def rotate(self, v):
        p = self.parent[v]
        assert p
        g = self.parent[p]
        side = int(self.child[p][1] == v)
        middle = self.child[v][1 - side]
        bit = {"promoted": self.label(v), "demoted": self.label(p),
               "grandparent": self.label(g), "middle": self.label(middle)}
        self.child[p][side] = middle
        if middle:
            self.parent[middle] = p
        self.child[v][1 - side] = p
        self.parent[p] = v
        self.parent[v] = g
        if g:
            self.child[g][int(self.child[g][1] == p)] = v
        else:
            self.root = v
        return bit

    def steps(self, key):
        x = self.index[key]
        while self.parent[x]:
            p = self.parent[x]
            g = self.parent[p]
            typ = "ZIG" if not g else ("L" if p < g else "R") + ("L" if x < p else "R")
            pivots = [x] if not g else [p, x] if typ in ("LL", "RR") else [x, x]
            yield typ, [self.rotate(v) for v in pivots]


def _scope_priority(bits, typ, key, actor, owner):
    scope = sorted({owner[v] for bit in bits for v in bit.values() if v is not None})
    target = owner[key]
    order = [target] + [b for b in scope if b != target]
    if actor == "B" and typ in ("LL", "RR"):
        first, second = bits
        roles = [key, second["middle"], first["grandparent"],
                 first["demoted"], second["demoted"], first["middle"]]
        order = []
        for v in roles:
            if v is not None and owner[v] not in order:
                order.append(owner[v])
    assert set(order) == set(scope) and len(scope) <= 8
    return scope, order


def compile_source(source, *, require_closed=True, states=False):
    keys = sorted(map(int, source["initial_A"]["children"]))
    assert keys and len(keys) == len(set(keys))
    a = Tree(source["initial_A"], keys)
    b = Tree(source["initial_B"], keys)
    diagonal = source.get("diagonal") or source["initial_A"]
    ra, rb = Tree(diagonal, keys), Tree(diagonal, keys)
    for mode, key in source.get("prefix", []):
        assert mode in ("K", "D")
        list(ra.steps(key))
        if mode == "K":
            list(rb.steps(key))
    assert (ra.flat(), rb.flat()) == (a.flat(), b.flat()), "Invalid reaching prefix."
    initial = (a.flat(), b.flat())
    owner = {v: i // 5 for i, v in enumerate(keys)}
    events, operations, snapshots = [], [], [initial] if states else []
    total_a = total_q = kb = physical_a = physical_b = 0
    for op, (mode, key) in enumerate(source["operations"], 1):
        assert mode in ("K", "D") and key in owner
        genuine = int(mode == "K" and b.label(b.root) != key)
        kb += genuine
        if genuine:
            events.append({"id": ["K", op], "a": 0, "q": 0, "k": 1,
                           "target": key, "scope": [owner[key]],
                           "priority": [owner[key]], "type": "VOUCHER", "bits": []})
        start = len(events)
        ac = qc = 0
        for actor, tree in (("A", a), ("B", b)) if mode == "K" else (("A", a),):
            for step, (typ, bits) in enumerate(tree.steps(key), 1):
                scope, order = _scope_priority(bits, typ, key, actor, owner)
                aa = int(actor == "A")
                qq = int(actor == "B" and len(bits) == 2)
                ac += aa
                qc += qq
                physical_a += len(bits) if aa else 0
                physical_b += len(bits) if not aa else 0
                events.append({"id": [actor, op, step], "a": aa, "q": qq,
                               "k": 0, "target": key, "scope": scope,
                               "priority": order, "type": typ, "bits": bits})
        total_a += ac
        total_q += qc
        operations.append({"id": op, "mode": mode, "target": key, "a": ac,
                           "q": qc, "k": genuine, "events": [start, len(events)]})
        if states:
            snapshots.append((a.flat(), b.flat()))
    closed = (a.flat(), b.flat()) == initial
    if require_closed:
        assert closed, "Both full labeled trees must close."
        assert kb <= total_a, "Cyclic genuine-KEEP gap injection."
    for name, value in (("expected_A", total_a), ("expected_Q", total_q)):
        if source.get(name) is not None:
            assert source[name] == value
    return {"source": source, "keys": keys, "blocks": [keys[i:i+5] for i in range(0, len(keys), 5)],
            "events": events, "operations": operations, "A": total_a, "Q_B": total_q,
            "K_B": kb, "physical_A": physical_a, "physical_B": physical_b,
            "paired_closed": closed, "states": snapshots}


def sweep(initial, events, *, record=False):
    stock = list(initial)
    paid = issued = unpaid = 0
    rows = []
    margin = None
    for clock, e in enumerate(events):
        order = e["priority"]
        before = [stock[v] for v in order]
        mass = sum(before)
        ip = pp = up = 0
        if e["a"] or e["k"]:
            for v in order:
                stock[v] = H
            ip = len(order) * H - mass
            assert 0 <= ip <= (40 if e["a"] else 5)
        else:
            pp = min(mass, e["q"])
            up = e["q"] - pp
            remaining = mass - pp
            for v in order:
                stock[v] = min(H, remaining)
                remaining -= stock[v]
            assert remaining == 0
            if e["q"]:
                margin = mass - 1 if margin is None else min(margin, mass - 1)
        after = [stock[v] for v in order]
        assert sum(after) - mass == ip - pp
        paid += pp
        issued += ip
        unpaid += up
        if record:
            rows.append({"event": clock, "id": e["id"], "priority": order,
                         "before": before, "after": after, "issued": ip,
                         "paid": pp, "unpaid": up})
    assert sum(stock) - sum(initial) == issued - paid
    return stock, {"paid": paid, "issued": issued, "Omega_5": unpaid,
                   "minimum_paid_step_margin": margin, "rows": rows}


def canonical(compiled, *, record=False):
    assert compiled["paired_closed"]
    events = compiled["events"]
    stock = [H] * len(compiled["blocks"])
    passes = []
    for lap in range(len(stock) * H + 1):
        new, counts = sweep(stock, events)
        assert all(x <= y for x, y in zip(new, stock))
        passes.append({"pass": lap, "mass_before": sum(stock),
                       "mass_after": sum(new), "Omega_5": counts["Omega_5"]})
        if new == stock:
            break
        stock = new
    else:
        raise AssertionError("Monotone finite descent bound.")
    final, counts = sweep(stock, events, record=record)
    assert final == stock and counts["paid"] == counts["issued"]
    assert counts["paid"] + counts["Omega_5"] == compiled["Q_B"]
    assert counts["issued"] <= 45 * compiled["A"]
    return {"policy": POLICY, "H": H, "initial_greatest_fixed_point": stock,
            "passes": passes, "cyclic_seam_closed": True, **counts}


def vouchers(compiled):
    ops = compiled["operations"]
    genuine = [op["id"] for op in ops if op["k"]]
    units = {}
    for e in compiled["events"]:
        if e["a"]:
            units.setdefault(e["id"][1], []).append(e["id"])
    answer = {}
    seen = set()
    for j, op in enumerate(genuine):
        previous = genuine[j - 1]
        at = previous % len(ops) + 1
        while True:
            if units.get(at):
                unit = units[at][0]
                break
            assert at != op
            at = at % len(ops) + 1
        assert tuple(unit) not in seen
        seen.add(tuple(unit))
        answer[str(op)] = {"A_unit": unit, "charge_lap_offset": -int(at > op)}
    return answer


def evidence(compiled, bank):
    """Literal dry-packet records; no bounded-congestion premise is supplied."""
    packets = []
    current = None
    last_drain = None
    last_op = None
    for e, row in zip(compiled["events"], bank["rows"]):
        if e["id"][0] != "B":
            continue
        op = e["id"][1]
        if op != last_op:
            current = None
            last_drain = None
            last_op = op
        if row["unpaid"]:
            if current is None:
                current = {"operation": op, "last_funded_target_drain": last_drain,
                           "unpaid_original_ids": [], "owner_blocks": set()}
                packets.append(current)
            current["unpaid_original_ids"].append(e["id"])
            current["owner_blocks"].update(e["scope"])
        else:
            current = None
        if row["before"][0] > 0 and row["after"][0] == 0:
            last_drain = e["id"]
    for packet in packets:
        packet["owner_blocks"] = sorted(packet["owner_blocks"])
    return {"dry_packets": packets,
            "largest_dry_packet": max((len(p["unpaid_original_ids"]) for p in packets), default=0),
            "first_missing_physical_implication":
                "A globally bounded original-A load for repeated dry packets; last-drain tracing alone supplies no such load."}


def evaluate(source, *, detail=False):
    compiled = compile_source(source)
    bank = canonical(compiled, record=detail)
    a, omega = compiled["A"], bank["Omega_5"]
    assert a or not omega
    ratio = Fraction(omega, a) if a else Fraction(0)
    result = {"schema": "gso.omega5.complete-cycle.v1",
              "status": "FINITE_EXACT_COMPLETE_SOURCE", "source_sha256": digest(source),
              "source": source, "A": a, "Q_B": compiled["Q_B"], "K_B": compiled["K_B"],
              "P_5": bank["paid"], "Omega_5": omega, "Omega_5_over_A": str(ratio),
              "Q_B_over_A": str(Fraction(compiled["Q_B"], a) if a else Fraction(0)),
              "physical_A": compiled["physical_A"], "physical_B": compiled["physical_B"],
              "max_B_doubles_per_access": max((o["q"] for o in compiled["operations"]), default=0),
              "distinct_KEEP_targets": len({x for mode, x in source["operations"] if mode == "K"}),
              "bank": bank, "full_pair_closure": True, "reaching_prefix_not_credited": True,
              "unrestricted_root_accepted": False, "universal_CD": "OPEN"}
    if detail:
        from credit import trace_credits
        result["events"] = compiled["events"]
        result["vouchers"] = vouchers(compiled)
        result["credit_provenance"] = trace_credits(compiled, bank, result["vouchers"])
        result["recurrence_evidence"] = evidence(compiled, bank)
    return result
