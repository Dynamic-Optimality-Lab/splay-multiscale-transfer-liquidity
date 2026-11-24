# IAGS 1.2 — BB-01: discounted polynomial-growth bootstrap

Date: 2026-11-10, Asia/Karachi.

**Overall verdict: BLOCKED on the source-derived strict discount.** The complete analytic bootstrap and all three inherited size ceilings are established at their stated qualifications. A normalized, physically admissible one-key-erasure auxiliary construction has exact weighted A cost one and unchanged physical population. No source comparison proving a strict discount for the selected frontier quantity is established. No unrestricted URCD coefficient or Dynamic Optimality conclusion follows.

This report executes BB-01 only. The near-optimality theorem and Route A comparator are inherited, not reopened. All constructions below are mathematical source constructions, not executed traces.

## 1. Scope, source pins and provenance

Repository: C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2. Branch coarse-double-branch; initial HEAD 6d532b2c795c0778f57d8023b23b5fedfc48b010.

The complete Route A, G0–D5, RG01, RG04, original Route 02/04 reductions, physical Pair Access/S-SET specifications and research rules were read in the preceding Route A work in this same session. Current hashes were compared with those complete reads and matched. Those actual unchanged texts, rather than a summary of their mathematics, remain the inputs. Route B, RG02, the completed existing D6 and CD6-TRANSFER triad were read in full for BB-01. Campaign 14's specification, theorem, full proof, final verdict, full final certificate, U14 transfer and audit report were read directly. Campaign 15's source, final verdict, U14 reconstruction, leaf-channel, zero-run, owner, group, supply, restricted-family and audit-status reports were read directly. Individual current pins are recorded in Section 16.

The static check of all 44 entries of Campaign 14's final certificate found no hash mismatch. Its 2,746 transitive checks were not rerun here. Campaign 15's partial_seal.json is absent, as its audit-status report states. Its completed source checks do not become a completed final integrity seal.

Current D6 gives its qualified substantive partial result
\[
R_{\rm fringe}\le6C_{\rm seq}A,\qquad
Q_B\le(32+12C_{\rm seq})A+R_6.
\]
It leaves the full residual open. The CD6-TRANSFER triad is STRUCTURAL ONLY with unrestricted transfer blocked. Neither is a strict-discount theorem.

The pre-execution research gates are fixed for this investigation:

1. The principal question is one weighted physical source transfer, rather than improving the external competitiveness factor or reopening the regeneration campaign.
2. First prove the analytic implication. Then use the inherited finite erased-tree recurrence as the concrete auxiliary-construction mechanism, retaining every A operation and proving its normalization cost. The proposed discovery is the remaining frontier comparison, not the mere existence of an auxiliary period.
3. Keep one selected quantity, one principal erasure transfer attempt, the requested static adversarial audit, and an exact obstruction. No second open mechanism is introduced after the comparison fails.
4. A successful strict discount would remove the unrestricted size dependence by the established bootstrap. An admissible erasure lift alone, already implicit in U14, is not promoted to substantive quantitative progress.

Freeze the original model. A and B are complete labelled physical BSTs on the same finite X. A splays every KEEP and DELETE; B splays KEEP only. DELETE removes no key. Both complete trees return to their individual starting trees over W; reachability from a diagonal is retained and its prefix is excluded. Private ancestors, complete hangers, all helpers, terminal zigs and real occurrence IDs remain. In particular,
\[
R_A=2A-V_A\le2A,\qquad
D_B=B_1+2B_2+Z_1=P_A-N_A.
\tag{1.1}
\]
A virtual companion is not a real rotation. An auxiliary source has its own physical occurrences; scalar weights do not turn them into additional original donor units.

No external research, source engine, replay, experiment, enumeration, solver, subagent, installation or later research gate is used. The prescribed repository report is the sole output; repository-recoverable mathematics is not duplicated into Notion.

## 2. Frozen Route A near-optimality benchmark

Use Route A at its reported same-agent symbolic level, with its established primary external dependency, without a new audit of the external theorem:
\[
2Q_B+Z_B+K_B
\le C_0g(n)(2A-V_A+K_B),\qquad K_B\le A,
\tag{2.1}
\]
\[
Q_B(W)\le Kg(|X|)A(W),\qquad K=\tfrac32C_0.
\tag{2.2}
\]
Here C_0 is absolute and symbolic. Its exact smoothed factor is
\[
\bar n=\max\{16,n\},\qquad
g(n)=\log_2\log_2\bar n
\bigl(1+\log_2\log_2\log_2\bar n\bigr)^2.
\tag{2.3}
\]
It is nondecreasing and positive on all nonnegative integers. Its minimum is exactly g(0)=8: at 16 the first factor is 2 and the squared factor is 4.

The physical population in (2.2) is |X|. There is no inherited replacement by the carrier size |S|. This report keeps that distinction in every auxiliary benchmark.

For any of the selected nonnegative quantities T below, put
\[
F_T(n)=\sup_{\substack{W\ {\rm admissible}\\|X(W)|\le n,\ A(W)>0}}
\frac{T(W)}{A(W)}.
\tag{2.4}
\]
Use value zero for an empty class, in particular at n=0,1. These are nondecreasing functions because the source classes are nested. The inherited K_B<=A implies that A=0 has no charged B fragment, no B double and no renewal residual; thus all three T vanish there. Zero-cost auxiliary sources require no division.

## 3. Complete abstract bootstrap proof

**BB-BOOT, with its threshold qualification.** Let F be finite and nonnegative on the relevant integers, with F(n)<=K_T g(n). Suppose a>=0, integer d>=2 and 0<=theta<1 are absolute and
\[
F(n)\le a+\theta F(n^d)
\quad\hbox{for every integer }n\ge N_0,
\tag{3.1}
\]
where N_0>=2 is absolute. Then
\[
F(n)\le\frac{a}{1-\theta}\quad(n\ge N_0).
\tag{3.2}
\]
If F is one of the monotone suprema (2.4), the same conclusion holds at every smaller finite n as well.

For a fixed n>=N_0, n^{d^j} stays in the recurrence domain. Induction gives, for every k>=1,
\[
F(n)\le a\sum_{j=0}^{k-1}\theta^j
+\theta^k F(n^{d^k}).
\tag{3.3}
\]
For k=1 this is the premise. Substituting (3.1) at n^{d^k} into the last term proves the k+1 case. Thus the terminal term has not been discarded.

