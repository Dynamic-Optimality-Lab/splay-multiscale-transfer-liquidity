"""Append-only delivery of the source audit, exact refutation and scoped proof ledger."""
from pathlib import Path
import json, textwrap, hashlib
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
REBOOT='DO_RESEARCH_REBOOT/'
F='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/'
G='DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/'
I=G+'STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/'

def link(path,label=None,line=None):
    p=(ROOT/path).as_posix()
    if line:p+=':'+str(line)
    return '['+(label or path)+'](<'+p+'>)'

def local(name,label=None):return link(str((OUT/name).relative_to(ROOT)).replace('\\','/'),label or name)
def save(name,text):
    with (OUT/name).open('x',encoding='utf-8') as f:f.write(textwrap.dedent(text).strip()+'\n')

def main():
    baseline=json.loads((OUT/'entry_baseline.json').read_text())
    seven=json.loads((OUT/'u4_counterexample_certificate.json').read_text())
    nine=json.loads((OUT/'five_keep_nine_core_counterexample.json').read_text())
    status=[s for s in baseline['status'].splitlines() if 'DIRECT_U4_PARALLEL_RESEARCH' not in s]
    save('U4_00_ENTRY_AND_SOURCE_MANIFEST.md',f"""
    # Entry and source manifest — 2026-10-30, Asia/Karachi

    Repository: Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity.
    Local root: `{ROOT}`. Branch: coarse-double-branch.
    HEAD and live remote refs/heads/coarse-double-branch: `fea2a25b05e97f726b6e1891cebb12c4cfca821a`.
    Tracked modifications/staged changes: none. Pre-existing nonignored untracked files: {len(status)}.
    Existing worktrees: one, this checkout. No origin/coarse-double-branch tracking ref exists locally;
    live comparison used read-only git ls-remote rather than fetch or a fabricated ahead/behind count.

    {local('entry_baseline.json')} pins all 11,415 tracked/nonignored pre-existing regular files,
    17,190,806,080 bytes, with SHA256. It contains the full untracked inventory, branch, remotes,
    worktree listing and actual remote tip. Ignored build/cache files are outside that digest coverage.
    The final integrity report separately compares those bytes and detects any external changes.

    CHR01, H2R01, FRC01, LDR01, M2-DSK01 and many later M3 campaigns ARE present locally.
    Their files are untracked and therefore absent from the matching pushed commit. START_HERE,
    CURRENT_STATE and NEXT_ACTION contain older session metadata; their historical branch/HEAD
    claims do not replace this inventory. Later local status is reconstructed in U4_07.

    Authorization: the human explicitly approved this fresh append-only directory in this chat.
    All new reports, scripts, JSON and replay logs are here. Python uses -B; no installs, commits,
    pushes, checkout/reset/stash/clean, worktree alterations or old research edits were performed.
    No subagents or messages to other chats were used. GitHub branch discovery and git ls-remote
    were read-only. All mathematical gates are saved as U4_GATE_01..03.
    """)
    save('U4_01_REPOSITORY_ARCHITECTURE.md',f"""
    # Dependency-driven architecture

    | Layer | Authority and role |
    |---|---|
    | Original target and cost model | {link(REBOOT+'ORIGINAL_PIPELINE.md')}; {link(REBOOT+'01_MAIN_PIPELINE/stage_04_coarse_double.md')} |
    | Physical Pair Access | {link('python/liquidity/legacy_embedding.py','pointer engine',107)}; {link('python/independent/splay.py','independent frame engine',92)} |
    | Historical event flow | {link('scripts/wp6_eventflow.py','build_flow',185)}: capacity THREE, all B StepEvs and pump ancestry; distinct from U4 |
    | Original U4 graph | {link('scripts/wp6_overflow.py','replay/origin/charge',152)}: capacity TWO, B DOUBLE units, local/creator/consumer-setup |
    | U1-U4 and Hall/E0 attempts | audits/PIVOT_OVERFLOW_GENEALOGY.md through PIVOT_18R_CLOSE.md; later correction supersedes earlier E0-necessity claims |
    | Restricted physical theorems | 02_PROVED/DIRECT_NFKS_RT2*, DIRECT_CD_K4*, DIRECT_CDK5_LOW* and corresponding certificate directories |
    | Stage 11F | {link(F+'S04_UNIVERSAL_FORWARD_SIMULATION.md')}: restricted physical W to symbolic closed P, weight <=2A-Q |
    | Stage 11G | {link(G+'11G_FOUR_RULE_FREEZE.md')}: frozen O/M product G_AF, low/high cycle sign, independent witness interfaces |
    | New local research | M2_DSK01; M3_CHR01/H2R01/FRC01; later M3_COMB_AUD01, UNITPAIR_FIN01, POP3/POP4 campaigns |
    | Downstream | C_ZIG_RECONSTRUCTED, PIVOT2_CONDITIONAL_REDUCTION, COST_TRANSLATION_CONDITIONAL, Levy-Tarjan v3 Theorem4.3 |

    Three meanings of source must be kept separate: actual BST transitions; the original frozen
    symbolic compiler relation; finite projected fragments. Acceptance by a symbolic original root
    does not itself provide a physical Pair Access lift. Our new witnesses use the physical engines.

    Reproducibility: historical programs frequently write old result paths on execution. They were
    inspected before use. replay_inherited.py runs the CHR nonwriting checker, redirects ONLY the
    FRC checker's OUT, and runs the nonwriting M2 provenance checker. Original constructors and
    historical nine_node_replay.py were not executed; its literal fixture was parsed with ast.
    """)
    save('U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md',f"""
    # Exact original Pair Access specification

    K is any finite totally ordered set, T0 any BST on K. A and B start at the SAME T0.
    KEEP x splays both; DELETE x splays A and freezes B. All x are present. DELETE omits an
    occurrence from the retained history; it never physically removes a key. The theorem domain
    is every finite exactly closed pair walk reachable from some such diagonal, any length.

    Depth d counts EDGES, root depth0. For each access a=ceil(dA/2); on KEEP q=floor(dB/2),
    z=dB mod2, b=q+z=ceil(dB/2); on DELETE q=z=b=0. A=sum a, Q_B=sum q, Z_B=sum z,
    B=Q_B+Z_B. A DOUBLE is one StepEv for two rotations; the final single ZIG is one StepEv.
    LT cost is d+1, a different quantity. In legacy_embedding.replay_A/replay_B the variable a
    actually stores that LT cost; wp6_overflow.replay recomputes the StepEv a. Names are not interchangeable.

    Pointer source: {link('python/liquidity/legacy_embedding.py','_depth_to / primitive rotations / splay_trace',59)}.
    Both zig-zig cases rotate parent over grandparent first, then target over parent; zig-zag
    rotates target over parent then target over grandparent. Events execute deepest first,
    with a terminal zig if depth is odd. Independent source: {link('python/independent/splay.py','_rebuild',92)}.
    Pair graph source: {link('scripts/wp6_cycle_ratio.py','build',58)}. Event counts and full
    states were compared at every access of both new physical witnesses.

    Root repeats are no-ops with zero event cost (but LT cost1); nongenuine KEEP is B identity,
    possibly with positive A cost. If every KEEP is nongenuine, Q=0. Empty walks/key domains are
    trivial. If some KEEP is genuine, every retained key on a B-closed period belongs to genuine
    support: the cyclic B root is the latest genuine target. Both trees, not roots alone, must
    close. Repeated accesses, zero operations, primitive/nonprimitive words, both orientations,
    sparse order-preserving relabeling and a single copy of cyclic credits are included.

    CD-U: Q_B<=2A for ALL such walks. U4-M is a sufficient stronger graph-matching claim,
    now REFUTED. U4-S (R<=S) remains equivalent to CD-U by R-S=Q_B-2A.
    """)
    save('U4_03_U1_U3_RECONSTRUCTION.md',f"""
    # U1-U3 and their exact limits

    Authority: {link('audits/PIVOT_UNIVERSALIZE_U1U4.md')} sections A-H;
    {link('lean/WP6/GCStaticGenealogy.lean')} is explicitly an ABSTRACT descent kernel.

    U1: take consumed B edges (x,parent),(parent,grandparent) before a double. Follow latest
    establishing rotations backwards, recursively through earlier steps of the same splay.
    The previous KEEP x rooted x, so every queried x-parent edge was absent then. The x-line
    therefore reaches a strictly previous KEEP inside that key epoch. Max over strictly prior
    origin accesses remains in-epoch because that x-branch is inside it. Eternal/Genesis
    alternatives on the other branch do not remove the x-branch. Periodic indexing locates
    predecessors; it does not create more credits. Epochs may cross.

    U2: for a zero-A-cost B-active access t to z, the last positive-cost A arrival s at z exists.
    Otherwise a non-z access would dethrone z and force a later positive z arrival; an all-z
    closed word has no B-active z access. Between s and t there are only z accesses. Thus s
    has a>=1. This applies to starved B-double consumers and starved B-active creators, not
    arbitrary A no-ops without B activity. L1 strengthens it: s is DELETE, because a KEEP s
    would root B at z throughout the quiet block. L2: distinct starved B-active ACCESSES have
    distinct setups; the first KEEP in a quiet block roots B and prevents a second active KEEP.

    U3: D->creator(D), then if that creator is starved ->setup(creator). The latter has positive
    A credit, so at most two hops suffice. This proves reachability of positive credit, neither
    availability nor ELIGIBILITY: charge() does not add creator-setup edges.

    U1's paper mechanism and U2/U3/quiet/L1/L2 arguments are reconstructed here. The Lean kernel
    receives the real-splay latest-establishment/consumed-edge facts AS HYPOTHESES; it does not
    implement all BST mechanics, cyclic matching or U4. No new Lean build/kernel promotion is claimed.

    H1 epoch confinement and H2 quiet blocks are valid at access level. H3 gives one active
    starved ACCESS per block, not one B-double: one access may have many doubles. The historical
    sentence 'no two starved doubles share one setup' is false on our three-double K7.
    H4's O(dB) fan-in narrative does not prove a capacity bound or a unit-level injection through
    recursive origins; no such theorem is inherited in the counterexample proof.

    Implementation scope: build_origin indexes logged edges by (access,StepEv); make_origin_fn
    recurses over changed AND consumed edges and contains an origin-set >64 cutoff. It is not
    an independently proved all-size canonical ancestry implementation. The new finite cyclic
    checks stabilize at 2/3/4 laps. More importantly, the refutation is independent of exact
    creator identity: every possible B-mutation creator is a KEEP with ZERO A credits.
    """)
    save('U4_04_HALL_AND_CREDIT_MODEL.md',f"""
    # Credit model, correct Hall normal form and exact all-starved factorization

    {link('scripts/wp6_overflow.py','charge',329)} allocates credits C=(i,j,b),
    j an A StepEv at access i and b in{{0,1}}. There are exactly 2A distinguishable units.
    Demands D=(t,B-double sequence index), one per individual double, total Q_B.
    For each demand, Gamma(D)=C_t union C_creator(D) union C_setup(t), omitting absent pools.
    Every named pool is joined completely; duplicate pool IDs are counted once. Creator's setup
    is NOT present. setup(t) is read before access t updates the root-arrival map, including
    at nonstarved accesses. Adjacency order local-first changes a search order, not graph feasibility.

    Hall: for every demand subset X, |X|<=|Gamma(X)|. Because access pools are disjoint,
    |Gamma(X)|=2 sum_(i in N_access(X)) a_i. This exactly equates the unit and capacity versions.
    Kuhn maximum matching and Konig alternating reachability are in the same file at277/299.

    Correct minimal-deficiency proof: let X be inclusion-minimal deficient, k=|X|. For any d in X,
    minimality gives |Gamma(X\\{{d}})|>=k-1, while it is contained in Gamma(X), whose size<k.
    Thus |Gamma(X)|=k-1 and Gamma(X\\{{d}})=Gamma(X). No neighbor credit is private to a single
    demand. Full pools have even capacities, so k is odd. This says nothing about different
    ACCESSES sharing a pool: three demands of ONE access can provide all the required sharing.

    Exact factorization theorem (all sizes): if every KEEP has a=0, every creator pool is empty,
    and every positive-demand access t has only its own DELETE-setup pool. Distinct such
    accesses have distinct setups by L2. Consequently the graph is a disjoint union of
    complete bipartite graphs K_(q_t,2a_setup(t)), plus unused credits. Its maximum matching is
    sum_t min(q_t,2a_setup(t)); its unmatched count is sum_t(q_t-2a_setup(t))^+.
    Proof: the stated pools are the entire source adjacency; match independently inside each
    disjoint complete component. This is a closed-form structural calculation, not a new Hall premise.

    Scalar identity: R=sum(q-2a)^+, S=sum(2a-q)^+, R-S=Q_B-2A. Thus U4-S iff CD-U;
    U4-M implies CD-U, while CD-U does NOT imply U4-M, as our physical witnesses prove.
    Canonical local-first residualization need not preserve all possible matchings: other
    demands can name an access's local pool as creator/setup. The historical 'locals exclusive'
    phrase in PIVOT_RESIDUAL_JOINT.md is not valid for this full graph.
    """)
    table='\n'.join(f"|{r['access']}|{r['mode']}{r['key']}|{r['dA']}|{r['a']}|{r['dB'] if r['dB'] is not None else '-'}|{r['q']}|{r['z']}|" for r in seven['full_state_replay'])
    save('U4_05_E0_MINIMAL_DEFICIENCY.md',f"""
    # Exact Hall obstruction outside the claimed E0 normal form

    Start A=B=the right vine 1->2->3->4->5->6->7. Execute

        D6 D7 K7 D6 K6 D5 K5 D4 K4 D3 K3 D2 K2 D1 K1.

    |0-based access|operation|dA|a|dB|q|z|
    |---|---|---|---|---|---|---|
    {table}

    Both complete trees return EXACTLY to the initial right vine; the initial state is diagonal,
    so no reachability prefix is needed. Every KEEP has a=0. A=11,Q=6,Z=4,B=10,R=6,S=22.
    In particular Q-2A=-16: scalar Coarse-Double holds.

    Let X be the three K7 doubles at access2, sequences0,1,2. Their triples are respectively
    (7,6,5),(7,4,3),(7,2,1), all RR. Cyclic creator indices from the original replay are6,10,14
    modulo15, all in the previous period, all zero-cost KEEPs. Latest positive A arrival of7
    is D7 at access1, with exactly one StepEv. Therefore the COMPLETE neighborhood is
    {{(1,0,0),(1,0,1)}}. |X|=3>2=|Gamma(X)|. Every proper subset satisfies Hall.
    Original matching is5/6; an independent exhaustive matching and all64 Hall subsets agree.

    There is NO nonstarved KEEP competitor anywhere. The earlier inference 'shared setup
    credits force a nonstarved co-namer' confuses demands with accesses. All three demands
    from K7 already share both credits. This is an actual source-realizable minimal deficiency
    outside E0's required s<t<u<t' with a positive-A-cost competing KEEP.

    E0's equation (q_t-2a_s)+(q_t'-2a_t')=1 is valid only for the stated two-access/full-demand/
    zero-fat graph with no further eligible positive pools. Fat pools must be distinct before
    subtracting their capacities; partial demand subsets need their actual cardinalities.
    E0-overfull is a sufficient Hall obstruction under those assumptions, not a universal normal form.
    {link('audits/PIVOT_18R_CLOSE.md','the historical correction',15)} already withdrew necessity.
    Our witness supplies an exact physical falsification of the earlier stronger bridge.

    L3 erratum: q>=2a+1 is equivalent to dB>=4a+2, not4a+1. The historical n<=8 examples
    dB=6/7 for a=1 are consistent with the corrected threshold.

    {local('u4_counterexample_certificate.json')} includes every state, event, creator, credit,
    adjacency and closure. {local('independent_witness_and_route_c.json')} records the independent check.
    """)
    save('U4_06_RESTRICTED_CD_INHERITANCE.md',f"""
    # Restricted inheritance and arbitrary marked sets

    {link(REBOOT+'02_PROVED/DIRECT_NFKS_RT2_three_keep_key_coarse_double.md')}: root-return +2,
    idempotence and depth<=4 yield Q<=2C_KEEP<=2C_full<=2A for at most three KEEP keys.
    {link(REBOOT+'02_PROVED/DIRECT_CD_K4_four_keep_key_coarse_double.md')}: arbitrary-M marked-core
    reduction and a 68,876-transition one-bit certificate prove the four-key class.
    {link(REBOOT+'02_PROVED/DIRECT_CDK5_LOW_five_key_submaximal_core.md')}: five-key core<=8,
    28,477 vertices/142,385 retained transitions, an explicit 0/1 potential and the same A charging.
    These are scoped proof components; this run read their proofs/certificate definitions, but
    did not rerun those complete older matrices or promote their union to a universal theorem.

    Arbitrary-M core growth: a marked splay never adds an ancestor-core member; an unmarked
    splay increases its size by at most2, because only the first mark-acquiring StepEv can grow
    it. Start a cyclic period just after one marked root; adding successive first-visited targets
    gives1+2(k-1)=2k-1, exact B closure transfers it to the start, and a rotated seam covers all
    boundaries. Pruning mark-free hanging subtrees commutes with marked splay, preserving depths.
    With M fixed, marked splays give core-set inclusion; cyclic closure therefore fixes the set.

    The old CDK5_LOW_source_reduction_proof paragraph asserting arbitrary label swapping is
    superseded by Stage11F's inclusion/constancy proof: an old mark-free hanger is rigid and
    cannot acquire a descendant mark from outside; all rotating operands already lie on a
    marked path. Its size-only overapproximation still suffices for the earlier finite certificate.

    For k=5: core<=9,dB<=8,q<=4, so positive individual overflow has a=0,q1..4 or a=1,q3..4.
    This is arithmetic, not payment. For k=6: core<=11 allows the arithmetic type a=2,q=5
    with overflow1; no physical closed six-support witness of that type is claimed by this run.
    No theorem reduces KEEP-support cardinality. Our second counterexample lies EXACTLY in
    the five-genuine-key/nine-core physical domain and leaves every scalar theorem intact.
    """)
    save('U4_07_CHR_FRC_POTENTIAL_AUDIT.md',f"""
    # Joint-potential audit, current local supersessions and replay scope

    Stage11F: {link(F+'S04_STAGE11F_COMPLETION_CERTIFICATE.md')} plus global-weight/forward-
    simulation/core/mask documents provide the restricted interface: for W in W_5^9, some closed
    P in G_AF has w(P)<=2A-Q. Low w=2H-q exactly; high w=6-q<=2H-q for H>=3. The terminal q
    is from the preterminal B source. All126 masks, permitted fringe/saturated signatures,
    zero/nongenuine operations and arbitrary lengths are in the claimed simulation domain.
    This run reviewed that interface and the low/high compiler predicates, and freshly rebuilt
    the original roots through FRC's verifier. It did NOT rerun every 11F assembly certificate.

    Stage11G freeze: original O/M sorts, same actual midpoint, exact Int, depth2/T266 and
    unchanged predicates. Low has root termination/no repeats; high does NOT. Negative abstract
    cycles need a physical lift before refuting Pair Access. Step01/02 certificates are inherited
    complete; old Step03 reports are OPEN. Later local M2-DSK01 supersedes the committed M2-open
    history: Phi=-3*1_chi8 on both sorts proves all high-only closed walks nonnegative. Its source
    proof includes RIGHT_SELF and LEFT_SUCCESSOR sentinel families; this run audited6,300 saved
    symbolic row provenances,39 controls and44 manifest hashes, not a fresh6,300-reduction execution.

    CHR01: fixed mask{{0,2,4,6,8}},sigma0,chi8,634 physical alpha7 patterns,4,862 core trees.
    Q in{{-2,-1,0}} is a completed table; Theta(O)=-3+Q, Theta(M)=-3. Every cheap low must
    have the specified physical fused H1 representative; expensive w>=2 and all chi8 highs use
    the range bound. Fresh complete independent regeneration passed255,064 vertices and
    2,309,760 edges, including759,788 weight0/+1 lows and96 manifest hashes. This proves the
    registered all-horizon fragment, not all physical W_5^9 or all masks/signatures.

    H2R01: cap Qbar=min(Q_extended_by0,-psi),psi in{{0,1,2}}. Gamma_pre0 gives a terminal debt
    floor; the residual gap0 two-splay kernel has16,842 retained rows. Exactly three old-cap
    failures have (entry,target,exit)=(952,2,1917),(1710,2,1937),(2538,3,2141), q3,H2,w+1,
    psi2->0, old reduced cost-1. They are legal SYMBOLIC original-root edges, not negative cycles.

    FRC01: R={{1917,1937,2141,2965}}; C=1_[sigma0>0 and core in R]; Qnew=Qbar-C.
    All four trees have max depth<=5. The only zero-psi/zero-weight H1 successor is2141--6-->2965,
    and2965 has none. Lowering the basin by1 repairs all three failures and preserves old good
    edges. All original chi8 H2 edges, all masks/signatures/A macros, and every H1 edge starting
    in C are covered; arbitrary other H1 edges remain outside this particular theorem.
    Old debt is repaid by the next transition, with at most one neutral delay. A zero edge can
    repay via increasing psi; this is not the creation of a named A credit.

    Fresh FRC replay passed16,842 fringe rows,4,224 Gamma0 rows,36 typed B transitions,
    seven full LOW roots,one full HIGH root and four full shared-state OPEN blocks. These point
    blocks are not cycles. The universal symbolic source lifting remains a written mathematical
    proof with dependencies, not a proof-assistant certification. Logs/JSON are saved here.

    Newer local work beyond FRC was also located and read:
    - {link('DO_RESEARCH_REBOOT/M3_COMB_AUD01/AUDIT_REPORT.md')}: all single-gap populations,
      all masks and both regions, W(O)=J-5chi8, W(M)=-5chi8,J in[-2,0], closed weight>=0.
      It explicitly rejects full M3 coverage and repairs withdrawn ACL01 via AER01.
    - {link('DO_RESEARCH_REBOOT/M3_UNITPAIR_FIN01/RESULT.md')}: all45 distinct two-unit
      supports, hence all signatures of total population<=2 with the single-gap bank.
    - {link('DO_RESEARCH_REBOOT/M3_POP3_ALL01/RESULT.md')}: restricted successes and a cap,
      not proof from UNKNOWN. Later RISK campaigns add further specific sectors.
    - {link('DO_RESEARCH_REBOOT/M3_POP4_RISK03/RESULT.md')}: reports531/715 total4 vectors,
      combined3,437 signatures/433,062 mask sectors; full M3 OPEN. Its3,620,950,791 residual
      checks were NOT rerun here. Treat these counts as source-reported, not fresh results.
    - M3_POP4_RISK04 has pre-execution/source-lift/partial files but no terminal RESULT or
      final certificate at inspection. Its completion is unverified; no interference occurred.

    Thus FRC's residual description is historical, not the newest coverage frontier. The later
    fixed-population tables still do not prove all saturated signatures, all-support CD-U,
    or original eligibility matching. No existing campaign status is changed by this report.
    """)
    save('U4_08_ELIGIBILITY_PRESERVING_BRIDGE.md',f"""
    # Proposed E0–joint repayment bridge: universal conclusion refuted

    Proposed implication: U1-U3 + original dynamics + restricted signed repayment => ORIGINAL
    local/creator/consumer-setup matching. It fails before a universal E0 compensation proof:
    there are physical minimal Hall obstructions without an E0 nonstarved competitor, and
    the original matching theorem itself is false.

    The second certificate {local('five_keep_nine_core_counterexample.json')} uses exactly
    five genuine KEEP keys{{1,3,5,7,9}}, a stable nine-node B core and exact diagonal paired closure.
    Its inherited eight-KEEP B cycle is preserved. All KEEP A costs are0; every setup has two
    units. Q=18,A=34,Q-2A=-50. Matching is16/18. Minimal triples at accesses3 and19 have exactly
    the setup units at accesses2 and18 respectively. Every other positive A pool is ineligible
    to those triples. There is no positive-A KEEP competitor anywhere.

    Exact lifting construction: begin A=B at each block. For a requested x, first DELETE x,
    obtaining T'=S_x(T). Choose any direct root child y of T'. DELETE y is one zig; DELETE x
    is its inverse zig, restoring T'. KEEP x now has a=0 and brings B to T'. Both trees
    synchronize again. The final DELETE x is the latest positive arrival and has a=1.
    Apply this to every access of any closed B-only word. The B word, KEEP support and core
    evolution are unchanged, and the final pair closes. All creators have zero A supply.
    A block costs ceil(dB/2)+2 in A; matching capacity is exactly2 per consumer setup.

    This construction explains the failure causally: work that made A and B agree BEFORE
    the cheap root-child detour is superseded as setup provenance. That real A work remains
    in total supply but disappears from the consumer's eligible neighborhood. No potential
    adjustment can make a 3-to-2 injection exist without adding eligibility edges or changing
    the theorem. An expanded causal graph would be a different theorem, not a proof of U4-M.

    | Accounting | U4 | CHR/FRC and later J |
    |---|---|---|
    | Unit | individual B double and A StepEv unit | signed macro edge weight and state label |
    | Provenance | exact local/creator/consumer setup | core/shadow/signature value differences |
    | Global sharing | each physical unit once under graph edges | telescoping at actual shared O/M states |
    | Needed import | explicit eligible unit and injection | no such object provided by a reduced-cost inequality |

    The valid weaker conclusion is scalar repayment on the certified symbolic domain.
    Our witnesses satisfy scalar Coarse-Double. No CHR/FRC inequality or graph is refuted.
    """)
    save('U4_09_UNIFORM_POTENTIAL_ALTERNATIVE.md',f"""
    # Route C: still open; two specific transplantations fail

    Desired direct source theorem: a uniformly defined Psi(A_tree,B_tree) on the entire
    claimed reachable transition domain satisfies q-2a<=Psi(source)-Psi(destination).
    Summing on an exactly closed pair walk gives Q<=2A. This implication is elementary;
    existence/verification of such a uniform function is the unresolved mathematics.

    Limitation1, all-size bounded range: in the seven-key construction generalized to n,
    the distinguished K_n has a=0 and q=floor((n-1)/2). Any direct single-access Psi must
    drop by at least that much on this reachable closed-walk edge. Consequently its range
    cannot have a bound independent of n. A range-two FRC correction cannot simply be
    transplanted to ALL raw Pair Access edges. This does not invalidate its macro domain,
    nor forbid a uniform formula with n-dependent unbounded range.

    Limitation2, B-only: start both trees at the three-key right vine; D3,K3,D1,K1 closes both.
    Both KEEPs have a=0,q=1 and B returns to itself. If Psi=phi(B), their two inequalities
    telescope to2<=0. DELETEs cannot help a B-only potential because they do not change B.
    Thus no B-only direct per-access potential works on the universal domain, even n3.
    {local('independent_witness_and_route_c.json')} contains the exact B states and costs.

    These eliminate specified candidates, not general Route C. A macro potential might absorb
    the overwritten setup work; a source potential might retain actual A geometry or a causal
    reserve with range growing in n. No such complete all-size construction is established
    here. 'Every finite graph admits a potential' would assume its missing cycle sign and
    cannot be used as a uniform proof. No finite Bellman-Ford enlargement or fitted all-size
    witness is proposed as progress. Stop after the concrete obstruction, per RESEARCH_RULES.
    """)
    w9=' '.join(m+str(x) for m,x in nine['word'])
    save('U4_10_FALSIFICATION_AND_COUNTEREXAMPLES.md',f"""
    # Falsification, witnesses and reproduction

    ## Seven-key witness and all-size family

    See U4_05 and u4_counterexample_certificate.json. Define V_n=right vine1..n and
    W_n=D(n-1),Dn,Kn,D(n-1),K(n-1),...,D1,K1. For every n>=2 it is exactly closed from
    (V_n,V_n). After D(n-1), n is its right child; Dn costs1. B is still V_n, so Kn has
    q=floor((n-1)/2) and a=0. Every KEEP is immediately preceded by DELETE of the same key.
    Every possible creator therefore has zero credits. Kn's complete neighborhood is the
    two Dn credits. For n>=7 the whole Kn bundle has Hall defect floor((n-1)/2)-2;
    any three of its demands already give a minimal deficiency1.

    Closure proof, not finite extrapolation: after the initial D(n-1), A's remaining non-noop
    key sequence is n,n-1,...,1; B's is that same descending sequence. A descending sweep
    sends any n-key BST to V_n. Inductively after k+1,...,n, the processed right subtree is
    a right vine; accessing k (maximum remaining left subtree) preserves it as the right
    subtree of the new root k. At a final attachment the access path is L followed by Rs,
    so the final zig/zigzag attaches the old root as right child. This proves the invariant.

    n<=6 sharpness for the original matching (paper proof): q<=2 for every access. Nonstarved
    demands fit their local2a>=2; starved demands fit the positive DELETE-setup2a>=2. Distinct
    active starved accesses have distinct DELETE setups, which are disjoint from nonstarved
    local pools. Thus U4-M holds at total key counts<=6 and first fails at n7. This is about
    total keys; the second witness already fails with only five KEEP keys.

    Finite controls: n2..64 in both mirror orientations,126 cases, exact paired closure and
    depth/event/state equality between the pointer and independent frame engines. They support
    the all-n proof; they do not replace it. The seven-key graph stabilizes under2/3/4 context
    laps with credits indexed once. W7 repeated twice closes with A22,Q12; no credit duplication.

    ## Physical five-KEEP/nine-core witness

    Initial trees are identical to the exact T0 literal in the inherited nine-node replay.
    Complete nested trees, all32 transitions and exact neighborhoods are in the new JSON.
    Its word is:

        {w9}

    Original B word: K3,K7,K1,K9,K5,K7,K1,K9. B depths6,4,4,4,6,4,4,4;
    genuine support{{1,3,5,7,9}}, nine-core at EVERY boundary. A34,Q18,Z0,B18,
    R18,S68. Two disjoint minimal Hall triples each have3 demands and2 neighbors;
    original maximum matching16/18 agrees with the exact disjoint-block formula.
    Original symbolic chi8 states or a symbolic lift are not asserted by this physical replay.

    ## Reproduction

    Run from the pinned repo root using Python -B. First certificate creators refuse overwrites:
    use a fresh versioned sibling run, copying ONLY the new verification scripts there. Their
    parent-depth ROOT calculation is unchanged at that level. Existing source/certificates remain inputs.

        python -B <fresh-run>/verify_u4_counterexample.py
        python -B <fresh-run>/verify_saved_and_route_c.py
        python -B <fresh-run>/verify_five_key_counterexample.py
        python -B <fresh-run>/replay_inherited.py chr
        python -B <fresh-run>/replay_inherited.py frc
        python -B <fresh-run>/replay_inherited.py m2

    The first checker uses source pointer + independent frame replay and original matching.
    The saved-certificate checker imports neither pointer genealogy nor original matching:
    it replays the tuple engine, derives complete neighborhoods from all-creators-zero,
    exhausts all64 Hall subsets and independently computes the maximum matching.
    All computations are exact integers. No search timeout is promoted. No genuine CD counterexample
    was found or claimed. Later multi-billion-row population certificates were not rerun here.
    """)
    save('U4_11_PROOF_DEPENDENCY_DAG.md',f"""
    # Proof dependency DAG and conditional downstream assembly

    ```mermaid
    flowchart TD
      PA[Physical splay semantics] --> U123[U1-U3: positive-credit ancestry]
      PA --> K[All KEEP A costs zero]
      K --> F[Eligibility factorizes into consumer setups]
      F --> CE[Exact Hall counterexamples]
      CE --> R[Original U4-M REFUTED]
      CE --> EN[E0 necessity REFUTED]
      J[CHR/FRC and later restricted J] --> RS[Restricted signed telescoping]
      RS -. no eligibility implication .-> R
      C[Uniform source potential: OPEN] --> CD[CD-U / U4-S: OPEN]
      CD --> SUM[B <= 3A: CONDITIONAL]
      Z[C.ZIG: mathematical proof] --> SUM
      SUM --> EX[Cycle excision]
      EX --> PRE[E_B <= 3 S_A + g]
      PRE --> LT[LT retained <= 7 LT full + 2g]
      LT --> DO[Levy-Tarjan 4.3 / DO conditional]
    ```

    No edge from R or EN proves CD-U false. U4-M=>CD-U remains a valid sufficient implication
    with a FALSE antecedent as a universal strategy; U4-S iff CD-U remains the scalar identity.

    C.ZIG: cyclically partition accesses into a positive-A-cost leader and subsequent A-root
    noops. Every later access in a block has the leader's key. At most one KEEP in the block
    can have a B zig, whether the leader is KEEP or DELETE. Charge it to a leader StepEv;
    blocks are disjoint. All-A-zero closed walks have no B work. Hence Z_B<=A universally.
    {link(REBOOT+'02_PROVED/C_ZIG_RECONSTRUCTED.md')} gives the full run proof; formal assembly separate.

    If CD-U were proved, B=Q+Z<=3A. For fixed n the reachable pair graph has at most Cat_n^2
    vertices. Every edge reward b-3a<=floor(n/2). Removing repeated-state nonpositive closed
    subwalks bounds any prefix by g(T0)=(Cat_n^2-1)floor(n/2), or the smaller source maximum
    over reachable simple paths. This proves the cycle-excision implication; its cycle premise
    remains open. Empty/single-key domains are trivial.

    LT translation: d+1<=2ceil(d/2)+1 and ceil(d/2)<=d+1, so LT(Y)<=2E_B+|Y|,
    S_A<=LT(X), and |Y|<=|X|<=LT(X). A universal E_B<=3S_A+g gives
    LT(Y,T0)<=7LT(X,T0)+2g(T0), with the same initial T0.

    Levy-Tarjan v3 Theorem4.3 states that eventual monotonicity of Splay suffices for dynamic
    optimality, using their repeatability/coercibility and specified-tree execution model.
    The primary [paper](https://arxiv.org/html/1907.06310v3#S4) was checked directly; no final
    numeric DO competitive factor is inferred from7 alone. Full proof/kernel assembly gates
    remain in {link(REBOOT+'12_FINAL_PROOF/ASSEMBLY_CHECKLIST.md')}.
    """)
    save('U4_12_FINAL_VERDICT_AND_NEXT_LEAF.md',f"""
    # Final verdict and next leaf

    **EXACT COUNTEREXAMPLE FOUND — original eligibility-constrained U4-M is false.**

    Seven total keys suffice; a second exact witness lies in the five-genuine-KEEP/nine-core
    domain. Both begin diagonally and close both full trees. Coarse-Double holds on both.
    The mathematical family has unbounded Hall deficit while the aggregate retains ample slack.
    The claimed E0 normal form misses same-access multi-double sharing; the proposed universal
    E0-to-eligible-repayment route therefore cannot prove its stated false conclusion.

    BEFORE: original U4-M treated as open; E0 necessity contradicted between historical reports;
    CHR/FRC exact domains required reconstruction. RESULT: U4-M and E0 necessity refuted by
    source-replayable witnesses; signed certificates independently checked at their stated scopes.
    AFTER: abandon ORIGINAL U4-M as a sufficient theorem target; retain CD-U/U4-S and valid
    restricted scalar proofs. NET universal positive-proof advancement: none. Net strategic
    advancement: a false load-bearing charging route is removed, with exact causal explanation.

    The first failed bridge is already 'minimal Hall deficiency requires a nonstarved E0 competitor'.
    The stronger 'restricted scalar repayment yields original eligible matching' is itself false.
    U1-U3 survive: every creator can reach a positive setup pool, but that two-hop pool is not
    one of the consumer's original eligible pools. Adding it changes the graph and needs a
    separately stated source-causal theorem; it is not silently authorized as U4-M.

    Route C remains OPEN. Direct B-only and size-independent bounded-range raw-access potentials
    are eliminated; an all-size A/B construction or complete macro repayment remains unproved.
    No credible positive all-size candidate meeting all four RESEARCH_RULES gates is supplied,
    so no new equivalent capacity premise, finite-fit campaign or support-by-support enlargement
    is launched. The next tightly scoped operation, if a successor is commissioned, is to audit
    a concrete proposed source potential against the explicit overwritten-setup family BEFORE
    fitting anything. It must preserve the work discarded by latest-arrival provenance and allow
    a range growing with n (or justify a different macro boundary). This is an acceptance test,
    not a claim that such a potential has been constructed.

    No Stage11G graph, solver contract, accepted certificate or proof-status file was edited.
    M2's local later proof is inherited; M1/M3/Step03 and full CD-U/DO remain open. Later
    fixed-population signature reports are read-only inputs, with independent-verification limits
    explicitly recorded. Final old-byte/Git comparison is in integrity_verification.json.
    """)
    az=[
    ('A','Repository identity','coarse-double-branch; HEAD/live remote fea2a25b05e97f726b6e1891cebb12c4cfca821a; no tracked changes; 7,825 pre-existing untracked files; one worktree. Newer local research is present.','U4_00_ENTRY_AND_SOURCE_MANIFEST.md'),
    ('B','Original goal','Uniform ordinary bottom-up splay competitiveness against offline BST optimum, present keys and a common specified initial tree. The intermediate cost is StepEv; LT uses access-path nodes.','U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md'),
    ('C','Pipeline','CD-U plus C.ZIG implies B<=3A; cycle excision and event-to-LT arithmetic yield eventual monotonicity with factor7 and overhead2g; Levy-Tarjan4.3 then applies conditionally.','U4_11_PROOF_DEPENDENCY_DAG.md'),
    ('D','Old U4','U1 gives in-epoch creators; U2 gives positive setup supply for starved B-active links; U3 reaches positive credit in <=2 hops. None proves eligible unused credit.','U4_03_U1_U3_RECONSTRUCTION.md'),
    ('E','Credit model','One demand per B double, two units per A StepEv; only consumer local, creator and consumer setup pools are eligible. Creator setup is absent.','U4_04_HALL_AND_CREDIT_MODEL.md'),
    ('F','Hall obstruction','Minimal X has |Gamma(X)|=|X|-1 and no private credit neighbors. Multiple doubles from one access can share all those neighbors. The new minimal obstruction is three demands versus two credits.','U4_05_E0_MINIMAL_DEFICIENCY.md'),
    ('G','E0','The two-access equation is scoped arithmetic. Its claimed universal necessity is false; our closed witnesses have no nonstarved KEEP competitor. The late18R correction had already identified necessity as missing.','U4_05_E0_MINIMAL_DEFICIENCY.md'),
    ('H','Earlier attempts','Net-depth correlation lacks cancellation control; creator fan-in does not bound A supply; epochs cross; greedy/local-first and total slack do not preserve Hall; neutral steps cannot be erased by weight alone. The original graph now has an exact counterexample.','U4_04_HALL_AND_CREDIT_MODEL.md'),
    ('I','Restricted progress','At most3/4 KEEP keys and five-key core<=8 scalar theorems remain valid. Arbitrary-k core<=2k-1 compresses ambient geometry, not support cardinality.','U4_06_RESTRICTED_CD_INHERITANCE.md'),
    ('J','Stage11F','The inherited restricted physical-to-symbolic simulation gives closed P with w(P)<=2A-Q. Its interface/compiler semantics were inspected; the whole original assembly was not freshly rerun.','U4_07_CHR_FRC_POTENTIAL_AUDIT.md'),
    ('K','Stage11G','G_star=G_AF remains frozen. M2 is proved in later local DSK01; M1/M3/Step03 remain open. Raw high witnesses retain sentinel/declared-depth behavior absent from physical splay.','U4_07_CHR_FRC_POTENTIAL_AUDIT.md'),
    ('L','New results inherited','CHR complete2,309,760-edge verification and FRC full row/root audit pass freshly. Later single/multi-gap population reports are newer restricted results, with their larger matrices not rerun here.','U4_07_CHR_FRC_POTENTIAL_AUDIT.md'),
    ('M','Candidate bridge','The original universal eligibility-preserving conclusion is refuted, including inside W_5^9. FRC reduced-cost compensation does not identify new admissible credit units for that graph.','U4_08_ELIGIBILITY_PRESERVING_BRIDGE.md'),
    ('N','Route C','A uniform original-state potential still could prove CD-U. B-only and n-independent bounded-range raw-access variants fail exactly; macro potentials are not refuted by that test.','U4_09_UNIFORM_POTENTIAL_ALTERNATIVE.md'),
    ('O','Falsification','W7 has A11,Q6,matching5/6,Hall3>2. The W_5^9 witness has A34,Q18,matching16/18 and two disjoint minimal triples. Both have exact paired closure.','U4_10_FALSIFICATION_AND_COUNTEREXAMPLES.md'),
    ('P','First theorem resolved','The exact all-starved graph factorization yields a systematic counterexample construction. Original U4-M is false; it is no longer an unresolved positive proof leaf.','U4_04_HALL_AND_CREDIT_MODEL.md'),
    ('Q','Dependencies','The refutation uses present-key rotations, DELETE freezing, root-child inverse zigs, cyclic setup definitions and the exact original adjacency. It assumes neither E0 completeness nor CD-U nor any symbolic sign theorem.','U4_08_ELIGIBILITY_PRESERVING_BRIDGE.md'),
    ('R','Circularity','Full neighborhoods and shortages are computed from source, independently of total slack. The all-n family is proved structurally, with finite controls only corroborating it. No equivalent capacity conjecture is added.','U4_10_FALSIFICATION_AND_COUNTEREXAMPLES.md'),
    ('S','Scope','The seven-key witness is fully physical; the second has exactly five genuine KEEP keys and nine core nodes. FRC remains a restricted symbolic theorem; no abstract cycle is called a physical one.','U4_08_ELIGIBILITY_PRESERVING_BRIDGE.md'),
    ('T','Credit audit','Each period contributes credits once. K7 has precisely two D7 setup units; all creator/local pools are empty. Context2/3/4 and a doubled nonprimitive period preserve accounting.','U4_10_FALSIFICATION_AND_COUNTEREXAMPLES.md'),
    ('U','Generalization','Hall shortage floor((n-1)/2)-2 is unbounded. At six KEEP keys the possible q5,a2 overflow lies outside the five-key arithmetic; this run does not claim a physical six-support realization or universal payment for it.','U4_06_RESTRICTED_CD_INHERITANCE.md'),
    ('V','Independent verification','Pointer/frame full-state replay, cyclic original charge, independent saved-certificate Hall/matching check,126 mirror/family controls, CHR/FRC reruns and M2 provenance audit completed. Full11F/Lean/later billion-row audits were not rerun.','U4_10_FALSIFICATION_AND_COUNTEREXAMPLES.md'),
    ('W','Research advancement','A false universal charging target and false E0 necessity bridge are removed. No original CD-U inequality case is newly proved by this negative result. Valid restricted scalar machinery is preserved.','U4_12_FINAL_VERDICT_AND_NEXT_LEAF.md'),
    ('X','Remaining gap','The all-size source-exact signed potential/repayment law remains missing. The preferred original matching bridge cannot be repaired while retaining its false matching conclusion.','U4_12_FINAL_VERDICT_AND_NEXT_LEAF.md'),
    ('Y','Recommended continuation','Use the explicit overwritten-setup family as the first acceptance test for a concrete Route C candidate. No positive all-size candidate presently passes the four-rule gate; stop instead of adding an equivalent open premise.','U4_12_FINAL_VERDICT_AND_NEXT_LEAF.md'),
    ('Z','Final proof verdict','EXACT COUNTEREXAMPLE FOUND: U4-M. Universal Coarse-Double/U4-S and Dynamic Optimality remain OPEN.','U4_12_FINAL_VERDICT_AND_NEXT_LEAF.md')]
    maintext='# DIRECT-U4 — A–Z research report\n\n2026-10-30, Asia/Karachi.\n\n**EXACT COUNTEREXAMPLE FOUND to the original U4 matching theorem. Universal Coarse-Double remains open.**\n\n'
    maintext+='Start both trees at the right vine1..7 and execute:\n\n`D6 D7 K7 D6 K6 D5 K5 D4 K4 D3 K3 D2 K2 D1 K1`.\n\nBoth full trees close. At K7, three B doubles have exactly two eligible credits. All KEEP A costs are zero. Totals: A11,Q6, so Q-2A=-16. A second physical counterexample has exactly five KEEP keys and nine core nodes.\n\n'
    for letter,title,body,filename in az:
        maintext+=f'## {letter}. {title}\n\n{body}\n\nDetails: {local(filename)}.\n\n'
    maintext+='The original reports and certificates are preserved. See '+local('proof_status_ledger.json')+' and '+local('integrity_verification.json')+'.\n'
    save('U4_AZ_RESEARCH_REPORT.md',maintext)
    claims=[
      ('U4-M','REFUTED EXACT','All reachable exactly closed physical Pair Access walks','u4_counterexample_certificate.json','One-period full graph, source matching and independent exhaustive check'),
      ('U4-S','OPEN','All finite supports and lengths','U4_04_HALL_AND_CREDIT_MODEL.md','Equivalent to CD-U; distinct from U4-M'),
      ('CD-U','OPEN','All finite supports and lengths','U4_12_FINAL_VERDICT_AND_NEXT_LEAF.md','Neither new witness violates Q<=2A'),
      ('HALL-MINIMAL','PROVED UNIVERSAL','Any finite unit graph','U4_04_HALL_AND_CREDIT_MODEL.md','Complete combinatorial proof; no access-level E0 inference'),
      ('E0-NECESSITY','REFUTED EXACT','Claim every minimal original Hall deficiency requires nonstarved competitor','u4_counterexample_certificate.json','Minimal triple, no nonstarved KEEP'),
      ('ALL-STARVED-FACTORIZATION','PROVED RESTRICTED','Every source closed walk with all KEEP A costs zero','U4_04_HALL_AND_CREDIT_MODEL.md','Exact union of disjoint setup complete bipartite components'),
      ('ALL-N-FAMILY','REFUTED EXACT','Original U4-M for every total key count n>=7','U4_10_FALSIFICATION_AND_COUNTEREXAMPLES.md','Structural construction plus126 finite controls'),
      ('W5-9-U4-M','REFUTED EXACT','Five genuine KEEP keys, stable nine-core','five_keep_nine_core_counterexample.json','32 physical transitions;18 demands, maximum matching16'),
      ('ROUTE-C-B-ONLY','REFUTED EXACT','Direct per-access potential depending only on B','independent_witness_and_route_c.json','Three-key B-projection cycle contradiction'),
      ('ROUTE-C-BOUNDED-RANGE','REFUTED EXACT','Direct per-access potential with range bound independent of n','U4_09_UNIFORM_POTENTIAL_ALTERNATIVE.md','Required distinguished drop floor((n-1)/2)'),
      ('ROUTE-C-GENERAL','OPEN','Uniform all-size source-exact state potential or complete repayment','U4_09_UNIFORM_POTENTIAL_ALTERNATIVE.md','No positive all-size candidate constructed'),
      ('CHR01','PROVED RESTRICTED','Registered fixed-mask sigma0 chi8 fragment','chr_independent_replay.log','Fresh complete255064-node2309760-edge independent regeneration'),
      ('FRC01','PROVED RESTRICTED','All original symbolic chi8 H2 edges and stated H1 basin','frc_independent_replay.json','Fresh row/typed/root audit; written source-lift proof separately reviewed'),
      ('M2-DSK01','PROVED UNIVERSAL','Complete frozen high O/M subgraph, not whole G_AF','m2_independent_replay.log','Paper proof reviewed;6300-row provenance audit, not fresh symbolic reductions'),
      ('M3-LATER','REPORTED BUT NOT RERUN','Later fixed-signature restricted banks','U4_07_CHR_FRC_POTENTIAL_AUDIT.md','Latest terminal report read: POP4_RISK03; RISK04 no terminal verdict at inspection'),
      ('11F','PROVED RESTRICTED','Inherited W_5^9 weighted simulation','U4_07_CHR_FRC_POTENTIAL_AUDIT.md','Interface/compiler audit; whole certification assembly not rerun'),
      ('M1-M3-STEP03','OPEN','Original frozen full sign obligations excluding proved M2','U4_07_CHR_FRC_POTENTIAL_AUDIT.md','No graph edits or promotions'),
      ('C.ZIG','PROVED UNIVERSAL','Finite closed present-key Pair Access walks','U4_11_PROOF_DEPENDENCY_DAG.md','Complete mathematical block proof; Lean assembly not claimed'),
      ('PIVOT2-COST-LT','PROVED CONDITIONAL','Reachable cycle bound plus common initial-tree cost model','U4_11_PROOF_DEPENDENCY_DAG.md','Cycle excision, factor7 translation, external4.3; upstream CD-U open'),
      ('DYNAMIC-OPTIMALITY','OPEN','Uniform competitiveness against offline BST optimum','U4_12_FINAL_VERDICT_AND_NEXT_LEAF.md','No full pipeline proof')]
    ledger={'date':'2026-10-30','timezone':'Asia/Karachi','head':baseline['head'],
            'relations':['U4-M => CD-U','U4-S <=> CD-U','CD-U does not imply original U4-M'],
            'verdict':'EXACT COUNTEREXAMPLE FOUND','claims':[dict(id=i,status=s,domain=d,artifact=a,verification=v) for i,s,d,a,v in claims],
            'forbidden_promotions_observed':False,'existing_research_modified':False}
    save('proof_status_ledger.json',json.dumps(ledger,indent=2))
    # Exact dependency paths cited in the reports are pinned in the full entry baseline.
    cited={}
    for path,meta in baseline['files'].items():
        if (path.startswith('audits/PIVOT_') and any(x in path for x in ('OVERFLOW','U1U4','U4_','TIGHT_DANCE','E0_','RESIDUAL_JOINT','18R_CLOSE','BINARY_DECISION'))) or path in ('python/liquidity/legacy_embedding.py','python/independent/splay.py','scripts/wp6_eventflow.py','scripts/wp6_overflow.py','scripts/wp6_coarse_double.py','scripts/wp6_cycle_ratio.py','lean/WP6/GCStaticGenealogy.lean'):
            cited[path]=meta
    save('source_index.json',json.dumps({'head':baseline['head'],'selected_source_pins':cited,'complete_pins':'entry_baseline.json','fresh_results':['u4_counterexample_certificate.json','independent_witness_and_route_c.json','five_keep_nine_core_counterexample.json','chr_independent_replay.log','frc_independent_replay.json','m2_independent_replay.log']},indent=2))
    print(json.dumps({'markdown_reports':14,'ledger_claims':len(claims),'directory':str(OUT),'verdict':ledger['verdict']}))

if __name__=='__main__':main()
