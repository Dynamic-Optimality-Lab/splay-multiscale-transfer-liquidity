# One delayed shallow payer can cover an entire positive run

Status: PROVED—RESTRICTED DOMAIN. This theorem extends delayed private-payer charging to several positive blocks using one physical payer pool, without reusing a credit. The shared payer serves one maximal consecutive positive run. Different runs retain separate payers.

The theorem has no bound on tree size, KEEP support, run length, deficit magnitudes, delay or fringe shape. Its source admissibility conditions are explicit restrictions. They are not claimed for every walk. No terminal potential, matching evaluator, flow optimizer or general allocation witness is used. The matching-terminal line remains frozen.

## Source blocks and maximal positive runs

For a finite reachable closed present-key pair walk use the established cyclic A-root blocks. Each block i has one leader of positive A cost a_i>=1, followed by same-key root no-ops, and at most one nontrivial B splay. Let q_i be its B-double count and delta_i=q_i-2a_i. Then

    sum_i delta_i=Q_B-2A.

If A=0, all A requests use a fixed root; B could change at most once, and closure forces no B change, so Q_B=0. Empty/one-key/empty-walk cases are included. If there are no positive blocks, every demand pays locally. If every block is positive, no distinct nonpositive payer gap exists, so the new class rejects rather than asserting an impossible budget.

Otherwise partition the positive blocks into maximal consecutive cyclic runs R. Each run begins after a nonpositive block and ends before a nonpositive gap. Define its actual excess

    E_R=sum_(i in R) delta_i>0.

Run starts are intrinsic even when a run crosses the chosen seam. Every positive block belongs to exactly one run.

## Common shallow key and one physical B-demand ceiling

For each positive anchor i, let T_i be B immediately before its unique nontrivial B splay. Let C_i contain T_i's root and its nonempty original children. For a proposed payer j, its leader key y must lie in

    C_R=intersection_(i in R) C_i.

This intersection has at most three keys and may be empty. No existence of a common key is assumed universally.

For each i in R let h_i(y) be y's actual depth just after anchor i's B splay. The source root/child transport lemma gives h_i(y)<=3. Let k_i(j) count every genuine B-changing KEEP strictly between anchor i and payer j. This includes later positive anchors, nonpositive interveners and zero-double zigs. DELETEs and B-root no-ops contribute zero. The source one-splay depth bound d'(y)<=d(y)+2 yields

    q_j<=c_i(j)=floor(h_i(y)/2)+k_i(j)

if j has a KEEP. If j has none, put c_i(j)=0. These are the established source bounds from DS, applied on the same actual walk. An intervening access to y is harmless: it resets the tracked depth and still satisfies the bound.

All anchors bound the SAME physical q_j. Therefore the correct shared ceiling is

    c_R(j)=min_(i in R) c_i(j),
    q_j<=c_R(j).                                  (1)

Neither the bounds nor their savings are credit units. They do not create multiple copies of the payer's capacity. Overlapping histories may appear in several k_i values because they support several upper bounds; only the minimum is used to bound the payer's own work once.

## Canonical restricted class and explicit A threshold

Scan forward after the run, stopping before the next positive block or returning to the run. Choose the FIRST block j whose leader key lies in C_R and satisfies

    E_R+c_R(j)<=2a_j.                             (S)

If a run has no such payer, reject that walk from this restricted class. This is a source A-cost restriction, equivalently

    a_j>=ceil((E_R+c_R(j))/2),
    d_A at payer LEADER >= 2ceil((E_R+c_R(j))/2)-1.

The leader may be DELETE followed by a starved KEEP. Its cost is the actual leader cost; it is not replaced by the zero A cost at a later KEEP. No source identity is asserted to force this threshold on arbitrary walks.

Every block between the run and its payer is nonpositive because the scan stops at the next positive. By (1) and (S),

    delta_j=q_j-2a_j<=c_R(j)-2a_j<=-E_R<0.         (2)