If theta=0, (3.2) follows immediately. Otherwise apply the finite ceiling to the terminal term:
\[
0\le\theta^kF(n^{d^k})
\le K_T\theta^k g(n^{d^k}).
\tag{3.4}
\]
For fixed n>=2 and fixed d, let L=log_2 n>0. Once n^{d^k}>=16,
\[
u_k=\log_2\log_2(n^{d^k})
=k\log_2d+\log_2 L,
\qquad
g(n^{d^k})=u_k(1+\log_2u_k)^2.
\tag{3.5}
\]
For all sufficiently large k, 2<=u_k<=c_{n,d}(k+1), with a finite c_{n,d}. Consequently
\[
g(n^{d^k})=O_{n,d}\bigl(k(\log(k+2))^2\bigr).
\tag{3.6}
\]
The finitely many earlier k are absorbed into the same finite constant. Since d is a fixed absolute constant, this is the requested O_n estimate.

Writing b=-log theta>0,
\[
\log\!\left(\theta^k k(\log(k+2))^2\right)
=-bk+\log k+2\log\log(k+2)\longrightarrow-\infty.
\]
Equations (3.4)–(3.6) prove that the entire terminal term tends to zero. The geometric sum tends to 1/(1-theta), establishing (3.2). The intermediate growth constant may depend on the fixed n; the resulting bound a/(1-theta) does not.

This is a pointwise limit of numerical inequalities valid for the already-defined finite supremum F(n). It neither chooses a maximizing source nor interchanges a supremum with a limit.

For the actual F_T, monotonicity gives F_T(n)<=F_T(N_0) for n<N_0. Thus the same coefficient applies, and F_T(0)=F_T(1)=0 handles empty source classes. The finite benchmark independently certifies finiteness at every small size.

A qualification to the literal abstract formulation is necessary: nonnegativity, a ceiling and a recurrence only above n_0 do not constrain a generic NONMONOTONE F below n_0 to the same coefficient. For example, take n_0=4, a=0, theta=1/2, d=2, set F(2)=1 and F(n)=0 elsewhere, and choose K_T with 8K_T>=1. All the large-n hypotheses hold, but F(2)>0. Without monotonicity, one can instead retain the absolute small-size coefficient
\[
\max\left\{\frac a{1-\theta},
K_T\max_{n<N_0}g(n)\right\}.
\]
For the functions in this request monotonicity is proved by (2.4), so the requested exact a/(1-theta) conclusion is valid. If a were initially allowed to be negative, the vanishing-remainder proof and F>=0 would force a>=0 whenever the premises are consistent.

Polynomial exponents can be taken integral without loss in the source application: enlarge a real exponent to an integer and use the monotonicity of F_T. A generic function without monotonicity needs an explicit integer/rounded argument convention.

## 4. Polynomial growth and terminal-remainder analysis

The relevant condition for a general nondecreasing enlargement majorant phi is exact. For n_k=phi^{circ k}(n), the inherited ceiling certifies disappearance of the remainder whenever
\[
\boxed{\ \theta^k g(n_k)\longrightarrow0
\quad\hbox{for each fixed starting }n.\ }
\tag{4.1}
\]
This is a sufficient condition for bootstrap; failure of (4.1) means that this ceiling alone does not bound the terminal term by something vanishing. It does not prove that the actual terminal F values fail to vanish.

A useful sufficient rate criterion, for 0<theta<1, is
\[
\limsup_{k\to\infty}\frac{\log g(n_k)}k<-\log\theta.
\tag{4.2}
\]
The exact criterion (4.1), rather than a strict root-test bound, governs equality/borderline rates. For every fixed theta<1, the stronger subexponential condition log g(n_k)=o(k) suffices. At large sizes, writing L_2(x)=log log x in any fixed base,
\[
g(x)=\Theta\!\left(L_2(x)(1+\log L_2(x))^2\right).
\]
This describes precisely which growth orbits the discount can dominate, including smoothing at finite sizes.

For polynomial growth with an absolute coefficient, suppose
\[
\phi(t)\le c\max\{N_0,t\}^{D},\qquad c\ge1,\ D\ge2.
\]
Starting above N_0 and writing h_k=log n_k gives
\[
h_k\le D^kh_0+\frac{D^k-1}{D-1}\log c.
\]
Hence log log n_k=O_{n,c,D}(k+1) and g(n_k)=O_{n,c,D}(k(\log(k+2))^2). Arbitrarily many recursive levels are allowed. Operation count is irrelevant to this population calculation, but remains fully relevant to auxiliary A cost.

Polynomial growth is sufficient, not logically the maximal allowable class. For instance the idealized orbit phi(x)=exp((log x)^q), q>1 fixed, has log log n_k=q^k log log n and g(n_k)=Theta_n(q^k k^2). The same ceiling works if theta*q<1, and does not vanish at theta*q>=1. Appropriate integer ceilings change constants and not that conclusion for large starting sizes.

For the proposed exponential enlargement phi(n)=2^n, in binary logarithms and k>=2,
\[
\log_2\log_2 n_k=n_{k-2}.
\]
The successive ratios n_{j+1}/n_j=2^{n_j}/n_j tend to infinity. Thus n_{k-2} eventually dominates every fixed exponential in k. For every fixed theta in (0,1), theta^k g(n_k) diverges, rather than tending to zero. No terminal estimate is therefore licensed for that growth rule by the present benchmark. Theta=0 remains the trivial nonrecursive case. No exponential physical gadget is substituted for an allowed polynomial lift.

## 5. Audit of Route B's physical-frontier theorem

Write c=C_seq>=1, retaining its inherited classical sequential-access qualification and unspecified absolute numerical value. Route B uses the ORIGINAL cyclic KEEP blocks and original fixed carrier S. D5 long-window coverage is an actual union of original double IDs. Its complement is partitioned into owned consecutive-rank fragments omega. Identity repeats remain inside their blocks and DELETEs retain all A work.

For an increasing irregular fragment with visited keys K=[a,b] in S rank, let U be the union of its targets' initial physical B ancestor paths. Let d_omega be its first target's initial B depth and
\[
f_\omega^+=|\{u\in U:u>b\}|.
\]
Reflect for a decreasing fragment, and use the increasing convention for a singleton. The selected quantity is
\[
\mathcal F_B(W)=\sum_{\omega\ {\rm irregular}}
\left(\frac{d_\omega}{2}+c f_\omega^{\rm dir}\right).
\tag{5.1}
\]

The audited argument is physical: U is ancestor-closed and its operand edges are actual edges; complete U-free subtrees are transported by every primitive rotation. After the first target, the relevant forward operand domain has ell_omega+f_omega^{dir} keys and the actual subsequent requests are a prefix of its complete sorted scan. No artificial scan continuation supplies A work. Therefore
\[
Q_B(\omega)\le c\ell_\omega+\frac{d_\omega}{2}+cf_\omega^{\rm dir}.
\]
The exact fragment partition and original KEEP-gap witnesses give sum ell_omega<=K_B<=A. Long union cost is <=2cA. Summation yields
\[
Q_B\le3cA+\mathcal F_B.
\tag{5.2}
\]

