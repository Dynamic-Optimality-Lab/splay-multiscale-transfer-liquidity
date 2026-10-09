"""Test R_B(y) <= absorbed(y) + (1-b_y) exhaustively n=5,6,7 + random BSTs."""
import sys, copy, random
sys.path.insert(0, "scripts")
sys.path.insert(0, "python")
import wp6_cycle_ratio as O
from wp6_staticR import R_static, depths_list


def subkeys(T, x):
    nd = T
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    out = []

    def go(m):
        if m is None:
            return
        out.append(m[0])
        go(m[1])
        go(m[2])
    go(nd)
    return set(out)


def rand_bst(keys, rng):
    ks = list(keys)
    rng.shuffle(ks)
    t = None
    for k in ks:
        # BST insert into list-shape
        if t is None:
            t = [k, None, None]
            continue
        nd = t
        while True:
            if k < nd[0]:
                if nd[1] is None:
                    nd[1] = [k, None, None]
                    break
                nd = nd[1]
            else:
                if nd[2] is None:
                    nd[2] = [k, None, None]
                    break
                nd = nd[2]
    return t


def main():
    bad = 0
    tot = 0
    worst = None
    for n in (5, 6, 7):
        print(f"[ABS] n={n} exhaustive...", flush=True)
        Sh = O.shapes_of(list(range(1, n + 1)))
        for T in Sh:
            for y in range(1, n + 1):
                R = R_static(T, y)
                b = 1 if T[0] == y else 0
                absorbed = n - len(subkeys(T, y))
                if R > absorbed + (1 - b):
                    bad += 1
                    if worst is None:
                        worst = (n, y, R, absorbed, b)
                tot += 1
        print(f"[ABS] n={n} done: bad={bad}/{tot}", flush=True)
    rng = random.Random(0)
    print("[ABS] random large...", flush=True)
    for t in range(400):
        n = rng.choice([10, 12, 16, 20])
        T = rand_bst(range(1, n + 1), rng)
        y = rng.randint(1, n)
        R = R_static(T, y)
        b = 1 if T[0] == y else 0
        absorbed = n - len(subkeys(T, y))
        if R > absorbed + (1 - b):
            bad += 1
            if worst is None:
                worst = (n, y, R, absorbed, b)
        tot += 1
    print(f"[ABS] FINAL violations: {bad}/{tot} worst={worst}", flush=True)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
