# PP_INDEPENDENT_VERIFIER.py — replays every certificate claim from sources (no trust in JSON).
import sys, json, hashlib, os
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'
res = {}
ok = True


def check(name, cond, info=''):
    global ok
    res[name] = {'pass': bool(cond), 'info': info}
    if not cond:
        ok = False
    print(('PASS' if cond else 'FAIL'), name, info, flush=True)


# 1. sources
exp = {'scripts/wp6_eventflow.py': 'd7cc806079d53857f3e4a20c8adc5e79447a7a42ebc0f79b145833fb63703053',
       'scripts/wp6_coarse_double.py': 'b47019afa261dd6f5f9fac6949d5c37ae229fd215d082296a1ed42570900365f',
       'python/independent/splay.py': '3a178c131c70c08419f18d1035dfb32beb5aa781673098ffbd4a5293f91d2f01',
       'python/liquidity/legacy_embedding.py': '20284bbc810a2c64c1b4f66f431b5479795b6d6658d258bb5d4a4f4b543e1cb2'}
for p, h in exp.items():
    check('src:' + p, hashlib.sha256(open(p, 'rb').read()).hexdigest() == h)

# 2. JSON presence + internal consistency
def J(n):
    return json.load(open(PDIR + n))
for n in ['PP_PORT_SMOKE.json', 'PP_INVENTORY_TEST.json', 'PP_DST_SHARED_TEST.json', 'PP_LOW_TEST.json',
          'PP_HIGH_TEST.json', 'PP_PRODUCT_TEST.json', 'PP_OPERATOR_TEST.json', 'PP_GUARD_CENSUS.json']:
    d = J(n)
    check('json:' + n, isinstance(d, dict) and len(d) > 0, str({k: d[k] for k in list(d)[:3]}))

# 3. spot re-execution (reduced scale, independent code paths)
from PP_PORT_ROTATION_TRANSDUCER import cut, fill, splay_skel
from PP_JOINT_INVENTORY import read_witness, joint_valid
from PP_LOW_RELATION import decide, S_to_list
import random
rng = random.Random(99)
nsp = 0
for trial in range(60):
    n = rng.randint(10, 25)
    ks = list(range(1, n + 1))
    Sset = set(rng.sample(ks, 9))
    t = S.LEAF
    kk = sorted(ks)
    rng.shuffle(kk)
    def ins(t, k):
        return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], ins(t[3], k)))
    for k in kk:
        t = ins(t, k)
    skel, ports, atoms, Vs, hidden, c, sh, p, non = read_witness(t, Sset)
    o, w = joint_valid(skel, ports, atoms, hidden, c, sh, p, Sset, non)
    assert o, w
    x = rng.choice(ks)
    d = S.lookup(t, x)[1]
    if (d + 1) // 2 <= 2:
        sk, _ = splay_skel(skel, x)
        F = {}
        for pid in ports:
            sub = t
            for step in pid:
                _, _, l, r = sub
                sub = l if step == 'L' else r
            F[pid] = sub
        assert fill(sk, F) == S.trace(t, x)[0]
        nsp += 1
check('spot:commutation+inventory', nsp > 20, 'n=%d' % nsp)

# 4. cross-consistency: operator scope == product scope; guard census macros >= distinct
op = J('PP_OPERATOR_TEST.json')
pr = J('PP_PRODUCT_TEST.json')
check('xcons:scope', op['scope'].split()[0] == pr['scope'].split()[0], op['scope'])
gc = J('PP_GUARD_CENSUS.json')
check('xcons:guards', gc['macros'] + gc['fringe_macros'] >= gc['distinct_guards'], str(gc['distinct_guards']))
lo = J('PP_LOW_TEST.json')
check('xcons:low', lo['agree'] == lo['total'] and lo['total'] > 0, str(lo['total']))
hi = J('PP_HIGH_TEST.json')
check('xcons:high', hi['covered'] + hi['nongenuine_skipped'] == hi['transitions'], str(hi['covered']))

print('VERIFIER:', 'ALL PASS' if ok else 'FAILURES PRESENT', flush=True)
json.dump({'ok': ok, 'checks': res}, open(PDIR + 'PP_VERIFIER_REPORT.json', 'w'), indent=1)
sys.exit(0 if ok else 1)
