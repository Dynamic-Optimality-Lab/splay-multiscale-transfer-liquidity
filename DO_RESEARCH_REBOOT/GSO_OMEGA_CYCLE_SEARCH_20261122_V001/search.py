"""Bounded complete-history adversary. Omega5/A is the PRIMARY exact objective."""
from __future__ import annotations

import random
import time
import hashlib
from pathlib import Path
from fractions import Fraction

from core import compile_source, digest, evaluate, write
from sources import H_source, closed_word, mirrored, mixed_source, recurrent_cycles


def score(result):
    margin = result["bank"]["minimum_paid_step_margin"]
    # Only the first coordinate is the mathematical optimization objective.
    # The remaining coordinates guide discovery when all residual ratios tie.
    return (Fraction(result["Omega_5_over_A"]),
            int(result.get("max_B_doubles_per_access", 0) > 5),
            -(margin if margin is not None else 10**9),
            Fraction(result["Q_B_over_A"]), -result["A"])


def seeds(n):
    out = []
    for p in range(1, min(9, (n - 1).bit_length())):
        stride = 2 ** (p + 1)
        if (n - 1) % stride == 0 and (n - 1) // stride >= 2:
            q = (n - 1) // stride - 1
            out.extend((H_source(p, q), mirrored(H_source(p, q))))
    levels = max(1, (n - 1).bit_length() - 1)
    traffic = []
    for scale in range(levels, 0, -1):
        width = min(n - 1, 2**scale)
        for offset in (0, 1, max(0, (n - width - 1) // 2)):
            left = min(n - width, 1 + offset)
            right = left + width
            traffic += [["K", right], ["K", left], ["D", max(left, right - 1)],
                        ["K", min(right, left + 1)]]
            traffic += [["K", k] for k in range(left, min(right, left + 4) + 1)]
    out.append(mixed_source(n, traffic, repeat=2, name=f"multiscale_N{n}"))
    out.append(mixed_source(n, traffic, repeat=2, adjacent=True, name=f"adjacent_multiscale_N{n}"))
    alternating = [["K", n - j] if j % 2 == 0 else ["K", j + 1] for j in range(n)]
    out.append(closed_word(n, alternating * 2, f"alternating_N{n}"))
    # A counted all-key warmup precedes internal renewals: no fresh-leaf shortcut.
    warm = [["K", k] for k in range(1, n + 1)] + [["K", k] for k in range(n - 1, 0, -1)]
    out.append(closed_word(n, warm + traffic * 2, f"internal_renewal_N{n}"))
    return out


def raw_word(source):
    construction = source.get("construction", {})
    if construction.get("kind") == "counted_full_restoration":
        return [list(x) for x in source["operations"][:construction["raw_operations"]]]
    return [list(x) for x in source.get("prefix", []) + source["operations"]]


def mutate(source, n, rng, partner=None):
    word = raw_word(source)
    if not word:
        word = [["D", k] for k in range(2, n + 1)]
    action = rng.randrange(9)
    pos = rng.randrange(len(word) + 1)
    current = word[pos - 1][1] if pos else 1
    if action == 0:
        target = rng.randrange(1, n + 1)
        sign = 1 if target >= current else -1
        block = [["D", k] for k in range(current + sign, target, sign)]
        block.append(["K", target])
        word[pos:pos] = block
    elif action == 1:
        j = min(pos, len(word) - 1)
        word[j][0] = "D" if word[j][0] == "K" else "K"
    elif action == 2:
        j = min(pos, len(word) - 1)
        distance = 2 ** rng.randrange(max(1, n.bit_length()))
        word[j][1] = min(n, max(1, current + rng.choice((-1, 1)) * distance))
    elif action == 3:
        if pos < len(word):
            del word[pos:pos + rng.randrange(1, min(17, len(word) - pos) + 1)]
    elif action == 4:
        begin = rng.randrange(len(word))
        block = word[begin:begin + rng.randrange(1, min(25, len(word) - begin) + 1)]
        word[pos:pos] = [list(x) for x in block] * rng.randrange(2, 5)
    elif action == 5:
        width = min(n - 1, 2 ** rng.randrange(1, max(2, n.bit_length())))
        left = rng.randrange(1, n - width + 1)
        right = left + width
        block = [["K", right], ["K", left]]
        block += [["K", k] for k in range(left, min(right, left + 5) + 1)]
        block += [["D" if rng.randrange(3) == 0 else "K", k]
                  for k in range(right, max(left, right - 5) - 1, -1)]
        word[pos:pos] = block
    elif action == 6:
        end = min(len(word), pos + rng.randrange(1, 33))
        word[pos:end] = [[mode, n + 1 - key] for mode, key in word[pos:end]]
    elif action == 7 and word:
        word = word[pos:] + word[:pos]
    elif partner is not None:
        other = raw_word(partner)
        if other:
            begin = rng.randrange(len(other))
            end = min(len(other), begin + rng.randrange(1, min(n, len(other) - begin) + 1))
            word[pos:pos] = [list(x) for x in other[begin:end]]
    if len(word) > 8 * n + 512:
        start = rng.randrange(len(word) - (8 * n + 512) + 1)
        word = word[start:start + 8 * n + 512]
    return closed_word(n, word, f"mutated_N{n}_{digest(word)[:12]}")


def run(output, *, supports=(17, 33, 65, 129), evaluations=1200,
        seconds=240, seed=120661, keep=6, initial_sources=()):
    start = time.monotonic()
    code = {}
    for name in ("core.py", "credit.py", "sources.py", "search.py", "gso_omega.py"):
        data = (Path(__file__).resolve().parent / name).read_bytes()
        code[name] = {"sha256": hashlib.sha256(data).hexdigest(), "text": data.decode("utf-8")}
    write(f"{output}/DISCOVERY_CODE.json.gz", {
        "revision": "complete_history_resume_and_nondegenerate_primary_search",
        "files": code,
        "note": "Rehydrate only into a fresh unsealed checkpoint; no implicit old stock."})
    rng = random.Random(seed)
    pool = {n: [] for n in supports}
    seen = {}
    records = []
    best = None
    count = 0
    cycles = 0
    positive = 0
    nonvacuous = 0
    nonvacuous_cycles = 0
    def admit(source, n, origin):
        nonlocal count, best, cycles, positive, nonvacuous, nonvacuous_cycles
        if count >= evaluations or time.monotonic() - start >= seconds:
            return None
        identity = digest([source["initial_A"], source["initial_B"],
                           source.get("prefix", []), source["operations"]])
        if identity in seen:
            return None
        result = evaluate(source)
        seen[identity] = result
        count += 1
        positive += int(result["Omega_5"] > 0)
        nonvacuous += int(result["max_B_doubles_per_access"] > 5)
        if origin == "recurrent":
            cycles += 1
            nonvacuous_cycles += int(result["max_B_doubles_per_access"] > 5)
        entry = (score(result), identity, result)
        pool[n].append(entry)
        pool[n].sort(key=lambda e: (e[0], e[1]), reverse=True)
        # Retain the exact-objective elite plus diverse complete histories.
        elite = pool[n][:8]
        rest = pool[n][8:]
        rng.shuffle(rest)
        pool[n] = elite + rest[:8]
        if best is None or entry[0] > best[0]:
            best = entry
            rec = {"evaluation": count, "support": n, "origin": origin,
                   "source": source["name"], "A": result["A"], "Q_B": result["Q_B"],
                   "Omega_5": result["Omega_5"], "Omega_5_over_A": result["Omega_5_over_A"],
                   "max_B_doubles_per_access": result["max_B_doubles_per_access"],
                   "minimum_margin": result["bank"]["minimum_paid_step_margin"]}
            records.append(rec)
            print(rec, flush=True)
        return result
    for source in initial_sources:
        n = len(source["initial_A"]["children"])
        assert n in pool
        admit(source, n, "resumed_complete_source")
    for n in supports:
        assert n >= 13, "The primary search must exceed the automatic five-credit depth regime."
        for source in seeds(n):
            result = admit(source, n, "seed")
            if result is not None:
                for cycle in recurrent_cycles(source, limit=2):
                    admit(cycle, n, "recurrent")
    generation = 0
    while count < evaluations and time.monotonic() - start < seconds:
        generation += 1
        for n in supports:
            if not pool[n]:
                continue
            parent = rng.choice(pool[n][:min(12, len(pool[n]))])[2]["source"]
            partner = rng.choice(pool[n])[2]["source"]
            child = mutate(parent, n, rng, partner)
            result = admit(child, n, "mutation")
            if result is not None and (generation % 5 == 0 or result["Omega_5"]):
                for cycle in recurrent_cycles(child, limit=3):
                    admit(cycle, n, "recurrent")
            if count >= evaluations or time.monotonic() - start >= seconds:
                break
        if generation % 20 == 0:
            print({"generation": generation, "complete_sources": count,
                   "positive_residual_sources": positive, "seconds": round(time.monotonic() - start, 2)},
                  flush=True)
    retained = []
    ranked = sorted(seen.values(), key=score, reverse=True)
    chosen = []
    used_supports = set()
    # Save the strongest score and a representative of each larger support.
    for result in ranked:
        n = len(result["source"]["initial_A"]["children"])
        if len(chosen) < keep and (not chosen or n not in used_supports):
            chosen.append(result)
            used_supports.add(n)
    for j, result in enumerate(chosen):
        detailed = evaluate(result["source"], detail=True)
        name = f"{output}/complete_{j:02d}.json.gz"
        write(name, detailed)
        retained.append({"file": name, "source": result["source"]["name"],
                         "A": result["A"], "Q_B": result["Q_B"],
                         "Omega_5": result["Omega_5"], "Omega_5_over_A": result["Omega_5_over_A"]})
    summary = {"engine": "WORKING_COMPLETE_HISTORY_OMEGA5_ADVERSARY",
               "supports": list(supports), "completed_evaluations": count,
               "recurrent_periods_evaluated": cycles, "positive_residual_sources": positive,
               "histories_exceeding_target_refill": nonvacuous,
               "recurrent_periods_exceeding_target_refill": nonvacuous_cycles,
               "primary_objective": "exact Omega5/A on complete original paired-closed periods",
               "initialization": "greatest clipped cyclic seam, no reaching-prefix credit",
               "restoration": "counted or exact full-pair recurrence; never omitted",
               "stop_at_failed_guard": False,
               "seed": seed, "seconds": round(time.monotonic() - start, 3),
               "resumed_sources": len(initial_sources),
               "records": records, "retained_certificates": retained,
               "best_Omega_5_over_A": ranked[0]["Omega_5_over_A"] if ranked else None,
               "source_uniform_proof": False, "universal_CD": "OPEN",
               "scope": "Bounded adversarial search. Neither zero residual nor a maximum ratio in this population is a universal statement.",
               "first_missing": "A physical all-source bound on accumulated dry B work with globally bounded original-A reuse."}
    write(f"{output}/SEARCH_RESULT.json", summary)
    return summary
