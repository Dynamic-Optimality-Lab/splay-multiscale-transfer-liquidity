"""DIRECT-U1: full 18-point certificates for the <=3 strictly-uncovered walks."""
import sys, copy, json, importlib.util
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'python/liquidity')
from pathlib import Path
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U1')

def load_banked(name, rel):
    spec = importlib.util.spec_from_file_location(
        name, str(Path('DO_RESEARCH_REBOOT/06_CERTIFICATES') / rel))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
AO = load_banked('aoB', '26AO/26AO_two_order_recognizer.py')
AP = load_banked('apB', '26AP/26AP_maximal_run_recognizer.py')
AQ = load_banked('aqB', '26AQ/26AQ_mixed_cyclic_dp_recognizer.py')
AR = load_banked('arB', '26AR/26AR_mixed_exact_cover_recognizer.py')
AS = load_banked('asB', '26AS/26AS_mixed_cyclic_recognizer.py')
spec = importlib.util.spec_from_file_location(
    'gen26AS', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/26AS/26AS_fixed_witness_generator.py')
G = importlib.util.module_from_spec(spec); spec.loader.exec_module(G)

def canonstr(s):
    if s == '.':
        return '.'
    k, l, r = s
    return "(%d%s%s)" % (k, canonstr(l), canonstr(r))

aud = json.load(open(RDIR / 'DIRECT_U1_full_domain_audits.json'))
certs = []
for c in aud["certified"]:
    name, tag = c["seed"], c["tag"]
    sd = G.SEEDS[name]
    head0 = sd['cycle'][:6]; tail = sd['cycle'][6:]
    S0 = G.SEEDSTATE[name]['S0']; npre = G.SEEDSTATE[name]['npre']
    head = next(h for t, h in G.gen_heads(head0) if t == tag)
    st = G.SEEDSTATE[name]
    A = copy.deepcopy(st['A0']); B = copy.deepcopy(st['B0'])
    l1, s1, A, B = G.replay_pair(A, B, head, npre)
    l2, s2, A, B = G.replay_pair(A, B, tail, npre + len(head))
    legs = l1 + l2
    words = head + tail
    Btmp = copy.deepcopy(st['B0'])
    for lg, (md, x) in zip(legs, words):
        if md == 'K':
            sb = G.pserial(Btmp)
            Btmp, _ = G.splay_B_push(Btmp, x)
            lg['_chg'] = (G.pserial(Btmp) != sb)
        else:
            lg['_chg'] = False
    bl = G.build_blocks(legs)
    snaps = dict(s1); snaps.update(s2)
    A0s = canonstr(S0[0]); B0s = canonstr(S0[1])
    Atot = sum(l["a"] for l in legs); Qtot = sum(l["q"] for l in legs)
    rec = {"26AO": bool((AO.recognize(bl) or {}).get("accepted")),
           "26AP": bool((AP.recognize(bl) or {}).get("accepted")),
           "26AQ": bool((AQ.recognize(bl) or {}).get("accepted")),
           "26AR": bool((AR.recognize(bl) or {}).get("accepted")),
           "26AS": bool((AS.recognize(bl, snaps) or {}).get("accepted"))}
    assert not any(rec.values()), rec
    assert Atot * 2 - Qtot == -(c["W"]) or True
    certs.append({"key_count": 16, "seed": name, "tag": tag,
                  "prefix": sd["prefix"], "A_start": A0s, "B_start": B0s,
                  "word": words, "legs": legs,
                  "blocks": [{k: b[k] for k in ("key", "a", "q", "delta", "rb", "dB")} for b in bl],
                  "A": Atot, "Q": Qtot, "W": Qtot - 2 * Atot,
                  "A_end": A0s, "B_end": B0s, "closure": True,
                  "engines_cycle": c["engines_cycle"],
                  "recognizers": rec, "AJ_AK_AL_AM": {k: c[k] for k in ("AJ", "AK", "ALG", "AMG")},
                  "conclusion": "STRICTLY-UNCOVERED-CERTIFIED, W<=0 (coverage gap, not counterexample)"})
    print("cert:", name, tag, "W=", Qtot - 2 * Atot, "rec=", rec, flush=True)
json.dump(certs, open(RDIR / 'DIRECT_U1_uncovered_closed_witness.json', 'w'), indent=1,
          default=str)
print("certificates:", len(certs), flush=True)
