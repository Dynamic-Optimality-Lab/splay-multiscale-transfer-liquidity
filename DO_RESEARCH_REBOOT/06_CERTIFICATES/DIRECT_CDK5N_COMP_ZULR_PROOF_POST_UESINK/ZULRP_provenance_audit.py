# Read-only OUT-provenance audit: regenerates the L1 grammar with EXACT
# canonical-string dedup, compares against committed parents_L1.txt, verifies
# rm7 reconstruction + SHA. No screening, no discovery, no writes to history.
import sys, json, hashlib
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_PROOF_POST_UESINK/'
GDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COMP_ZULR_G0_POST_UESINK/'
def parse(c):
    return [(t[0], int(t[1:])) for t in c.split(",")]
def canon(w):
    return ",".join(m + str(k) for m, k in w)
IN_CANON = ("D5,D4,D3,K3,K7,D5,K1,D8,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,"
            "K5,K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_CANON = ("D5,D4,D3,K3,K7,D5,K1,K9,K5,K7,K1,K9,D5,D4,K3,K7,D5,K1,D8,K9,K5,"
             "K7,K1,K9,D8,D4,D2,D5,D6,D1,D9")
OUT_SHA = "8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd"

def mutants(word):
    n = len(word)
    dpos = [i for i, (m, _) in enumerate(word) if m == 'D']
    for i in dpos:
        yield ("rm%d" % i, word[:i] + word[i + 1:])
    for i in dpos:
        for k in range(1, 10):
            if k == word[i][1]:
                continue
            w = list(word); w[i] = ('D', k)
            yield ("rep%dk%d" % (i, k), w)
    for g in range(n + 1):
        for k in range(1, 10):
            w = list(word); w.insert(g, ('D', k))
            yield ("ins%dk%d" % (g, k), w)

if __name__ == "__main__":
    out = {}
    IN_W = parse(IN_CANON)
    assert hashlib.sha256(IN_CANON.encode("ascii")).hexdigest() == \
        "593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9"
    out["IN_SHA_ok"] = True
    seen = set()
    order = []
    raw = 0
    collisions = []
    for op, w2 in mutants(IN_W):
        raw += 1
        c = canon(w2)
        if c in seen:
            collisions.append((op, c))
            continue
        seen.add(c)
        order.append((op, c))
    out["raw_count"] = raw
    out["distinct_count"] = len(order)
    out["collisions"] = len(collisions)
    committed = [l.rstrip("\n") for l in open(GDIR + "zsearch_in/parents_L1.txt") if l.strip()]
    out["committed_lines"] = len(committed)
    out["order_identical"] = ([op + " " + c for op, c in order] == committed)
    out["first5"] = order[:5]
    out["first5_expected"] = [["rm0", None], ["rm1", None], ["rm2", None], ["rm5", None], ["rm7", None]]
    out["first5_ops"] = [op for op, _ in order[:5]]
    rec = list(IN_W)
    del rec[7]
    out["rm7_reconstructs_OUT"] = (canon(rec) == OUT_CANON)
    out["OUT_SHA_ok"] = (hashlib.sha256(OUT_CANON.encode("ascii")).hexdigest() == OUT_SHA)
    out["OUT_tokens"] = len(OUT_CANON.split(","))
    json.dump(out, open(PDIR + "ZULRP_provenance_audit.json", "w"), indent=1, default=str)
    for k, v in out.items():
        if k not in ("first5",):
            print("%s: %s" % (k, v), flush=True)
    print("first5:", out["first5"], flush=True)
    ok = (out["order_identical"] and out["rm7_reconstructs_OUT"] and out["OUT_SHA_ok"]
          and out["OUT_tokens"] == 31 and [op for op, _ in order[:5]] == ["rm0", "rm1", "rm2", "rm5", "rm7"])
    print("PROVENANCE: %s" % ("PASS" if ok else "FAIL"), flush=True)
    sys.exit(0 if ok else 1)
