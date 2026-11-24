# Universal Relaxed Coarse-Double via early pairing conservation

**Research plan and execution record, 2026-11-23.** The root inequality is open. This document specifies the proof target, the parts of the argument already justified, and the first source and symbolic audits. The [GSO record](https://app.notion.com/p/41f6251839be81d18fd6c910dcaa8a2d) and [previous complete-period calculation](GSO_OMEGA5_COMPLETE_PERIOD_20261123.md) preserve the antecedent attempts.

## Original quantities and acceptance condition

Take a finite admissible original history $W$ on a fixed ordered physical key set of size $n$. Both full labeled trees close exactly. A splays at every KEEP and DELETE. B splays only at KEEP. DELETE retains its key. An A unit is an original A splay step, either a double or a terminal zig. Write $R_A$ for the number of real A rotations and $Z_A$ for the number of its terminal zigs. Thus $R_A=2A-Z_A\le 2A$. A pays one unit per genuine B KEEP in the aggregate, by the disjoint cyclic A gaps between changing retained roots. In particular, $K_B\le A$ and B's terminal zigs are at most $K_B$.

The frozen selected $H=5$ bank runs on blocks of five consecutive physical ranks, with the original reset, transfer, and priority rules. Evaluate it at its greatest clipped cyclic seam. In this calculation:

- $Q_B$ counts all actual B doubles.
- $P_5$ counts the actual doubles funded on that bank trajectory.
- $\Omega_5$ counts the complementary original double occurrences, including those between funded steps in a single splay.
- Paid-double receipts assign distinct issuance slots to literal A units, at load at most 45 per A unit. A slot is an accounting index within its unit. Real A-rotation coordinates will use the first real rotation of the relevant unit. A terminal zig has only one real rotation.
- Reaching-prefix work supplies no period coordinates. Earlier-lap receipts are reduced to their actual occurrence within the counted cyclic period, with their chronological offset retained.

The established interface is

$$
Q_B=P_5+\Omega_5,\qquad P_5\le45A.
$$

The acceptance condition is a source-independent finite $K$ with $\Omega_5(W)\le KA(W)$ for **every** admissible exactly paired-closed $W$. It would give $Q_B\le(45+K)A$. This document does not change the chosen bank or require $\Omega_5=0$. Other original residual partitions, source conditions, and proof ledgers retain their stated scopes. See the [frozen engine](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/README.md) and [root acceptance record](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/ROOT_ACCEPTANCE.json).

## Why to count repeated pairings across a lifetime

The depth quantity $F$ from the prior calculation has genuine B descent but incurs a signed A recharge at least $m(m+2)$ on complete $H_{3,q}$ periods with $A=8m$. The entire initial B burst in that calculation is paid. Capping straddler counts gives a bounded signed A budget but can miss a dry event while its containing A intervals still have a straddler. The next proof must distinguish actual unpaid occurrences from large arbitrary depth changes and must retain physical chronology through re-creation.

[Chmel et al., *Splay trees are almost dynamically optimal*](https://arxiv.org/html/2607.18498v1), Theorems 1–2 and Sections 5.2–5.6, supply two tools. Their heavy paths relate each B same-side double to two pairings of off-path members. Their ordered groups can grow, convert to shrinking, split, and move, while each persistent group entry has a well-defined join time and each split inherits the pass count. The published total-cost theorem has a support-dependent factor $O(\log\log n(\log\log\log n)^2)$. We use the group's decay with a **fixed fractional error** and keep the original $H=5$ paid/unpaid labels on the resulting pairing records.

### Opposite-side work via a bend count on the original trees

Let $S$ and $Z$ count same-side and opposite-side B doubles. Let $U$ count the original unpaid members of $S$. The following direct calculation adapts the published bend argument without using the published normal-form tree as a donor.

For analysis, augment physical B with a value leaf at each key and the null-gap leaves in inorder. Their positions are the $n$ key values and the $n+1$ gaps between them and at the extremes. Give a value leaf the actual depth of that key in A, with root depth zero. Give an interior gap rank $\tfrac12$ plus the smaller of the A depths of its two neighboring real keys. An exterior gap uses its only real neighbor. These leaves record labels and supply no credit.

A B subtree whose physical key interval is $[l,u]$ contains the values $l,\ldots,u$ and all gaps from the one just before $l$ to the one just after $u$. Its minimum-rank leaf is determined by the shallowest A key of $[l-1,u+1]\cap X$, with indices interpreted as physical ranks. The shallowest key is the LCA of that interval's endpoints in A. It lies in the interval and is an ancestor of every key in it. An interior minimizing key gives the value leaf. An exterior minimizing neighbor gives its adjacent boundary gap. Thus the minimum is unique. Every B vertex selects the child toward this minimum. A bend consists of two consecutive selected physical edges with opposite directions.

For a real A rotation promoting $x$ over $p$, the shallowest key of a contiguous interval can change only from $p$ to $x$. An interval meeting the rotated frame and its exterior has an unaffected shallower ancestor in it, by the LCA of an inside key and an outside key. Inside the frame, the two pivots separate the three hanging ranges. A range containing neither pivot stays inside one unchanged hanger. A range containing one pivot keeps it as its shallowest key. A range containing both switches from $p$ to $x$. The reflection has the same reasoning. Therefore a change of selected edge in the fixed B tree has previous minimum from the value of $p$ and its two gaps, and new minimum from the value of $x$ and its two gaps. An ordered pair of distinct leaves can change a selected outgoing edge only at the B LCA of the two leaves. There are at most nine such changes. A newly selected physical edge lies in at most two new bends, so one A rotation can create at most 18 bends.

During a nontrivial B splay of $x$, the post-A root is already $x$. The old B search path is selected all the way to $x$. Every opposite-side double consumes a distinct bend at its lower old ancestor. The old path direction there is the same before the double because previous steps change only the shape below the two current old ancestors. After the splay, each side of $x$ selects the unique gap immediately adjacent to $x$ on that side. Its path is monotone. A right-right rewrite
$$
g(L,p(M,x(C,D)))\longmapsto x(p(g(L,M),C),D)
$$
adds $p$ to the left side's right-going path. The retired $g$ has a light incoming edge from $p$ and can extend the selected path into at most one of its old hanging subtrees, creating at most one bend at the hanger root. Left-left is its reflection. An opposite-side double places one consumed ancestor on each monotone side path, and a terminal zig places one ancestor on its own side path. Subsequent steps extend those side paths above the portions already processed. The internal selected edges of the old hangers remain unchanged. Thus the net change during B is at most $S-Z$ summed over the period.

The bend count is a function of the full pair and therefore cancels on exact cyclic closure. We obtain

$$
Z\le S+18R_A\le S+36A,\qquad
\Omega_5\le U+Z\le 2U+81A.
$$

The last inequality uses $S\le P_5+U\le45A+U$. This supplies a direct comparison for the opposite-side term. It does not give a numeric point-gap budget for the original A ranks. Compare the original literature method in [Lemmas 11, 13, 16 and 17](https://arxiv.org/html/2607.18498v1#S5.SS2).

### Boundary and late pairing absorption

Fix $W$ and consider $r$ copies. Run the published lazy-interval analysis with its own normal-form comparator on the genuine B KEEP sequence. The original B execution and occurrence IDs remain in order when DELETEs and root-identical KEEPs are omitted from this analytic sequence. All A rotations that matter to the comparison can be scheduled between the retained requests, ending with that target at the root. This is a legal root-BST comparator costing $O(rA+n)$, including an optional terminal adjustment. The published normal-form theorem changes that cost by an absolute factor. Its rotations supply a numerical comparison only. They do not enter the original physical A coordinate set. See [the existing transfer audit](IAGS12_PARALLEL_A_PERIODIC_NEAR_OPTIMALITY.md) and [Chmel et al., Section 5.1](https://arxiv.org/html/2607.18498v1#S5.SS1).

Each original same-side double gives two published pairing occurrences, even where the bookkeeping groups reorder disjoint pairings within a splay. Attach the original double ID and its frozen paid/unpaid value to both. The greatest fixed point of the monotone clipped period map is the same as that of its $r$th iterate. Indeed, descending iterates from the top stock vector converge to the same fixed point if we retain every $r$th iterate. The repeated physical costs and labels are therefore $r$ copies of their original values.

The number of lazy interval creations, updates associated to comparator rotations, and heap-child exchanges is $O(rA+n)$ before counting boundary pairing moves. These follow from the bounded local edits of Lemmas 11, 15 and 23 and the interval creation count in Lemma 31. Separate out the explicit boundary delete-and-insert moves in Lemma 24. The following bounds are on all pairings of the indicated kind, so they also bound any subset whose original parent is unpaid.

1. **Boundary pairings.** An interval can lose at most four members to boundary pairings in one splay. A broken first use costs at most four. Once an interval is shrinking and has size below 70, its subsequent uses below that threshold can lose at most 69 members. A singleton exchange can be counted as the start of a new membership instance at the existing $O(rA+n)$ exchange cost. When an unbroken interval of size at least 70 is processed, Lemma 21 gives at least 32 internal pairings involving that interval. Thus the boundary count is at most $I_r/8+O(rA+n)$, where $I_r\le 2rS$ is the internal pairing count. To sum the large-interval charges, index them by the original interval instance and the splay in which the corresponding internal pairings occur. An internal pairing contributes to one such interval and splay.

2. **Late internal pairings.** In the published Pass interface, a shrinking group of initial size $b$ that was converted from growing may split into several descendants. All descendants inherit the pass count. Their membership sets are disjoint and a member may reach a given age at most once in that family. Delete and exchange cannot increase the surviving count within the family. After a fixed number of exempt passes, one pass removes at least a fixed fraction $\gamma>0$ of the current members. Consequently at most $b(1-\gamma)^{\tau-O(1)}$ entries can reach pass index $\tau$, by induction across all split descendants. Every later pairing loses a different such entry. Fix $\tau$ large enough that this factor is at most $1/8$. Summing over initial converted memberships, and charging each entry once at its insertion into a growing group, gives a late bound at most $(2rS+O(rA+n))/8$. The $2rS$ term allows one new next membership per pairing, including a boundary pairing. Other insertions and exchanges are included in the original bounded comparison overhead in the paper.

These arguments specialize the published decay and boundary estimates with fixed constants. They avoid multiplying the late count by the paper's contracted rank range. The split inheritance and the separation of chronological group entries are necessary for the induction. A re-entry into a new growing group is counted as a new membership, even when its key label previously appeared. See [Lemmas 18–28 and 31](https://arxiv.org/html/2607.18498v1#S5.SS4).

Let $E_{\tau,r}$ count **internal pairing occurrences in passes before $\tau$ whose original same-side double was unpaid** in the repeated trace. Then

$$
2rU\le E_{\tau,r}+\tfrac12 rS+O(rA+n),
\qquad
\tfrac32rU\le E_{\tau,r}+O(rA+n).
$$

The second inequality uses $S\le45A+U$. Each original unpaid same-side double contributes exactly two pairing occurrences. All constants in these expressions are absolute once the fixed thresholds are chosen. A proof that $E_{\tau,r}\le C(rA+n)$ with one absolute $C$ would, after division by $r$ and a limit with $W$ fixed, bound $U$ by an absolute multiple of $A$. The bend inequality and the frozen paid interface would then close Universal Relaxed Coarse-Double. This argument allows the analytic groups themselves to have a nonperiodic seam, with their initialization counted once.

## Quadratic congestion on genuine A work

For a set of $M$ demand occurrences, let $N(e)$ be the specified nonempty set of eligible genuine A rotation IDs for each $e$. An eligible original rotation can obtain eligibility through an explicit causal ancestry event or a frozen paid receipt. A derived rank label, an auxiliary comparator rotation, a copied physical label, or a virtual bit supplies no coordinate. Let $p_{e,j}$ be nonnegative, supported on $N(e)$, and sum to one for each demand. The load is $\ell_j=\sum_e p_{e,j}$. We need a source-uniform bound of the form

$$
\sum_j\ell_j^2\le C M.
$$

Indeed $\sum_j\ell_j=M$ and there are at most $R_A$ real A rotations, so $M^2\le R_A\sum_j\ell_j^2$ proves $M\le C R_A\le2CA$ if $M>0$. The same argument on $r$ copies uses at most $rR_A$ real coordinates. The inherited paper's one-time bookkeeping initialization can be treated separately at an explicitly proved additive cost. A bound on $E_{\tau,r}$ follows if this quadratic estimate can be verified for the early demand rows. Funding a fixed positive fraction of those rows with bounded load would also suffice.

The attachment's Gram reformulation is exact. For unit vectors $v_e$ in $\mathbb C^d$, let $Q=\sum_e v_ev_e^*$. Then
$$
\operatorname{tr}(Q)=M,\qquad
\operatorname{tr}(Q^2)=M+\sum_{e\ne f}|\langle v_e,v_f\rangle|^2
\ge\sum_j Q_{jj}^2.
$$
Setting $p_{e,j}=|(v_e)_j|^2$ gives the load diagonal. Conversely, for fixed nonnegative row weights choose independent coordinate phases with these squared magnitudes. For different rows the cross-coordinate expected products vanish, giving expected Gram energy $M+\sum_j\ell_j^2-\sum_{e,j}p_{e,j}^2$. The physical restriction is on the supports. With unrestricted coordinates the least possible energy for $d>0$ is $\max(M,M^2/d)$. Use orthonormal columns at $M\le d$. At $M\ge d$ take the first $d$ rows of an $M$ by $M$ unitary Fourier matrix and scale columns to norm one. If $R_A=0$, the actual source has no unpaid demands. The identity alone supplies no physical congestion bound.

### Exact optimization and falsification for fixed eligibility

The squared load minimum on the declared graph is

$$
F_{\rm opt}
=\max_{x_j\ge0}\left(2\sum_e\min_{j\in N(e)}x_j-\sum_jx_j^2\right).
$$

For every $x$ the claimed lower bound follows by expanding $\sum_j(\ell_j-x_j)^2\ge0$ and minimizing each linear row contribution over its eligible simplex. At an optimal load vector a row uses only bits attaining the minimum load on its eligible support. Otherwise moving a sufficiently small amount from a larger-load eligible bit to a smaller one reduces the square sum strictly. Taking $x=\ell$ attains the dual value. This gives an exact finite diagnostic suitable for the existing GSO framework.

If $t$ demands share a combined support of $s$ bits, their load forces energy at least $t^2/s$. To reject a fixed quadratic law for every constant using a family of **complete** histories, this lower bound must grow compared with the full relevant demand count, not merely compared with one selected set of high-load bits. A single large load or a Hall obstruction at capacity one or two is insufficient. A fixed positive fraction of bounded-load coverage can suffice for the root proof even if full quadratic funding on that eligibility graph fails.

### Initial graph from existing paid receipts

For an original KEEP $t$, use the distinct real first rotations of the donor A units of its $p_t$ paid B doubles. Permit each demand arising in that KEEP to use those coordinates. This is a specified same-splay comparison for an aggregate proof and includes its later paid doubles. A dry double can only follow at least five paid doubles in that splay, since the target starts at cap five. The receipts themselves carry actual cyclic provenance.

Let $e_t$ be the number of demand rows from KEEP $t$. It can count dry original doubles in the audit or the selected early internal pairing occurrences in a proof. By positivity across KEEP groups and Cauchy--Schwarz within each group, every allocation has energy at least $\sum_{t:e_t>0}e_t^2/p_t$. Uniform use of the $p_t$ distinct paid receipt slots achieves that sum on the slot inventory. The preserved at-most-45 slots per original A unit gives, after collapse to first real rotations, an energy at most 45 times that sum. This specifies exactly what must be checked for this graph. It does not claim a universal estimate for the sum.

On [the saved positive 257-key witness](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/run_003/complete_00.json.gz), the two raw dry rows are B(99,14) and B(99,15). Both follow B(99,13), with the paid receipt tied to A(363,1), slot 40, in the previous lap. One-bit eligibility gives squared energy 4. All 14 paid receipts of this splay use seven distinct A units, so the same-splay graph for these two rows has exact minimum $4/7$. This audit calibrates the original A supports. It does not classify those two B doubles' auxiliary early pairing occurrences.

## First execution

1. **Replay the fixed witness and its two-lap version.** Use the existing source checker and paid-credit provenance. Pin each same-splay donor occurrence and its lap offset. Check that the energy refers to distinct original chronological work, including cross-seam aliases. Treat the structural trace and weighted experiment as an exact finite test.

2. **Try to attach early pairings to original membership entries.** Check the topology of the published grouping on the original A gap ranks. The physical mechanism is a change of at most nine B selected edges for one real A rotation, and a full B splay that ends with monotone sides. If this suffices for the published group edits without point-gap numerical constraints, it permits actual group membership provenance on the original paired trees. Charge an original A rotation only when its edit creates a literal entry. Charge a paid B entry through its existing original A receipt. A membership can be used in at most one pairing per pass index within its group and split descendants. Each early entry with a proved funded origin therefore has bounded use. Confirm group edits and identity inheritance mathematically before any implementation.

3. **Attack regeneration through unpaid entries.** In the early part, a pairing may use two members that joined their respective current group through earlier unpaid pairings. Carry the ancestry identity through all such moves. A branch split inherits the old membership and pass count. A move into a growing group creates a new membership instance, with its earlier producer still in the account. The intended proof is a uniform bound on the squared load or a bounded-load positive fraction of the early rows, using their actual entry histories. The decisive audit is whether age-based decay survives a change of group without minting fresh supply. Test the concrete claim that the amount of work reachable through purely unpaid re-entries is forced to decay by a constant fraction per sustained round. A grouping argument must verify that decay from original A/B dynamics. Static identity overlap, creation of a new group name, and the fact that a component eventually shrinks do not establish it by themselves.

A repeated history with $A,Q_B,\Omega_5$ all growing proportionally is a seam and eligibility test. It may refute a graph that folds chronological occurrences together, but it does not pressure the absolute cost ratio. A parameterized family that makes the exact minimum energy per early event unbounded refutes its frozen eligibility rule. That need not refute other eligibility rules or Universal Relaxed Coarse-Double. A finite coverage percentage is not an acceptance result. Current working target is the support-independent estimate for $E_{\tau,r}$, with any finite coefficient.

## Conditional route to Dynamic Optimality

The link in the attachment is conditional on the universal original inequality for all admissible paired-closed sources. For arbitrary fixed-key sequences $X$ and a subsequence $Y$, start both trees at the same $T$ and mark the removed requests DELETE. Complete the source by first restoring B to $T$ with shared KEEP accesses. [Levy–Tarjan, Theorem 3.4](https://arxiv.org/html/1907.06310v3#S3) supplies an $O(n)$-cost splay transformation for all $n\ge4$, in particular at most $O(n)$ restoration requests. A may pay $O(n^2)$ on that shared restoration. Then use A-only DELETE splays to restore A to $T$, at $O(n)$ cost. No physical keys are removed. The pair is exactly closed and starts on the diagonal. For $n<4$ every search path has bounded length, which gives the requisite constant-cost comparison directly.

If $Q_B\le C A$ holds on these closed histories, the actual B rotations of $Y$ are at most the full-period $2Q_B+Z_B\le(2C+1)A$. A full-period cost is at most the rotations on $X$ plus $O(n^2)$. Including the access count $|Y|\le |X|$ gives eventual monotonicity in the exact search-path cost of Levy–Tarjan. Their [Theorem 4.3](https://arxiv.org/html/1907.06310v3#S4) converts that to Dynamic Optimality for Splay. The root inequality above remains the missing premise.

## Execution ledger

The proof and test conditions above were fixed before starting this round. The first execution is recorded below. Prior sources, seals, and root acceptance records are read-only for this round.

### First execution result. Receipt overlap across the cyclic seam

The existing independent checker passed the 686-operation source and its 1,372-operation repetition. The single period has $(A,Q_B,P_5,\Omega_5)=(989,519,517,2)$. The two-lap period has $(1978,1038,1034,4)$, the same greatest seam balances, and a paid-receipt load at most 10 per original A unit in both replays. The two-lap dry IDs are B(99,14), B(99,15), B(785,14), and B(785,15). All subsequent operations, including restoration, are replayed.

The following table lists the seven distinct base-period donor A units for the same-splay eligibility of B(99,14) and B(99,15). An offset is relative to the original 686-operation lap. Each listed unit supplies its first real rotation as a coordinate.

| Original A unit | Offsets appearing among the 14 paid receipts | Number of receipts |
| --- | --- | ---: |
| A(95,1) | 0 | 5 |
| A(101,3) | −1 | 2 |
| A(383,1) | −2 | 1 |
| A(72,4) | −1 | 1 |
| A(363,1) | −2, −1 | 3 |
| A(377,1) | −1 | 1 |
| A(72,3) | 0 | 1 |

For two laps each KEEP's support has eight chronological coordinates. The two supports intersect at A(363,1) and A(1049,1). The union has 14 chronological coordinates. Give each row weight $1/7$ on each of its six exclusive coordinates and $1/14$ on each of its two shared coordinates. Every coordinate receives total load $2/7$, attaining the Cauchy--Schwarz lower bound $16/14=8/7$. The last-drain-only rule would instead put two units each on A(1049,1) and A(363,1), giving energy 8.

There is a general check for these periodic eligibility experiments. If a graph on one period is lifted to chronological copies by assigning each edge its actual permissible winding offsets, symmetrizing any feasible allocation by simultaneous shifts of all demand and resource laps preserves supports and does not increase energy. Equivalently, averaging loads over the laps gives the lower bound $F_{\rm opt}(W^r)\ge r F_{\rm opt}(W)$. Conversely, choose one admissible winding for each used base edge and lift an optimal base allocation in all translated copies. Each resource type's load is then identical in all the laps, giving the reverse inequality. This argument applies to graphs whose lifted supports are exact.

For the frozen same-splay graph the FIFO receipt wiring has this lift property. The bank balances and prioritized queues of slots repeat. Walking backward from a paid debit along the slot wiring to its issuance is independent of where the cyclic trace is cut. Only the printed operation ID and offset change. The genuine-KEEP voucher also keeps its cyclic incoming A-gap source. Hence on this witness the optimum for all $r$ copies is $4r/7$, with normalized energy $2/7$. Folding the lap IDs together would instead give the spurious energy $4r^2/7$. The two replays checked here are finite exact controls. The lift proof determines their extension for this frozen eligibility graph.

### Original-tree group edits for the count argument

The published boundary and late estimates can also be applied to a separate bookkeeping trace built directly on the original A gap ranks above. This step uses the grouping for structural counts only. Its numerical contracted-point-gap proof has no role. The published normal-form construction remains a valid baseline, and the two group event classifications need not coincide.

Use the ternary value-and-gap tree above. At each heavy path, record the light-child paths separately on its left and right, ordered top down by their attachment on that path. At a tie on one side, read the outer child subtree before the value nearer the path head. In each side list, partition the memberships into ordered intervals. Each membership carries its entry identity and the physical parent node and slot of its light edge. A growing group can receive members only at the front. It converts to shrinking before its first pass or when the relevant path is transferred. A split partitions the memberships and inherits the pass count. A prefix transfer keeps the group identity. Losing a pairing removes the membership and inserts its leaf into a growing group of the winner as a new entry, keeping the old pairing as its actual producer. An exchange replaces the old entry by a new entry. These are the topological operations of [Chmel et al., Sections 5.2.4 and 5.4.2–5.4.3](https://arxiv.org/html/2607.18498v1#S5.SS2).

The edits needed during A can be made at individual changed outgoing heavy edges while physical B stays fixed. Each such junction cuts the upper prefix of the old heavy path and attaches it to the formerly light new continuation. Only the light attachments at the junction can change side or disappear. Every light child attached above the junction has its whole interval outside the junction subtree. Its side relative to the old and new endpoint is therefore the same. Light children below the junction on either unchanged continuation keep their old order. Split the two old side lists where the prefix ends, transfer the prefix groups, and handle the bounded local attachments at the junction. At the old upper light connection, isolate the exchanged entry before replacing it. This follows the topology of Lemma 11. It creates or replaces at most a constant number of entries and groups. The transferred prefix does not enter the middle of an existing group. Applying the at most nine selector changes one at a time accounts for an original A rotation at constant structural cost. Intermediate selectors are only path bookkeeping. The rank update with identical selectors needs no new entry for this count argument.

In B's genuine KEEP phase the old root heavy path leads to the actual target value. The two members at its bottom are the adjacent-gap minima of the target's old left and right subtrees. Isolate those two entries and convert the growing groups of the target and these two side heads. For each same-side double, the old grandparent and parent contribute four light children on one side. The retired grandparent's value and its two final hanging subtrees give the ordered triple for pairing. Pair its unique minimum with the other two, in adjacency order after each loser is removed. The value of the old parent is skipped. Different doubles in one KEEP have disjoint triplets because they use disjoint old path nodes and their associated off-path attachments. The two batches of pairs are matchings. Opposite-side doubles and the terminal zig remove path vertices into the two monotone side paths. The remaining groups are transferred in their existing order to the two adjacent-gap paths above their old memberships. In the original A gap ranks these side heads are the actual side minima. There is no finishing correction of the selected edges at that KEEP. This is the topological content of Lemmas 16, 18 and 19 applied to the original B events. A pair-generated entry cannot participate in another pairing in that same original splay. Within a triple only the surviving winner pairs twice and the first loser has left.

After a group's first splay, its surviving attachments are on a monotone part of one of the side paths. The operations above can cut such a group, remove its members, or attach the whole group as part of a prefix elsewhere. They add no attachment in the interior of the retained group. A singleton exchange is tracked separately. Thus the proof of unbrokenness in Lemma 20 and the counting proof of Lemma 21 apply without a numeric point gap. The first splay contributes at most two exempt batches, with any constant change of pass-index convention allowed in the cutoff below. Each later nonempty batch removes a fixed fraction of its group's members. For example, the published $(|G|-6)/4$ bound in each batch gives a fixed fraction for large groups, and one pairing suffices for the bounded small sizes. This verifies the structural hypotheses used for boundary and late counts on this original-tree trace. It does not transfer the paper's rank-dependent charging estimates to original A.

Initially there are $O(n)$ entries and groups. In every later edit, original A rotations, and the bounded non-pairing edits per genuine B KEEP, create $O(rA)$ additional entries. The latter may be associated to actual A work through the disjoint incoming KEEP gaps if needed. For fixed cutoff $\tau$, an entry participates in at most $\tau$ early internal pairings across the split descendants of its group. In a particular pass it is in one group and matched once at most, and a split inherits its age. This upper bound applies before the entry leaves its group. A subsequent re-entry is a different chronological entry with its own actual producer.

### Narrower early recurrence estimate

Here is what can already be eliminated from the native early count.

- An early unpaid pairing with a member inserted by an original A edit, a bounded non-pairing KEEP edit, or a paid original double can be charged to that member's entry. Initialization can be counted once at $O(n)$. Each real A rotation produces only a bounded number of such entries in the structural edits. The bounded KEEP edits use at most $O(K_B)$. Each paid double produces at most two pairing insertions, and its frozen receipt is tied to an actual A unit with the existing load bound 45. The at-most-$\tau$ uses per entry give $O_\tau(rA+n)$ for all these early pairings, counted once.
- An early unpaid pairing incident to a membership produced by a boundary or late pairing is at most one of $\tau$ later early uses of that pairing's one new membership.

For the second count, choose the absolute age threshold $\tau$ so large that
$$
2(\tau+1)(1-\gamma)^{\tau-a}\le\tfrac14 ,
$$
where $a$ is a fixed upper bound on the exempt pass count. Exponential decay makes such a fixed choice possible. Choose a fixed large-interval threshold $b\ge6+64(\tau+1)$. The proof of the earlier boundary estimate with threshold $b$ gives at most $8I_r/(b-6)+O_b(rA+n)$ boundary pairings. The late count is at most $(1-\gamma)^{\tau-a}(2rS+O(rA+n))$. Including their at-most-$\tau$ early successors, the combined count is at most $\tfrac12 rS+O_{\tau,b}(rA+n)$.

Let $E^\circ_{\tau,r}$ count native early internal unpaid pairings for which **both current membership entries were generated by earlier native early internal unpaid pairings**. The partition above yields
$$
2rU\le E^\circ_{\tau,r}+\tfrac12 rS+O(rA+n).
$$
The constants are absolute because the thresholds have been fixed. This reduces the root estimate to the genuinely recurrent part of the early count. Since $S\le45A+U$, an absolute bound $E^\circ_{\tau,r}\le C(rA+n)$ gives the required universal $K$ after division by $r$ and the limit. No uniform estimate for $E^\circ_{\tau,r}$ follows from the fact that every individual shrinking group decays. A move to another growing group starts a new age, and many distinct membership instances can have common ancestors.

### Real A eligibility for a reused B-born membership

A B-generated membership in the native construction has a physical A contributor even when its producer was unpaid. Fix such an entry at birth in a real same-side double at target $x$. Let $g$ be the retired grandparent, $p$ the old parent of $x$, and $J$ the new physical subtree interval at $g$. In right-right, $p<x$ and $\max J<p$. For left-left the inequalities reflect. Let $v$ be the real A key determining the winner of the triple, namely the shallowest key of $J$ enlarged by its immediate boundary neighbors. Even if the winner is a gap leaf, its representative $v$ is a genuine original key. The enlarged interval excludes $x$. The entire $J$ lies in the proper post-A interval $I_A(v)$.

At the end of that splay each of its two inserted memberships is attached at a light edge of $g$. While subsequent B KEEPs avoid $J$, that physical subtree and its interior edges are intact. A transfer of a retained group keeps its attachment, and a replacement arising at an A junction is a new entry with a separate A origin. Thus a later pairing using the old *retained* entry cannot occur before the first KEEP inside $J$. If any such later use occurs, there is a first hit inside $J$ on the lifted chronology. When A has processed that hit, its root lies inside the original $I_A(v)$. If no A rotation since birth had used $v$ as a pivot, the proper subtree interval $I_A(v)$ would be unchanged. A proper subtree cannot contain the A root. Therefore the first real A rotation after birth with pivot $v$ exists before or in the A phase of the first hit, and it precedes the entry's later use. This gives a literal eligible original A rotation. It may lie across the cyclic seam, in which case its actual chronological ID is used.

For a fixed candidate rotation $\rho$, a useful exact constraint on its load source is that it has only two possible representative pivots. In any one B splay the retired-grandparent intervals of the same-side doubles are disjoint. The sets can be read directly from the old path's disjoint off-path components plus the corresponding $g$. Enlarging each by one key on each side allows at most three of them to contain any fixed representative key $v$. Thus at most six new memberships from a single KEEP can use a given representative $v$, with at most $\tau$ early uses per retained membership. A fixed $\rho$ can still receive entries from many different earlier KEEPs during those pivots' preceding lifetimes. The per-splay and per-entry bounds do not control that global overlap.

### Read-only physical check of two unpaid births

The pinned 257-key witness has both dry doubles in the same KEEP to key 226. The following data are obtained directly from the original post-A tree, RR rotation records, and later first-hits.

| Original dry double | Retired interval $J$ | Three competing leaves in the new grandparent subtree | Winning group and arrivals | First later real A pivot of the winner's representative | First later B KEEP inside $J$ |
| --- | --- | --- | --- | --- | --- |
| B(99,14) | $[135,138]$, root 138 | value 137, value 138, gap 138 | gap 138, represented by key 139. Both losers enter its left growing group. | A(296,2), first rotation, promoting 139 over 207 | KEEP 135 at operation 308. All three B doubles in that access are paid. |
| B(99,15) | $[1,133]$, root 118 | value 111, value 118, value 122 | value 122. Both losers enter its left growing group. | A(101,2), first rotation, demoting 122 under 209 | KEEP 110 at operation 104. Both B doubles in that access are paid. |

For B(99,14), the minimum of the enlarged retired interval $[134,139]$ is 139, of depth 5 in A. Its gap rank is 5.5. The other two candidates have ranks 7 and 8. In B(99,15), the larger hanger on the right within the retired 118 subtree contains 122, of A depth 2. The left hanger supplies 111, of depth 3, and 118 has depth 8. The label on either losing leaf is retained as it joins the corresponding growing group.

This rejects the simple eligibility premise that an original unpaid same-side double can introduce only one member into a growing group. Both witnesses introduce two into one side of the same group. The first-hit calculations demonstrate where their later A rotation is found. They do not certify that either first-hit splay consumes both of those entries as a dry early pair, or that the full native group count on this witness has any particular $E^\circ_{\tau,r}$ value. The two birth calculations concern physical events independently of whether their generating pairings are classified as early or boundary.

### Remaining proof and preserved state

The first iteration established exact lift behavior of the physical eligibility graph and provided a genuine A coordinate for each retained reused B-born membership in the native group analysis. A natural frozen graph for the next bound adds the two participants' first real representative pivots to the same-splay paid coordinates of an $E^\circ$ demand. All of these coordinates have explicit source witnesses. The remaining quantitative task is to bound the squared load or a fixed-fraction capacity cut on that graph. In particular, one A rotation can close many earlier memberships at once, even though they originated at distinct timestamps. The argument does not yet prove the required global bound or a uniform decay of all recursive unpaid re-entries.

More explicitly, use $N^\circ(e)=N_{\rm KEEP}(e)\cup\{\rho_1(e),\rho_2(e)\}$ for an $E^\circ$ pairing, with each $\rho_i$ the first representative pivot of that member's own birth. Merge duplicate coordinates but retain each support witness separately. The exact target for this graph is the dual bound in the quadratic section with $M=E^\circ_{\tau,r}$, allowing a separately proved $O(n)$ initial boundary term. A capacity test can instead use the condition $|D|-b_0|N^\circ(D)|\le(1-\sigma)M$ for every demand subset $D$, for fixed capacity $b_0$ and fixed fraction $\sigma>0$. This is exactly the max-flow condition for a bounded-load $\sigma$ fraction. It states the quantitative obligation for this graph. The lifetime proof establishes eligibility, and the next missing implication is a global restriction on shared supports.

The study uses read-only calls to the existing GSO evaluator and independent verifier. No new GSO code, source, acceptance certificate, or finite coverage claim was introduced. The 48-file checkpoint seal and all 5,544 pinned prior paths passed byte verification. The tracked checkout still matches commit `a3edf4f6`.

## Second execution. Two renewed entries and directional restoration

### Exact exclusion on the 257-key source

The independent GSO verifier replayed the reaching state, both full labeled trees, every original rotation and the greatest cyclic bank seam of the preserved source. It returned $A=989$, $Q_B=519$, $P_5=517$ and $\Omega_5=2$ on 686 operations. Its two unpaid doubles are both RR at KEEP 226, with IDs B(99,14) and B(99,15). There are 344 same-side doubles and 688 associated pairings in one period. [Complete original source](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/run_003/complete_00.json.gz).

For a necessary condition on a current entry, keep the last B pairing in which its exact augmented leaf lost. Splits and transfers retain its identity. Losing replaces the entry. A-side exchanges and non-pairing B insertions can also replace it. Ignoring the latter replacements can only retain extra possible unpaid origins. Therefore an input whose last B loss is paid cannot have a current entry born in an unpaid pairing. This exclusion uses literal leaves and original costs independently of the pass cutoff and the internal/boundary classification. In an RR double the three inputs are the minima of the pre-double grandparent and parent left hangers and the value of the grandparent itself. Include the corresponding gap at any empty hanger and reflect the rule for LL. Compare their post-A ranks, then replay the first and second pairing in adjacency order.

| Unpaid pairing, in B step order | Inputs in winner, loser order | Last B loss of winner's leaf | Last B loss of loser's leaf |
| --- | --- | --- | --- |
| B(99,14), first | gap 138, value 138 | B(73,3), second, paid | B(75,2), first, paid |
| B(99,14), second | gap 138, value 137 | B(73,3), second, paid | B(75,2), second, paid |
| B(99,15), first | value 122, value 118 | B(60,3), first, paid | B(89,7), first, paid |
| B(99,15), second | value 122, value 111 | B(60,3), first, paid | B(89,7), second, paid |

The last-loss predecessors are read in chronological order, with the preceding lap available. Every listed predecessor in the table actually lies in the consuming lap. The two-lap replay also follows the four outgoing leaves until their next B loss. Their next losses are B(308,1) first and second for values 138 and 137, B(104,1) first for value 118, and B(40,35) first of the next lap for value 111. All four losses are paid. These are leaf-label traces. The A-junction check below gives the earlier end of each original birth membership. The raw necessary condition already proves $E^\circ_{\tau,r}=0$ on the pinned source for every cutoff and lap count. The search for a pairing with two unpaid-born inputs remains open.

### Exact geometry when one A rotation is shared

Let an original same-side B double retire the grandparent $g$ into its new physical subtree $J$, with $p$ the old B parent of the target. In RR, $g$ is now the left child of $p$. Hence $p$ is the immediate successor of $\max J$ in physical rank. In LL it is the immediate predecessor of $\min J$. If $w$ is the winner leaf and $v$ its real A representative, the enlarged interval of $J$ includes $p$. It lies inside the proper A subtree interval $I=I_A(v)$ as in the previous eligibility proof. Both $g$ and $p$ are in $I$. The target is outside $I$.

Until the first later actual A rotation $\rho$ using $v$ as a pivot, the proper interval $I$ stays fixed. Any B KEEP in that open time interval has its target outside $I$, since A must put that KEEP target at the root before B runs. A splay with target outside a physical B subtree leaves that subtree intact as a labeled rooted tree. Its pivots lie on the access path, which cannot reach the subtree. A whole subtree can move as a hanging child. Thus every producer retirement selecting the same $\rho$ remains intact just before $\rho$, even if earlier B KEEPs moved its attachment in the surrounding tree.

For fixed $(\rho,v,w)$, these retired roots are distinct ancestors of the one augmented leaf $w$ in that snapshot. A second retirement at the same $g$ would require a KEEP inside its still protected subtree. All the birth intervals for that triple of coordinates are strictly nested in birth order. A later retired root on the common path cannot be inside the earlier protected subtree, since its target was outside $I$. The growing interval can therefore acquire a long chain only across distinct producing KEEPs. A real rotation has at most two pivots, and each pivot can represent its own value and the two adjacent gaps. There are at most six such ancestry chains per $\rho$. This bound controls their number. The lengths and the reuse of one KEEP across different chains are still unbounded by this argument.

There is also a nesting restriction that does not require coincident donation times. Every internal pairing uses entries descended from one growing group. Groups split only after conversion to shrinking, transfers preserve whole groups, and groups do not merge. The original growing owner $w$ and side are therefore the same for both unpaid-born inputs. If the producer intervals differ, the earlier one is physically intact through the later insertion into that growing group. Indeed, before the first B KEEP inside the earlier interval, its saved $g$-to-$w$ path is internally unchanged in B. The first A selector change on that path has old endpoint $w$ and converts its growing groups. If there is no such change, a first KEEP inside that subtree must end its post-A selected path at the same leaf $w$. This is possible only when the target is the value at $w$, and that genuine KEEP converts $w$'s growing groups before doing its pairings. Hence an earlier inside hit would end the common growth epoch. At the later insertion both retired subtrees contain $w$, and the later retired root lies outside the earlier protected interval. This gives strict containment in birth order. Two entries from the same double can share a single retired interval. [The underlying group operations](https://arxiv.org/html/2607.18498v1#S5.SS2).

### Fixed-interval restoration on complete original periods

For a fixed physical interval $I$, retain the earlier definition

$$
S_I(B)=\{g\in I:I_B(g)\not\subseteq I\}.
$$

A whole B splay of a target outside $I$ adds no member to $S_I$. In a splay to $x\in I$, at most two keys can newly join $S_I$. One is $x$. A non-target key can gain subtree keys only if it is promoted as the lower pivot $p$ of a same-side double over $g$. Both old pivot subtrees have the same physical key sets as immediately before that splay, since earlier steps rotate only below them. If $I_B(p)\subseteq I$ originally and $p$ ends with a subtree that leaves $I$, then the old $I_B(g)$ was already outside the containment condition. Along the original root-to-target path, the nodes whose subtree is contained in $I$ form a suffix. The edge $g$ to $p$ must cross into that suffix, so there is at most one such non-target $p$. All other non-target keys either keep or lose subtree keys.

Let $K_B(I)$ count genuine original B KEEPs in $I$ in one period. Each outside-target retirement with $g\in I$ and new $J\subseteq I$ removes $g$ from $S_I$. The before and after $S_I$ are equal at the period boundary. Therefore the number of these double occurrences in a period is at most $2K_B(I)$. This counts both directions, with arbitrary interleavings and no support-size factor for this fixed $I$. Any selected $E^\circ$ occurrence can be associated to the distinct birth of its losing entry, since that entry can lose only once. Each producing double inserts at most two entries. For a fixed birth interval $I$, at most $4K_B(I)$ such losing entries can be produced in a period. This last count concerns the actual original producing occurrences, independently of which analytic lap later uses each entry.

There is a directional account of where an old reach comes back. An RR retirement of this kind removes the reach of $g$ above $\max I$. Its old left endpoint stays in $I$ and its old right reach contained the exterior target. The first return to $S_I$ requires an original B KEEP inside $I$. The return of the original right reach can happen then or later. Whenever that right reach returns, the splay must target $g$ or promote $g$ as the lower pivot of an LL. In RR, the old lower pivot and grandparent have the same right endpoint, so a right-right promotion cannot restore right reach for the lower pivot. LL mirrors this statement for left reach. The inside-target conclusion applies while the old subtree of $g$ is contained in $I$. For a fixed key, direction and threshold, the next loss of reach requires an intervening return. The first return of a lost reach therefore exists before the same physical retirement in the next lap. Its original IDs and chronological offsets are observable. Recall that $\rho$ precedes any KEEP inside the unchanged $I$. The first KEEP inside $J$, which can end membership protection, may precede actual return of the old reach by many operations.

| Producer and protected interval $I$ | First representative pivot | First A selector change at the old grandparent | First KEEP inside $J$ | First B return of right reach beyond $I$ |
| --- | --- | --- | --- | --- |
| B(99,14), $[123,206]$ | A(296,2), rotation 1 | A(307,2), rotation 2, right to left at 138 | 308, key 135 | B(310,1), LL rotation 1 promoting 138 over 139, key 137 |
| B(99,15), $[1,224]$ | A(101,2), rotation 1 | A(103,3), rotation 2, right to left at 118 | 104, key 110 | B(285,1), LL rotation 1 promoting 118 over 134, key 112 |

The A selector changes occur before the first B hit of each retired subtree. The newly heavy slot loses its former light entry, and the remaining light entry is replaced by the A junction. This is the literal point at which the four old birth IDs stop being available, even if the same leaves later appear. Both directional returns are on paid original doubles. The second return occurs 181 operations after the first inside hit. These clocks distinguish representative eligibility, actual membership lifetime, and shape restoration.

### Complete-history stress and unresolved cut

Existing GSO source construction, cyclic bank evaluation and physical replay were used read-only. The following are separate sweeps and may share sources.

| Sweep | Distinct complete sources within the sweep | Sources with positive $\Omega_5$ | Sources passing the two unpaid last-loss necessary condition |
| --- | ---: | ---: | ---: |
| W257 single insertions and adjacent local changes | 642 | 623 | 0 |
| Repeated, shifted, reflected and mutated source words with counted restoration | 332 | 166 | 0 |
| Inactive-key padding in literal BST gaps | 286 | 32 | 0 |
| Archived H3Q, internal renewal and interleaved multiscale sources | 30 | 0 | 0 |

The strongest verified complete ratio in these runs was $\Omega_5/A=2/956$ with $Q_B=531$. It did not supply a two-renewal example. Small exact replay additionally checked the restoration predicate over all six-key BSTs, all targets and all contiguous intervals, for 16,632 transition–interval combinations. That transition check is a test of the independent rotation argument above. All source-specific claims use complete original periods and the frozen paid labels. The archived multiscale witnesses are fully funded under this bank.

The proof still needs a bound on the overlap of distinct historical intervals and donor chains **for the two-renewal demand set**. A fixed $I$ needs distinct inside restorations, with the capacity just proved. The same KEEP can restore reach for several different historical intervals. A single producing KEEP can also extend several donor chains. The argument has no bound on either combined multiplicity. The next test on the unchanged graph is whether a subset of $E^\circ$ demands whose two eligible pivots and same-KEEP paid receipts all lie in a small set of literal A rotations must leave a fixed positive share fundable at absolute load. Keep the physical restore IDs as evidence about that cut, with no additional donor coordinates. No universal bound on $E^\circ_{\tau,r}$ or $\Omega_5$ follows from this checkpoint.

## Step 2. Exact shared-donor obstructions

The complete family below has unbounded unpaid B work in one KEEP under the frozen $H=5$ policy. Its unpaid early internal pairings reuse two literal B-born entries, and the first representative pivot and current KEEP's paid receipts lie in an absolute number of original A rotation coordinates. The earlier input births in this family are paid. Thus the obstruction applies to a geometry-only relaxation of the shared-donor graph. The two-unpaid-birth graph and the root inequality are still open.

### Freeze the candidate being tested

For this obstruction only, test the assertion that a fixed positive fraction of the following demands admits constant load on the two first representative pivots and the consuming KEEP's paid receipts. A demand is a current early internal unpaid pairing whose two literal inputs were generated by earlier B pairings. The test allows any earlier pairing classification and either paid label at those earlier births. The original $E^\circ_{\tau,r}$ is the stricter class in which each birth itself is early, internal and unpaid. It keeps its original eligibility and accounting.

### A complete family with one congested A pivot

Take $m\ge5$, $q=5m-2$, $h=q+2=5m$ and $n=h+5q$. The physical ranks are $[1,n]$. Put

$$
p_j=j+2,\qquad x_j=n-4-5(j-1),\qquad 1\le j\le q.
$$

The internal interval is $I=[1,h]$. Write $C_k=[5k-4,5k]$ for its owner blocks, $1\le k\le m$. The disjoint exterior owner blocks are $E_j=[x_j,x_j+4]$, with $x_q=h+1$.

Use the following common starting tree $T$. Its root is $2$, its left child is $1$, and its right subtree is $T_1$. Construct $T_j$ from the end, with $T_{q+1}$ empty. Its root $p_j$ has empty left child and a right child at $x_j+4$. That right child's entire subtree is a left chain $x_j+4,x_j+3,x_j+2,x_j+1,x_j$, where $x_j$ has left subtree $T_{j+1}$ and empty right child. All omitted children are null.

First use original DELETE-tagged splays to move A alone from $T$ to the following tree. The exterior keys form the left vine from $n$ down to $x_q$. The left child of $x_q$ is the fixed root $3$ of $I$. At $3$ the left subtree is $1$ with right child $2$ and the right subtree is the right vine $4,\ldots,h$. B stays at $T$. The existing exact restoration primitive constructs this preparatory word. Then descend through every exterior key from $n$ to $x_q$, KEEP exactly $x_1,\ldots,x_q$, and DELETE at the other ranks. This entire A descent consists of adjacent zigs after the first root-identical operation. The internal subtree of $3$ stays fixed. A rotation in the exterior can include $3$ as a hanging-subtree root and cannot see other keys from $I$ in its physical footprint.

The next operation is KEEP $3$. Its A phase is one real zig promoting $3$ over $x_q$, with middle root $4$. Denote this actual rotation by $\rho$. After the KEEP, use DELETE-tagged splays to align A to the current B tree, then a common KEEP word to return to $T$. Use the exact restoration primitive for both words. Its actual macro paths have at most four vertices. In particular, every KEEP in the closing word has at most one B double. This completes both full labeled trees with all preparatory and restoring work counted. The reaching prefix is empty. The three transformation phases each have $O(n)$ A work, and the descent through the exterior plus KEEP $3$ has exactly $5q$ A units. [Existing restoration primitive](EXP04_UNIVERSAL_RESIDUAL_CONSERVATION/CONTINUATION_05_UNIVERSAL_RESTORATION_CLOSURE/coercion.py), [Levy–Tarjan, Theorem 3.4](https://arxiv.org/html/1907.06310v3#S3).

### Production and actual bank depletion

At producer KEEP $x_j$, the first two B doubles are LL on the four exterior spacer keys of $E_j$. They leave $T_{j+1}$ on the left of $x_j$. Next the RR double has old grandparent $g_j=j+1$, old parent $p_j=g_j+1$, and middle subtrees empty and $T_{j+1}$ in rotation order. The old grandparent retires into the complete left vine $J_j=[1,g_j]$, now the left child of $p_j$. The right child of $p_j$ is $T_{j+1}$. For $j=1$ the RR ends the splay. In later stages, $g_j$ was the preceding $p_{j-1}$, and before the RR it is the left child of the preceding root $x_{j-1}$. The final zig promotes $x_j$ over $x_{j-1}$, preserving its new left child $p_j$. This is the induction that gives the complete original B path at the next stage. After the last producer, the B path to $3$ is the consecutive left vine $x_q,h,h-1,\ldots,3$.

The KEEP refill covers all three B doubles in each producer splay. The first LL only uses $E_j$. The second uses $E_j$ and the internal block of $p_j$. Immediately after them the total in those two blocks is at most eight. Their initial total was at most ten and both doubles debited one. The final zig uses exterior blocks only.

Fix $2\le k<m$ and consider the two successive producer stages with $p_j=5k$ and $p_{j+1}=5k+1$. In the first main RR the frozen priority lists the target $E_j$, the block $C_{k+1}$ of middle2, and the external block $E_{j-1}$ before the old block $C_k$. The mass just before that RR is at most $8+5+5=18$. After the debit, at most two credits can be returned to $C_k$. Up to the next main RR, A cannot refill $C_k$, and the next two preliminary LL doubles do not touch it. The next RR has at most eight in its new target and $C_{k+1}$ together, at most five in the exterior predecessor block, and at most two in $C_k$. It pays one. Since $C_k$ is last, its resulting balance is zero. No subsequent producer scope reaches that block. This argument fixes all middle blocks $C_2,\ldots,C_{m-1}$ at zero without any assumption on the entrance seam.

At the last producer the RR has no middle2. Its target and last internal block have at most eight credits together before the RR, and the exterior predecessor contributes at most five. The paid debit and the priority of the two exterior blocks put at most two credits back in $C_m$. Thus after the A zig at KEEP $3$, the only eligible positive banks for its B phase are $C_1$ with at most five, $C_m$ with at most two, and $E_q$ with at most five. The old B path contains $q$ ancestors of $3$ and produces $\lfloor q/2\rfloor$ LL doubles. Every pre-final double sees only $I$ in its footprint. The exterior root $x_q$ first occurs in the last double, as old grandparent or as external parent of the old grandparent according to parity. The last double is paid by the fresh $E_q$. All earlier doubles consume at most seven units in total. Therefore the complete source satisfies

$$
P_5(\text{KEEP }3)\le 8,\qquad
\Omega_5(W)\ge \lfloor q/2\rfloor-8.
$$

All unpaid B doubles are at this one KEEP. Every other genuine KEEP has at most three B doubles. The source refutes an absolute per-KEEP bound on the frozen unpaid count. Its complete $A$ cost is $\Theta(q)$, including preparation and restoration.

### Literal membership origins and the cut

For the first retirement $J_1$, the shallowest A key of the enlarged interval is $3$ outside $J_1$. For $j\ge2$ the same representative is inside $J_j$ and its winner is the value leaf $3$. For $j\ge3$ both losing leaves of the original producer RR are the value $g_j$ and the right null gap after $g_j$. They join the same right growing group of $3$. The actual B subtree at each such $g_j$ stays intact, and all A rotations before $\rho$ avoid pivots in $I$. No such A rotation can change a selector with old or new endpoint the value $3$. The exterior B targets and their adjacent gaps cannot convert the growing group of the value $3$. Each new B enclosure extends this group from above.

At KEEP $3$, the A pivot preserves the selectors and all light attachments inside the selected $J_j$. The pivot pair $3,x_q$ cannot change a minimum on an enlarged $J_j$ that excludes $x_q$. The upper-prefix edits and the isolation of the target's adjacent gaps preserve the joint descendant of the growing group containing the value and right-gap labels at $g_j\ge4$. Any split at the adjacent target gap is at its bottom. Its first two pairing passes are early. All LL doubles except the last use old pivots $g,p$ from these protected roots, with $p=g-1$ and $4\le p<g<h$. Their three members are the gap after $p$, the value $g$, and the gap after $g$, all in this group. In the post-A tree the gap after $p$ has lowest rank of the three, from the right vine of A below the demoted $x_q$. The two losers are the original entries born at the earlier producer for $g$. The winner's own entry was born at the earlier producer for $p$. Thus both current pairings are internal, in the two initial passes, with literal earlier birth IDs. The last double, which can involve an unprotected boundary pivot, is paid.

In particular each unpaid double yields two rows in the relaxed test. Both inputs of each row have the same first representative pivot $\rho$. The unchanged receipt part of the eligibility graph supplies at most eight additional distinct chronological A rotations. These are one real first rotation per A unit of the existing paid receipts for this KEEP. For $r$ laps the complete relaxed demand set has $M_{\mathrm{relax}}=2r\Omega_5(W)$ and at most $9r$ available rotations. Receipt offsets still refer to actual earlier laps. For fixed capacity $b$ the funded fraction is at most

$$
\frac{9b}{2(\lfloor q/2\rfloor-8)}
$$

when the denominator is positive. Taking $q$ large and then repeating the exact source also defeats a fixed additive initialization term. This gives an unbounded Hall obstruction to the stated relaxed rule, even with all the same-KEEP receipts. Using the paid receipts of the **earlier births** pays the very same dry pairings. Each loses a different membership, at most two per earlier original RR, and those earlier RRs hold distinct paid slots. This spends at most $2\cdot45$ per original A unit for this account. The literal $E^\circ_{\tau,r}$ is empty on this family because all earlier inputs of its only dry doubles are paid births.

| Support $n$ | $q$ | Full $A$ | Full $Q_B$ | $\Omega_5$ | Distinct A rotations in relaxed support per lap |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 140 | 23 | 2968 | 464 | 3 | 4 |
| 290 | 48 | 6211 | 976 | 16 | 4 |
| 440 | 73 | 9468 | 1489 | 28 | 4 |
| 590 | 98 | 12711 | 2001 | 41 | 4 |

All four rows passed the independent original-event and frozen-bank checker. The 290-key source is saved with the entire word, 5,073 original operations, full bank rows, and the earlier producer receipts for the 32 unpaid pairings. The exact local cut is 32 rows on four rotations, requiring load at least eight. Using the earlier paid births instead gives 16 literal donor coordinates with load two each in this witness. The witness can be checked with the existing GSO verify command using its absolute path. [Full original witness](GSO_OMEGA5_SHARED_DONOR_CONTROL_20261123.json.gz).

### One restoring promotion can cross arbitrarily many actual historical thresholds

There is a separate exact obstruction to bounding the number of historical intervals cleared by one physical B restoration using containment alone. For $k\ge1$ take $n=2k+2$ and start both trees at the result of splaying $2$ in the full left vine. Its root is $2$, its left leaf is $1$, and its right child is $n-1$. The right subtree has the descending left chain $n-1,n-3,\ldots,3$, with the right leaf $p+1$ at each odd $p$ on that chain.

Apply DELETEs $1,\ldots,n$. A is now the left vine. Descend from $n$ through $3$, marking the even targets and the final $3$ as KEEP. B's KEEP of $p+1$ for odd $p$ starts with the RR that retires the same $g=2$ into $J=[1,p-1]$. The old lower parent is $p$. For the first stage it is the only double. For each later even KEEP the remaining LL above the RR places the new target at the root with left child $p$. Thus B has the same residual form with the next odd parent below $2$. A before each such B phase is the two-vine tree rooted at $p+1$. The true A representative for the enlarged $J$ is $p$, so the actual historical threshold is $[1,p]$. The recorded right reach decreases through all these $k$ overlapping intervals.

The KEEP of $3$ puts B's $3$ at the root with left child $2$, leaving the latter's subtree $[1,2]$ intact. Then KEEP $1$ performs LL with the first real rotation promoting $2$ over $3$. That one rotation returns the right reach of $2$ beyond every recorded threshold. Each return is the first such directional return after its actual original birth. A shared ascending KEEP scan $1,\ldots,n$ forms the full left vine in both trees, then KEEP $2$ returns the initial common pair. The counted source closes exactly with empty prefix. The 130-key case with $k=64$ passed GSO with $A=572$, $Q_B=192$ and $\Omega_5=0$. This construction shows unbounded multiplicity of the direction-specific restoration record even when every historical threshold is realized at a preceding physical retirement of the very same key. It is a geometry control with paid births.

### Remaining aggregate obligation

For the frozen $E^\circ$ graph, count one literal losing membership per demand. At any particular producing KEEP and first representative pivot $\rho$, at most twelve such births can come from the at most six chains. A single KEEP contributes at most one retirement per chain, with at most two entries per retirement. Thus a long single-donor chain takes many distinct producing KEEPs. The same producing KEEP can still contribute to many different first pivots.

The strict early condition supplies a further restriction on a crowded chain. Fix $(\rho,v,w)$ and count the literal prior births of the chosen losing entries in this chain. At each such birth $w$ was the winner, and its own input membership was in an early internal pairing. A single literal membership of $w$ can win at most $T=\tau+2$ such pairings, using the fixed pass bound. Thus a chain of $L$ chosen births requires at least $\lceil L/T\rceil$ different input memberships of the same $w$. Apart from the first, each such membership must have been renewed during the protected interval window, between a preceding counted winning use and its next winning use. The known bounded edits and the existing absorbed pairing classes can account for their own renewals.

Consider a remaining renewal in which $w$ lost an early internal unpaid pairing to $z$, then retained that new membership until its next counted winning use. Write $J_z$ for the retired B interval at that renewal. If $J_z$ were contained in the unchanged $I=I_A(v)$, an exterior KEEP could never reach it before $\rho$. Neither a pure transfer nor a group split moves its retained light entry out of the protected physical attachment. This contradicts the next winning use before $\rho$. Hence $J_z$ contains an exterior key. Its enlargement also contains $v$, since it contains the value or gap leaf $w$. An adjacent gap's representative cannot change while $v$ avoids all pivots. The shallowest A representative $v_z$ of the new enlargement is therefore a proper A ancestor of $v$. At renewal it has an actual subtree interval $I_z\supsetneq I$. The first subsequent pivot $\rho_z$ of $v_z$ occurs before the next counted winning use, by the same first-hit eligibility argument as before. Distinct such renewals along this one chain give distinct earlier rotations $\rho_z$, because their renewal-to-use windows are disjoint.

If the next counted producer pairing is itself in $E^\circ$, then $\rho_z$ is an original donor already on its frozen support, from the prior birth of its winner $w$. Thus, in a set of demands with all support trapped in a set of rotations, there is a definite next incidence to test. A large chain needs earlier pivots at strictly enclosing intervals, unless the preceding producer or renewal is accounted for by an existing absorbed class or escapes that set of rotations. The new incidence is ordered by strict containment and has distinct predecessor clocks within one chain. The missing implication is a source-uniform density bound across all those chains after the paid origins are absorbed. Distinctness within a chain permits several chains to share the same earlier enclosing pivot. Neither complete family above violates the original $E^\circ$ cut, and the global bound $\Omega_5\le KA$ remains open.

## Step 3. Distinct pivots are paid and equal pivots give single-leaf paths

### Global bounded load for distinct first representative pivots

Keep the original demand set $\mathcal E=E^\circ_{\tau,r}$ with its actual age, internality, and two unpaid prior births. Write $\mathcal E_{\ne}$ for the literal rows with $\rho_1\ne\rho_2$ and $\mathcal E_{=}$ for the complementary rows with $\rho_1=\rho_2$. Let $T=\tau+2$ be a safe bound on the number of early pass indices along any lineage. Each row is counted with its original double ID, pairing index and chronological lap.

Both input births of a row in $\mathcal E$ occurred in the same growing group lineage, with a common original owner leaf $w$ and side. Growing groups take insertions at the front. Conversion stops their insertions, split descendants cover disjoint consecutive portions of their member order, and transfers preserve the order. An exchange in a singleton cannot bring another birth into that same singleton lineage. Thus the order of the original joining times defines a permanent cut through a group's split descendants at any real timestamp. At most one live descendant can contain entries on both sides of such a cut. Its age inherits at a split and advances at each pass. An internal pass uses disjoint adjacent pairs. For each age at most one pairing crosses the cut. Across the early passes this gives at most $T$ crossing pairings in the entire original growing group. These properties use the original-tree group operations already proved above. [Growing, shrinking, and pass operations](https://arxiv.org/html/2607.18498v1#S5.SS2).

Now consider two birth times $s_1<s_2$ in one such group. The representative of $w$ is fixed until its first real A pivot after $s_1$. For a value leaf it is a fixed key. For a gap it is the shallowest of its adjacent real keys. A rotation changing the minimum of that two-key interval uses the old representative as a pivot. The one-neighbor exterior gaps are fixed as well. Consequently if the second birth were before the first representative pivot of the first birth, both births would have that same first pivot. In a row of $\mathcal E_{\ne}$ the earlier pivot $\rho$ therefore lies strictly between the birth times. It is already an eligible original rotation for that row. The same argument proves that for an equal-pivot row the two birth representatives are the same real key, even when $w$ is a gap.

Charge every $\mathcal E_{\ne}$ row to its earlier pivot. At one fixed $\rho,w$, and side, at most one growing group's insertion interval straddles the timestamp of $\rho$. There is only one growing group per owner and side at any time, and a transfer occurs after conversion. The cut argument bounds the charge for this group by $T$. A real rotation has two pivots, each of which can represent only its own value and up to two adjacent gaps. Including both sides gives at most $12T$ rows on any actual A rotation. Thus

$$
|\mathcal E_{\ne}|\le 12T\,rR_A\le 24T\,rA.
$$

This proof retains the frozen eligibility graph and applies to any original paired-closed period with arbitrary interleavings and actual repeated lap IDs. No receipt or reconstructed ancestry credit is needed for the distinct-pivot rows. Together with the earlier estimate it yields

$$
\frac32 rU\le M_=+C_1(rA+n),\qquad M_=|\mathcal E_=|,
$$

for an absolute constant $C_1$ incorporating the original reduction and the new distinct-pivot charge.

### Exact capacity form for the remaining equal-pivot rows

For each $e\in\mathcal E_=$ use its one common original rotation $\rho(e)$ and its consuming KEEP $t(e)$. Let $P_t$ be the number of literal paid double receipts in KEEP $t$. Use a graph with row $e$ adjacent to its rotation and its KEEP. With trial capacity $b$, give a rotation capacity $b$ and a KEEP capacity $bP_t$. This is an exact replacement for the receipt layer up to absolute load factors:

- A frozen original allocation at capacity $b$ can be copied into this graph. Every row allocated to $\rho(e)$ can keep it. Every receipt allocation for KEEP $t$ uses one of at most $P_t$ distinct rotation coordinates there, so their combined load is at most $bP_t$.
- An allocation in this graph can split at most $bP_t$ rows assigned to KEEP $t$ across its $P_t$ literal paid receipts, at load at most $b$ per receipt. The frozen provenance assigns each receipt one actual A unit and distinct issuance slot, with at most 45 slots per A unit. Move each slot's charges to that unit's first real rotation. This produces at most $45b$ load on that rotation from the receipt layer and at most $b$ additional from the common-pivot layer. A full A unit thus bears at most $47b$.

For a set $X$ of original rotation coordinates and a set $Y$ of consuming KEEPs put

$$
D(X,Y)=\{e\in\mathcal E_=:\rho(e)\in X,\ t(e)\in Y\},\qquad P(Y)=\sum_{t\in Y}P_t.
$$

The exact capacity deficiency is

$$
\max_{X,Y}\left\{|D(X,Y)|-b\bigl(|X|+P(Y)\bigr)\right\}.
$$

Indeed, under any fixed set of available resources the maximal violating row set contains all rows whose two resources belong to the set. Conversely the neighbors of any violating row subset give one of these resource tests. This is the finite maximum-flow cut identity on original clocks. An absolute bound by $(1-\sigma)M_=+C_0n$ for any fixed $\sigma>0$ suffices. The matched mass could then be at least $\sigma M_=-C_0n$ and at most $b(rR_A+rP_5)\le47b\,rA$. Combining the previous display with $\Omega_5\le2U+81A$ and then taking $r\to\infty$ closes $\Omega_5=O(A)$. The initial $O(n)$ is paid once. Total receipt capacity is over the actual paid slots and includes seam offsets.

### One-to-one dependence on a fixed losing leaf

The following describes all the remaining dependencies in a rectangle $D=D(X,Y)$. Let $\mathcal P$ be all early internal unpaid pairings, and put $F=|\mathcal P\setminus\mathcal E|$. For each $e\in D$, trace its losing membership to the precise earlier pairing $f(e)\in\mathcal P$ that inserted it. This map is injective, because a new membership from one pairing can be lost only once. The same analytical leaf is the loser of $f(e)$ and $e$.

Group the chosen birth pairings $f(e)$ by the common pivot $\rho(e)$, its actual representative $v(e)$ and their winning leaf $w(e)$. In any one such chain, the earliest literal input identity of $w$ at these births can win at most $T$ early pairings. There are at most six chains per $\rho$. Give the corresponding rows no incoming edge. Also give a row no edge when $f(e)\notin D$. There are at most $(M_=-|D|)+|\mathcal E_{\ne}|+F$ such rows, using the injectivity of the actual birth map.

In every other case let $f(e)\to e$ be an edge. The input identity of $w$ used by $f(e)$ belongs to a later lifetime within the fixed pre-$\rho(e)$ window. That identity was born when $w$ lost to a leaf $z$ in an earlier physical retirement. This birth occurred after an earlier winner use already in the chain. Because $f(e)$ occurs while the A subtree $I(e)=I_A(v(e))$ is fixed and proper, every intervening KEEP targets outside $I(e)$. Therefore the retired interval of the last birth of $w$ must extend outside $I(e)$, or the literal membership of $w$ could never enter $f(e)$. Its enlargement includes $v(e)$, the representative of the value or gap $w$ throughout this window. Its min representative $v_z$ is a strict A ancestor of $v(e)$ at birth. Since $f(e)\in\mathcal E_=$, the first pivot of $v_z$ is exactly the common pivot $\rho(f(e))$ and both inputs of $f(e)$ have the same representative. The associated actual A interval satisfies

$$
I(f(e))\supsetneq I(e).
$$

Each directed link carries the same literal losing leaf. Each row has at most one predecessor, and injectivity of $f(e)$ gives at most one successor. Strict interval containment rules out cycles even when an ancestry path crosses the periodic seam. Thus all rows of $D$ are partitioned into paths, with at most

$$
6T|X|+\bigl(M_=-|D|\bigr)+|\mathcal E_{\ne}|+F
$$

path starts. This is a one-to-one dependence across enclosing pivots. A renewal can support several early uses of its winner, yet every resulting edge here is mediated by its own distinct original producing pairing. That is why the start count does not multiply error rows by the reuse parameter $T$.

The beginning of each path is controlled by literal original rotations or one of the displayed discarded demands. Its length currently has only a support-dependent upper bound from strict containment. The required quantitative implication is a uniform bound on the total lengths at a large-capacity cut, or an equally strong source-level inequality. The same A pivot may still lie on paths belonging to different losing leaves. The new proof has not bounded that combined load.

### Complete control for the two different clocks

The 290-key Step 2 source can be altered to exercise an actual crossing pair. In the A preparation alone give $3$ a proper subtree ending at $h+2$. In that subtree let $3$ have right child $h+1$, with the unchanged interior vine $4,\ldots,h$ on its left and right child $h+2$. The exterior left vine down from $n$ stops at $h+3$, with left child $3$. The B preparation and all producer KEEPs remain as in Step 2.

Insert DELETE $h+2$ after producer 13. Its bottom A double is RR with first rotation promoting $h+1$ over $3$. This makes the proper subtree of $3$ end at $h$ and leaves every B retired interval and its light attachments fixed. At the current B parent of the protected chain, both the old A root and the new DELETE target lie in the augmented interval on the exterior side. The selected continuation there can change within that exterior side. The value $3$ keeps its separate growing group. No A pivot during this insertion changes a minimum of an enlarged retired interval, and the two protected entries survive. Continue the original descending exterior word, then KEEP $3$ and the exact counted restoration. The second actual rotation involving $3$ since producer 13 is its final A zig. The work and all credits of the additional original DELETE are included.

In the replay B(1782,6) is an unpaid LL double with old grandparent 15 and old parent 14. Both of its pairings use the gap after 14, whose literal birth is B(1605,3), and the two losing entries were born at B(1611,3). The two distinct first pivots are A(1606,1), rotation 1, and A(1782,1), rotation 1. Both earlier births are paid. Therefore this is a structural positive control for the crossing proof. The independent verifier checked the full pair closure, 5,078 original operations, $A=6393$, $Q_B=976$ and $\Omega_5=16$. [Complete original crossing control](GSO_OMEGA5_SPLIT_PIVOT_CONTROL_20261123.json.gz).

## Step 4. Stable A snapshots and shared-pivot overlap

Use exactly the equal-pivot rows, actual growth identities, and paths of Step 3. The new bounds concern the real A pivots already present on those paths. All operations run on the full original trees.

### All later intervals of one path coexist in an earlier A tree

For a representative key $v$ due to be touched in A operation $k$, consider the operation boundaries after its previous touching operation and strictly before $k$. Use the initial boundary if this is the first touch in the lifted history. When the physical subtree at $v$ is proper during this window, its full labeled shape is fixed. A full A splay toward a key inside it must pivot $v$ somewhere in that operation, because $v$ is on the search path. A splay toward an exterior key can move the whole subtree of $v$ as a hanging child. It cannot change its internal shape. This statement uses boundaries of full original operations. In the releasing operation, earlier rotations inside the subtree can precede the first bit pivoting $v$. Those earlier rotations still preserve the subtree key set at $v$.

If two such windows overlap while one subtree is strictly inside the other, the outer subtree and its entire interior stay fixed throughout its window. The inner window therefore contains the whole outer window. A first release of the inner subtree in a strictly earlier A operation than the outer release is impossible. Both releases can occur in one A operation in this general observation.

On a path link $f\to e$ of Step 3, the two proper subtrees actually coexist at the earlier birth of the winner's membership used by $f$. The rectangle reduction proves $I(e)\subsetneq I(f)$ there, with the representative of $e$ an actual descendant of the representative of $f$. Therefore the window for $I(e)$ includes the whole window for $I(f)$. Its release is in a strictly later operation, since $f$ executes in B after $\rho(f)$, whereas $\rho(e)$ is after that B birth. By induction every later path interval is an actual proper subtree in the same A snapshot taken at any boundary in the first window. Its real representative already sits in the corresponding descendant position. The path uses a chain of ancestors of its losing leaf in that snapshot. A gap leaf may be located using either adjacent real key inside its enlarged birth interval. This is a label for the argument, with no A credit attached to it.

Two paths that branch into disjoint physical intervals cannot share a later rotation. Subsequent intervals on each path are subsets of the respective disjoint intervals. The two possibilities for the old subtree sets of one later real rotation are nested, since its pivots are parent and child. This implication holds for distinct historical starts and actual lap offsets.

### A fixed rank point sees at most a constant number of links from one pivot

Fix a real pivot $\alpha$, one of its possible birth representatives $u$, an original growing owner leaf $z$ represented by $u$, and a side. Relevant births with this first pivot lie in the same window of the proper A subtree $I_u$. Every B KEEP in that window targets outside $I_u$.

A B subtree with selected minimum $z$ must have its enlarged key interval entirely inside $I_u$. If it included an exterior key, the enlargement also contains $u$, and the minimum of the contiguous A key interval is an ancestor of $u$ and that exterior key. It would be strictly above $u$. This contradicts the selected minimum. In particular every light attachment on the heavy path with endpoint $z$ has its own enlarged range inside $I_u$. Original A ranks inside this stable proper subtree shift only by a common depth offset during outside operations. The selected directions there stay fixed. An exterior A junction may change the entry for $z$ in its parent group. The groups of $z$'s own light children stay intact. Exterior B targets avoid the old subtrees of these children. The B edits that convert the target's growing groups and those of its immediately adjacent gaps concern leaves represented by the exterior target. Thus all the joins to this fixed owner and side within the window use one growing group.

In one side group the order of the member leaves is monotone in symmetric rank order. At a higher attachment on the heavy path, the off-path range on that side lies beyond all lower attachments on the same side, and the two-slot tie uses the outer child first. Front insertion, conversion, split and transfer preserve the resulting membership order. Within one pass the internal pairs join adjacent surviving entries and have disjoint rank spans. The same holds across split descendants at one common pass index, which are disjoint consecutive portions of the old order. A rank point therefore lies in the span of at most one pairing in that group per pass. There are at most six possible owner leaves for the pivot $\alpha$ and two sides per leaf. A fixed physical rank point is consequently in the winner-to-loser span of at most $12T$ early equal-pivot rows at $\alpha$. The same bound applies when the rank point is an actual null-gap position. This uses the existing pass and age conventions. [Original grouping and split operations](https://arxiv.org/html/2607.18498v1#S5.SS2).

### Uniform two-pivot bound, including nested branches

For any two distinct actual A pivots $\alpha<\beta$ in the chronological lift, at most $54T$ paths of any equal-pivot rectangle $D(X,Y)$ visit both. To count them, let $f$ be the row at $\alpha$ on a given path. This row has one successor $e$ on a path that visits $\beta$, and its winner $w$ is the owner of the losing birth used by $e$. Its loser $\lambda$ is the fixed leaf followed by the whole path.

- If $e$ is already the row at $\beta$, leaf $w$ must be represented by one of the two physical pivots of $\beta$. There are at most six possibilities for the leaf. At $\alpha$ all rows with winner $w$ and first pivot $\alpha$ use one literal membership of $w$. It was born before $\alpha$ and is retained at least to its use after $\alpha$. Distinct memberships of a leaf cannot coexist at this clock. Its at-most-$T$ early winning uses give at most $6T$ such paths.
- Otherwise the representative of $w$ at $e$ is outside the later physical interval $J$ used by the path at $\beta$. The intervals strictly descend along the path, and at the next link the strict descendant subtree excludes the root of $I(e)$. The losing leaf $\lambda$ lies inside the ternary leaf interval of $J$. Since $w$ is outside or at a boundary gap of that interval, the span of the pairing $f$ meets at least one of its two boundary gaps. The fixed-rank-point bound gives at most $24T$ paths for this $J$. There are only two possible old physical intervals at the real rotation $\beta$, giving at most $48T$ in this case.

No path visits one chronological rotation twice, since releases increase through distinct original operations. In particular, if $L_p$ are the path lengths in the cut and $X$ is its rotation set, this proves

$$
\sum_p\binom{L_p}{2}\le54T\binom{|X|}{2}.
$$

This controls reuse at any two specified pivots. The bound applies also when two paths come from nested branches and later meet. It leaves the source-uniform sum $\sum_p L_p$ open.

### Why snapshot geometry and the two-pivot bound alone leave a gap

Here is an abstract implication test for the path constraints. Its paths are combinatorial objects, with no B events or unpaid labels asserted. Fix any number $s$ of stages. Define heights $h_s=0$ and $h_i=h_{i+1}+2^{h_{i+1}}$ for $i=s-1,\ldots,0$. Take a full ordered binary tree of height $h_0$ with $m=2^{h_0}$ leaves. The nodes are available rank intervals. Add $m$ private ancestor nodes as a chain above the tree, and start a distinct path for each leaf at its own private ancestor. Give ancestors earlier clocks than descendants and use a common left end for the time windows. This satisfies reverse nesting of the time windows.

In stage $i<s$, for the path of a leaf $\lambda$, take the ancestor at the following depth. Use depth $h_0-h_i$ plus the index of $\lambda$ among the $2^{h_{i+1}}$ leaves of its subtree rooted at depth $h_0-h_{i+1}$. The index starts at zero. This selected depth lies strictly before the next stage. Finish the path at its own leaf.

If two paths share a stage-$i$ node, their next-stage subtrees of height $h_{i+1}$ must be different. Otherwise their distinct leaf indices in that same subtree would put them at different stage-$i$ depths. Thus their later intervals are disjoint. In particular any two pivots share at most one path, and outgoing winner-to-loser spans from a common pivot lie in disjoint next-stage subtrees. There are at most $3m-1$ distinct vertices, with one start at each private ancestor and $m(s+2)$ path occurrences. Even with one formal KEEP of five receipts at each vertex, the ratio of occurrences to total vertex and receipt capacity before multiplication by $b$ grows with $s$.

The example satisfies the proved path stability, rank-span separation, and pairwise overlap properties. It exposes the missing global implication in an argument using those properties alone. In particular, repeatedly sharing the *same pair* of pivots is not necessary for high aggregate density in that abstract model. A valid closing argument for original sources still has to use constraints tying first meetings of numerous losing paths to their actual B production and restoration.

### Original controls and result

Both saved 290-key controls passed the independent original-event and cyclic-bank replays. On those complete words, a second read-only A audit compared the full rooted subtree shapes at every boundary without a pivot of their root. It checked 1,458,177 and 1,459,262 such subtree-boundary pairs, and 1,098,748 and 1,131,433 nested live-window comparisons at departure. This exercises the A window lemma with original costs and retained shapes.

The directed GSO adversary used the Step 2 cold preparation, then put a higher protected A interval under one fixed real representative while B performed additional exterior KEEPs and inside hits. The strongest independently replayed complete control has 770 keys, 10,123 original operations, $A=12005$, $Q_B=2541$ and $\Omega_5=97$. It uses $m=26$ in Step 2 and alters its prepared A right vine below $3$ as follows. Key $74$ has right child $110$. Key $110$ has left subtree $[75,109]$ rooted at $83$, with a left vine on $75,\ldots,82$ and a right vine on $84,\ldots,109$. Use KEEPs $4,6,7,9,17,82,83,74,110,83$ immediately after KEEP $3$. Restoration completes an ascending common KEEP sweep and returns the common left vine to the initial tree using the old primitive. Source digest is `1b9f01b2c50a08942b8f92de76b3f870a596aa792ee011bd8e50f447ab08adef`.

The first replay screen used the necessary two-unpaid-last-loss condition in the targeted phase of each tested history. The strongest control then passed a second, complete two-lap check including its entire original restoration. All 2,948 pairings in one period were traced in chronological order with the preceding lap available. Every unpaid pairing has at least one input with no earlier unpaid last B loss at its use. Therefore this particular complete control has empty $\mathcal E$, even under the relaxed membership persistence used in the last-loss test. The broader source-uniform status is unchanged by a finite negative trace.

Step 4 supplies a source-uniform bound on shared pivots in pairs of coordinates. The original equal-pivot capacity inequality still needs a source-uniform bound on total length. A proof focused solely on reunions of the same paths leaves open the first meetings of paths with different origins. Those meetings have to be tied to actual B birth KEEPs and their restoration over the original period. The verified Step 3 partition and all original paid interfaces continue to apply.

## Step 5. Occupied-bucket accounting

Fix the native grouping, the original unpaid labels, and the early cutoff from Steps 1–4. Work on $r$ copies of an arbitrary admissible exactly paired-closed source. Use $T=\tau+2$ as the established upper bound on the number of early pairings in which a literal entry can participate. Let $\mathcal L$ be the unpaid pairing occurrences outside $\mathcal P$, so these are the boundary and late ones. Let $\mathcal R=\mathcal P\setminus\mathcal E_=$ and write $L=|\mathcal L|$, $R=|\mathcal R|$. The three counts partition the two pairings of each original unpaid same-side double, giving

$$
2rU=L+R+M_=.
$$

The boundary and late budget including the early successors, together with the different-pivot bound, gives

$$
L+R\le \tfrac12rS+O(rA+n).
$$

There is also a separate bound $R\le TL+O(rA+n)$. Each row in $\mathcal P\setminus\mathcal E$ has a current input that was initialized, created by an A or non-pairing B edit, created by a paid double, or created by a row of $\mathcal L$. Charge the first three kinds to their established $O(rA+n)$ inventory of entries, each having at most $T$ early uses. One row of $\mathcal L$ creates one entry and can therefore account for at most $T$ early uses. The remaining rows in $\mathcal R$ are $\mathcal E_{\ne}$, already bounded by $24TrA$. It follows that

$$
R\le \frac{T}{2(T+1)}rS+O(rA+n).
\tag{5.1}
$$

This uses the fixed original cutoff and keeps the count of the omitted parent pairings in the same budget as their early successors.

### An exact potential on live memberships

Mark an entry if its literal birth was a pairing of $\mathcal P$ during the lifted trace. At that birth tag it with the first later real A rotation $\rho$ of its winner leaf's real representative. The physical paired orbit may be continued to obtain tags beyond the right end of the counted trace. For any birth, its retired subtree $J$ has to be hit by a B KEEP before the next copy of the birth step. Otherwise the full subtree at the old grandparent stays intact, and that grandparent cannot be on the original search path to the repeated exterior target. The A phase of the first hit must have reached inside the proper birth interval of the representative, so its first pivot occurs by then. Thus the tag exists even if a marked entry is never used again. It is at most one period beyond the birth. Use actual chronological rotation IDs throughout.

For each **current live group** $G$ and chronological tag $\rho$, write $k_{G,\rho}$ for the number of its live marked entries with that tag. Use

$$
\Phi=\sum_{G,\rho}(k_{G,\rho}-1)_+.
$$

Conversion and intact transfer preserve the terms. At a split, each tag's stock partitions and the sum of the resulting terms is at most the original term. An exchange discards its old marking and supplies a fresh unmarked entry. No A edit or non-pairing B edit creates a marked entry. All memberships present at initialization start unmarked.

At an $\mathcal E_=$ pairing the losing membership leaves a bucket containing its marked winning partner. The removal decreases $\Phi$ by exactly one. The new marked output enters the winner's growing group with the output's own future tag. It increases $\Phi$ by one exactly when that tag was already present in the recipient group. Call this a refill. Let $Z$ count the $\mathcal E_=$ pairings that do not refill. They each decrease $\Phi$ by one. Let $R_+$ count $\mathcal R$ pairings whose output is a refill, irrespective of their effect on their input groups. Each can raise $\Phi$ by at most one. An unmarked output cannot raise $\Phi$. These statements apply to sequential updates within each pass since only disjoint pairs run in parallel. Summing the changes gives

$$
0\le \Phi_{\mathrm{end}}\le R_+-Z,\qquad Z\le R_+\le R.
\tag{5.2}
$$

The analytic grouping needs no cyclic seam for this inequality. The initial potential is zero, and the actual chronology and unpaid labels come from exact closure of the original orbit.

### The companion output in the same KEEP

Say an $\mathcal E_=$ refill is within the current KEEP if every marked incumbent in the bucket was born in this KEEP. Otherwise it is across KEEPs. In a genuine KEEP the double triplets are disjoint and each winner occurs in at most one triplet. The recipient growing group is separate from the root's input group. The only other insertion into this recipient and tag during the KEEP can be the companion pairing of the same double. If no older KEEP occupies the bucket, that earlier insertion opened it. In particular it was counted in $Z$ if it was in $\mathcal E_=$, or in $R-R_+$ if it was in $\mathcal R$. One opener has at most one such companion. With $N_{\rm same}$ the number of within-KEEP refills, this proves

$$
N_{\rm same}\le Z+R-R_+,\qquad Z+N_{\rm same}\le 2R.
$$

In particular the previous refill target can be weakened to the across-KEEP count $N_\times$, with

$$
2rU\le N_\times+\tfrac32rS+O(rA+n).
$$

### Discounting older non-equal producers and the first literal winner

During a fixed tag's pending window, a recipient winner leaf $w$ has a fixed real representative $v$ and a fixed proper A subtree $I_A(v)$. For a shared tag, the constancy of $v$ follows from the Step 3 observation about the first pivot of an adjacent gap's representative. Every birth into the bucket is protected until that pivot. Its B retirement stays inside $I_A(v)$, and the post-A target of every intervening genuine KEEP is outside this interval. The argument of Step 4 gives one growing group per side of this $w$ throughout the births of the tag. The old marked entries at their protected light attachments survive in it. In particular the next insertion becomes the most recent marked output in that bucket and stays there until at least the tag. Later births with that same tag cannot occur after the tagged pivot.

For every $\mathcal E_=$ refill, take $h(e)$ to be the producer of its most recent live incumbent of the same tag. This map is injective over all the refills. One output can serve immediately before the next marked insertion into its bucket, and it cannot become the most recent output again during that tag's pending window. Different live buckets use distinct membership IDs. Define $N_{\times,\mathcal R}$ to count across-KEEP refills with $h(e)\in\mathcal R$. A within-KEEP refill has its opener in $Z$ or $\mathcal R$. The two domains are disjoint and both use the same injective map. Consequently

$$
N_{\rm same}+N_{\times,\mathcal R}\le Z+R.
\tag{5.3}
$$

Also record the literal input membership of the winner at the first marked insertion into each recipient bucket. At most $T$ early pairings into that bucket use that initial winner membership. A given tagged rotation has two real pivots, at most three representing leaves per pivot, and two sides per leaf. There are at most $12(r+1)R_A$ recipient buckets encountered by marked births in the trace, allowing one look-ahead period for their tags. The refills using the initial winner membership therefore number at most $12T(r+1)R_A\le48TrA$. This bounds occurrences using the number of tag IDs. It draws no bank credit from the reaching prefix or the look-ahead period.

Let $C_*(W,r)$ count precisely those $\mathcal E_=$ refills that meet all three conditions at their insertion.

1. The recipient bucket has a live marked incumbent born in a strictly earlier original KEEP.
2. Its most recent marked incumbent was produced by an $\mathcal E_=$ pairing.
3. The winning input uses a different literal membership from the winner's first marked insertion into this bucket.

The most recent incumbent in item 2 can be the companion from the current KEEP if an older KEEP also occupies the bucket. With those predicates the above deductions give

$$
M_=\le C_*+Z+(N_{\rm same}+N_{\times,\mathcal R})+48TrA
   \le C_*+3R+O(rA+n).
$$

Combining this with (5.1) and the original partition proves the source-uniform reduction

$$
\begin{aligned}
2rU
  &\le C_*+(L+R)+3R+O(rA+n)\\
  &\le C_*+(2-\delta)rS+O(rA+n),\qquad
      \delta=\frac{3}{2(T+1)},\\
\delta rU
  &\le C_*+O(rA+n),
\end{aligned}
\tag{5.4}
$$

where the last line uses $S\le45A+U$. Thus a bound $C_*(W,r)\le C_0(rA+n)+\eta rU$ with an absolute $C_0$ and any fixed $0\le\eta<\delta$ would close $\Omega_5=O(A)$. Divide by $r$ and take $r\to\infty$ with $W$ fixed, then use $\Omega_5\le2U+81A$ and the frozen $Q_B=P_5+\Omega_5,\ P_5\le45A$.

### Original renewal in the remaining class

For a row counted by $C_*$, its current winning membership was born later than its first marked output into the recipient bucket. There is one possible incoming membership of a leaf at a time. As the row is in $\mathcal E_=$, this particular later membership was born in an actual $\mathcal P$ pairing that the leaf lost. Denote that birth by $b$. Its physical B retirement interval $J_b$ must extend outside the recipient's fixed proper $I_A(v)$. Containment would leave the literal light attachment intact under all intervening outside-target KEEPs, so the current pairing could not use it. Its enlarged interval contains $v$ and an exterior key. The real A representative of $b$ is thus a strict ancestor of $v$ at that birth. Its first later pivot is the common input tag of the row. That pivot has occurred by the consuming KEEP, before the future tag of the recipient bucket.

This records the precise nested renewal and its chronological order. It bounds the early uses of one literal birth by $T$. The aggregate sharing of one enclosing pivot or one original KEEP that restores reach across different recipient buckets remains open.

### Complete-period controls for the remaining geometry

The read-only replay used the literal leaf labels and each leaf's latest B loss. It did not infer retention across A exchanges or infer group age and internality from that B loss. The independent checker replayed the 257-key source, both saved 290-key controls, and the 770-key Step 4 source through full restoration, including the greatest clipped cyclic seam. The two-lap screen then compared both input last losses, each output's real first A pivot, and earlier same-tag output births.

The 770-key source exposes a renewed winner with three actual unpaid predecessor events. In the following IDs the lap is suppressed because the listed events lie in the same chronological lap.

| Occurrence | Original leaf event | Status |
| --- | --- | --- |
| B(4737,41), second pairing | Gap after 84 wins over the gap after 85 | Unpaid |
| B(4738,20), second pairing | Value 83 wins over the gap after 84 | Unpaid |
| B(4739,10), first pairing | Value 83 wins over value 86 | Unpaid |
| B(4744,1), first pairing | Gap after 84 wins over value 86 | Paid |

The middle two historical births have the same later first A pivot, A(4743,1), rotation 1. Their output owner and side agree in the last-loss screen. The first and last rows enter the same output owner, side, and future pivot A(4831,1), rotation 1. Their original retired intervals are $[85,85]$ and $[85,89]$. At the last row, the genuine KEEP has reissued the target's five units. The independent bank record has starting stocks $(5,0)$ in its two footprint blocks. This is a physical control for renewal and older occupancy under the last-loss filters. The consuming paid double excludes it from $C_*$.

A padding test moved the consuming configuration deeper without making it dry. Insert 20 keys between old ranks 82 and 83, shift the larger ranks by 20, and put the new keys in a right vine rooted at the old null attachment at that gap in the diagonal tree. Replace KEEP 83 at operation 4744 by KEEP 102. The other original operations before the common KEEP sweep use their shifted targets. Append the ascending common KEEP sweep and the counted restoration from the common left vine to the augmented initial tree. The independent checker verified the resulting 790-key full source over 10,263 operations, with $A=12210$, $Q_B=2608$ and $\Omega_5=97$. Its source digest is bf6eee5f8c908da1997ea4f35995b583b9843dbecd279dbfda4536f27a870c67. At B(4744,11) the old grandparent and parent are now 106 and 104. The footprint stocks are $(4,0)$, after the ten deeper doubles and their physical pooled credit. Moving beyond the first five target debits does not force unpaid status for this geometry.

The source-uniform refill estimate for $C_*$ and the final universal bound remain open. Equation (5.4) keeps the original unpaid predicate and uses the established membership interface.

### Test of a direct charge to the A parent

A charge based on the representative's current physical A parent would need that parent to pivot between the B renewal and the first B reuse. Renewal geometry alone does not force that event. The [complete 257-key source](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/run_003/complete_00.json.gz) gives a check on the unchanged original replay. At B(174,3) the gap after 82 wins at retired interval $[82,82]$. At B(175,2) this gap and value 81 both lose to the gap after 74, entering the same side of its group. The new retired interval is $[75,82]$. B first enters that interval at KEEP 75, operation 248. At B(248,2) the gap after 82 again wins over value 81, now with retirement $[81,82]$. The two earlier births into the gap after 74 have first A pivot A(247,1), rotation 1. The two wins by the gap after 82 have the same next representative pivot A(250,2), rotation 1.

Throughout the renewal and reuse, the relevant A representative 83 has fixed subtree $[77,84]$ and physical parent 85. There are 167 real A rotations after the renewal through the reuse, none pivoting 85. The 72 intervening original KEEPs avoid $[75,82]$. Exact closure of both full trees and the paid labels passed independent replay. The three cited B doubles are paid. This refutes the parent-pivot premise for the physical renewal pattern alone and supplies no unpaid counterexample.

## Cycle-wide attempts after the parent-pivot failure

### Bounded signed recharge with local A holders

For each physical key $g$, choose an A subtree interval $H_g(A)$ that contains $g$. Use the mismatch count

$$
\Gamma(A,B)=\sum_g {\bf 1}\{I_B(g)\not\subseteq H_g(A)\}.
$$

Use either of two fixed holder rules. For rank radius $b$, take the A subtree at the minimum-depth key of the contiguous radius-$b$ window around $g$. For ancestor radius $d$, take the subtree at the $d$th A ancestor of $g$, stopping at the root. At each B phase the target is already A's root. A proper holder excludes this target. Every physical B rotation demotes a key on the target's path, removing an interval containing the target and giving the demoted key a smaller subtree. The promoted key's old and new subtrees both contain the target. The mismatch indicators are therefore nonincreasing throughout B. The full interval gives a constant zero indicator.

A real A rotation changes at most $2(2b+1)$ rank-window holders. A change of minimum in a fixed contiguous interval requires both real pivots in that interval. The only A subtree intervals at fixed roots that can change belong to the two pivots. For the ancestor rule, affected nodes are within $d+1$ edges of one of the two pivots in a pre- or post-rotation tree, so their number is bounded in terms of $d$ alone, for example by $2^{d+4}$. Summing over a complete period bounds the total B decrease by that constant times $R_A\le2A$. These counts follow individual keys through lost and regained ancestry. They do not count the same key once for every containing A interval.

For radius zero, neither B(99,14) nor B(99,15) in the original 257-key period decreases the count. The following full-source construction tests the stronger claim that any fixed finite set of rank and ancestor radii gives a decrease on every unpaid double.

Let $L\ge20$ be a multiple of five. In the original 257-key source insert $L$ ranks in each of the six gaps after keys $115,117,120,130,134,135$, and shift original keys accordingly. In the common diagonal tree attach each new subtree in its original null gap, rooted at the first inserted rank, with a balanced remainder. In B the old word only uses original keys until the optional restoration below. Each actual old-key rotation then carries any inserted subtree as a hanger. It neither pivots inside a new gap nor changes the old-key rotation order.

Cut at the boundary after original operation 31. In A the old keys 118 and 134 are singletons there in the old-key projection. Lift the inserted subtree after 117 into a right vine immediately above old key 118. Lift the inserted subtree after 134 into a left vine immediately above old key 134. Keep the old-key projection of A and all other gap attachments. The desired full A tree is reached with the established actual splay coercion primitive using DELETEs. B stays at the shifted original cut state. The reaching prefix is excluded. Use the original suffix followed by operations 1 through 31 as the measured body. An optional counted common KEEP sweep over the whole augmented support followed by a common KEEP coercion restores B to the cut state and makes every inserted key a real KEEP target. The increasing sweep gives both trees the same left vine. Each successor splay puts the processed predecessor directly to its left and retains the previous left vine. Use a final A-only increasing sweep over the whole support, then A-only coercion to the required stretched A cut state. All those events count. The sweep gives every owner block a cap-five reset and the remaining A-only operations cannot reduce stocks. The greatest cyclic seam is consequently the full vector. [Splay coercion through actual requests](https://arxiv.org/html/1907.06310v3#S3).

Up to the original operation 99, all actual A targets following the cut avoid the two stretched subtrees. The old A rotations are unchanged outside them. The only new labels in a hot footprint are roots of inserted hanging subtrees. This leaves the ordered equality pattern of all footprint blocks constant as $L$ varies over its allowed multiples of five. Old ranks retain their residues modulo five. Every hanger root used in the hot phase is at the first or last inserted rank of its gap. Its block coincidences with neighboring old keys and its order among occupied blocks are constant for $L\ge20$. Blocks with no footprint in the hot phase do not affect the replay. Thus the starting full bank and the literal hot event word give the same unpaid labels at every $L$ as in the independently checked $L=20$ trace.

B(68,15) relative to the new cut is unpaid. Its two post-rotation demoted subtrees contain original key 1. They have old-rank intervals $[1,133]$ and $[1,225]$ before expansion, rooted at old keys 118 and 134 respectively. All ancestor holders of radii at most $L$ at these two demoted keys are within the added A chains and exclude 1. For rank radii at most $L$, the four exterior padding gaps keep each window within the extension of the corresponding old block $[116,120]$ or $[131,135]$. Every included padded key is an A descendant of some old key in that old block. This holds for a boundary gap because its two adjacent keys are comparable in A, and it holds for the lifted chains because their unlifted outer endpoint remains an ancestor. In the original post-A tree the minimum-depth keys of those two blocks have subtrees excluding 1. Every radius-window holder therefore excludes 1 as well. The promoted keys cannot decrease $\Gamma$ in either physical rotation. Thus even a finite family of rank and ancestor radii has a literal unpaid double with no decrease. Counting ranks active anywhere in the period in place of all ranks gives the same obstruction when the optional all-key KEEP sweep is included.

The [377-key fully active control](GSO_OMEGA5_ACTIVE_ANCESTRY_STRETCH_20261123.json.gz) has 5,458 measured operations, $A=7112$, $Q_B=1599$, and $\Omega_5=2$. The replay verifies the new cut, the complete reaching prefix, both full restorations, and the full-stock seam. The missed event is B(68,15), including both original halves. Larger $L$ executions without the optional active sweep also passed at support 497 and 737. This test concerns a required decrease on each unpaid double. Decreases elsewhere in a period can still matter for aggregate conservation.

### All currently live containing A intervals can still be shared too much

The next direct payment rule gives an unpaid original B double access to **every** proper A interval lifetime present in its B phase that contains the new subtree of either real demoted pivot after that pivot's rotation. One A interval lifetime is a maximal chronological run of existence of that physical key interval in A. One actual A rotation replaces exactly one proper interval in the collection, so a fixed capacity per lifetime is an actual A-work budget, with at most $n$ initialized lifetimes in a lifted run.

This also tests a sum of bounded-range monotone functions of the B straddlers of the live A intervals when each function is fixed throughout its interval's lifetime. During a B rotation, such a term can decrease only for a holder interval containing the newly formed demoted subtree. A uniform positive decrease on each unpaid double would require uniformly bounded load on precisely these lifetime resources, even with splitting among them.

Here is a complete original family disproving full payment on this eligibility, for every fixed capacity. Fix a stage count $s$ and a number of cells $k$. Use the Step 2 diagonal tree and high producer word, with $h=5m$ large, $q=h-2$, and $n=h+5q$. Choose a guard $b=5(s+2)$ and $h-b\ge 2^s(k+3)$. The inner interval $I_0=[b+1,h]$ is a union of full owner blocks. Modify the A-only preparation of the Step 2 tree below 3. Give 3 right child $b$, give $b$ left subtree the ascending right vine $4,\ldots,b-1$, and put a fixed A tree on $I_0$ as the right subtree of $b$. The shape on $I_0$ will be specified by the actual B rotations. The high preparatory accesses do not enter the proper subtree of 3. The Step 2 stock calculation still applies. All blocks strictly between the first and last low blocks are empty after the high producers, and the last low block has at most two credits. In particular $I_0$ has total stock at most two.

Use the hot KEEP targets $3,4,\ldots,s+2$. The prospective B word is known before choosing the arbitrary fixed A shape on $I_0$. At its start B has root $h+1$ with left vine $h,\ldots,1$. The first hot search follows that vine. For each later hot operation the target is the physical successor of B's old root. The search first takes the right edge and then follows the full left spine down to that successor. The same-side doubles along this spine are LL. There is at most one final operation involving the old root with a different pairing form.

Initially mark the consecutive segment of that spine in $I_0$. Retain marked status at a surviving smaller pivot $p$ whenever a hot LL pairs two consecutive marked pivots $g,p$ with $g>p$. Its new right child is the retired $g$. At every stage the surviving marked pivots form a consecutive segment of the left spine on the new target's right. The full successor search at the next stage visits that segment. A pairing inside the segment puts the smaller pivot on this left spine and the larger pivot in its right hanger. Their old right hangers cannot be rotated by any of these exterior targets. The count of marked survivors is at least half the previous count minus one, since only the first and last old marked positions can pair across the segment boundary. Every such retiree's subtree stays inside $I_0$. Its minimum is above the smaller pivot in $I_0$, and its maximum was inside $I_0$ for the old marked upper pivot. The new marked pivot has the same maximum. This proves the containment invariant by induction.

Every marked survivor after stage $s$ has a nested chain of $s$ retired intervals, one per stage. In fact, at stage $t$ the retired $g$ retains its old right subtree, which at stage $t-1$ was the new retirement interval carried by $g$ as the surviving pivot. All later retirements on that chain contain any chosen real key $v_i$ of the first interval. There are at least $(h-b)/2^s-2\ge k$ final marked survivors. Choose $k$ consecutive ones. Their final retirement intervals $I_i$ are disjoint and separated by at least one physical key, a surviving smaller pivot of the final LL pass.

Choose the fixed A tree on $I_0$ so each $I_i$ is a proper subtree rooted at $v_i$. Separate neighboring bins with one intervening physical key, used as an ancestor on a binary routing tree over the bins. Each terminal routing range has unused keys on at most two sides of its bin. Hang those ranges from at most two further boundary ancestors. Thus the union of ancestors of the $v_i$ inside $I_0$, including the $v_i$, has at most $4k$ keys. Their subtrees and lifetimes are fixed throughout the hot phase. The A hot splay at 3 is the zig over $h+1$. In A the next target 4 is reached along $3,h+1,b,4$ and its splay transfers the whole $I_0$ from $b$'s right to $(h+1)$'s left. Each subsequent A search goes from the previous root to $b$ and then its left child, the current successor. It keeps $I_0$ intact. At each hot boundary there are only two proper A ancestor intervals of $I_0$ outside this fixed tree, those at $b$ and $h+1$.

Consider the $ks$ selected LL doubles along the chains. For each one, both newly demoted B subtrees contain its real $v_i$. For the second rotation this holds because the old parent retains the first retired grandparent as its right child. Every eligible A lifetime therefore belongs either to an ancestor of some $v_i$ inside the stable $I_0$ tree or to one of the two outer proper intervals at a hot boundary. The union of all eligible lifetime resources for the selected demands has size at most $4k+2s$.

The paid labels do not erase this obstruction. To bound payment into $I_0$, use the actual LL footprint roles. In the hot LL block, the old pairs $(p,g)$ are processed in increasing rank order. The middle of the first rotation lies between $p$ and $g$. Except in the first LL, the middle of the second rotation is the previous deeper LL's surviving smaller pivot. The exterior parent of $g$ lies at the immediately next old search-path position. Along the monotone old path the positions in $I_0$ are consecutive. Thus at most two LL pairs cross an endpoint of $I_0$, at most two further pairs have the preceding smaller pivot across an endpoint, and at most two further pairs have their exterior parent across an endpoint. The first bottom double and the final operation with the old root contribute at most two more exceptions. A conservative bound of 12 exceptional B steps per hot KEEP covers all steps using stock inside $I_0$ together with exterior stock other than the target. These can import at most 40 units each. All other LLs touching the interior form at most 13 runs with scopes contained in $I_0$ plus the target block. Each run can start with at most five units in the target block, and every paid debit in the run consumes one unit of the combined stock. The hot A operations can supply at most five new units per KEEP to $I_0$, since only its unchanged subtree root can appear in an exterior A footprint. The total possible paid selected doubles over all $s$ stages is at most

$$
2+s(5+12\cdot40+13\cdot5+12)\le 2+600s.
$$

Here the last 12 allows the exceptional steps themselves to be paid. The stock bound sums the initial interior mass, actual A issuance, and the exceptional imports over the whole hot segment. It does not count interior mass afresh for every stage.

Close both original full trees by A-only coercion to the current B tree, then by a common KEEP coercion back to the original diagonal. This yields a complete original history and counts all preparation and restoration. The chosen actual unpaid subset has at least $(k-600)s-2$ rows on at most $4k+2s$ available A lifetime IDs. Set $k=s+1204$ and let $s$ grow. The load required to fund every row diverges, for this fixed broad eligibility. Repeating each complete source also defeats a one-time initialization allowance. It leaves open a proof that an absolute fraction of the total original unpaid work is fundable on these lifetimes, with the remainder absorbed by a separate aggregate argument.

The [2,120-key complete control](GSO_OMEGA5_PARALLEL_INTERVAL_LIFETIMES_20261123.json.gz) uses $s=5$ and $k=7$. It has 37,379 operations, $A=45826$, $Q_B=7388$, and $\Omega_5=287$. Of 35 selected physical rows, 24 are unpaid. Their exact union of live A-interval creation IDs has size 22, and the unit-capacity optimum is 22. A second independently verified control used separate larger shoulder ranges at support 2,780 and found 38 selected unpaid rows on 27 creation IDs. The parametric argument above is what excludes every fixed cap for complete coverage.

### Looking back to original B gains and their actual A receipts

The lifetime Hall family explains the need to retain old physical work through the entire period. Each selected grandparent retires inside the fixed $I_0$ and remains untouched in the rest of the hot segment. Its earlier high producer made it the lower pivot of a paid RR and gained its left reach. The chosen grandparent IDs are distinct in the whole hot segment. Their actual earlier paid producers therefore fund these selected debits at load one on paid receipts, and at most 45 on original A units. The interval-lifetime obstruction is present even with that ample earlier physical work.

The next direct test follows the most recent original promotion restoring the direction of each of a dry double's two endpoint losses. In a right rotation the demoted key loses lower reach and the promoted key gains upper reach. The signs reverse in a left rotation. The exact cyclic orbit ensures a most recent gain in the lost direction for every counted loss, including across the seam. The read-only test admitted only gains in paid doubles or terminal zigs. W257, both saved 290-key controls, the 770-key cold control, and both new saved controls each had a complete assignment at unit load in that test. The 2,120-key control assigned all 287 raw unpaid doubles this way, with some gain coordinates offered to as many as five demands. The assignment result does not bound reuse in arbitrary periods.

A gain by the B target need not itself be paid to be a possible original budget. Within one genuine KEEP only the last target gain in either direction can be the last gain used by a later KEEP. This gives at most $2K_B\le2A$ distinct target-gain coordinates, in addition to the genuine paid receipts of non-target gains. A non-target gain from an unpaid double still has to be accounted for. The source-uniform issue is the combined load when many losses draw on the same earlier non-target gain or on A-interval lifetimes recycled during interleaved restoration. No bound for that combined load or for $\Omega_5/A$ has been proved.

The two unqualified gain arms of a same-side double would have to come from distinct original earlier KEEPs. In an LL with old keys $p<g$, both losses are of lower reach. If both last gains were non-target gains in the same earlier KEEP, both keys were promoted as non-target parents of RR doubles during that earlier KEEP. They end on its left side's right-going spine. On that spine $p$ is above $g$, so $p$ is absent from $I_B(g)$. In the consuming LL it is the left child of $g$. Its inclusion requires a real subsequent lower-endpoint expansion of $I_B(g)$. That expansion contradicts the asserted last gain. The RR case reflects the argument. This uses full chronological occurrences, including when one producer lies across the cyclic seam.

To stress this exact predecessor rule, the 2,120-key control was continued with single and interleaved high KEEPs, each finished by counted common all-key restoration. A physical screen found late RR configurations with two unqualified previous gain arms before evaluating their actual bank labels. On 21 complete continuations every unpaid row still had two qualifying earlier gains. A further 27 measured continuations prepared the eventual high target with a DELETE and spent high stock with an actual earlier KEEP before the cold low phase. Each candidate returned both full trees and was evaluated at the greatest seam. These also retained the two earlier gain arms on every unpaid row. Both experiments chose pressure using the complete-period $\Omega_5/A$. The global load bound remains open.