For each fragment, the first-path term is <=Q_B(omega)+1/2. Every forward-frontier vertex is an initial ancestor of the last target and must be removed from that fixed target's B ancestor path before it reaches the root. A real B rotation removes at most one such ancestor. Thus f_omega^{dir}<=2Q_B(omega)+ell_omega. Summation proves the actual converse comparison
\[
\mathcal F_B\le(1+2c)Q_B^{\rm irregular}+(c+\tfrac12)A.
\tag{5.3}
\]
These are the source facts used below. There is no inherited frontier-to-A payment.

Combining (5.3), Q_B^{irregular}<=Q_B, (2.2), monotonicity of g and g>=8 proves, for every physical-population cap n,
\[
\boxed{
F_{\mathcal F}(n)\le K_{\mathcal F}g(n),\qquad
K_{\mathcal F}=(1+2c)K+\frac{c+1/2}{8}.
}
\tag{5.4}
\]
This is an explicit absolute constant. It does not replace |X| by |S| or use the unproved summability of the frontier.

Route B's converse estimate has recurrent coefficient 1+2c>=3, so substituting it into (5.2) is not a contraction. A positive physical definition is not an independently proved A resource.

## 6. Choice of source quantity T

Select **T(W)=mathcal F_B(W)** from (5.1), with F_T=F_mathcalF.

| Candidate | Complete inherited ceiling | Source-transfer burden |
| --- | --- | --- |
| Total Q_B | F_Q(n)<=Kg(n) | Few historical predicates, but no simpler direct discounted physical transformation is supplied by the sources. |
| Physical frontier | (5.4) with the explicit K_mathcalF | Actual ancestor geometry and fragment boundaries expose what an erasure lift would need to preserve or pay. This is the selected interface. |
| Original R_irr | F_R(n)<=Kg(n), and Q_B<=(32+6c)A+R_irr | Auxiliary carrier changes also require rebuilding every chosen birth, whole-frame/Pi predicate, complete cohort and first-change incidence. No essential new invariant justifying those extra requirements was found. |

This is one source construction attempt, not three separate investigations. The selected quantity is eligible for BB-BOOT before any transfer is assumed. Current D6 further controls a subcount of R_irr; it gives no missing strict discount for (5.1).

For every COMPLETE source with genuine KEEP support at most six, CD5/CD6 and (5.3) already give
\[
\boxed{\mathcal F_B(W)\le a_6 A(W),\qquad a_6=5c+\tfrac52.}
\tag{6.1}
\]
Indeed Q_B^{irregular}<=Q_B<=2A. This is an inherited whole-period bounded case. It does not make a six-target open fragment certified. It supplies the local terminating source class of the proposed erasure strategy, not a new partial-discount theorem.

## 7. Proposed one-step physical transfer

The principal candidate is **averaged one-key erasure with actual periodic alignment**. It uses the same physical X and the same full A target word. Erasing a KEEP key means changing only its KEEP tags to DELETE; it does not remove that key or suppress its A rotations.

For an original W with r>=7 genuine KEEP keys M, construct the genuine sources V_z for all z in M as in Section 8. Let L_z be their actual period multiplier and define
\[
\lambda_z=\frac1{rL_z},\qquad
E_{\mathcal F}(W)=\sum_{z\in M}\lambda_z\mathcal F_B(V_z).
\tag{7.1}
\]
All terms are nonnegative actual source quantities. The intended discovery would be absolute 0<=a_E<infinity and 0<=beta<1 satisfying
\[
\boxed{\mathcal F_B(W)\le a_E A(W)+\beta E_{\mathcal F}(W)
\quad\hbox{for every such }W.}
\tag{7.2 — UNPROVED}
\]
The lower-support case is paid by (6.1), so a=max{a_6,a_E} would give one all-source statement.

The motivation is a possible physical incidence coupling: an original irregular incoming path and terminal-side ancestor frontier would either survive in the erased source's actual frontier, or disappear for a reason chargeable to actual original A work. A strict effective gain would have to come from that coupling with bounded global load. It cannot come merely from an erased target name or from averaging r alternative trees.

The first unsupported physical assertion is that such coupling exists. Erasing z changes later B paths, the recurrent B starting tree, its canonical carrier, S-rank gaps, long-window membership and irregular-fragment partition. There is no established map from original frontier incidences into retained auxiliary frontier incidences with a uniformly paid deficit. Section 8 proves that the auxiliary words really exist; it does not assume that missing map.

## 8. Auxiliary source construction and exact closure

Fix the complete original starting pair (A_0,B_0) of W and an actual legal reaching prefix P from some diagonal (T_0,T_0). Let W_z have the same target at every occurrence as W and the same tags except that each KEEP z becomes DELETE z.

Let H_z be the deterministic map on full n-key BSTs obtained by applying the W_z KEEP subsequence. At boundaries of repetitions of W_z the A tree is always A_0: every A access, including every converted z request, is unchanged from W. The B tree follows
\[
B_0,\ H_z(B_0),\ H_z^2(B_0),\ldots .
\]
There are Cat_n complete labelled BSTs on the fixed ordered X. Choose the first repeated tree in this finite orbit: least v>=1 with H_z^v(B_0)=H_z^u(B_0) for an earlier u, and that unique earlier index u. Put u_z=u and L_z=v-u>=1.

Define the auxiliary source completely by
\[
X_z=X,\quad A'_0=A_0,\quad B'_0=H_z^{u_z}(B_0),
\quad V_z=(W_z)^{L_z}.
\tag{8.1}
\]
Its legal reaching prefix is P followed by u_z copies of W_z. No computation of the orbit is run. Finiteness proves the existence and deterministic specification of these integers, with u_z<Cat_n and L_z<=Cat_n.

The auxiliary A endpoint is A_0, since each copy's target word is unchanged. The auxiliary B endpoint equals B'_0 by its actual recurrent orbit. Thus both COMPLETE labelled trees close. All original and converted helper requests occur in each auxiliary period; every physical key remains present. No independent inverse-rotation operation is assumed.

The whole-period genuine KEEP support of V_z is at most M minus {z}. If all its KEEPs are B identities, it has no B/frontier cost. Otherwise closed-source genuine-support normalization applies to its own complete period. Its carrier and fragment decomposition must be recomputed on V_z itself; they are not copied from W.

Each auxiliary event has a fresh namespace (z,copy,original operation position,StepEv,real bit). The occurrence-position correspondence is for an exact scalar cost identity, not a donor duplication license. Prefix P and the u_z transient copies establish legal reachability only and contribute no auxiliary-period donor units.

