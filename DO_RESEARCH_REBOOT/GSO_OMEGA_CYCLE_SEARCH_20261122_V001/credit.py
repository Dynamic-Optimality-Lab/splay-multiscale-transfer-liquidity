"""Conservative FIFO token decomposition of a canonical closed scalar bank.

Entry tokens are symbolic. End-to-entry predecessor paths identify earlier-lap
issuance. A pure circulation cannot finance a debit. Geometry never mints credit.
"""
from __future__ import annotations

from collections import Counter


def trace_credits(compiled, bank, voucher_map):
    entries = {}
    queues = []
    for block, count in enumerate(bank["initial_greatest_fixed_point"]):
        queue = []
        for slot in range(count):
            name = f"E:{block}:{slot}"
            entries[name] = (block, slot)
            queue.append(name)
        queues.append(queue)
    issuance = {}
    debits = []
    for clock, (e, row) in enumerate(zip(compiled["events"], bank["rows"])):
        order = e["priority"]
        assert [len(queues[b]) for b in order] == row["before"]
        if e["a"] or e["k"]:
            serial = 0
            for block in order:
                while len(queues[block]) < 5:
                    label = f"I:{clock}:{serial}"
                    if e["a"]:
                        a_unit = e["id"]
                        charge_slot = serial
                        charge_lap = 0
                    else:
                        binding = voucher_map[str(e["id"][1])]
                        a_unit = binding["A_unit"]
                        charge_slot = 40 + serial
                        charge_lap = binding["charge_lap_offset"]
                    issuance[label] = {"issue_event": clock, "issue_id": e["id"],
                                       "A_unit": a_unit, "A_slot": charge_slot,
                                       "charge_lap_offset": charge_lap}
                    queues[block].append(label)
                    serial += 1
            assert serial == row["issued"]
        else:
            pool = [token for block in order for token in queues[block]]
            if row["paid"]:
                assert row["paid"] == 1
                debits.append({"B_id": e["id"], "event": clock, "token": pool.pop(0)})
            assert len(pool) == sum(row["after"])
            offset = 0
            for block, count in zip(order, row["after"]):
                queues[block] = pool[offset:offset + count]
                offset += count
            assert offset == len(pool)
        assert [len(queues[b]) for b in order] == row["after"]
    assert [len(q) for q in queues] == bank["initial_greatest_fixed_point"]
    predecessor = {f"E:{block}:{slot}": token
                   for block, queue in enumerate(queues)
                   for slot, token in enumerate(queue)}
    assigned = []
    used_slots = set()
    loads = Counter()
    event_by_id = {tuple(e["id"]): i for i, e in enumerate(compiled["events"])}
    for debit in debits:
        token = debit["token"]
        crossings = 0
        seen = set()
        while token.startswith("E:"):
            assert token not in seen, "A pure cyclic token cannot pay a demand."
            seen.add(token)
            token = predecessor[token]
            crossings += 1
        origin = issuance[token]
        a_unit = tuple(origin["A_unit"])
        charge_lap = origin["charge_lap_offset"] - crossings
        slot = (a_unit, origin["A_slot"])
        assert slot not in used_slots, "Original A slot reused within the period."
        used_slots.add(slot)
        loads[a_unit] += 1
        assert loads[a_unit] <= 45 and 0 <= origin["A_slot"] < 45
        assert event_by_id[a_unit] + charge_lap * len(compiled["events"]) < debit["event"]
        assigned.append({**debit, "origin_issuance": token, "A_unit": list(a_unit),
                         "A_slot": origin["A_slot"], "A_lap_offset": charge_lap,
                         "seam_crossings": crossings})
    assert len(assigned) == bank["paid"] == len(issuance)
    assert len(used_slots) == len(assigned)
    return {"method": "exact_cyclic_FIFO_predecessor_paths",
            "issuance": issuance, "end_to_entry_predecessor": predecessor,
            "paid_original_B_assignments": assigned,
            "loads": [{"A_unit": list(k), "load": v} for k, v in sorted(loads.items())],
            "maximum_original_A_load": max(loads.values(), default=0),
            "paid_total": len(assigned), "prefix_credit": 0,
            "pure_circulations_supply_no_demands": True,
            "unpaid_cost_not_funded_by_this_certificate": bank["Omega_5"]}
