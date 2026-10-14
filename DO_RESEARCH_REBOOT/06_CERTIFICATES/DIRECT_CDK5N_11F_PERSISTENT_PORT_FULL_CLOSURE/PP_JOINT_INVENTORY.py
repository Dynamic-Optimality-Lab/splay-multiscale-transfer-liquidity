# PP_JOINT_INVENTORY.py — shared inorder atoms + JointInventoryValid + reconstruction.
import sys, json, random
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S
from AFSP_allocate import solve_allocation
from PP_PORT_ROTATION_TRANSDUCER import cut, fill, splay_skel, CUT

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'


def srank(Sset):
    return {k: i for i, k in enumerate(sorted(Sset))}  # gap index = # S keys strictly below


def gap_of(Ssorted, x):
    i = 0
    for s in Ssorted:
        if x > s:
            i += 1
        else:
            break
    return i  # 0..9


def atoms_of(skel, ports, Sset):
    """V = S | exposed keys. Atoms: open intervals between consecutive V keys (+infinities).
    Each atom -> (lo, hi, gap, port-or-None). Port-less atoms are forced empty."""
    Ss = sorted(Sset)
    V = set(Ss)
    def collect(s):
        if s[0] == 'E':
            return
        if s[0] == 'P':
            return
        _, k, l, r = s
        V.add(k)
        collect(l)
        collect(r)
    collect(skel)
    Vs = sorted(V)
    bounds = [None] + Vs + [None]
    atoms = []
    for a in range(len(bounds) - 1):
        lo, hi = bounds[a], bounds[a + 1]
        mid = lo if hi is None else hi  # gap determined by keys strictly below hi
        g = gap_of(Ss, hi) if hi is not None else 9
        # owning port: unique port with lo>=plo and hi<=phi (using None-safe compare)
        owner = None
        for pid, pr in ports.items():
            plo, phi = pr['lo'], pr['hi']
            oklo = (plo is None) or (lo is not None and lo >= plo) or (lo is None and plo is None)
            okhi = (phi is None) or (hi is not None and hi <= phi) or (hi is None and phi is None)
            # atom inside port range: plo <= lo and hi <= phi
            left = (plo is None and True) or (plo is not None and lo is not None and lo >= plo) or (plo is None)
            right = (phi is None) or (hi is not None and hi <= phi)
            # careful with None infinities: represent -inf as None lo
            Lin = (plo is None) or (lo is not None and lo >= plo)
            Rin = (phi is None) or (hi is not None and hi <= phi)
            if Lin and Rin:
                # exclude atoms strictly outside: need overlap of (lo,hi) with (plo,phi); since V-keys split, containment suffices
                if owner is not None and owner != pid:
                    pass  # nested impossible for disjoint port ranges; keep first
                owner = pid if owner is None else owner
        atoms.append({'lo': lo, 'hi': hi, 'gap': g, 'port': owner})
    return atoms, Vs


def joint_valid(skel, ports, atoms, hidden, c, sigma_hat, p_exp, Sset, nonempty):
    """hidden: pid -> sorted list of S keys. c: per-atom fringe counts. Returns (ok, reason)."""
    Ss = sorted(Sset)
    # (d) S uniqueness + placement
    seen = []
    for pid, hs in hidden.items():
        pr = ports[pid]
        for k in hs:
            if (pr['lo'] is not None and k <= pr['lo']) or (pr['hi'] is not None and k >= pr['hi']):
                return False, 'S-interval'
            seen.append(k)
    if sorted(seen) != Ss and set(seen) != set(Ss):
        # hidden + exposed-S must cover S
        expS = set()
        def col(s):
            if s[0] == 'K':
                if s[1] in Sset:
                    expS.add(s[1])
                col(s[2])
                col(s[3])
        col(skel)
        if set(seen) | expS != set(Ss):
            return False, 'S-cover'
        if len(set(seen)) != len(seen):
            return False, 'dup-S'
    # (b) per-gap conservation
    for i in range(10):
        tot = sum(cc for a, cc in zip(atoms, c) if a['gap'] == i)
        if tot != sigma_hat[i] - p_exp[i]:
            return False, ('gap', i, tot)
    # (c) occupancy
    for pid, pr in ports.items():
        idx = [n for n, a in enumerate(atoms) if a['port'] == pid]
        pop = sum(c[n] for n in idx)
        hs = hidden.get(pid, [])
        if pid not in nonempty:
            if pop != 0 or len(hs) != 0:
                return False, ('empty-viol', pid)
        else:
            if len(hs) == 0 and pop < 1:
                return False, ('nonempty-viol', pid)
    # forced-empty port-less atoms
    for n, a in enumerate(atoms):
        if a['port'] is None and c[n] != 0:
            return False, ('exposed-atom', n)
    return True, ('ok',)


