# STRICT_BISECT.py — iterative failing-leaf finder for strict grounded failures.
import sys, json
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
import random

d = DAG()
L = build_slow(d, 'SL')
keys = list(range(1, 10))
Sset = set(keys)
rng = random.Random(7)
A = S.balanced(keys)
M = set(rng.sample(keys, 5))
x = rng.choice(sorted(M))
a = (S.lookup(A, x)[1] + 1) // 2
print('trial0:', M, x, a)
st, info = ssertify(d, L, serial(A), serial(A), Sset, M, [('K', x)], a)
print(st, str(info)[:100] if isinstance(info, dict) else info)
if st == 'fail' and isinstance(info, dict) and 'env' in info:
    env = info['env']
    shown = [0]
    stack = [(L['root'], 0)]
    while stack and shown[0] < 10:
        n, depth = stack.pop()
        k, t, aa, e = d.nodes[n]
        v = d.ev_iter(n, env)
        if v is True:
            continue
        if k in ('and', 'or'):
            for xx in aa:
                stack.append((xx, depth + 1))
        else:
            print('  FAIL nid=%d kind=%s' % (n, k))
            shown[0] += 1
