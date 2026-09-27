from pathlib import Path
lines = Path("python/independent/ledger.py").read_text(encoding="utf-8").splitlines(keepends=True)
# 0-based idx: 0 doc,1 future,2 blank,3-6 imports/consts(C,K,LAT,LEAF)... verify anchors below
src = "".join(lines)
assert "def serial(t):" in src and "def fires(mode, ev):" in src
i_serial_end = next(i for i, l in enumerate(lines) if l.startswith("def fires(mode, ev):"))
tree_part = "".join(lines[7:i_serial_end])
Path("python/independent/splay.py").write_text(
    '"""WP-1 STEP 16a: independent splay core (tuple trees, recursive frames)."""\n'
    "from __future__ import annotations\n\n" + tree_part, encoding="utf-8")
pair_src = ('"""WP-1 STEP 16b: independent pair dynamics (KEEP/DELETE, regret)."""\n'
            "from __future__ import annotations\n\nfrom .splay import cost\n\nC_PAIR = 2\n\n\n"
            "def keep_costs(A, B, x):\n    return cost(A, x), cost(B, x)\n\n\n"
            "def delete_cost(A, x):\n    return cost(A, x), 0\n\n\n"
            "def regret(y, a):\n    return y - C_PAIR * a\n\n\n"
            "def required(y, a):\n    return max(regret(y, a), 0)\n")
Path("python/independent/pair.py").write_text(pair_src, encoding="utf-8")
ledger_rest = "".join(lines[i_serial_end:])
ledger_rest = ledger_rest.replace("def need_of(y, a):\n    return max(y - C * a, 0)\n\n\n", "")
ledger_rest = ledger_rest.replace("need = need_of(y, a)", "need = required(y, a)")
header = ('"""WP-1 STEP 16c: independent ledger + replay (imports .splay/.pair only)."""\n'
          "from __future__ import annotations\n\nfrom .pair import required\n"
          "from .splay import cost, trace\n\nK = 6\nLAT, ACT, SP = \"LATENT\", \"ACTIVE\", \"SPENT\"\n\n\n")
Path("python/independent/ledger.py").write_text(header + ledger_rest, encoding="utf-8")
print("split ok")
