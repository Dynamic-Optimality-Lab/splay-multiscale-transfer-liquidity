# PC_CONCRETIZE.py — concrete transition -> full symbolic witness assumption env (V8 bridge).
# Plain-dict models drive BOTH var assignment AND path computation (single source of truth).
# Filter: terminal target marked with all-core B-ancestors (skeleton depth == concrete depth).
import sys
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial


def depths_keys(t):
    out = {}
    def go(s, d, par=None, side=None):
        if s[0] == 'leaf':
            return
        _, k, l, r = s
        out[k] = (d, par, side)
        go(l, d + 1, k, 0)
        go(r, d + 1, k, 1)
    go(t, 0)
    return out


def gap_of(Ss, x):
    i = 0
    for s in Ss:
        if x > s:
            i += 1
        else:
            break
    return i


def serial(t):
    if t[0] == 'leaf':
        return None
    _, k, l, r = t
    return [k, serial(l), serial(r)]


class AModel:
    """Cut model of concrete A tree: slots + ports + ranks + bounds."""

    def __init__(self, t, Sset):
        Ss = sorted(Sset)
        self.Ss = Ss
        self.sidx = {k: i for i, k in enumerate(Ss)}
        # BFS slots
        self.slots = {}  # sid -> dict(key,depth,par,side)
        self.kids = {}   # sid -> ( (kl,rl),(kr,rr) ) with rl = sid | ('P',s,b) | None
        q = [(t, 0, None, None, 0)]
        ns = [1]
        while q:
            nd, sid, par, side, d = q.pop(0)
            _, k, l, r = nd
            self.slots[sid] = {'key': k, 'depth': d, 'par': par, 'side': side, 'l': l, 'r': r}
            if d < 6:
                lk = {}
                for ch, b in ((l, 0), (r, 1)):
                    if ch[0] == 'leaf':
                        lk[b] = (2, None)
                    else:
                        cs = ns[0]
                        ns[0] += 1
                        q.append((ch, cs, sid, b, d + 1))
                        lk[b] = (0, cs)
                self.kids[sid] = (lk[0], lk[1])
            else:
                self.kids[sid] = tuple((1, (sid, b)) if ch[0] != 'leaf' else (2, None) for ch, b in ((l, 0), (r, 1)))
        # V ranks
        V = sorted(set(Ss) | {v['key'] for v in self.slots.values()})
        self.V = V
        self.rank = {k: i for i, k in enumerate(V)}
        # bounds
        self.lo = {}
        self.hi = {}
        self.lo[0], self.hi[0] = 0, 136
        for sid, v in self.slots.items():
            if sid == 0:
                continue
            p = v['par']
            if v['side'] == 0:
                self.lo[sid], self.hi[sid] = self.lo[p], self.rank[self.slots[p]['key']]
            else:
                self.lo[sid], self.hi[sid] = self.rank[self.slots[p]['key']] + 1, self.hi[p]
        # ports content: hidden S + fringe by gap
        self.phS = {}
        self.pz = {}
        dk = depths_keys(t)
        for (s, b), sub in self._port_subs(t).items():
            hk = [kk for kk in self._keys(sub) if kk in Sset]
            self.phS[(s, b)] = sorted(hk)
            z = [0] * 10
            for kk in self._keys(sub):
                if kk not in Sset:
                    z[gap_of(Ss, kk)] += 1
            self.pz[(s, b)] = z
        # sigma + pexp
        self.sig = [0] * 10
        for kk in V:
            if kk not in Sset:
                pass
        for kk in S.inorder(t):
            if kk not in Sset:
                self.sig[gap_of(Ss, kk)] += 1

    def _keys(self, s):
        out = []
        def go(x):
            if x[0] == 'leaf':
                return
            _, k, l, r = x
            out.append(k)
            go(l)
            go(r)
        go(s)
        return out

    def _port_subs(self, t):
        out = {}
        for sid, v in self.slots.items():
            if v['depth'] == 6:
                nd = self._find(t, v['key'])
                _, k, l, r = nd
                if l[0] != 'leaf':
                    out[(sid, 0)] = l
                if r[0] != 'leaf':
                    out[(sid, 1)] = r
        return out

    def _find(self, t, key):
        if t[0] == 'leaf':
            return None
        _, k, l, r = t
        if k == key:
            return t
        return self._find(l if key < k else r, key)

    def path_to(self, key):
        """(slots bottom-up from target's slot, dirs) or None if key not exposed."""
        tgt = None
        for sid, v in self.slots.items():
            if v['key'] == key:
                tgt = sid
        if tgt is None:
            return None
        path, dirs = [tgt], []
        cur = tgt
        while cur != 0:
            dirs.append(self.slots[cur]['side'])
            cur = self.slots[cur]['par']
            path.append(cur)
        return path, dirs