This is a valid physical lift, already supported in substance by the U14 erased-recurrence interface and instantiated here for (7.1). It is not a new source-uniform comparison of frontier quantities.

## 9. Absolute auxiliary A-cost accounting

Because the original A target word and its complete initial tree are unchanged in each auxiliary copy, exact determinism gives
\[
A(V_z)=L_z A(W),\qquad
R_A(V_z)=L_zR_A(W).
\tag{9.1}
\]
Every DELETE, preparation, ordinary KEEP, omitted-in-B z request and restoration request in W_z is included. There is no additional closing operation after L_z copies because full closure has been proved from the actual B recurrence. All closing work already belongs to the displayed periods.

Consequently the complete weighted A sum is exactly
\[
\boxed{\sum_z\lambda_z A(V_z)=A(W).}
\tag{9.2}
\]
Thus kappa=1 is proved, independently of source length, support size, L_z, preperiod length, renewal depth and all private populations.

There are no new physical keys:
\[
|X(V_z)|=|X(W)|
\le\max\{2,|X(W)|\}^{2}.
\tag{9.3}
\]
The polynomial-universe requirement holds with n_0=2 and d=2. A potentially large Cat_n period multiplier is an OPERATION-count bound, not an enlarged physical population. It is allowed here, and its actual A cost is included and normalized in (9.1)–(9.2).

No A comparison is inferred from a B ancestor path. The equality follows solely from unchanged full physical A dynamics.

## 10. Strict discount calculation

For this candidate, the proved kappa is one, so the effective discount would be theta=beta. Neither beta<1 nor even a useful undiscounted frontier-domination formula has been proved from the construction. In particular, r-1 retained target names are not a factor (r-1)/r in the weighted frontier cost.

If (7.2) were proved, (9.1) and the definition of F_T would give, for |X(W)|<=n,
\[
E_{\mathcal F}(W)\le F_{\mathcal F}(n)A(W).
\tag{10.1}
\]
Taking the supremum would therefore yield the STRONGER same-universe recurrence
\[
F_{\mathcal F}(n)\le a+\beta F_{\mathcal F}(n),
\tag{10.2 — CONDITIONAL}
\]
and hence the requested polynomial-growth recurrence by monotonicity. Finiteness from (5.4) would already allow subtraction in (10.2); the general BB-BOOT proof remains available for constructions that actually enlarge populations. This does not weaken the missing source theorem.

A normalization cannot manufacture strict discount. Rescaling all lambda_z by a factor t>0 changes kappa to t and the comparison coefficient beta to beta/t; their product stays beta. Similarly, reproducing an unchanged closed source b times gives T(W^b)=bT(W) for the canonical cyclic frontier partition and A(W^b)=bA(W). The exact comparison T(W)=(1/b)T(W^b) has beta=1/b and kappa=b: product ONE.

The frontier scaling assertion uses actual repeated B snapshots, unchanged closed carrier and repeated cyclic KEEP blocks. Same-sign runs cannot wind around a full circle of strictly ordered ranks; canonical long coverage and ownership cuts therefore repeat with the source phase. No new source resources arise at the display seam. Cyclic copies with transported original phase labels likewise preserve T and A.

For any construction made solely of such full-source copies or relabellings, write s=sum_i lambda_i b_i. Its proposed comparison is
\[
T(W)\le aA(W)+\beta sT(W).
\]
With theta=beta*s<1 this is exactly the already-desired bound T/A<=a/(1-theta), with no independent smaller physical statement. Using one complete rotated copy per fragment instead gives total A replication equal to the number of fragments, unbounded in repeated complete G sources. These are diagnostics of false discounts, not a second proposed research route.

Even a hypothetical per-support gain 1-1/r would approach one and fail the required absolute theta<1 condition. No such per-support comparison is proved here either.

## 11. CD(6) local-certificate interface

Campaign 14 certifies the COMPLETE original reachable paired-closed domain with exactly six distinct genuine KEEP targets, arbitrary physical population/private A ancestry/helpers, and original StepEv/double costs. CD5 supplies smaller support. One whole-period backend is selected from core sizes 6 through 11. Its historical computer-assisted symbolic and same-agent distinct-implementation qualifications remain; there is no new formal or external certification.

It supplies (6.1) for an auxiliary V_z whenever that ACTUAL complete auxiliary period has at most six genuine targets. At larger support it does not supply a local bound just because one frontier currently contains at most six distinguished operands.

A proposed “cut a fragment, retain six targets, then add a six-support return” has an exact obstruction from CD6-TRANSFER Section 9.1. For n>=12, let R_n be the full right vine and T_n=splay_n(R_n). DELETE n reaches the admissible pair
\[
s=(T_n,R_n).
\]
The one KEEP n fragment reaches (T_n,T_n). There is no continuation returning exactly to s with at most six genuine KEEP targets: its hypothetical closed support includes n, whose initial root-to-key path in B contains all n vertices, contradicting the closed-core bound |S|<=2r-1<=11.

This fragment is inside the complete admissible source
\[
W_n={\rm DELETE}\ n;\ {\rm KEEP}\ n,n-1,\ldots,1.
\]
The full source retains its preparation and closes to (R_n,R_n), with Q_B<=A. The example refutes only the proposed same-state six-support closing interface; it is not a source-ratio counterexample. Different auxiliary trees remain allowed but would need their own original-quantity and A-cost comparisons.

If an actual partition I_j has certified returns J_j, CD6 instead gives the valid conditional closure price
\[
Q_B(I_j)\le2A(I_j)+2A(J_j)-Q_B(J_j).
\tag{11.1}
\]
Neither existence of these returns nor a global bound for their total price is supplied for arbitrary fragments. A finite-state six-support potential replaces a missing return by a boundary term, not by a source-valid discounted auxiliary obligation.

Campaign 15 does not fill this gap. On maximal cores its raw leaf-channel construction is a globally injective PARTIAL map with branch deficit (beta_e+z_e-2H_e)_+. Its actual seven-key source has A=90,Q_F=58,Q_E=17 and a real certified six-key smaller map; the prescribed locked-owner walk reaches an undefined ordinary branch at occurrence 39. The reset bit (50,1,0) repairs that family. Its r-4 consecutive zero-transfer family refutes every fixed own-unused bounded-lookback repair, while retaining nonlocal reset repairs.

Thus neither raw donor uniqueness nor support changes license a uniform paid local portion of every frontier. The C15 image-wide impossibility attack did not succeed; nonlocal reassignment remains unproved rather than refuted. New partial C15 results retain SOURCE-AUDITED / FINAL INTEGRITY SEAL PENDING. No allocation or owner is changed in BB-01.

