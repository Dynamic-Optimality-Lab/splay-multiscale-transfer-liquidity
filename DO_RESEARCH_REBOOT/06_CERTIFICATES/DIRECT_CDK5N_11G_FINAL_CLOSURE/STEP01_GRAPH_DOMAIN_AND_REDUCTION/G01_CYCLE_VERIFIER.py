# G01_CYCLE_VERIFIER.py — cycle verification (Phase H).
# verify_cycle(verts, edge_fn, decide): checks closure (first==last), per-edge
# SAT with witness extraction, total signed weight. classify_source_liftability:
# TYPE C (fails relation) / TYPE A-or-B-or-D (valid abstract cycle; liftability
# decided separately by source replay, never assumed here).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')


def verify_cycle(verts, edge_fn, decide):
    """verts: [v0..vk=v0] pin-dicts; edge_fn(a,b)->(root,w). Returns cert dict."""
    if not verts or verts[0] != verts[-1]:
        return {'closed': False, 'verdict': 'NOT-CLOSED'}
    tot = 0
    segs = []
    for a, b in zip(verts[:-1], verts[1:]):
        root, w = edge_fn(a, b)
        r = decide(root, dict(a, **b))
        if r[0] != 'SAT':
            return {'closed': True, 'verdict': 'EDGE-UNSAT', 'at': (a, b, w, r[0], r[2])}
        tot += w
        segs.append((w, r[1] is not None))
    return {'closed': True, 'verdict': 'SAT', 'total': tot, 'negative': tot < 0, 'n': len(segs)}


def classify_source_liftability(cycle_cert):
    if cycle_cert.get('verdict') != 'SAT':
        return 'TYPE-C'
    return 'TYPE-B-or-D (abstract-valid; liftability requires source replay)'
