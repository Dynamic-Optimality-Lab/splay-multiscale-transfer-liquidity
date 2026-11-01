# Gate for one shared shallow payer per positive run

2026-10-31, Asia/Karachi. The user requests a shared-payer extension of delayed shallow charging, with no credit reuse. The matching-terminal line remains frozen. Sources, old artifacts/statuses, Git and Stage 11G are read-only. All new writes are exclusive to this append-only run.

## One concrete restricted mechanism

Use cyclic A-root blocks and delta_i=q_i-2a_i. Group maximal consecutive POSITIVE blocks into runs R. For a run, define its source-known excess E_R=sum_(i in R) delta_i. Allow only one private payer for the entire run; different runs never share a payer.

The payer key y must belong to the intersection of all run anchors' pre-B-splay root/child sets. For each anchor i, let h_i(y)<=3 be its actual post-splay depth and k_i(j) count genuine B-changing KEEPs strictly between i and proposed payer j, including later positive anchors and zero-double zigs. The established source bound gives q_j<=floor(h_i/2)+k_i(j). These are bounds on the SAME q_j, so use their MINIMUM, never their sum:

    c_R(j)=min_(i in R)(floor(h_i(y)/2)+k_i(j)).

Set c_R(j)=0 for a KEEP-less payer. Require the explicit source A threshold E_R+c_R(j)<=2a_j. Scan after the run, stopping before the next positive run, and choose the FIRST qualifying common-key payer. Intervening nonpositive blocks pay only their own demands. Concatenate the anchors' excess demands in run order into separate contiguous slices of the payer pool, then pay the payer's own B demands from the remaining units.

This is a restricted one-pool construction with a prescribed allocation. It is not a general capacity theorem or an unknown matching witness. The threshold is a restriction on actual A leader cost, equivalently an explicit A-depth bound; it is not claimed mandatory for every source walk.

## Four rules

1. **Strictly smaller — PASS.** One maximal positive run, one common tracked shallow key and one payer in its following nonpositive gap. No cross-run sharing, unknown allocation, inter-packet transfer, potential, Hall system or global CD restatement. Runs may have arbitrary length and non-unit deficits.
2. **Concrete reason — PASS.** Each anchor supplies an established source-exact delayed bound on one physical B access. Taking the minimum bounds that access once. The explicit A threshold bounds the concatenated excess list plus the payer's own demand count. Positive-run gaps force disjoint packet ownership. No independent open geometry or availability theorem is used.
3. **One bounded audit — PASS.** Prove this one construction, its first-payer scan, containment of DS when runs are singletons and no-reuse assignment. Check the fixed analytic thirteen-key witness below and reflection, preserve acceptance and exact rows of the four DS/SC witness controls already certified, and check cuts. No word search, size sweep, finite potential fit, graph or optimizer. Stop if the fixed witness or strict-coverage check fails; do not search for an automatic replacement.
4. **Original connection — PASS subject to the fixed source check.** Success settles CD on this shared-run class and strictly extends DS, which rejects consecutive positives. Non-unit consecutive positives also distinguish the proposed witness from the named banked unit-run packet classes. This closes one further restricted original CD case, not universal CD, Stage 11G, or general shared-payer admissibility.

## Analytically specified strict witness

Start diagonally at R13 and use prefix D9. Freeze the cycle

    K13 K12 K11 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D9.

The construction is derived from the source RR recurrence before evaluation:

- D9 leaves A rooted at 9 with right path 10,11,12,13. KEEP13 therefore has a=2 while B has q=6, giving deficit 2.
- After that splay, KEEP12 is at A depth 2 and B depth 6, giving a=1,q=3,deficit 1.
- The intervening KEEP11 has a=1,q=2,deficit 0: its own pool is fully spent and must not lend.
- Common payer KEEP2 should have a=2,q=0. Key 2 is a pre-positive root child at both anchors. Both post-anchor heights are 1, with intervention counts 2 and 1; the shared ceiling is min(2,1)=1. Total run excess is 3, so 3+1=4=2a_payer.

Check all these claims, no extra positives, exact reachability and closure, and synchronization by KEEP10. This is ONE source construction at thirteen keys, not a larger finite fit or an enlarged state graph. Every number is predetermined by the displayed source shapes; no parameter or word is selected from a finite sweep.

For every n>=13, keep prefix D9 and replace the common ascending/descending scan ranges by 1,...,n: first segment K13 K12 K11 K2 K3 ... Kn, then K1 ... Kn, K(n-1) ... K1, D9. The untouched right fringe at 13 preserves the local computation until synchronization. Common full scans restore R_n; final D9 restores the initial A. Prove this unbounded-support extension analytically without evaluating another finite n. The fixed <=13 word likewise commutes with grafting an arbitrary unrequested BST of keys >13 at key 13's right child.

## No-reuse, novelty and verification requirements

Prove maximal positive runs and their following gaps give disjoint packet cells on the circle, including wraparound. All positive blocks must be covered exactly once. The one payer pool is reserved once for E_R excess demands; each run anchor receives a distinct slice. The payer's own q is counted once; intermediates use no borrowed credits. Handle empty/zero-A/no-positive/all-positive and short cycles explicitly.

Independently replay every new and preserved row using the pointer engine; verify the intersection, every h and intervention count, the minimum bound, first-payer choice, all cyclic cuts, physical pair closure and every actual source credit identity. No producer, matching evaluator, flow optimizer or old recognizer is imported by the verifier.

DS containment is exact for singleton runs. The strict witness should be rejected by DS because its first two blocks are positive. Check the older necessary source predicates directly; do not claim execution of old recognizers. Record restrictions, BEFORE/RESULT/AFTER, the restricted original case deleted and no universal promotion.

Preserve all inherited non-advancing counts, source and previous-run hashes, the matching-terminal freeze, and every one of the 125 Stage 11G files and their complete inventory. No Stage 11G code or old status writer is called. No shared payer across distinct runs or unrestricted allocation successor is launched automatically.