## 12. Adversarial source tests

The tests below are mathematical checks on the selected averaged-erasure comparison and its tempting shortcuts. No source was replayed. They preserve complete words, closing work and inherited full-Pi qualifications.

| Complete source/control | Preserved data | Consequence for BB-01 |
| --- | --- | --- |
| H_pq | N=2^{p+1}(q+1)+1; DELETE preparation; descending EVERY key through 1, KEEP only x_j=N+1-2^j; full increasing and reverse scans; A=4(N-1). | Its entire R_branch is D5-covered. It does not create newly unpaid R_irr generations. Critical doubles can still lie in Route B's broader irregular class. The p-1 shared first-hit layer references do not give separate A payments for erased frontier incidences. |
| H_(6,1) | N=257, all 1026 operations, A=1024, genuine relay [11,33] to [19,129], old roots/births and full receiver retained. | No decreasing-interval premise can prove a gain in (7.2). A statement about auxiliary frontier survival still requires its own actual B analysis. This source is not a refutation of every possible beta. |
| Original 65-key G | DELETE 2,...,65; full descending 65,...,1 with KEEP 65,64,62,58,50; KEEP 1,...,31; KEEP 1; full KEEP 1,...,65; reverse KEEP 64,...,1. All 290 operations, A=237+C_close and the cost-15 reset at 161 remain. | The genuine R_irr pair at 132 stays an early short-scan event. A later full reset is not a discounted auxiliary copy of it. For erasure lifts A cost equality holds, but the original frontier-to-auxiliary-frontier comparison is unproved. |
| Route B generalized G_{p,q,s,L,r} | All parameter restrictions and complete prefix/closing words of Route B Section 9. N=2^{p+1}(q+1)+1, a'=3+2^{2s-1}<=L<=2^{2s+1}-1, s>=2,p>=2s,q>=1. Repeat (KEEP 1,...,L; KEEP 1) r times, with full preparation and final scans. | After the first reset, actual local repeats are complete-pair returns; A_r=A_1+(r-1)a_L, Q_r=Q_1+(r-1)q_L, q_L<=a_L. The proved complete ratio bound is beta_G=1/2+65c/96, uniformly in the parameters. No old chosen outputs issue fresh renewal demand on every restart. Full-copy-per-fragment closure has unbounded replication here. |
| Incoming-first-path counterexample | X={0,...,2m+1}, E_1=2(-,3), E_j=2j(E_{j-1},2j+1), T_0=0(-,1(-,E_m)); full all-KEEP word 1,2; 0,1,...,2m+1; 1;0. | The seam-crossing 0,1,2 fragment has length 3, first depth 1, but KEEP 2 has floor(m/2) doubles. Full B closure and A=B remain. Any proposed lift retaining only the incoming first path omits the actual successor ancestor frontier. The proper definition (5.1) retains it. |
| W_hit | Entire W_pq preparation, marked packet, added low hit, full increasing/reverse reset; cost includes ceil((m_0-a_i)/2) and the entire new forward scan. | One persistent obstruction key and one first-hit/exit event can serve arbitrarily many nested cover histories. They cannot pay one erased-frontier incidence independently. |
| W_star | All 235 operations and A=282; helper excursions P,Q; middle candidate fails its complete Pi at A(36,7,1); original valid pair is R_sep through [3,9]. | Erasing or relabelling B history does not transport original Pi membership automatically. Selecting the frontier avoids imposing these residual predicates on auxiliaries, but it does not preserve frontier geometry either. |
| W_5 | Complete 106-operation source, A=82+C_full_increasing, first LR signs (0,-1); edge (10,6,LEFT) dies and returns inside one B hit with changed descendants. | No intervening A exists between that deletion and recreation. A purported paid frontier mapping cannot count every reattachment or tuple return as a new original A resource. |
| Repeated 21-key I^r Z | Entire 34r+87 operations, fixed physical odd leaves/tail, A=32r+A(Z), full closing builder Z. | Persistent leaf 7 is not freshly born each copy. Actual nonleaf outputs and first-hit IDs differ. Population remains 21 in both the benchmark and every erasure lift; geometric reference count is not source cost. |
| Warmed-up closed repeat | Actual legal reaching prefix excluded; original marked S, complete physical low/gap hangers, full descending period and A-only ascending restoration; A=2(2^p-1). | The q-sized first wave in the prefix cannot fund auxiliaries or be charged again. W_z retains the full period's A-only tail, so (9.1) includes it in every auxiliary copy. |
| Campaign 15 | Entire r7 witnesses, actual six-key receipt, full reset and r-4 zero runs; all original owners fixed. | Refutes the specified leaf-only/fixed-lookback repair, not every relaxed nonlocal transfer. The construction of V_z changes no owner and provides no new free-image theorem. |
| Existing D6 physical lift | Full variable-size lifted H word with every genuine odd fringe and its closing builder; original full carrier and copy-by-copy Pi audit. | Fixed path-isolated windows already have an absolute paid bound. This is an inherited source-uniform controlled class, not a proof of contraction for all original frontiers or for G's remaining boundary. |

Two exact auxiliary-support checks sharpen the failure diagnosis.

First, one-key erasure does not preserve the other B paths even before alignment. From common R4 the complete word KEEP 4,3,2,1 closes, with A=5,Q=3. Its B trees after 4 and 3 are respectively
\[
4(1(-,3(2,-)),-),\qquad 3(1(-,2),4).
\]
Converting KEEP 3 to DELETE leaves the first of these B trees in place before KEEP 2. The old path 3->1->2 becomes 4->1->3->2. After KEEP 2,1, the erased B ends at
\[
1(-,2(-,4(3,-)))\ne R4.
\]
This refutes exact path preservation and same-one-copy closure for the naive erasure comparison. Section 8's actual recurrent alignment repairs closure, but does not restore the old paths or frontier incidences.

Second, a closed subword can change frontier classification when isolated. In the generalized G family, fix r>=3 and an interior additional post-reset word (KEEP 1,...,L; KEEP 1), numbered j with 2<=j<=r-1. It is a genuine paired return, with identical A/B lower operand paths and unchanged complete upper hangers. Its ending reset to 1 has initial B depth L-1. In the full G source, S=[N]; that reset anchors the following short, irregular low progression, rather than the final long closing scan. It therefore contributes a positive original first-depth surcharge. As a standalone cyclic closed auxiliary period, the same word has genuine support and carrier [1,L]. Its ending reset and the next copy's initial identity KEEP 1 belong to the same cyclic minimum block; the full increasing window from this block through L is long and covers every B double occurrence, including the reset. Its own mathcalF_B is ZERO. Hence original frontier records cannot simply be copied as the auxiliary quantity.

