# QG-DAG emitter (hash-consed, de Bruijn binders) + rotation transducer + node accounting.
import sys, json

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_STAGE11F_CLOSURE_CERTIFIED/'

class DAG:
    def __init__(self, budget=4000000):
        self.nodes = []  # (tag, args)
        self.memo = {}
        self.budget = budget
    def mk(self, tag, args):
        key = (tag, tuple(args))
        if key in self.memo:
            return self.memo[key]
        if len(self.nodes) >= self.budget:
            raise ResourceWarning("QG-DAG node budget exceeded")
        i = len(self.nodes)
        self.nodes.append((tag, tuple(args)))
        self.memo[key] = i
        return i
    def var(self, name):
        return self.mk('var', (name,))
    def const(self, v):
        return self.mk('const', (v,))
    def cmp(self, op, a, b):
        return self.mk('cmp', (op, a, b))
    def AND(self, *xs):
        r = self.const(1)
        for x in xs:
            r = self.mk('and', (r, x))
        return r
    def OR(self, *xs):
        r = self.const(0)
        for x in xs:
            r = self.mk('or', (r, x))
        return r
    def NOT(self, x):
        return self.mk('not', (x,))
    def add(self, a, b):
        return self.mk('add', (a, b))
    def exists(self, varname, body):
        return self.mk('exists', (varname, body))
    def pred(self, name, *xs):
        return self.mk('pred', (name,) + tuple(xs))
    def ref(self, target, tag):
        return self.mk('ref', (target, tag))

def build_rotation_circuit(dag):
    # one primitive-rotation transducer slot over symbolic node variables:
    # inputs: parent key kp, child key kc, side s, subtree occupancy flags (4)
    # output: legality + effect descriptors for LL/RR/LR/RL/ZIG cases
    kp = dag.var('kp')
    kc = dag.var('kc')
    side = dag.var('side')
    occ = [dag.var('occ%d' % i) for i in range(4)]
    # BST-order legality: (side=L & kc<kp) | (side=R & kc>kp), keys in 0..267 range (9-bit + slack)
    legal = dag.OR(
        dag.AND(dag.cmp('eq', side, dag.const(0)), dag.cmp('lt', kc, kp)),
        dag.AND(dag.cmp('eq', side, dag.const(1)), dag.cmp('lt', kp, kc)),
    )
    # effect: child rises one level (d-1), parent drops one (d+1), middle subtree keeps level
    dc_in = dag.var('d_child_in')
    dp_in = dag.var('d_par_in')
    eff = dag.AND(
        dag.cmp('eq', dag.var('d_child_out'), dag.add(dc_in, dag.const(-1))),
        dag.cmp('eq', dag.var('d_par_out'), dag.add(dp_in, dag.const(1))),
        dag.cmp('eq', dag.var('d_mid_out'), dag.var('d_mid_in')),
    )
    # case selector over 5 event kinds
    ev = dag.var('evkind')
    cases = [dag.cmp('eq', ev, dag.const(i)) for i in range(5)]
    out = dag.AND(legal, eff, dag.OR(*cases))
    return out

if __name__ == "__main__":
    dag = DAG()
    r = build_rotation_circuit(dag)
    print("rotation-slot nodes: %d" % len(dag.nodes), flush=True)
    # 4 slots (shared single-slot circuit referenced 4x => sharing, not 4x nodes)
    slots = [dag.ref(r, i) for i in range(4)]
    print("4-slot shared nodes: %d" % len(dag.nodes), flush=True)
    # order validation fragment: BST interval check (lo<k<hi, 9-bit) + S-membership bitmask (9 bits)
    k = dag.var('k')
    lo = dag.var('lo')
    hi = dag.var('hi')
    Smask = dag.var('smask')
    Sb = dag.var('sbit')
    order_ok = dag.AND(dag.cmp('lt', lo, k), dag.cmp('lt', k, hi),
                       dag.OR(dag.cmp('eq', dag.mk('and', (Smask, Sb)), Sb), dag.const(1)))
    print("+order nodes: %d" % len(dag.nodes), flush=True)
    # Hall-guard arithmetic fragment: one subset inequality sum_{i in I} d_i >= |{r: N(r) subset I}|
    # (representative: 3 gaps, threshold compare, 12-bit sum)
    dd = [dag.var('d%d' % i) for i in range(3)]
    ssum = dag.add(dag.add(dd[0], dd[1]), dd[2])
    hall1 = dag.cmp('ge', ssum, dag.const(2))
    print("+hall nodes: %d" % len(dag.nodes), flush=True)
    # B-core successor fragment: table lookup predicate (9-key B state + target -> depth + q)
    bb = dag.var('bstate')
    vv = dag.var('vtarget')
    bpred = dag.pred('Bsucc', bb, vv, dag.var('bnext'), dag.var('q'))
    print("+bcore nodes: %d" % len(dag.nodes), flush=True)
    json.dump({"rotation_slot": len([n for n in dag.nodes]),
               "total": len(dag.nodes)},
              open(PDIR + "CC_DAG_PROBE.json", "w"), indent=1)
    print("DAG OK", flush=True)