class BModel:
    """19-node skeleton model: core links (nearest-S) + gap slots at valid NULLs."""

    def __init__(self, B, Sset):
        Ss = sorted(Sset)
        self.Ss = Ss
        self.sidx = {k: i for i, k in enumerate(Ss)}
        dk = depths_keys(B)
        ch = {}
        def go(s):
            if s[0] == 'leaf':
                return
            _, k, l, r = s
            ch[k] = (l[1] if l[0] != 'leaf' else None, r[1] if r[0] != 'leaf' else None)
            go(l)
            go(r)
        go(B)
        self.ch = ch
        self.dk = dk
        # core parent links
        self.cpar = {}
        for k in Ss:
            a = dk[k][1]
            while a is not None and a not in Sset:
                a = dk[a][1]
            self.cpar[k] = a
        # NULL spans for gap attach
        self.spans = {}
        def walkf(k, lo, hi):
            for side in (0, 1):
                c = ch[k][side]
                if c is None:
                    self.spans[(k, side)] = (lo, hi)
                elif c in Sset:
                    kk = self.sidx[c]
                    if side == 0:
                        walk(c, lo, kk)
                    else:
                        walk(c, kk + 1, hi)
                else:
                    walkf(c, lo, hi)
        def walk(k, lo, hi):
            kk = self.sidx[k]
            for side in (0, 1):
                c = ch[k][side]
                nlo, nhi = (lo, kk) if side == 0 else (kk + 1, hi)
                if c is None:
                    self.spans[(k, side)] = (nlo, nhi)
                elif c in Sset:
                    walk(c, nlo, nhi)
                else:
                    walkf(c, nlo, nhi)
        root = next(k for k, (d, p, s) in dk.items() if p is None)
        if root in Sset:
            walk(root, 0, 9)
        else:
            walkf(root, 0, 9)
        self.attach = {}
        for g in range(10):
            self.attach[g] = None
            for (k, side), (lo, hi) in self.spans.items():
                if lo <= g <= hi:
                    self.attach[g] = (k, side)
                    break
        # skeleton children: core id i -> per side nearest S descendant (max depth) or None.
        # m in left subtree of k  <=>  k ancestor of m and m < k (BST property).
        def is_anc(a, m):
            x = dk[m][1]
            while x is not None:
                if x == a:
                    return True
                x = dk[x][1]
            return False
        self.sk = {}
        for k in Ss:
            i = self.sidx[k]
            for side in (0, 1):
                best, bd = None, 10 ** 9
                for m in Ss:
                    if m == k or not is_anc(k, m):
                        continue
                    if (side == 0 and m < k) or (side == 1 and m > k):
                        if dk[m][0] < bd:
                            best, bd = m, dk[m][0]
                self.sk[(i, side)] = ('C', self.sidx[best]) if best is not None else ('NULL', None)
        # validity: nearest-links form a single BST tree over S (single root, sides consistent, connected)
        self.ok = True
        roots = [k for k in Ss if self.cpar[k] is None]
        if len(roots) != 1:
            self.ok = False
        else:
            seen = set()
            st = [roots[0]]
            while st:
                k = st.pop()
                if k in seen:
                    self.ok = False
                    break
                seen.add(k)
                i = self.sidx[k]
                for side in (0, 1):
                    e = self.sk[(i, side)]
                    if e[0] == 'C':
                        m = Ss[e[1]]
                        if (side == 0 and m > k) or (side == 1 and m < k):
                            self.ok = False
                        if self.cpar[m] != k:
                            self.ok = False
                        st.append(m)
            if len(seen) != len(Ss):
                self.ok = False

    def path_to_core(self, k):
        """Bottom-up core path (S keys) from k to core root + dirs."""
        path, dirs = [k], []
        cur = k
        while self.cpar[cur] is not None:
            p = self.cpar[cur]
            # side: which side of p (compare sidx)
            dirs.append(0 if self.sidx[cur] < self.sidx[p] else 1)
            cur = p
            path.append(cur)
        return path, dirs

    def path_to_gap(self, g):
        """Bottom-up path to gap slot g: core path to attach parent + final step. Returns (nodes, dirs)
        where nodes[0] = ('G',g). Core nodes as S keys; dirs aligned."""
        att = self.attach[g]
        if att is None:
            return None
        pk, side = att
        if pk in self.Ss:
            path, dirs = self.path_to_core(pk)
            nodes = [('G', g)] + path
            dirs = [side] + dirs
            return nodes, dirs
        # attachment under fringe: walk core path of nearest S below/above? fallback: None (skip)
        return None