This is not a counterexample to a transfer allowing an immediate A payment: these local repeats have q_L<=a_L and are already payable. It is a counterexample to the claimed equality of original and isolated-auxiliary frontier definitions.

Finally, reversing a fine rotation ledger is not a free Pair Access closing word. In the complete three-key source KEEP 3; KEEP 1 from the right vine, after KEEP 3 both trees are the left vine rooted at 3. The first inverse B bit would promote 2 while keeping A rooted at 3. No original operation realizes that pair transition: a B move to root 2 requires KEEP 2 and ends A rooted at 2, while DELETE leaves B fixed. Additional legal helper operations could be considered only with their actual A cost and full endpoint proof. This refutes the naive reverse-ledger closing algorithm, not the existence of every legal return.

## 13. Global original and auxiliary event-overlap audit

For the selected V_z construction the A-overlap calculation is exact. Fix one original cost-one A StepEv e. For a fixed z it has L_z genuine auxiliary copies. Each has scalar weight 1/(rL_z), so its total weight for that z is 1/r; summing over r erasures gives one. Thus
\[
\sup_{e\in\mathcal E_A(W)}
\sum_{z,\ {\rm copies\ of}\ e}\lambda_z=1.
\tag{13.1}
\]
This is a complete global accounting of ALL auxiliary A work, not merely a per-fragment or per-generation statement. Real rotation and virtual-unit conventions stay separate. No auxiliary occurrence is physically identified as a new original donor.

At multiple recursive levels the same argument would bound total weighted A by one per level, or by kappa^k for a general cost multiplier. A strict beta would then produce geometric total effective weight. Without it, infinitely many levels can reuse the same normalized amount of original work; summing that amount is not an absolute A bound.

No analogous load theorem has been proved for the proposed frontier matching. A single original A root entry, SET loss or resetting rotation can affect many original B frontier histories. The supplied H/W_hit examples reject specified per-history uses of those events. Source-local donor units already owned in C14/C15 do not become vacant because the proof labels their occurrences by an erasure.

The construction compares alternative source executions by scalar weights. It never requires simultaneous cofunding of their donor ledgers, transports a transient prefix into a period, or overwrites an old frozen owner.

## 14. Final recurrence and full quantitative consequence, if proved

For completeness, the exact general bridge is established as a CONDITIONAL implication. Suppose an independent source rule supplies finite genuine admissible W_i, nonnegative lambda_i and absolute a,beta,kappa,d such that
\[
T(W)\le aA(W)+\beta\sum_i\lambda_iT(W_i),\qquad
\sum_i\lambda_iA(W_i)\le\kappa A(W),
\tag{14.1}
\]
\[
|X(W_i)|\le\max\{N_0,|X(W)|\}^{d},\qquad
\theta=\beta\kappa<1.
\tag{14.2}
\]
Zero-A auxiliaries contribute zero T. For n>=N_0 and each W of size <=n with A>0, the definition of the FINITE F_T gives
\[
\frac{T(W)}{A(W)}
\le a+\beta F_T(n^d)
\frac{\sum_i\lambda_iA(W_i)}{A(W)}
\le a+\theta F_T(n^d).
\]
Taking the supremum over W proves the claimed recurrence without assuming a maximizer. BB-BOOT then yields F_T(n)<=a/(1-theta) for every finite n, with small sizes handled as in Section 3.

One may instead expand only finitely many recursive levels. Each level has finitely many nodes. At depth k the total effective weighted A cost is at most theta^k A(W), and each leaf has population at most max{N_0,|X(W)|}^{d^k}. The inherited ceiling bounds the entire finite-level remainder by
\[
K_T\theta^k
g\!\left(\max\{N_0,|X(W)|\}^{d^k}\right)A(W).
\]
It tends to zero by Section 3. There is no infinite physical source, infinite set of new donor events, or unproved limiting-source admissibility.

For the selected T=mathcalF_B, (5.2) would therefore give the exact coefficient
\[
\boxed{Q_B(W)\le
\left(3C_{\rm seq}+\frac a{1-\theta}\right)A(W).}
\tag{14.3 — CONDITIONAL}
\]
For total Q the corresponding coefficient is a/(1-theta); for the unselected original R_irr it would be 32+6C_seq+a/(1-theta), at the inherited D5 scope. These are implications, not values of constants established by BB-01.

In the actual construction, (14.2)'s size bound and kappa=1 are proved, but (14.1)'s FIRST inequality with beta<1 is not. Consequently no final recurrence or unrestricted coefficient has been established. The near-optimality benchmark has been used as a ceiling for the terminal estimate and finiteness, not as a substitute for the missing physical one-step inequality.

## 15. First unsupported implication and alternative sufficient lemma

For this concrete construction, the first missing assertion is exactly
\[
\exists\,0\le a_E<\infty,\ 0<\epsilon\le1\quad\forall W\ (r\ge7):
\quad
\mathcal F_B(W)-(1-\epsilon)
\frac1r\sum_{z\in M}\frac{\mathcal F_B(V_z)}{L_z}
\le a_EA(W).
\tag{15.1 — OPEN}
\]
The candidate construction, closure, cost normalization and population bound preceding this assertion are proved. Its frontier domination and strict surplus are not.

To prove it geometrically one would need a source-specified rule for the lost/changed incoming-path and successor-frontier incidences, retaining all actual changes of carrier and fragment partition, and a globally bounded original A charge for the uncovered part. No such rule is obtained by looking at only the incoming path, local six-key patterns, one neutral renewal, a fixed lookback, or arbitrary primitive reversal.

| Exact attempted shortcut | Strongest proved case | Adversarial status | Weakest useful replacement and difficulty |
| --- | --- | --- | --- |
| Erasing a target preserves retained B paths/frontiers and one-copy closure | A trajectory is unchanged; recurrent closure (8.1) is valid | R4 calculation refutes the exact preservation claim | A paid incidence coupling between ACTUAL original and recurrent auxiliary frontiers. Its global gain is open; easier difficulty is not established. |
| Every <=6-target fragment has a <=6-support return to its starting pair | Already closed certified periods; conditional return-price identity | W_n,n>=12 refutes universal same-state restricted return | A specially constructed partition/auxiliary state with proved weighted return price and coverage. No such uniform construction is inherited. |
| First incoming path describes the whole difficult frontier | Path-preserving ancestor domain U and full terminal-side frontier are valid | Route B's complete three-target source refutes the first-path law | Retain successor ancestors and prove their global paid or discounted comparison. This is the selected missing physical step. |
| Each birth/reattachment creates an independent A unit | Actual distinct KEEP-gap witnesses; restricted seed and family-reset maps | H/W_hit sharing, W_5 within-hit return and I^r Z persistence refute stated shortcuts | An actual event rule with a proved all-history load bound. None for (15.1) is supplied. |
| Smaller weights or repeated full sources create beta*kappa<1 | Exact copy comparison and exact weighted erasure A identity | Algebra gives invariant beta*kappa; copy product is one | A change in represented physical obligation, not a normalization. This must be proved from source behavior. |
| C15 fixed lookback repairs all erased-owner frontiers | Raw channels, partial exchange and explicit nonlocal family reset repairs | r-4 zero runs refute every fixed own-unused lookback | A source-uniform nonlocal repair with actual eligibility and total load. It remains open; whole image impossibility was not proved. |

