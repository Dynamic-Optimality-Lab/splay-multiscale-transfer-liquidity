# Bank-cap regeneration review

The capped potential and packet entrance budgets are valid on the original source model. The repo's aligned cold-spine family refutes BC5, any fixed bound on the length of a cap-five-invisible packet, and the proposed same-lifetime paid offset HI-PAID-01. The aggregate obligation stays $\Omega_5(W)\le K A(W)$ for one absolute finite $K$.

## What the imported attempts establish

For a real B rotation after A has rooted the same target, the old rotated subtree contains that target and the new subtree of the demoted pivot excludes it. Comparing the two pairs of subtree intervals before and after the rotation gives the exact capped decrease in the [bank-cap report](BANK_CAP_REGENERATION_GATE_20261123.md). A real A rotation replaces one proper interval, so the complete-period bound $V_5\le D_5\le 10A$ holds. Here $V_5$ counts the unpaid doubles visible at cap five.

The target's block has five units at the start of a genuine B KEEP, and target-first pooling reduces its stock by at most one per B double. The first five doubles are therefore paid if present. Each maximal packet of cap-five-invisible unpaid doubles has a distinct immediately preceding paid or visible double in the same KEEP. With $M_5$ packet entrances and $C_5$ later packet events, this gives $M_5\le P_5+V_5\le55A$ and

$$
\Omega_5=V_5+M_5+C_5\le65A+C_5,\qquad Q_B\le110A+C_5.
$$

The [historical attempt](HISTORICAL_INVARIANT_ATTEMPT_20261123.md) also correctly counts the two primitive decreases of each bad double against the stock of excess straddlers at the actual A interval births. The obstruction is the size and reuse of that stock. Raw excess at an interval birth has no absolute bound.

## Original-source counterexample to BC5 and bounded packet lengths

The archived [290-key shared-donor control](../GSO_OMEGA5_SHARED_DONOR_CONTROL_20261123.json.gz) has 5,073 operations, $A=6211$, $Q_B=976$ and $\Omega_5=16$. The existing independent checker verified the physical events, both labeled restorations and the greatest cyclic bank. A separate read-only calculation of both primitive thresholds gives the following results.

| Original occurrence | Frozen bank | Primitive caps |
| --- | --- | --- |
| B(1777,6) | Unpaid, with zero on every footprint block | $(36,36)$ |
| B(1777,6) through B(1777,20) | Fifteen consecutive unpaid LL doubles | $36,34,\ldots,8$ on each half |
| B(1777,23) | Unpaid | $h(e)=2$ |

Thus $V_5=1$, $H_5=15$, $M_5=1$, and $C_5=14$. The 257-key results from the imported report are exactly reproduced, including caps $(2,3)$ and $(2,1)$. The 290-key result concerns the same original bank and a different complete source.