def build_envA(env, am, Sset, vpre='PLw'):
    Ss = sorted(Sset)
    V = am.V
    nV = len(V)
    for sid, v in am.slots.items():
        env[f'{vpre}_p{sid}'] = 1
        env[f'{vpre}_dep{sid}'] = v['depth']
        env[f'{vpre}_par{sid}'] = v['par'] if v['par'] is not None else 0
        env[f'{vpre}_side{sid}'] = v['side'] if v['side'] is not None else 0
        k = v['key']
        isS = 1 if k in Sset else 0
        env[f'{vpre}_isS{sid}'] = isS
        env[f'{vpre}_sidx{sid}'] = Ss.index(k) if isS else 0
        env[f'{vpre}_rank{sid}'] = V.index(k)
        env[f'{vpre}_lo{sid}'] = am.lo[sid]
        env[f'{vpre}_hi{sid}'] = am.hi[sid]
        (kl, rl), (kr, rr) = am.kids[sid]
        env[f'{vpre}_kl{sid}'] = kl
        env[f'{vpre}_kr{sid}'] = kr
        env[f'{vpre}_cl{sid}'] = rl if kl == 0 else (rl[0] * 2 + rl[1] if kl == 1 else 255)
        env[f'{vpre}_cr{sid}'] = rr if kr == 0 else (rr[0] * 2 + rr[1] if kr == 1 else 255)
    # absent slots
    for sid in range(127):
        if sid not in am.slots:
            env[f'{vpre}_p{sid}'] = 0
            env[f'{vpre}_dep{sid}'] = 0
            env[f'{vpre}_par{sid}'] = 0
            env[f'{vpre}_side{sid}'] = 0
            env[f'{vpre}_isS{sid}'] = 0
            env[f'{vpre}_sidx{sid}'] = 0
            env[f'{vpre}_rank{sid}'] = 0
            env[f'{vpre}_lo{sid}'] = 0
            env[f'{vpre}_hi{sid}'] = 136
            env[f'{vpre}_kl{sid}'] = 2
            env[f'{vpre}_kr{sid}'] = 2
            env[f'{vpre}_cl{sid}'] = 255
            env[f'{vpre}_cr{sid}'] = 255
    return nV