Allowing polynomially larger populations could support a different genuine lift in a future authorized investigation. The weakest sufficient quantitative replacement would still need source domination, complete weighted A accounting and effective product below one as in (14.1)–(14.2). Merely restating that package is not an independently easier lemma; none is accepted as proved here.

For the PARTICULAR same-universe erasure construction, the unstructured existence of a_E and beta<1 in (15.1) is equivalent, up to constants, to the selected frontier bound. In one direction, finite F_T(n) and (10.2) give the absolute bound. In the other, a known T<=CA makes (15.1) true with a_E=C and beta=0. That converse is a difficulty diagnosis, not a proposal to assume the target or to pay the entire frontier without a source proof.

There is therefore no demonstrated reduction of the original proof difficulty merely from writing (15.1). The independent constructive ingredient furnished here is the exact auxiliary source/cost interface; the contraction remains the substantive missing theorem. The benchmark remains useful as a rigorous terminal condition whenever a valid discounted physical comparison is obtained. Failure of this attempt does not refute it or URCD.

## 16. Verification limitations and dependency ledger

| Obligation | Result and precise qualification |
| --- | --- |
| BR-1 physical sources | Original semantics frozen; all V_z are genuinely reachable, fully paired-closed on X by (8.1). |
| BR-2 independent construction | Erasure and first-repeat alignment are specified without an assumed Q/A or T/A bound. The quantity comparison is not constructed. |
| BR-3 absolute constants | kappa=1, n_0=2,d=2 and K_mathcalF are explicit absolutes. No a_E or beta<1 is proved. |
| BR-4 strict discount | NOT ESTABLISHED. Rescaling and full-source copies do not establish it. |
| BR-5 complete auxiliary cost | Every original A access in every auxiliary period is counted; A(V_z)=L_z A(W). |
| BR-6 global overlap | Weighted A-StepEv load is exactly one; no frontier-to-A load rule is asserted. |
| BR-7 polynomial population | Same X, hence the required squared upper bound. Large recurrence multipliers affect operation count and are included in cost. |
| BR-8 no disguised target | Conditional transfer existence is explicitly distinguished from proof; the same-universe equivalence is diagnosed in Section 15. |
| BR-9 benchmark use | Frozen Route A ceiling; explicit terminal estimate, with no new competitiveness/comparator proof. |
| BR-10 upward implication | Complete conditional coefficient (14.3) is proved, but its missing source premise prevents a complete or substantive partial verdict. |

BB-BOOT and the source-normalized erasure equations are same-agent symbolic arguments. Route A/B, G0–D6 and the triad retain their recorded author-level qualifications and the inherited classical scan constant. C14 retains its accepted computer-assisted symbolic scope and historical same-agent separate implementation; hashes are not independent mathematical verification. C15 remains source-audited with final seal pending. No external/formal certification is claimed.

The source pins below were captured before report creation and rechecked after writing. Paths are relative to the repository root in Section 1.