def read_witness(t, Sset):
    """Completeness direction: cut a real tree, read hidden/c/p_exp/nonempty/sigma_hat."""
    skel, ports = cut(t, Sset)
    atoms, Vs = atoms_of(skel, ports, Sset)
    Ss = sorted(Sset)
    hidden = {pid: sorted(pr['hidden_S']) for pid, pr in ports.items()}
    # per-atom fringe counts from actual hidden keys
    c = [0] * len(atoms)
    def walk(s, depth=0):
        if s[0] == 'leaf':
            return
        _, k, l, r = s
        if depth > CUT and k not in Sset:
            for n, a in enumerate(atoms):
                lo, hi = a['lo'], a['hi']
                if (lo is None or k > lo) and (hi is None or k < hi):
                    c[n] += 1
                    break
        walk(l, depth + 1)
        walk(r, depth + 1)
    walk(t)
    # exposed fringe per gap
    p_exp = [0] * 10
    def walk2(s, depth=0):
        if s[0] == 'leaf':
            return
        _, k, l, r = s
        if depth <= CUT and k not in Sset:
            p_exp[gap_of(Ss, k)] += 1
        walk2(l, depth + 1)
        walk2(r, depth + 1)
    walk2(t)
    # sigma_hat from full gap counts
    sigma_hat = [p_exp[i] for i in range(10)]
    for n, a in enumerate(atoms):
        sigma_hat[a['gap']] += c[n]
    nonempty = set(pid for pid, pr in ports.items()
                   if pr['hidden_S'] or any(c[n] for n, a in enumerate(atoms) if a['port'] == pid))
    return skel, ports, atoms, Vs, hidden, c, sigma_hat, p_exp, nonempty


def reconstruct_completion(skel, ports, atoms, Vs, hidden, c, Sset):
    """Soundness: build a completion BST per port over (hidden S ints + ordered anonymous markers).
    Total order via V-positions: int k -> Vs.index(k); marker of atom n -> (atom V-index)+0.5."""
    F = {}
    atompos = {}
    for n, a in enumerate(atoms):
        lo = a['lo']
        m = -1 if lo is None else Vs.index(lo)
        atompos[n] = m + 0.5
    byport = {}
    for n, a in enumerate(atoms):
        if a['port'] is not None:
            byport.setdefault(a['port'], []).append(n)
    for pid, pr in ports.items():
        items = []  # (pos, seq, key)
        for k in hidden.get(pid, []):
            items.append((Vs.index(k), 0, k))
        for n in byport.get(pid, []):
            for s in range(c[n]):
                items.append((atompos[n], 1, ('F', n, s)))
        items.sort(key=lambda z: (z[0], z[1]))
        mkeys = [z[2] for z in items]
        def build(ks):
            if not ks:
                return S.LEAF
            m = len(ks) // 2
            return S.node(ks[m], build(ks[:m]), build(ks[m + 1:]))
        F[pid] = build(mkeys)
    return F, atompos


def check_bst_pos(T2, Vs, atoms, atompos, Sset):
    """Verify inorder strictly increasing under true order (ints via Vs.index, markers via atompos)."""
    seq = S.inorder(T2)
    pos = []
    for k in seq:
        if isinstance(k, tuple):
            pos.append((atompos[k[1]], k[2]))
        else:
            pos.append((Vs.index(k), -1))
    return all(a < b for a, b in zip(pos, pos[1:]))


