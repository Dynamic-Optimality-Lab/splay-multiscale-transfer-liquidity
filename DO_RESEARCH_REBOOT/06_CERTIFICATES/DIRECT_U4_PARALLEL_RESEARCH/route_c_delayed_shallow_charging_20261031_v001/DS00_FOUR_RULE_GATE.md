# Gate for delayed shallow successor charging

2026-10-31, Asia/Karachi. Extend the restricted shallow-successor source charging theorem to delayed payers without credit reuse. The matching-terminal line remains frozen. No potential, terminal matching, allocation optimizer or source-state graph is proposed. All old sources, reports, statuses, Git and Stage 11G remain read-only. New outputs are exclusive to this versioned run.

## One exact restricted target

Use the existing cyclic A-root blocks, a_i>=1, q_i, delta_i=q_i-2a_i. For a positive block i, take its pre-B-splay root and nonempty original children as candidate payer keys y. Let h_i(y) be y's actual depth immediately after that splay; SC gives h<=3. Between i and a later payer block j count k genuine B-changing KEEPs, one at most per intermediate block. Count zero-double zigs; do not count DELETEs or B-root no-ops.

The source one-splay displacement bound gives

    q_j <= c_i(j)=floor(h_i(y)/2)+k,

when j has a KEEP of y. Set c_i(j)=0 if j has no KEEP. Require the concrete leader-depth threshold

    delta_i+c_i(j)<=2a_j.

For each positive i, scan forward only until the next positive block and choose the FIRST candidate satisfying this condition. No qualifying payer means rejection of this restricted class. Intervening nonpositive blocks pay themselves locally; they do not lend any credits. The endpoint alone pays the anchor's excess and its own B work. The directed intervals lie inside disjoint gaps between positive anchors; derive disjointness rather than assume an unknown allocation.

## Four rules

1. **Strictly smaller — PASS.** One positive anchor, one delayed private payer from its pre-splay root neighborhood, explicit A-cost threshold, and no intervening positive. Arbitrary size/support/delay/fringes are allowed, but this is a visibly restricted source class. It neither restates global CD nor assumes a general capacity witness.
2. **Concrete reason — PASS.** Source frame tables show a single splay raises any tracked depth by at most 2, and the old-root neighborhood starts at h<=3. Induction over actual intervening B changes gives the displayed integer bound. The endpoint's source A threshold then pays all remaining anchor demands. Cyclic gaps force disjoint ownership; no second open theorem is needed. The displacement component is already banked in 26AL and is not counted as new advancement.
3. **One bounded mechanism — PASS.** Prove this one parameterized delayed theorem, its canonical scan and exact unit assignment. Audit the new fixed seven-key word below and reflection, preserve acceptance of the old SC word and reflection, and check three literal three-key depth-tax controls plus reflection. No word search, alternative packet, larger finite size, fit, or graph. Stop if the fixed strict-coverage witness fails; do not hunt for a replacement automatically.
4. **Original connection — PASS subject to the fixed strict-coverage check.** The theorem settles CD on this delayed private-payer class and contains SC: an immediate SC payer has k=0,c<=1 and meets the new threshold. New coverage requires a reachable witness that fails SC and the named older former-root/packet predicates. Universal CD, all walk-admissibility, shared payers and intervening positives remain open. This is a restricted case removed, not completion of the original universal obligation.

## Fixed nontrivial-delay witness

Start at the diagonal R7 and retain prefix D7,D6. Freeze

    K7 K3 K2 K3 K4 K5 K6 K7
    K1 K2 K3 K4 K5 K6 K7
    K6 K5 K4 K3 K2 K1 D7 D6.

The first KEEP7 should remain the sole positive, (a,q,delta)=(1,3,1). Its immediate successor key 3 is at pre-positive B depth 2, so the old SC condition fails. KEEP3 is a genuine B-changing intervention, not a DELETE detour. The delayed KEEP2 should have a=1,q=0. Its pre-positive depth is 1 and post-positive depth h=1, giving k=1,c=1 and exact threshold delta+c=2=2a_payer. Check the first qualifying payer is this block and all credit identities are genuine.

The following ascending accesses should synchronize both trees by KEEP6, after which common scans and final D7,D6 restore the initial pair. The first former-root return 1 is delayed beyond three successors; the single positive excludes the multi-positive packet patterns. The seven genuine KEEP keys exclude <=5-support classes. Old recognizers are not run: test their necessary source predicates from pinned definitions.

For every n>=7, the analytic extension uses diagonal R_n, the same prefix, first segment K7 K3 K2 K3 ... Kn, then K1 ... Kn, K(n-1) ... K1, D7,D6. The seven-key calculation is unchanged under the untouched right fringe at 7 until synchronization; subsequent common accesses and full scans close the trees. This unbounded-support family is proved analytically, without evaluating another size. The fixed <=7 word also commutes with grafting an arbitrary unrequested BST of keys >7 at key 7's right child.

## Source controls, verification and stop

The three-key controls are R3 with tracked key 1 and targets 1,2,3: respectively a B-root no-op (tax 0), a zero-double genuine zig (tax 1, depth gain 1), and a double (tax 1, depth gain 2). Reflect all three. These guard the difference between B activity and positive q.

Verify the one-splay region table, actual versus potential/synthetic counts (there is no potential here), zero-A and empty cases, cyclic seams, distinct block intervals, every demand/credit identity and no unit reuse. Check every cyclic cut for new and inherited witnesses; independently replay with the pointer engine and import no producer or optimizer.

Record BEFORE/RESULT/AFTER, the precise restricted original case discharged, restrictions and remaining complement. Preserve previous counts and statuses. No Stage 11G code, graph, solver or predicate is changed or run. Pin all inherited/previous-run files and all 125 Stage 11G files and compare final inventory/bytes. No automatic delayed-sharing, larger-radius, matching-terminal or global-capacity successor is launched.
