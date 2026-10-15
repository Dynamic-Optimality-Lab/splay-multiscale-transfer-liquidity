# PC_DEBUG1.py — flatten AND-chain, eval every leaf conjunct on failing env.
import sys, json
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG
from PC_LOW_COMPILER import build_low
import PC_LOW_TEST_RUN as T

d = DAG()
L = build_low(d, 'PL')


def flat(n, depth=0):
    k, t, a, e = d.nodes[n]
    if k == 'and' and depth < 3:
        out = []
        for x in (a[0], a[1]):
            out += flat(x, depth + 1)
        return out
    return [n]


leaves = flat(L['root'])
print('leaf conjuncts:', len(leaves))

# get failing env: patch run_grounded to return it
import PC_LOW_TEST_RUN as TR
orig = TR.run_grounded


def patched(dd, LL, ntrans=120, seed=71):
    import random
    from PC_CONCRETIZE import (AModel, BModel, depths_keys, gap_of, build_envA, build_envB,
                               build_envBT, build_envW, build_envI, shadow_of, serial)
    from CRA_pointer_tuple_replay import replay, from_serial
    import splay as S
    rng = random.Random(seed)
    # reuse body via exec of module source with hook? simplest: copy minimal failing-case extraction
    raise AssertionError('use direct approach below')


# direct: run loop from TR with sys.monitoring off; instead import and call internals is messy.
# Fallback: replicate minimal env build by calling TR.run_grounded with a poisoned ev that records.
import types
call = {}


def main():
    # run original until assert; catch via rewriting assert? Instead: temporarily replace d.ev
    real_ev = d.ev
    seen = {}
    def rec(n, env, _memo=None):
        r = real_ev(n, env, _memo)
        return r
    try:
        TR.run_grounded(d, L, ntrans=120, seed=71)
    except AssertionError as ex:
        print('failed as expected:', str(ex)[:200])


main()