if __name__ == '__main__':
    rng = random.Random(11)
    N = 600
    nok_val = nflow = 0
    for trial in range(N):
        n = rng.randint(10, 18)
        keys = list(range(1, n + 1))
        Sset = set(rng.sample(keys, 9))
        Ss = sorted(Sset)
        rk = {k: i + 1 for i, k in enumerate(Ss)}
        t = S.LEAF
        ks = sorted(keys)
        rng.shuffle(ks)
        def ins(t, k):
            if t[0] == 'leaf':
                return S.node(k, S.LEAF, S.LEAF)
            _, kk, l, r = t
            return S.node(kk, ins(l, k), r) if k < kk else S.node(kk, l, ins(r, k))
        for k in ks:
            t = ins(t, k)
        # completeness: real tree induces satisfying assignment
        skel, ports, atoms, Vs, hidden, c, sigma_hat, p_exp, nonempty = read_witness(t, Sset)
        ok, why = joint_valid(skel, ports, atoms, hidden, c, sigma_hat, p_exp, Sset, nonempty)
        assert ok, ('completeness', trial, why)
        # flow: same instance through AFSP solver at (gap x port) granularity
        plist = sorted(ports)
        R = len(plist)
        pidx = {p: r for r, p in enumerate(plist)}
        S_holes = []
        for pid in plist:
            S_holes.append(sorted(rk[k] for k in hidden[pid]))
        # exact compat: port range (lo,hi) in true keys vs gap-i S-interval
        compat = []
        for i in range(10):
            glo = Ss[i - 1] if i > 0 else None
            ghi = Ss[i] if i < 9 else None
            row = []
            for pid in plist:
                if pid not in nonempty:
                    row.append(False)
                    continue
                pr = ports[pid]
                plo, phi = pr['lo'], pr['hi']
                # intervals (plo,phi) and (glo,ghi) overlap?
                a = plo if plo is not None else -10**9
                b = phi if phi is not None else 10**9
                ga = glo if glo is not None else -10**9
                gb = ghi if ghi is not None else 10**9
                row.append(a < gb and ga < b)
            compat.append(row)
        non = set(pidx[pid] for pid in plist if pid in nonempty and not hidden[pid])
        z = solve_allocation(p_exp, S_holes, compat, sigma_hat, non)
        assert z is not None, ('flow-feasible', trial)
        nflow += 1
        # soundness: alternative distribution from flow -> reconstruct -> verify BST + gaps + S
        # distribute z[(i,r)] across port r's atoms in gap i (first-atom packing)
        c2 = [0] * len(atoms)
        for (i, r), v in z.items():
            pid = plist[r]
            tgt = [m for m, a in enumerate(atoms) if a['port'] == pid and a['gap'] == i]
            assert tgt, ('atom-target', trial, i, pid)
            c2[tgt[0]] += v
        ok2, why2 = joint_valid(skel, ports, atoms, hidden, c2, sigma_hat, p_exp, Sset, nonempty)
        assert ok2, ('soundness-pred', trial, why2)
        F2, atompos = reconstruct_completion(skel, ports, atoms, Vs, hidden, c2, Sset)
        T2 = fill(skel, F2)
        assert check_bst_pos(T2, Vs, atoms, atompos, Sset), ('soundness-bst', trial)
        # gap counts + S positions in reconstruction
        cnt = [0] * 10
        for k in S.inorder(T2):
            if isinstance(k, tuple):
                # anonymous: determine gap from atom n
                cnt[atoms[k[1]]['gap']] += 1
            elif k not in Sset:
                cnt[gap_of(Ss, k)] += 1
        assert cnt == sigma_hat, ('soundness-gaps', trial, cnt, sigma_hat)
        nok_val += 1
    print('trials=%d complete+sound=%d flow=%d' % (N, nok_val, nflow), flush=True)
    json.dump({'trials': N, 'ok': nok_val, 'flow': nflow}, open(PDIR + 'PP_INVENTORY_TEST.json', 'w'), indent=1)
