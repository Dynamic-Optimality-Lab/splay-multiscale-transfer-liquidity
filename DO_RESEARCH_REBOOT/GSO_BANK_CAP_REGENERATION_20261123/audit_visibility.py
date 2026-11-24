"""Read-only visibility and interval-lifetime audit for both 290-key controls."""

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "GSO_OMEGA_CYCLE_SEARCH_20261122_V001"))

from core import Tree, read
from verify import check


def refresh(tree, key, lower, upper):
    left, right = tree.child[key]
    lower[key] = lower[left] if left else key
    upper[key] = upper[right] if right else key


def subtree_bounds(tree):
    lower = list(range(len(tree.keys) + 1))
    upper = lower.copy()
    pending = [(tree.root, False)]
    while pending:
        key, visited = pending.pop()
        if visited:
            refresh(tree, key, lower, upper)
        else:
            pending.append((key, True))
            pending.extend((child, False) for child in tree.child[key] if child)
    return lower, upper


def audit(path):
    cert = read(path)
    verified = check(cert)
    source = cert["source"]
    keys = sorted(map(int, source["initial_A"]["children"]))
    a = Tree(source["initial_A"], keys)
    b = Tree(source["initial_B"], keys)
    a_lo, a_hi = subtree_bounds(a)
    b_lo, b_hi = subtree_bounds(b)
    births = {
        (a_lo[v], a_hi[v]): None for v in range(1, len(keys) + 1) if v != a.root
    }
    paid_receipts = {
        tuple(row["B_id"]): row
        for row in cert["credit_provenance"]["paid_original_B_assignments"]
    }
    unpaid_caps = {}
    unpaid_by_lifetime = Counter()
    paid_by_lifetime = Counter()
    latest_left_gain = {}
    ancestral_receipts = {}

    # The first physical lap supplies lifetimes and B gains crossing the seam.
    for lap in range(2):
        for event, row in zip(cert["events"], cert["bank"]["rows"]):
            event_id = tuple(event["id"])
            caps = []
            owners = []
            for serial, bit in enumerate(event["bits"], start=1):
                promoted = a.index[bit["promoted"]]
                demoted = a.index[bit["demoted"]]
                if event["a"]:
                    del births[a_lo[promoted], a_hi[promoted]]
                    assert a.rotate(promoted) == bit
                    refresh(a, demoted, a_lo, a_hi)
                    refresh(a, promoted, a_lo, a_hi)
                    interval = a_lo[demoted], a_hi[demoted]
                    assert interval not in births
                    births[interval] = (*event_id, serial)
                    continue

                assert a.label(a.root) == event["target"]
                old_bounds = {
                    v: (b_lo[v], b_hi[v]) for v in (promoted, demoted)
                }
                assert b.rotate(promoted) == bit
                refresh(b, demoted, b_lo, b_hi)
                refresh(b, promoted, b_lo, b_hi)
                if promoted > demoted:
                    latest_left_gain[bit["promoted"]] = event_id
                if lap == 0 or not (row["paid"] or row["unpaid"]):
                    continue

                holders = []
                holder = demoted
                while holder != a.root:
                    low, high = a_lo[holder], a_hi[holder]
                    if low <= b_lo[demoted] and b_hi[demoted] <= high:
                        # Measure each candidate in the pre-rotation B state.
                        count = sum(
                            left < low or right > high
                            for left, right in (
                                old_bounds.get(v, (b_lo[v], b_hi[v]))
                                for v in range(low, high + 1)
                            )
                        )
                        birth = births[low, high]
                        assert count >= 1 and birth is not None
                        holders.append((count, birth, (low, high)))
                        if row["paid"]:
                            if count > 5:
                                paid_by_lifetime[birth] += 1
                            break
                    holder = a.parent[holder]
                assert holders
                if row["unpaid"]:
                    caps.append(min(item[0] for item in holders))
                    owners.append(holders[0][1:])

            if lap == 1 and row["unpaid"]:
                assert len(caps) == 2
                unpaid_caps[event_id] = tuple(caps)
                if min(caps) > 5:
                    unpaid_by_lifetime.update(birth for birth, _ in owners)
                    assert owners[1][1] == (4, 50)
                    assert event["type"] == "LL"
                    gain = latest_left_gain[event["bits"][0]["demoted"]]
                    assert gain in paid_receipts
                    ancestral_receipts[event_id] = gain

        assert a.state() == source["initial_A"]
        assert b.state() == source["initial_B"]

    packet = {
        ("B", 1777, step): (48 - 2 * step, 48 - 2 * step) for step in range(6, 21)
    }
    assert len(unpaid_caps) == 16
    assert {key: caps for key, caps in unpaid_caps.items() if min(caps) > 5} == packet
    assert min(unpaid_caps["B", 1777, 23]) == 2
    lifetime = ("A", 1290, 1, 1)
    assert (unpaid_by_lifetime[lifetime], paid_by_lifetime[lifetime]) == (15, 6)
    assert len(set(ancestral_receipts.values())) == len(packet)
    assert ancestral_receipts["B", 1777, 6] == ("B", 1601, 3)
    assert ancestral_receipts["B", 1777, 20] == ("B", 1741, 3)
    return {
        "file": path.name,
        "independent_replay": verified,
        "first_bad": {"B_id": ["B", 1777, 6], "caps": unpaid_caps["B", 1777, 6]},
        "bad_packet_length": len(packet),
        "high_cap_continuations": len(packet) - 1,
        "lifetime_birth": lifetime,
        "u_L": unpaid_by_lifetime[lifetime],
        "p_L": paid_by_lifetime[lifetime],
        "distinct_older_paid_gains": len(set(ancestral_receipts.values())),
    }


if __name__ == "__main__":
    for fixture in (
        HERE.parent / "GSO_OMEGA5_SHARED_DONOR_CONTROL_20261123.json.gz",
        HERE / "CAP_FIVE_290_DELETE_4_CONTROL.json.gz",
    ):
        print(json.dumps(audit(fixture)), flush=True)
