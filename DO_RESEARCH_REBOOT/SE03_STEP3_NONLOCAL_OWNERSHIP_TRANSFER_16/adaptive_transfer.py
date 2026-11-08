"""Producer implementation of the CONDITIONAL fresh-image escape theorem.
No source supplier is invented here. A recipe must separately certify each
escape pair, including original block/period/working eligibility.
"""
def extend(D, U, old_a, initial_h, recipe, roots=None):
    D, U = set(D), set(U)
    a, h = dict(old_a), dict(initial_h)
    assert set(a) <= D and set(h) <= D
    assert len(set(a.values())) == len(a) and len(set(h.values())) == len(h)
    assert set(a.values()) | set(h.values()) <= U
    inv = {u:d for d,u in a.items()}
    image = set(h.values())
    roots = sorted(D-set(a)) if roots is None else sorted(roots)
    assert set(roots) <= D-set(a)
    paths, escapes, blocked = [], [], []
    global_seen = set()
    for p in roots:
        d, steps = p, []
        while True:
            assert d not in global_seen, 'a rooted ownership component repeated'
            global_seen.add(d)
            if d not in h:
                # Returning None is honest failure to supply, not success.
                item = recipe(d, frozenset(image))
                if item is None:
                    blocked.append({'root':p, 'frontier':d})
                    break
                u, source_receipt = item
                assert u in U-image
                before = (len(D-set(h)), len(set(roots)-set(a)))
                h[d] = u
                image.add(u)
                after = (len(D-set(h)), len(set(roots)-set(a)))
                assert after < before
                escapes.append({'frontier':d, 'unit':u, 'receipt':source_receipt,
                    'rank_before':before, 'rank_after':after})
            u = h[d]
            owner = inv.get(u)
            steps.append({'demand':d, 'unit':u, 'current_owner':owner})
            if owner is None:
                before = (len(D-set(h)), len(set(roots)-set(a)))
                a[p] = u
                inv[u] = p
                after = (len(D-set(h)), len(set(roots)-set(a)))
                assert after < before
                break
            d = owner
        paths.append({'root':p, 'steps':steps,
            'terminal':a.get(p), 'blocked':p not in a})
    assert len(set(a.values())) == len(a) and all(a[d] == u for d,u in old_a.items())
    assert len(escapes) <= len(D-set(initial_h))
    assert len(global_seen) <= len(D)
    return {'allocation':a, 'comparison':h, 'paths':paths, 'escapes':escapes,
        'blocked':blocked, 'all_old_values_fixed':True,
        'visited_distinct_demands':len(global_seen)}
