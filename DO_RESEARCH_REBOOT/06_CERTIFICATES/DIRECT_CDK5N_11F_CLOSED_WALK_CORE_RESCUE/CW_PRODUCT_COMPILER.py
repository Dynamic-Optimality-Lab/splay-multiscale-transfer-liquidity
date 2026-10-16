# CW_PRODUCT_COMPILER.py — Gate G: complete repaired weighted product (low+high+operators-ready).
# Sharing via capture-safe subst renaming (no historical modification): low/high built with fresh
# tags, then s/t/g vars renamed to canonical QO/QO2/QM. Hash-consing shares structure.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
from PC_TYPED_DAG import DAG, BOOL, INT
from STRICT_LOW_COMPILER import StateVars7, build_slow, state_valid7
from STRICT_HIGH_COMPILER import FiberVars7, build_shigh

WALPHA = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]


def state_suffixes7(prefix):
    # StateVars7 var names and their canonical suffixes
    out = [prefix + '_mu']
    for v in ['bkl%d', 'brl%d', 'bkr%d', 'brr%d', 'blo%d', 'bhi%d']:
        out += [prefix + '_b_' + (v % i) for i in range(19)]
    out.append(prefix + '_b_broot')
    for p in range(7):
        out += [prefix + '_ak%d' % p, prefix + '_aS%d' % p, prefix + '_aI%d' % p]
    for i in range(10):
        out.append(prefix + '_sg%d' % i)
    return out


def fiber_suffixes(prefix):
    out = [prefix + '_fmu']
    for i in range(10):
        out.append(prefix + '_fsg%d' % i)
    for v in ['bkl%d', 'brl%d', 'bkr%d', 'brr%d', 'blo%d', 'bhi%d']:
        out += [prefix + '_fb_' + (v % i) for i in range(19)]
    out.append(prefix + '_fb_broot')
    out.append(prefix + '_fv')
    return out


class Product:
    def __init__(self, dag):
        d = dag
        self.d = d
        self.O = StateVars7(d, 'QO')
        self.O2 = StateVars7(d, 'QO2')
        self.M = FiberVars7(d, 'QM')
        self.low = build_slow(d, 'CL')
        self.high = build_shigh(d, 'CH')
        # rename maps to canonical sets
        mpL = {}
        for a, b in zip(state_suffixes7('CLs'), state_suffixes7('QO')):
            mpL[a] = b
        for a, b in zip(state_suffixes7('CLt'), state_suffixes7('QO2')):
            mpL[a] = b
        mpH = {}
        for a, b in zip(state_suffixes7('CHs'), state_suffixes7('QO')):
            mpH[a] = b
        for a, b in zip(state_suffixes7('CHt'), state_suffixes7('QO2')):
            mpH[a] = b
        for a, b in zip(fiber_suffixes('CHg'), fiber_suffixes('QM')):
            mpH[a] = b
        # q/weight vars renamed per edge below (keep originals, add EQ bridges instead)
        self.E_low = {}
        for w in WALPHA:
            if -4 <= w <= 4:
                e = d.AND(self.low['root'], d.EQ(self.low['w'], d.const_int(w, 5, signed=True)))
                self.E_low[w] = d.subst(e, mpL)
        hroot = d.subst(self.high['root'], mpH)
        o2b = sorted(v for v in d.vars_in(hroot) if v.startswith('QO2'))
        o1b = sorted(v for v in d.vars_in(hroot) if v.startswith('QO') and not v.startswith('QO2'))
        self.E_sm = d.EXISTS(tuple(o2b), hroot)
        self.E_mt = d.EXISTS(tuple(o1b), hroot)
        # weight selectors over renamed q (original var name retained; bridge by EQ below in edge())
        self._hq = self.high['q']
        self._mpH = mpH

    def edge(self, w, sort_s, sort_t):
        d = self.d
        if sort_s == 0 and sort_t == 0:
            if w in self.E_low:
                return self.E_low[w]
            return d.const_bool(False)
        if sort_s == 0 and sort_t == 1:
            if 0 <= 6 - w <= 9:
                return self._sm_w(w)
            return d.const_bool(False)
        if sort_s == 1 and sort_t == 0:
            if w == 0:
                return self.E_mt
            return d.const_bool(False)
        return d.const_bool(False)

    def _sm_w(self, w):
        # s->m weight 6-q == w  <=>  original q == 6-w, conjoined inside the fiber scope.
        # Rebuild: EXISTS O2 (hroot_subst AND q==6-w) where hroot_subst keeps original q var.
        d = self.d
        hroot = d.subst(self.high['root'], self._mpH)
        o2b = sorted(v for v in d.vars_in(hroot) if v.startswith('QO2'))
        return d.EXISTS(tuple(o2b), d.AND(hroot, d.EQ(self.high['q'], d.const_int(6 - w, 4))))