The calculation extends to the [aligned complete family](../GSO_OMEGA5_EARLY_PAIRING_CONSERVATION_20261123.md#step-2-exact-shared-donor-obstructions). Write $h=5m$, $q=h-2$, $n=h+5q$, with $m\ge5$. The high producer word ends with B rooted at $h+1$ and its full left vine $h,h-1,\ldots,1$. A splays the focus KEEP 3 by a zig. At its B phase A is rooted at 3, and the A subtree at 4 is the right vine on $[4,h]$ under $h+1$. The high producers emptied all middle low blocks. After the A zig only the target's low block $[1,5]$, the last low block $[h-4,h]$, and the exterior block of $h+1$ can have credit in a focus footprint. The first has five, and the last low block has at most two. The depletion argument in the original aligned family holds from any admissible seam stock.

For each $1\le j\le\lfloor(h-9)/2\rfloor$, the $j$th focus double is LL with $g=2j+3$, $p=g-1$ and $x=3$. Its footprint uses no key above $g+1\le h-5$. The first five such doubles drain the target block. Every later double in this range is unpaid. The two new demoted subtrees, in physical rotation order, are $\{g\}$ and $[4,g]$. Before the first rotation every key $g,\ldots,h$ still has 3 in its B subtree. Every proper A holder containing $g$ contains $[g,h]$, and the holder at $g$ contains exactly those keys. This gives $h(R_1)=h-g+1$. Before the second rotation the straddlers of $[4,h]$ are $p$ and the untouched keys $g+1,\ldots,h$. Larger eligible A holders still count these same keys. Hence $h(R_2)=h-g+1$ as well.

In particular the sixth double is unpaid and has $h(e)=h-14$, which is unbounded. The consecutive cap-five-invisible packet begins at double six and has length at least $\lfloor(h-9)/2\rfloor-5$. This is a complete-source obstruction to every fixed cap and every fixed cap-five packet length. Its preparation and closure still have linear A work, so the packet lower bound does not contradict $C_5=O(A)$.

## Same-lifetime paid offsets also fail with every fixed constant

Use the same family and insert a counted A-only DELETE 4 immediately after the focus KEEP. Real A-only splay coercion then aligns A with B, followed by common KEEP coercion back to the original diagonal. In the added [290-key lifetime-death control](CAP_FIVE_290_DELETE_4_CONTROL.json.gz), operation 1778 is this DELETE. Both full trees close, the canonical bank is recomputed, and all 15 bad events above persist.

Let $L$ be the actual lifetime of the proper A interval $[4,h]$ through the focus. In the original diagonal the key 4 has an exterior descendant, so $[4,h]$ is absent there. It is established by the A-only preparation and stays present through the high producers and the A zig at the focus. The inserted DELETE 4 kills $L$, since a proper A interval cannot contain the root.

The second primitive of each bad double in the displayed packet has $[4,h]$ as its unique smallest proper A holder. Even the least straddler count is above five there. Consequently,

$$
u_L\ge\lfloor(h-9)/2\rfloor-5.
$$

During the earlier paid high producers, the two preliminary LLs demote exterior keys. The main RR's two demoted subtrees both contain key 1. None is contained in $[4,h]$. After the focus there are no B rotations before $L$ ends. The focus has at most eight paid doubles, so $p_L\le16$ for the whole lifetime. In the saved $h=50$ replay the exact owner is the lifetime born at A(1290,1), rotation 1, with $(u_L,p_L)=(15,6)$. As $h$ grows, $u_L$ grows and $p_L$ stays bounded. This disproves $u_L\le C+\lambda p_L$ for all choices of finite absolute $C$ and $\lambda$.

## What this changes in the global proof attempt

The actual paid funding for this packet predates the consuming lifetime's own paid debits. The distinct retired grandparents acquired their left reach as lower pivots of distinct earlier paid RR doubles. Each remains on its original left-gain record until its bad LL, so those older receipts pay the selected run at load one on original B receipts. In the lifetime-death control the fifteen gains are distinct. The first and last are B(1601,3) for B(1777,6) and B(1741,3) for B(1777,20). Some originating A slots are in the previous lap of the complete period, with the original seam offsets preserved. The independent checker includes those slots and all restoring A work.

The imported budgets can be combined with the existing directional-gain account. Deduct visible unpaid events and bad-packet entrances at their proved total budget $V_5+M_5\le65A$. Retain their original IDs as possible producers of a non-target gain. Follow both endpoint losses of each remaining continuation to the latest real gains of their own keys and directions. Paid gains, last target gains and non-target gains from the deducted classes have at most

$$
P_5+2K_B+V_5+M_5\le112A
$$

distinct physical gain coordinates. Give those coordinates capacity $b$ and give a non-target gain from a continuation one provisional use. If $R_b^{\rm cont}$ counts excess endpoint losses, the same two-loss and one-gain balance gives

$$
2C_5\le112bA+C_5+R_b^{\rm cont}.
$$

This is a proved accounting identity and upper bound. An estimate $R_b^{\rm cont}\le\eta C_5+cA$ with $\eta<1$ would yield $\Omega_5\le(65+(112b+c)/(1-\eta))A$. That estimate remains open for arbitrary original sources. Every real old path key is demoted at most once per original KEEP, so the same directional gain cannot serve two loss occurrences within a single KEEP. The missing load bound is across different KEEPs and overlapping restorations, even if each local lifetime has a small paid count. Neither a cap threshold nor a packet-length threshold is used as an acceptance condition.

## Preservation and reproduction

The four supplied files are stored here byte-for-byte. Each zip's embedded Markdown matches the supplied loose Markdown. The three deterministic reproduction scripts for the 257-key source, the abstract opposite-vine test, and the historical packet table ran in a temporary directory and regenerated the packaged checks. The supplied probe starts from a right vine, which explains the scope of its standalone search. Its default unpaid-local-cap helper stops counting at six and can test whether cap five suffices. That helper does not report larger exact thresholds.

Run the read-only audit from this folder to replay the original 290-key control and the counted DELETE-4 variant through the frozen independent checker and recompute both per-rotation thresholds and the exact lifetime ownership.

~~~powershell
python -B audit_visibility.py
~~~

| Preserved file | SHA-256 |
| --- | --- |
| [Bank-cap report](BANK_CAP_REGENERATION_GATE_20261123.md) | 2bb5a0b6f92e6d81d66bb55859fa0488758f2214c89b4e4c97ff98e39a3ebdc5 |
| [Bank-cap repro](BANK_CAP_REGENERATION_REPRO.zip) | 727fe53c69603277df904ec81ee610af218fa3d1f162b73f36917b0898c81e11 |
| [Historical report](HISTORICAL_INVARIANT_ATTEMPT_20261123.md) | a756a9c2a00d108d0ca8a462fdeba2bc29b70e886d8e2a3fb2080d571bfba11b |
| [Historical repro](HISTORICAL_INVARIANT_ATTEMPT_20261123.zip) | c3ee937f922a07d2c01c0fc6394d83a7415c546756b80e8364083eb7f24f14a2 |
| [Counted DELETE-4 control](CAP_FIVE_290_DELETE_4_CONTROL.json.gz) | e5b7c0ab5fadf242198ed8deca0f51700511f1ea74b7b12e2c99b67b971bb2dc |
