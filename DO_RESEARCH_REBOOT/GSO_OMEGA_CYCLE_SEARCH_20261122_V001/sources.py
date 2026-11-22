"""Complete original sources and exact full-state cycle extraction."""
from __future__ import annotations

from fractions import Fraction
from core import Tree, compile_source, digest


def vine(keys):
    keys = list(keys)
    return {"root": keys[0], "children": {
        str(k): [None, keys[i + 1] if i + 1 < len(keys) else None]
        for i, k in enumerate(keys)}}


def closed_word(n, raw, name="closed_candidate"):
    initial = vine(range(1, n + 1))
    restoration = [["K", k] for k in range(1, n + 1)]
    restoration += [["K", k] for k in range(n - 1, 0, -1)]
    return {"name": name, "initial_A": initial, "initial_B": initial,
            "diagonal": initial, "prefix": [],
            "operations": [list(x) for x in raw] + restoration,
            "construction": {"kind": "counted_full_restoration",
                             "raw_operations": len(raw),
                             "restoration_operations": len(restoration)}}


def H_source(p, q):
    n = 2 ** (p + 1) * (q + 1) + 1
    marked = {n + 1 - 2 ** j for j in range(p + 1)}
    raw = [["D", k] for k in range(2, n + 1)]
    raw += [["K" if k in marked else "D", k] for k in range(n, 0, -1)]
    source = closed_word(n, raw, f"H_{p}_{q}")
    source.update({"p": p, "q": q, "expected_A": 4 * (n - 1)})
    return source


def mixed_source(n, targets, *, repeat=1, adjacent=False, name="interleaved"):
    """Preparatory helpers, multiscale traffic and real restoration in one word."""
    raw = [["D", k] for k in range(2, n + 1)]
    current = n
    for _ in range(repeat):
        for mode, target in targets:
            if adjacent:
                sign = 1 if target >= current else -1
                raw.extend(["D", k] for k in range(current + sign, target, sign))
            raw.append([mode, target])
            current = target
    return closed_word(n, raw, name)


def mirrored(source):
    keys = sorted(map(int, source["initial_A"]["children"]))
    mapping = dict(zip(keys, reversed(keys)))
    def tree(t):
        return {"root": mapping[t["root"]], "children": {
            str(mapping[int(k)]): [mapping[r] if r is not None else None,
                                  mapping[l] if l is not None else None]
            for k, (l, r) in t["children"].items()}}
    out = {k: v for k, v in source.items() if k not in ("expected_A", "expected_Q")}
    out.update({"name": "mirror__" + source["name"],
                "initial_A": tree(source["initial_A"]),
                "initial_B": tree(source["initial_B"]),
                "diagonal": tree(source.get("diagonal", source["initial_A"])),
                "prefix": [[m, mapping[x]] for m, x in source.get("prefix", [])],
                "operations": [[m, mapping[x]] for m, x in source["operations"]]})
    return out


def _state(flat, keys):
    def key(v):
        return keys[v - 1] if v else None
    return {"root": key(flat[0]), "children": {
        str(k): [key(flat[2 * (i + 1) - 1]), key(flat[2 * (i + 1)])]
        for i, k in enumerate(keys)}}


def recurrent_cycles(source, *, limit=6):
    """Exact physical pair equality; bank state and source prefixes are not credit."""
    compiled = compile_source(source, states=True)
    first = {}
    ranges = []
    cumulative_a = [0]
    cumulative_q = [0]
    for op in compiled["operations"]:
        cumulative_a.append(cumulative_a[-1] + op["a"])
        cumulative_q.append(cumulative_q[-1] + op["q"])
    for j, pair in enumerate(compiled["states"]):
        if pair in first:
            i = first[pair]
            aa = cumulative_a[j] - cumulative_a[i]
            qq = cumulative_q[j] - cumulative_q[i]
            if aa and qq:
                ranges.append((Fraction(qq, aa), j - i, i, j))
        else:
            first[pair] = j
    ranges.sort(reverse=True)
    out = []
    seen = set()
    for _, _, i, j in ranges:
        a, b = compiled["states"][i]
        candidate = {"name": f"recurrent_{source['name']}_{i}_{j}",
                     "initial_A": _state(a, compiled["keys"]),
                     "initial_B": _state(b, compiled["keys"]),
                     "diagonal": source.get("diagonal", source["initial_A"]),
                     "prefix": source.get("prefix", []) + source["operations"][:i],
                     "operations": source["operations"][i:j],
                     "construction": {"kind": "exact_full_pair_recurrence",
                                      "parent_source_sha256": digest(source),
                                      "parent_operation_range": [i + 1, j],
                                      "reaching_prefix_not_credited": True}}
        key = digest([candidate["initial_A"], candidate["initial_B"], candidate["operations"]])
        if key not in seen:
            seen.add(key)
            compile_source(candidate)
            out.append(candidate)
        if len(out) >= limit:
            break
    return out