def build_envB(env, bm, Sset, vpre='PL_b0'):
    Ss = sorted(Sset)
    for k in Ss:
        i = bm.sidx[k]
        for side in (0, 1):
            e = bm.sk.get((i, side), None)
            if e is not None and e[0] == 'C':
                env[f'{vpre}_bkl{i}' if side == 0 else f'{vpre}_bkr{i}'] = 0
                env[f'{vpre}_brl{i}' if side == 0 else f'{vpre}_brr{i}'] = e[1]
            else:
                env[f'{vpre}_bkl{i}' if side == 0 else f'{vpre}_bkr{i}'] = 2
                env[f'{vpre}_brl{i}' if side == 0 else f'{vpre}_brr{i}'] = 19
    for g in range(10):
        i = 9 + g
        env[f'{vpre}_bkl{i}'] = 2
        env[f'{vpre}_bkr{i}'] = 2
        env[f'{vpre}_brl{i}'] = 19
        env[f'{vpre}_brr{i}'] = 19
        env[f'{vpre}_blo{i}'] = 2 * g
        env[f'{vpre}_bhi{i}'] = 2 * g
    rootS = next(k for k in Ss if bm.cpar[k] is None)
    env[f'{vpre}_broot'] = bm.sidx[rootS]
    blo = {bm.sidx[rootS]: 0}
    bhi = {bm.sidx[rootS]: 18}
    order = [rootS]
    while order:
        k = order.pop(0)
        i = bm.sidx[k]
        r = 2 * i + 1
        for side in (0, 1):
            e = bm.sk.get((i, side))
            if e is not None and e[0] == 'C':
                j = e[1]
                if side == 0:
                    blo[j], bhi[j] = blo[i], r - 1
                else:
                    blo[j], bhi[j] = r + 1, bhi[i]
                order.append(Ss[j])
    for k in Ss:
        i = bm.sidx[k]
        env[f'{vpre}_blo{i}'] = blo[i]
        env[f'{vpre}_bhi{i}'] = bhi[i]
    return rootS


def build_envBT(env, bt_info, vpre='PLbt'):
    for e in range(5):
        if e < len(bt_info):
            b = bt_info[e]
            env[f'{vpre}_bT{e}'] = b['T']
            env[f'{vpre}_bd{e}'] = b['d']
            for k in range(19):
                env[f'{vpre}_bp{e}_{k}'] = b['path'][k] if k < len(b['path']) else 0
            for k in range(18):
                env[f'{vpre}_bdir{e}_{k}'] = b['dirs'][k] if k < len(b['dirs']) else 0
        else:
            env[f'{vpre}_bT{e}'] = 0
            env[f'{vpre}_bd{e}'] = 0
            for k in range(19):
                env[f'{vpre}_bp{e}_{k}'] = 0
            for k in range(18):
                env[f'{vpre}_bdir{e}_{k}'] = 0


def build_envW(env, w_info, vpre='PLw'):
    env[f'{vpre}_nev'] = len(w_info)
    for e in range(5):
        if e < len(w_info):
            b = w_info[e]
            env[f'{vpre}_eK{e}'] = 1 if b['isK'] else 0
            env[f'{vpre}_eT{e}'] = b['slot']
            env[f'{vpre}_ed{e}'] = b['d']
            for k in range(5):
                env[f'{vpre}_ep{e}_{k}'] = b['path'][k] if k < len(b['path']) else 0
            for k in range(4):
                env[f'{vpre}_edir{e}_{k}'] = b['dirs'][k] if k < len(b['dirs']) else 0
        else:
            env[f'{vpre}_eK{e}'] = 0
            env[f'{vpre}_eT{e}'] = 0
            env[f'{vpre}_ed{e}'] = 0
            for k in range(5):
                env[f'{vpre}_ep{e}_{k}'] = 0
            for k in range(4):
                env[f'{vpre}_edir{e}_{k}'] = 0


def build_envI(env, am, Sset, vpre='PLv'):
    Ss = sorted(Sset)
    for s in range(127):
        for b in range(2):
            key = (s, b)
            for k in range(9):
                env[f'{vpre}_hs{s}_{b}_{k}'] = 0
                env[f'{vpre}_hsr{s}_{b}_{k}'] = 0
            for i in range(10):
                env[f'{vpre}_z{i}_{s}_{b}'] = 0
    for (s, b), hk in am.phS.items():
        for kk in hk:
            env[f'{vpre}_hs{s}_{b}_{Ss.index(kk)}'] = 1
            env[f'{vpre}_hsr{s}_{b}_{Ss.index(kk)}'] = am.V.index(kk)
    for (s, b), z in am.pz.items():
        for i in range(10):
            env[f'{vpre}_z{i}_{s}_{b}'] = z[i]
    for i in range(10):
        env[f'{vpre}_sg{i}'] = am.sig[i]


def shadow_of(t):
    if t[0] == 'leaf':
        return None
    _, k, l, r = t
    def d1(s):
        if s[0] == 'leaf':
            return (2, None)
        return (0, s[1])
    return (k, d1(l), d1(r))
