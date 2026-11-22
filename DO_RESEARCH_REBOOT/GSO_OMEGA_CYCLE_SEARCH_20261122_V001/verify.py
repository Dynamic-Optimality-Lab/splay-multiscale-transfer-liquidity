"""Independent full-source checker. Imports no producer or bank implementation."""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
from vendor import independent_splay as F

HERE = Path(__file__).resolve().parent
POLICY = "selected_H5_target_middle2_external_grandparent_parent_middle1"


def load(path):
    path = Path(path)
    with (gzip.open(path, "rt", encoding="utf-8") if path.suffix == ".gz"
          else path.open(encoding="utf-8")) as stream:
        return json.load(stream)


def signature(tree):
    children = {}
    stack = [tree]
    root = tree[1]
    while stack:
        t = stack.pop()
        if t[0] == "leaf":
            continue
        _, key, left, right = t
        assert key not in children
        children[key] = [left[1] if left[0] != "leaf" else None,
                         right[1] if right[0] != "leaf" else None]
        stack.extend((left, right))
    return {"root": root, "children": {str(k): children[k] for k in sorted(children)}}


def functional(state, keys):
    made = {}
    stack = [(state["root"], False, None, None)]
    seen = set()
    while stack:
        key, done, low, high = stack.pop()
        if key is None:
            continue
        if done:
            left, right = state["children"][str(key)]
            made[key] = F.node(key, made[left] if left is not None else F.LEAF,
                               made[right] if right is not None else F.LEAF)
        else:
            assert key not in seen and (low is None or low < key) and (high is None or key < high)
            seen.add(key)
            left, right = state["children"][str(key)]
            stack.extend(((key, True, low, high), (right, False, key, high),
                          (left, False, low, key)))
    assert seen == set(keys) == set(map(int, state["children"]))
    return made[state["root"]]


def rotation(tree, key):
    node, path = F._descend(tree, key, [])
    assert path
    side, parent, sibling = path[-1]
    grand = path[-2][1] if len(path) >= 2 else None
    _, _, left, right = node
    if side == "L":
        middle = right
        after = F.node(key, left, F.node(parent, right, sibling))
    else:
        middle = left
        after = F.node(key, F.node(parent, sibling, left), right)
    bit = {"promoted": key, "demoted": parent, "grandparent": grand,
           "middle": middle[1] if middle[0] != "leaf" else None}
    return F._plug(path[:-1], after), bit


