# PP_DESTINATION_SHARED.py — one inventory across source AND destination of an H<=2 macro.
# View (a): destination = carried skeleton (RotatePorts, same pids/F/xi) — validity with same xi.
# View (b): fresh depth-7 cut of destination — valid by completeness; S-union + sigma conserved.
import sys, json, random
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S
from PP_PORT_ROTATION_TRANSDUCER import cut, fill, splay_skel, CUT
from PP_JOINT_INVENTORY import atoms_of, read_witness, joint_valid, gap_of

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'

if __name__ == '__main__':
    rng = random.Random(23)
    N = 800
    na = nb = 0
    for trial in range(N):
        n = rng.randint(10, 30)
        keys = list(range(1, n + 1))
        Sset = set(rng.sample(keys, 9))
        Ss = sorted(Sset)
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
        skel, ports, atoms, Vs, hidden, c, sigma_hat, p_exp, nonempty = read_witness(t, Sset)
        H, word, tg = 0, [], t
        cand = list(keys)
        rng.shuffle(cand)
        for x in cand:
            a = (S.lookup(tg, x)[1] + 1) // 2
            if H + a <= 2 and (a > 0 or len(word) < 3):
                word.append(x)
                H += a
                tg = S.trace(tg, x)[0]
                if H == 2 and rng.random() < 0.7:
                    break
        F = {}
        for pid in ports:
            sub = t
            for step in pid:
                _, _, l, r = sub
                sub = l if step == 'L' else r
            F[pid] = sub
        sk = skel
        for x in word:
            sk, _ = splay_skel(sk, x)
        tc = t
        for x in word:
            tc = S.trace(tc, x)[0]
        assert fill(sk, F) == tc, ('dst-fill', trial)
        # (a) carried view: same hidden/c/nonempty/sigma; atoms recomputed on carried skeleton
        atoms_d, Vs_d = atoms_of(sk, ports, Sset)
        assert Vs_d == Vs, ('V-stable', trial)
        ok, why = joint_valid(sk, ports, atoms_d, hidden, c, sigma_hat, p_exp, Sset, nonempty)
        assert ok, ('carried-valid', trial, why)
        na += 1
        # (b) fresh-cut view
        sk2, ports2, atoms2, Vs2, hidden2, c2, sh2, p2, non2 = read_witness(tc, Sset)
        ok2, why2 = joint_valid(sk2, ports2, atoms2, hidden2, c2, sh2, p2, Sset, non2)
        assert ok2, ('fresh-valid', trial, why2)
        union_src = sorted(k for hs in hidden.values() for k in hs)
        union_dst = sorted(k for hs in hidden2.values() for k in hs)
        expS = set()
        expS_src = set()
        def col(s, acc):
            if s[0] == 'K':
                if s[1] in Sset:
                    acc.add(s[1])
                col(s[2], acc)
                col(s[3], acc)
        col(sk2, expS)
        col(skel, expS_src)
        assert set(union_dst) | expS == set(Sset), ('S-cons', trial)
        assert set(union_src) | expS_src == set(Sset), ('S-cons-src', trial)
        assert sh2 == sigma_hat, ('sigma-cons', trial)
        nb += 1
    print('dst-shared: carried=%d fresh=%d / %d' % (na, nb, N), flush=True)
    json.dump({'trials': N, 'carried': na, 'fresh': nb}, open(PDIR + 'PP_DST_SHARED_TEST.json', 'w'), indent=1)