| Read-only input, relative to repository root | SHA-256 |
| --- | --- |
| DO_RESEARCH_REBOOT/02_PROVED/PIVOT2_CONDITIONAL_REDUCTION.md | bf49cb509c811cc97721fa0c206e146da6a36528a5c6e982498f31be574bd5d3 |
| DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md | 8be55471edfdac31f59d552952c84f8d380bbfa3a7e46b7643d22af766757fd5 |
| DO_RESEARCH_REBOOT/IAGS12_CD6_TRANSFER_TRIAD.md | d820821ed22a084a57c6777cb9f14d7caf8e900f1824f779faaad11ec8fbd934 |
| DO_RESEARCH_REBOOT/IAGS12_D1_COLLISION_PROVENANCE.md | 0aa9cbf3e9cc036af5d4bbdf3ea3acdfcbef9341c856401b74247a615c4f814f |
| DO_RESEARCH_REBOOT/IAGS12_D2_RESIDUAL_REGENERATION_COST.md | 4b1623da997a7c1dbd40073809d198cfd8c850b48edc1db6b42b5655b1808b0e |
| DO_RESEARCH_REBOOT/IAGS12_D3_BLIND_GAP_COMPOSITION.md | 303f270f78d777932040e0e4f9ddd46cdd74f1835bdeaf1ad50f286bba1f02bc |
| DO_RESEARCH_REBOOT/IAGS12_D4_NEUTRAL_RENEWAL.md | f6d0d7d256064a5b456b13befe3d87c042f4b3105c3cf6604ab496139b9d34c2 |
| DO_RESEARCH_REBOOT/IAGS12_D5_BRANCH_RENEWAL_COST.md | 4a3cb7a156618489bf6d51ca51662f49b3fc8297b8fd99ad9086a0f6dc09c905 |
| DO_RESEARCH_REBOOT/IAGS12_D6_INTERRUPTED_SCAN_COST.md | a34f59c727cea9bf0921fa5305cae17d5097b9e6168f77ce1e1421e58625c875 |
| DO_RESEARCH_REBOOT/IAGS12_G0_QUANTITATIVE_BASELINE.md | 09863af3277745f5ebef956e680feb43a3d1ad4e5c7bb57bb545918c4813523a |
| DO_RESEARCH_REBOOT/IAGS12_PARALLEL_A_PERIODIC_NEAR_OPTIMALITY.md | aa4558285d1325f7cc05f9748de2d9c90ca6c4dbbefa3cddd627043ad7fe2bb4 |
| DO_RESEARCH_REBOOT/IAGS12_PARALLEL_B_BOUNDARY_SURCHARGE.md | 2571600e7ec3e6eca1711ad88d22dd5facf7f237e3e44e5b1b2d04a3afaec617 |
| DO_RESEARCH_REBOOT/PARALLEL_ROUTE02_STEP04_LINEAR_INCIDENCE_20261108/STEP04_LINEAR_INCIDENCE_SOURCE_GEOMETRY.md | 77702f3cb914d36a62adb5ba7511c141d92068b52680138997aefc845349e11a |
| DO_RESEARCH_REBOOT/RESEARCH_RULES.md | c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc |
| DO_RESEARCH_REBOOT/RG01_PRIMITIVE_ACCOUNTING.md | f46c0ee4e549ee8223bd97e4e28b364e415566129ad09df32558f5819500d7fa |
| DO_RESEARCH_REBOOT/RG02_EDGE_CONSERVATION.md | 16b93dbe5fa80a75da0591ad79765581ffc8a8c826b6f41758e985270de2253e |
| DO_RESEARCH_REBOOT/RG04_GLOBAL_REGENERATION.md | 52072e0c9a5214cf16b7bf44e3efb09df102e91e939bf3186b2e280b0763832b |
| DO_RESEARCH_REBOOT/ROUTE04_RELAXED_UNIVERSAL_CD_20261108/RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md | f85354f04eed727e3bdc4c0ddca72c1a6f706885c35721ced525ee52fa26e712 |
| DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json | 0ec0767e5212bda70b051a1e172464eed6c8c9a787937ea2601481cb438cc2cc |
| DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_THEOREM.md | 45ad72acb656ebec5b54f57715a71b4a37c04b67db00afc5894e084ba9702b1b |
| DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FINAL_VERDICT.md | 3f3b26059b9a8ab251572f088c92f9dad0279c06a5c42d30fe6f80a457f1387f |
| DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FULL_PROOF.md | 4b4a422fa81046012cb749a29cd86965faff9f5f88d0ce0c3fdf9f13a34357bb |
| DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/INDEPENDENT_AUDIT.md | 7b12661d5d16a4cb69af0f4ea40879f47d3fa7fd7570a6af70dcfd625525b70a |
| DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/SOURCE_SPEC.md | 2afc510aec106e3ec8ee0565d0a2db536410105b1dfa41917f1f3794c70d2546 |
| DO_RESEARCH_REBOOT/SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md | 0d60121dfd15db899c900e9bde73b0a9ca1354787f5682cbfe0070c69c8fa664 |
| DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md | a52487cfe212aa562b91406bb6006d2f9a9469bebcfd4e039d9cd224fc6d677b |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/AUDIT_CAP_CHECKPOINT.md | e06b238ca330a57d3788f3119e90369c48921a6427e2706750def0210c3c2ed3 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/FINAL_VERDICT.md | 0b0cb756bd02e934b8c5e49bdb313f8585c49135146b87b4ad5fa03f894798e6 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/FROZEN_OWNER_EXCHANGE.md | e376879f126cdf85c664869106caa86d954fab5f3233b212c9f954a06cbd24e6 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/GATE_U14_RECONSTRUCTION.md | 359344b572e5c935e51bcaa21aa6872ed59320166a3c86de9e34b8d541ddfe90 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/GLOBAL_GROUP_NONOVERLAP.md | 42eccb875ae68c48acc23b5012f65ffe5c6bb68290124252c3e641876e50b5ae |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/GROUPING_TO_TRANSFER_BRIDGE.md | 63ae75beb703555f8c773a7c5ee401e500f4a077401154c3c1681e20c435ac7f |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/GROUP_SIGNED_ACCOUNTING.md | a5723a101e51181a80441ab57ba10cd1b9a84f6e9db585b836cb7c05fa31d105 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/PHYSICAL_GROUP_SEEDS.md | 34e220831748b4cabc7294fb1124cdf4d6f5cdeab6dc9f493b3047eac65176e1 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/RESTRICTED_FAMILY_FUNDING.md | 11c8e816022bcc8154e22be67bf47121bad41b694123e9fdd42896b57598014c |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/SOURCE_OWNER_IMAGE_AUDIT.md | 086344f279d7b957ca1106148438511d6d83f1087692e83928c4c0200d501c6b |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/SOURCE_SPEC.md | 5c0025cf973850f190c5794b270cb993ac6aef7fe5beb41903b1b5cb8b2fac99 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md | 9a91782c35c91b92069367ba1bfcafd362dadb788bcd5f76ba217724fcbd6a75 |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_TRANSFER_VERDICT.md | 51fcaab21acd5c762e0dbcdb891872b6bc9cb9bfe05206be45b7df89a0cf417a |
| DO_RESEARCH_REBOOT/SE03_STEP3_UNIFORM_DONOR_GROUPING_15/ZERO_RUN_FAMILY_THEOREM.md | 7c333ad24b4e9251e52c1830915c020d468244b995385d9e132d6e1f3c53cc79 |

Complete earlier reads were reused only after current-byte equality was checked; newly required documents were read in full. No claim is made that every transitive C14 grammar/table certificate was independently reconstructed. The governing BB-01 request is the pasted attachment at C:/Users/Saif malik/.codex/attachments/16dc14d7-fb14-4e33-9699-f27d723821f8/Pasted text.txt.

Only this report is created/edited by this task. All historical sources, programs, resource records, event IDs, owners, other research reports, branch and HEAD remain untouched by this task. Static text/hash/certificate-entry checks do not run a source engine or charge a new semantic/audit allowance. No stored CPU cap is reset or treated as permission for further execution.

Final manuscript checks: all 17 required sections are present; the report was read back in full; all 40 listed current input hashes match their pre-write pins. Branch and HEAD are unchanged and the tracked Git diff is empty. Preexisting untracked reports are retained. These checks certify artifact preservation and text consistency, not the missing mathematical discount or any new independent audit.

## 17. Final verdict

**BB-01: BLOCKED.**

Established:

- A complete BB-BOOT proof with the terminal term retained, exact polynomial-orbit estimate, pointwise limiting argument, small-size/monotonicity qualification and a precise growth-orbit criterion.
- Explicit inherited ceilings for all three candidate quantities, including K_mathcalF from (5.4), and selection of the original physical frontier.
- A genuine recurrent-erasure auxiliary construction, same physical population, full exact A/B closure, and total weighted auxiliary A cost exactly A(W).
- Exact rejection of normalization-created discounts, first-path-only frontier lifts, naive inverse ledgers, and automatic same-state six-support fragment closure, at their stated scopes.

Not established: (15.1), an actual source-derived strict discounted comparison, any qualifying new arbitrary-depth partial-discount theorem, or an unrestricted URCD coefficient. The valid erasure correspondence is inherited structural infrastructure; it is not promoted to a substantive bootstrap success.

BEFORE: a slowly growing full-source ceiling was available, but no one-step discount. RESULT: the analytic terminal argument is complete, the selected source construction has exact cost and population bounds, and the first missing frontier-domination step is isolated. AFTER: the strict comparison remains open; no mathematical source-ratio refutation or Dynamic Optimality conclusion is made.

**STOP — BB-01 only. No later gate is executed.**