def physical(source):
    keys = sorted(map(int, source["initial_A"]["children"]))
    owner = {k: i // 5 for i, k in enumerate(keys)}
    diagonal = source.get("diagonal") or source["initial_A"]
    ra = rb = functional(diagonal, keys)
    for mode, key in source.get("prefix", []):
        assert mode in ("K", "D")
        ra, _ = F.trace(ra, key)
        if mode == "K":
            rb, _ = F.trace(rb, key)
    assert signature(ra) == source["initial_A"] and signature(rb) == source["initial_B"]
    trees = {"A": ra, "B": rb}
    events = []
    A = Q = KB = PA = PB = 0
    for op, (mode, key) in enumerate(source["operations"], 1):
        assert mode in ("K", "D") and key in owner
        genuine = mode == "K" and trees["B"][1] != key
        if genuine:
            KB += 1
            events.append({"id": ["K", op], "a": 0, "q": 0, "k": 1,
                           "target": key, "scope": [owner[key]],
                           "priority": [owner[key]], "type": "VOUCHER", "bits": []})
        for actor in ("A", "B") if mode == "K" else ("A",):
            tree = trees[actor]
            expected, types = F.trace(tree, key)
            step = 0
            while tree[1] != key:
                _, path = F._descend(tree, key, [])
                step += 1
                typ = "ZIG" if len(path) == 1 else path[-2][0] + path[-1][0]
                parent = path[-1][1]
                pivots = [key] if typ == "ZIG" else [parent, key] if typ in ("LL", "RR") else [key, key]
                bits = []
                for pivot in pivots:
                    tree, bit = rotation(tree, pivot)
                    bits.append(bit)
                assert types[step - 1][0] == typ
                scope = sorted({owner[v] for bit in bits for v in bit.values() if v is not None})
                assert len(scope) <= 8
                priority = [owner[key]] + [b for b in scope if b != owner[key]]
                if actor == "B" and typ in ("LL", "RR"):
                    priority = []
                    one, two = bits
                    for role in (key, two["middle"], one["grandparent"],
                                 one["demoted"], two["demoted"], one["middle"]):
                        if role is not None and owner[role] not in priority:
                            priority.append(owner[role])
                assert set(priority) == set(scope)
                a, q = int(actor == "A"), int(actor == "B" and typ != "ZIG")
                A += a
                Q += q
                PA += len(bits) if a else 0
                PB += len(bits) if not a else 0
                events.append({"id": [actor, op, step], "a": a, "q": q, "k": 0,
                               "target": key, "scope": scope, "priority": priority,
                               "type": typ, "bits": bits})
            assert step == len(types) and signature(tree) == signature(expected)
            trees[actor] = tree
    assert signature(trees["A"]) == source["initial_A"]
    assert signature(trees["B"]) == source["initial_B"]
    assert KB <= A
    return keys, events, A, Q, KB, PA, PB


def bank_pass(initial, events):
    b = list(initial)
    rows = []
    paid = issue = omega = 0
    minimum = None
    for clock, e in enumerate(events):
        order = e["priority"]
        before = [b[i] for i in order]
        mass = sum(before)
        if e["id"][0] in ("A", "K"):
            after = [5] * len(order)
            ii, pp, uu = 5 * len(order) - mass, 0, 0
        else:
            ii = 0
            pp = min(e["q"], mass)
            uu = e["q"] - pp
            after = [max(0, min(5, mass - pp - 5 * j)) for j in range(len(order))]
            if e["q"]:
                minimum = mass - 1 if minimum is None else min(minimum, mass - 1)
        for block, value in zip(order, after):
            b[block] = value
        assert sum(after) - mass == ii - pp
        issue += ii
        paid += pp
        omega += uu
        rows.append({"event": clock, "id": e["id"], "priority": order, "before": before,
                     "after": after, "issued": ii, "paid": pp, "unpaid": uu})
    return b, rows, paid, issue, omega, minimum


def check_tokens(cert, events, rows):
    # Prove the voucher injection independently using cyclic operation distances.
    count = len(cert["source"]["operations"])
    units = [e["id"] for e in events if e["a"]]
    genuine = [e["id"][1] for e in events if e["k"]]
    binding = {}
    for j, op in enumerate(genuine):
        previous = genuine[j - 1]
        length = (op - previous - 1) % count + 1
        available = [u for u in units if (u[1] - previous - 1) % count + 1 <= length]
        assert available
        chosen = min(available, key=lambda u: ((u[1] - previous - 1) % count + 1, u[2]))
        binding[str(op)] = {"A_unit": chosen, "charge_lap_offset": -int(chosen[1] > op)}
    assert len({tuple(v["A_unit"]) for v in binding.values()}) == len(binding)
    assert binding == cert["vouchers"]
    stock = cert["bank"]["initial_greatest_fixed_point"]
    queues = [[f"E:{b}:{j}" for j in range(value)] for b, value in enumerate(stock)]
    issue = {}
    consumed = []
    for clock, (e, row) in enumerate(zip(events, rows)):
        order = e["priority"]
        assert [len(queues[b]) for b in order] == row["before"]
        if e["a"] or e["k"]:
            serial = 0
            for block in order:
                missing = 5 - len(queues[block])
                for _ in range(missing):
                    token = f"I:{clock}:{serial}"
                    a_unit = e["id"] if e["a"] else binding[str(e["id"][1])]["A_unit"]
                    lap = 0 if e["a"] else binding[str(e["id"][1])]["charge_lap_offset"]
                    issue[token] = {"issue_event": clock, "issue_id": e["id"],
                                    "A_unit": a_unit, "A_slot": serial if e["a"] else 40 + serial,
                                    "charge_lap_offset": lap}
                    queues[block].append(token)
                    serial += 1
            assert serial == row["issued"]
        else:
            all_tokens = sum((queues[b] for b in order), [])
            if row["paid"]:
                consumed.append({"B_id": e["id"], "event": clock, "token": all_tokens[0]})
                all_tokens = all_tokens[1:]
            for j, block in enumerate(order):
                queues[block] = all_tokens[5*j:5*j+row["after"][j]]
        assert [len(queues[b]) for b in order] == row["after"]
    predecessor = {f"E:{b}:{j}": token for b, queue in enumerate(queues)
                   for j, token in enumerate(queue)}
    given = cert["credit_provenance"]
    assert given["issuance"] == issue and given["end_to_entry_predecessor"] == predecessor
    provided = given["paid_original_B_assignments"]
    assert len(provided) == len(consumed) == cert["P_5"] == len(issue)
    used = set()
    loads = Counter()
    clock_by_id = {tuple(e["id"]): i for i, e in enumerate(events)}
    for debit, claimed in zip(consumed, provided):
        assert all(debit[k] == claimed[k] for k in debit)
        token = debit["token"]
        seen = set()
        crossings = 0
        while token.startswith("E:"):
            assert token not in seen
            seen.add(token)
            token = predecessor[token]
            crossings += 1
        origin = issue[token]
        unit = tuple(origin["A_unit"])
        lag = origin["charge_lap_offset"] - crossings
        assert claimed["origin_issuance"] == token
        assert claimed["A_unit"] == list(unit)
        assert claimed["A_slot"] == origin["A_slot"]
        assert claimed["A_lap_offset"] == lag and claimed["seam_crossings"] == crossings
        slot = (unit, origin["A_slot"])
        assert slot not in used and 0 <= origin["A_slot"] < 45
        assert clock_by_id[unit] + lag * len(events) < debit["event"]
        used.add(slot)
        loads[unit] += 1
    assert given["loads"] == [{"A_unit": list(k), "load": v} for k, v in sorted(loads.items())]
    assert given["maximum_original_A_load"] == max(loads.values(), default=0) <= 45
    assert given["prefix_credit"] == 0
    assert given["unpaid_cost_not_funded_by_this_certificate"] == cert["Omega_5"]
    return len(consumed), max(loads.values(), default=0)


def check(cert):
    assert cert["schema"] == "gso.omega5.complete-cycle.v1"
    assert cert["status"] == "FINITE_EXACT_COMPLETE_SOURCE"
    assert cert["unrestricted_root_accepted"] is False and cert["universal_CD"] == "OPEN"
    assert cert["source_sha256"] == hashlib.sha256(json.dumps(
        cert["source"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    keys, events, A, Q, KB, PA, PB = physical(cert["source"])
    assert cert["events"] == events
    assert (cert["A"], cert["Q_B"], cert["K_B"], cert["physical_A"], cert["physical_B"]) == (A, Q, KB, PA, PB)
    stock = [5] * ((len(keys) + 4) // 5)
    passes = []
    for lap in range(5 * len(stock) + 1):
        new, _, paid, issued, omega, minimum = bank_pass(stock, events)
        assert all(x <= y for x, y in zip(new, stock))
        passes.append({"pass": lap, "mass_before": sum(stock),
                       "mass_after": sum(new), "Omega_5": omega})
        if stock == new:
            break
        stock = new
    else:
        raise AssertionError("Finite greatest-seam descent failed.")
    final, rows, paid, issued, omega, minimum = bank_pass(stock, events)
    assert final == stock and issued == paid and paid + omega == Q
    assert paid <= 45 * A
    bank = cert["bank"]
    assert bank["policy"] == POLICY and bank["H"] == 5
    assert bank["initial_greatest_fixed_point"] == stock
    assert bank["passes"] == passes and bank["rows"] == rows
    assert bank["paid"] == paid and bank["issued"] == issued and bank["Omega_5"] == omega
    assert bank["minimum_paid_step_margin"] == minimum and bank["cyclic_seam_closed"]
    assert (cert["P_5"], cert["Omega_5"]) == (paid, omega)
    assert cert["Omega_5_over_A"] == str(Fraction(omega, A) if A else Fraction(0))
    assert cert["Q_B_over_A"] == str(Fraction(Q, A) if A else Fraction(0))
    per_access = Counter()
    for e in events:
        if e["q"]:
            per_access[e["id"][1]] += 1
    maximum_access = max(per_access.values(), default=0)
    if "max_B_doubles_per_access" in cert:
        assert cert["max_B_doubles_per_access"] == maximum_access
    if "distinct_KEEP_targets" in cert:
        assert cert["distinct_KEEP_targets"] == len({
            x for mode, x in cert["source"]["operations"] if mode == "K"})
    token_count, load = check_tokens(cert, events, rows)
    # Bind the dry-packet records to precisely the original unpaid event IDs.
    unpaid = [e["id"] for e, row in zip(events, rows) if row["unpaid"]]
    packet_ids = [identifier for p in cert["recurrence_evidence"]["dry_packets"]
                  for identifier in p["unpaid_original_ids"]]
    assert packet_ids == unpaid
    assert sum(len(p["unpaid_original_ids"]) for p in cert["recurrence_evidence"]["dry_packets"]) == omega
    return {"passed": True, "support": len(keys), "operations": len(cert["source"]["operations"]),
            "A": A, "Q_B": Q, "Omega_5": omega, "paid_A_slot_assignments": token_count,
            "maximum_A_load": load, "whole_original_operations_completed": True,
            "max_B_doubles_per_access": maximum_access,
            "greatest_cyclic_seam_verified": True, "source_uniform_bound_proved": False}


def accept_unrestricted(_certificate):
    # The engine has no independently verified arbitrary-source induction proof.
    # Caller-supplied PROVED metadata cannot bypass that mathematical requirement.
    return {"accepted": False, "scope": "ALL_ORIGINAL_SOURCES",
            "reason": "MISSING_INDEPENDENT_SOURCE_UNIFORM_OMEGA5_BOUND",
            "universal_CD": "OPEN"}


if __name__ == "__main__":
    for name in sys.argv[1:]:
        print(json.dumps({"file": name, **check(load(name))}))