Thus the payer's negativity is derived, rather than supplied as another repayment premise. The run plus interveners plus payer has nonpositive total deficit.

For unit-positive runs E_R is the run length; the same threshold becomes a_j>=ceil((|R|+c_R)/2). For non-unit runs use their actual source excess E_R. No assertion of realizability for every numerical parameter combination is needed or made.

## No packet overlap on the circle

The maximal positive runs and their following nonpositive gaps form disjoint cyclic cells. Each selected packet is a prefix of its own cell: the entire positive run, followed by nonpositive blocks through its first qualifying payer. It cannot cross the start of the next positive run.

Hence distinct selected packets share no block or payer. This remains true for a single run, for seam-crossing runs or packets, and when a packet uses every block once. Full-lap repeated positions are not introduced. Unselected tails of gaps contain only nonpositive blocks.

The common payer may be eligible for other anchors as a key, but only its own packet owns that physical pool. The disjoint-cell rule prevents its credits from being promised to another run. Sharing ACROSS distinct positive runs is outside this theorem.

## Constructive allocation inside the shared pool

Give each actual A StepEv two distinguishable units. In every positive anchor i, use its own 2a_i units on its first 2a_i B doubles. Exactly delta_i B demands remain.

List the anchors of R in their intrinsic run order i_1,...,i_p. Let

    D_0=0, D_t=sum_(s<=t) delta_(i_s), D_p=E_R.

Number the payer's 2a_j units in source event/bit order. Give anchor i_t the disjoint slice [D_(t-1),D_t). Then pay payer j's own q_j demands from [E_R,E_R+q_j). These intervals fit because

    E_R+q_j<=E_R+c_R(j)<=2a_j.

Every intermediate nonpositive block uses its own leader units locally. None of its unused capacity is borrowed. All remaining nonpositive blocks outside packets also pay locally. Positive leaders and payers have different physical identities, packets are disjoint, and the slices inside each payer pool are disjoint. Thus every B double is paid once and no A unit is reused.

This counts the payer's own B demand once and its actual A pool once. The source ceiling c_R reserves room for that one B demand; it is not added to the resource budget. The allocation is explicit concatenation, not Hall feasibility or a solver result.

Summing the charges proves Q_B<=2A on the stated shared-run class. This is closed-walk scalar charging: future payer work can be assigned to earlier demands, including across the seam, with one cyclic budget. It is not an online claim or a claim about the refuted creator/setup eligibility graph.

## Canonical scan and seam invariance

Each run's common keys, all actual h_i values, intervention histories and first qualifying physical payer are intrinsic to the cyclic trace. Changing the cut only relabels blocks. The first-payer scan examines exactly the candidates in the run's gap, so it is sound and complete for the explicitly defined restricted class. It introduces no unknown allocation selection.

Run order fixes the anchor slices even when the cut passes between positive anchors. Every source occurrence retains the same A event/bit and B-double identity. Rotating a proof therefore cannot duplicate a payer pool or reuse prefix/startup credit.

## Containment and unresolved complement

Every DS walk is included. DS cannot admit consecutive positive blocks: its first anchor would find no payer before the next positive. Thus every positive run in a DS walk is a singleton. Then E_R=delta_i, C_R=C_i, the minimum has one term, and the threshold and first-payer scan are exactly DS. Zero-positive and zero-A cases agree as well.

SP02 supplies a reachable consecutive-positive witness admitted here but rejected by DS, proving strict containment. It uses two non-unit-compatible anchors with deficits 2 and 1, a saturated zero-deficit intervener and one common payer. Four earlier DS/SC witness controls are preserved unchanged.

The source displacement and shallow-transport components are already banked; they are not counted as new advancement. The new restricted case is the common-pool positive-run construction and its no-reuse allocation. Runs lacking a common shallow key, inadequate A capacity, sharing across different runs, split payers and arbitrary interleaved allocation remain outside the theorem. Universal Step 3, CD and all Stage 11G statuses remain OPEN and unchanged.
