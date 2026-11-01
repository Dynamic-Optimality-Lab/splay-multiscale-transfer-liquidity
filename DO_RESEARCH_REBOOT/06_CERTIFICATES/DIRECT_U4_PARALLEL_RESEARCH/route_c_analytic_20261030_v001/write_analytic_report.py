"""Append-only mathematical proof and bounded analytic verdict, no fits."""
from pathlib import Path
import json,hashlib,subprocess,ast,datetime
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]

def save(name,value):
    with (OUT/name).open('x',encoding='utf-8') as f:
        if isinstance(value,str):f.write(value.strip()+'\n')
        else:json.dump(value,f,indent=2)

def main():
    save('RA01_UNIFORM_ROTATION_IDENTITY.md',r"""
# Uniform source rotation identity for the complete joint-depth profile

**Status: exact universal source mechanics. This is a transport identity, not a signed repayment theorem.**

For finite present-key BSTs A,B on the same ordered keys, define

    H(A,B;z,w)=sum_y z^{d_A(y)} w^{d_B(y)}.

For a key subset E write H_E for its contribution measured in CURRENT GLOBAL depths, and e_y=z^{d_A(y)}w^{d_B(y)}. For an A rotation let T_s multiply every monomial by z^s; for a B rotation let T_s multiply by w^s. Negative exponents in the formal operator cause no actual negative depth, since those operators act only on regions deep enough to rise.

## Primitive rotation (all sizes, arbitrary hanging trees)

Consider a right rotation of child x over parent p, with x.left=L, x.right=M and p.right=R before rotation. The exact identity is

    H_after-H_before = (T_{-1}-I)(e_x+H_L) + (T_{+1}-I)(e_p+H_R).

M has zero depth displacement. Keys outside the old p-subtree are unchanged. The left-rotation formula is its reflection: the child-side outer subtree rises, the opposite parent-side outer subtree descends, and the middle subtree stays at the same global depth.

Proof: source _rot_right writes x.right=p and p.left=M, preserves the external attachment, and changes no internal hanging-tree pointer. Thus x and L rise one level; p and R descend one; M stays fixed. The other tree is frozen, so its depth exponent is unchanged. Summing the corresponding monomials proves the identity. _rot_left is exactly reflected. This proves arbitrary cardinalities and arbitrary internal A/B geometry without enumeration.

Sources: python/liquidity/legacy_embedding.py:_rot_right (line77), _rot_left (line92), splay_trace (line107); python/independent/splay.py:_rebuild (line92). These are PHYSICAL splay operations, not symbolic high witnesses.

## Source StepEv composition

For each double, T1..T4 are the four hanging subtrees in inorder. Region monomials below always use their actual pre-StepEv global joint depths.

|Kind|Depth -2|Depth -1|Depth +1|Depth +2|Depth unchanged|
|---|---|---|---|---|---|
|LL|x,T1|T2|T3|g,T4|p|
|RR|x,T4|T3|T2|g,T1|p|
|LR|x|T2,T3|g,T4|none|p,T1|
|RL|x|T2,T3|g,T1|none|p,T4|

Definitions: LL has T1=x.left,T2=x.right,T3=p.right,T4=g.right; RR is its reflection. LR has T1=p.left,T2=x.left,T3=x.right,T4=g.right. RL has T1=g.left,T2=x.left,T3=x.right,T4=p.right.

The formula for a row is the sum over its nonzero columns of (T_s-I) times the listed region profiles. For example,

    Delta_LL H = (T_-2-I)(e_x+H_T1)+(T_-1-I)H_T2
                 +(T_+1-I)H_T3+(T_+2-I)(e_g+H_T4).

The source performs parent-over-grandparent THEN target-over-parent for LL/RR, and target-over-parent THEN target-over-grandparent for LR/RL. Substituting the primitive identity in that order yields the table. It is valid independently in A or B, with z or w shifts respectively. Both zig orientations are already the primitive identity. Reflection preserves all depth exponents after the corresponding key relabeling.

Checks: evaluate z=w=1 to obtain cardinality conservation. An A rotation preserves H(1,w), and a B rotation preserves H(z,1). The first depth moments reproduce the historical total-depth formulas in scripts/wp6_symtable.py; those first-moment formulas are inherited, not new discoveries.

## Whole access

Sum these exact identities along the actual A trace and then along the actual B trace, with DELETE omitting the latter. Regions/profiles must be refreshed at each step. One cannot substitute a single source profile for every later occurrence of a changing region. In particular, commuting formal shift operators does not license commuting changing SOURCE regions.

The identities hold for every n. However H does not specify the region decomposition H_L,H_M,H_R (nor the double word). Hence the identity is not a deterministic update on global H alone. RA02 gives an exact same-input/different-output example and its arbitrary-fringe extension.

This reconstructs and strengthens the explicit algebra of the older wp6_jointupdate.py rigid-carrier mechanics. It does not by itself bound a nonlinear function F(H_after)-F(H_before), allocate credits, or prove CD-U. No potential-existence assertion is smuggled into the statement.
""")
    save('RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md',r"""
# Zero-helper arbitrary-fringe identity and exact nonclosure theorem

**Status: source-exact universal family identity; deterministic summary-update claim REFUTED.**

Let c1<...<c6 be ordered core keys. Let U,V be ANY two BSTs on the same m additional keys in the open interval (c4,c5); m may be zero. A tree is written k(left,right), and omitted children are empty.

Define

    A = c6( c2(c1, c3(empty,c4(empty,c5(U,empty)))), empty ).

Both B variants have outer skeleton c6.left=c5, c5.left=c4, c4.right=V, and all other outer children empty. Their c4.left trees differ:

    L: c1.right=c2, c2.right=c3;
    R: c3.left=c2, c2.left=c1.

Access x=c2 with KEEP. In both variants d_A(x)=1 and d_B(x)=4, hence a=1,q=2 and 2a-q=0. A performs one left-oriented zig. B_L performs LR then LL; B_R performs LL then LL, in exactly the source order. The input root labels are the SAME c6,c6; the output root labels are the SAME c2,c2.

Put C(z,w)=H_{additional keys} before the access. More explicitly C=z^5 w^3 J_{U,V}, where J is the internal paired-depth profile of U,V. The roots/internal shapes of U and V may differ; only the common ordered key set is required. No access descends into them.

## Depth tables prove the identity

|Core key|A before|B_L before|B_R before|A after|B_L after|B_R after|
|---|---|---|---|---|---|---|
|c1|2|3|5|1|1|1|
|c2|1|4|4|0|0|0|
|c3|2|5|3|2|3|2|
|c4|3|2|2|3|2|3|
|c5|4|1|1|4|1|1|
|c6|0|0|0|1|2|2|

The c1/c3 swap has equal A depth, so both input global histograms are identical. The A fringe root stays at depth5. In B_L it stays at depth3, whereas in B_R it moves to depth4. Every fringe key moves rigidly by the same amount; its internal structure is untouched.

Consequently, with H0 the common input and HL/HR the two outputs,

    H0(C)=1+z*w^4+z^2*(w^3+w^5)+z^3*w^2+z^4*w+C,
    HL(C)=1+z*w+z*w^2+z^2*w^3+z^3*w^2+z^4*w+C,
    HR(C)=1+z*w+z*w^2+z^2*w^2+z^3*w^3+z^4*w+w*C.

Subtracting gives the exact uniform identity

    HR(C)-HL(C) = (w-1)[C+z^2*w^2*(z-1)].

This is an identity in the formal polynomial ring Z[z,w,C], so substitution of ANY realizable fringe polynomial C is permitted. It was also independently checked symbolically. Arbitrary m/internal geometry enter only through C; there is no finite-n induction guess.

## What is refuted

There is no deterministic successor-histogram rule using only (n,rootA,rootB,H,accessed key,dA,dB,a,q). All these inputs agree between the variants for each fixed U,V, yet the output histograms differ. Even C=0 suffices: the remaining 2x2 mixed term is nonzero. For C nonempty, its A exponents are>=5 and cannot cancel the core difference at rows2/3.

This does NOT refute an arbitrary nonlinear potential F(n,rootA,rootB,H): one potential can satisfy inequalities for more than one successor. The previous quotient construction correctly retained this nondeterminism. At m=1, reading the existing seven-key table gives Phi7=-2 at both inputs and -3 at both outputs, also after reflection. No table was refitted; the zero edge has potential drop1, and that is legal.

## Physical-domain reachability and closure

These are real present-key BSTs, not symbolic abstract-only witnesses. For any m, n=6+m>=4. Levy–Tarjan v3 Theorem3.4 provides splay request sequences between any same-key BSTs of that size. Starting from a common diagonal, KEEP requests can reach (B,B), then DELETE requests reach (A,B). After the selected KEEP, DELETE requests align A' to B', and KEEP requests return both to the common diagonal. Thus these helpers occur inside admissible exactly closed original Pair Access walks. This argument uses existence of connecting source requests, not a sign bound.

Primary source: [Levy–Tarjan, Theorem3.4](https://arxiv.org/html/1907.06310v3#S3). The theorem was checked directly. Independently, the m=0 controls include complete explicit connecting words and full pointer/frame replays. Their totals are (A,Q)=(16,4) and (20,5), so neither is a Coarse-Double counterexample.

Controls at m=0,1,2,5 and both mirrors verify the algebra/source wiring only; they do not replace this arbitrary-fringe proof. There were zero finite fits and zero larger finite graph searches.
""")
    save('RA03_UNIFORM_MOMENT_REPAIR_OBSTRUCTION.md',r"""
# Uniform obstruction to depth moments plus bounded nonlinear repair

**Theorem.** Fix any real alpha, any beta>0 and any finite K. No source potential

    Psi(A,B)=alpha*D_A(A)+beta*D_B(B)+R(A,B)

can satisfy q-2a<=Psi(source)-Psi(destination) on every admissible original transition if D_A,D_B are sums of edge depths and R has oscillation at most K on each n-key state domain, uniformly in n. R may otherwise depend on both full trees, n, labels, nonlinear statistics or hidden joint structure. A size-dependent additive gauge does not matter. Alpha and beta are fixed constants, not functions growing with n.

**Proof.** Apply the R branch of RA02 with m arbitrary. Differentiate its profile in z or w and evaluate at z=w=1. The source core A-depth sum is12 and destination sum11; the fringe's A depths are unchanged. Hence Delta D_A=-1. B's core sum goes15 to9, while every fringe node descends one level. Thus Delta D_B=m-6.

The access has a=1,q=2, so the required inequality is Delta Psi<=0. But

    Delta Psi = -alpha+beta*(m-6)+Delta R
              >= -alpha+beta*(m-6)-K.

Choose an integer m>6+(alpha+K)/beta, with m>=0. Then Delta Psi>0, contradiction. RA02 proves physical admissibility for every such m. This proves the all-size exclusion without any larger fit or sampled tail argument. Reflection gives the same obstruction in the other orientation.

Equivalently, a repair of this positive-B-moment strategy must have a DROP on the zero helper of at least beta*(m-6)-alpha, growing linearly with the fringe size. A fixed range-two joint correction, root/vine bits or any other uniformly bounded correction cannot repair that strategy globally.

**Scope limits.** This excludes the specified moment-plus-bounded-repair architecture. It does not exclude beta<=0, n-dependent moment coefficients, a genuinely unbounded nonlinear correction, a nonlinear histogram potential with no such decomposition, a structural full-tree invariant, or a justified macro potential. It does not refute any CHR/FRC theorem at its certified scope. In particular RA02 contains no negative-weight closed walk.

Historical comparison: depth sums and their fringe-recharge failure were already recorded in PIVOT_CONSTRAINT_GUIDED_DUAL.md and wp6_symtable.py. The new explicit arbitrary-fringe zero-helper family gives a uniform quantitative obstruction covering arbitrary bounded JOINT repair, rather than announcing an old depth-moment idea as a new viable candidate. This is strategic elimination, not a positive CD-U proof leaf.
""")
    save('RA04_NECESSARY_PROFILE_TESTS_AND_GATE.md',r"""
# Exact interface for a future nonlinear joint-depth construction

Write F_{n;rA,rB}(H) for a proposed potential over the complete joint-depth histogram and exact roots. RA02 gives NECESSARY, explicitly source-realized constraints, for every realizable C=z^5w^3 J_{U,V} on m keys:

    F_{6+m;c2,c2}(HL(C)) <= F_{6+m;c6,c6}(H0(C)),
    F_{6+m;c2,c2}(HR(C)) <= F_{6+m;c6,c6}(H0(C)).

Both are forced by weight-zero helpers. This is a fixed six-core, all-fringe family, not a replacement equivalent to full Coarse-Double. It is an acceptance test for a CONCRETE proposed F, not a new global existence premise. There is no assertion that satisfying this family is sufficient for CD-U.

The exact rotation identity remains conditional on REGION profiles and source orientation. These are physical source data. The global histogram does not determine them. It is therefore invalid to derive a deterministic scalar recurrence by silently replacing those conditional profiles with global H or deleting zero-weight helpers.

What the seven-key table establishes is that the finite successor inequalities can be simultaneously satisfied there. Reading it at the m=1 family controls confirms a drop of1 on each branch. No uniform formula or induction follows from that coincidence.

## Four-rule disposition after the analytic audit

- Rule1: the specified deterministic summary-closure shortcut is now refuted exactly, including an all-size rigid-fringe family.
- Rule2: the mechanical identity is proved by source rotation writes; its arbitrary-C algebra and closed source controls verify it independently. Turning it into a signed nonlinear F inequality still lacks a construction.
- Rule3: the one registered profile-transport obstruction mechanism is complete. No larger graph, fit, extra feature or automatic successor was run.
- Rule4: the positive moment-plus-bounded-repair candidate class is eliminated analytically; no original CD-U sign obligation is newly discharged. A positive universal repayment campaign still does NOT pass this rule.

The first unsupported implication is now explicit:

    exact region-profile transport, with arbitrary C and both hidden orientations
        => an explicit nonlinear F with the required signed transition bounds.

That is not supplied by the identity. Naming a new invariant, assuming a fringe-capacity law, or restating maximum future excess would hide the same construction burden. No such replacement is made.

BEFORE: finite joint-depth table; no uniform update proof.
RESULT: exact arbitrary-n transport formulas; explicit complete-histogram nonclosure on zero helpers; uniform moment/bounded-repair exclusion.
AFTER: generic nonlinear histogram and general source-exact Route C remain OPEN. Net positive CD-U advancement:0. Net strategic result: a deterministic-closure shortcut and a bounded repair of positive B moments are unavailable.

The next positive campaign requires a specific function or source recurrence whose nonlinear change can be bounded on these arbitrary profiles as well as on B-double consumers and overwritten setups. No candidate currently has that proof mechanism. RESEARCH_RULES.md forbids converting this missing construction into another equivalent open premise, or continuing the same non-advancing mechanism by renaming it. The source audit therefore stops at this precise interface, without a permission request or a larger fit.
""")
    save('RA05_FINAL_REPORT.md',r"""
# Route C analytic continuation — uniform identity and exact obstruction

Started 2026-10-30; completed following the updated client date 2026-10-31, Asia/Karachi.

**Uniform source rotation transport is proved. It does not yet extend the seven-key potential to a universal signed invariant.**

For a B right rotation of child x over parent p, with outer subtrees L=x.left and R=p.right, and H the complete joint A/B depth polynomial,

    Delta H = (w^{-1}-1)(e_x+H_L)+(w-1)(e_p+H_R).

The middle subtree contributes zero. For A rotations replace w by z. The exact LL/RR/LR/RL transport table is in RA01, derived in source order with arbitrary hanging profiles.

The decisive analytic test is an arbitrary-fringe family of zero-weight helpers. Two source pairs have the same n, roots, COMPLETE joint-depth histogram, accessed key and costs dA1,dB4,a1,q2. Their successor histograms differ by

    HR-HL=(w-1)[C+z^2*w^2*(z-1)],

where C is the profile of an arbitrary paired fringe. The two possibilities come from LR/LL versus LL/LL bottom-up B rotations. This refutes a deterministic histogram-only successor recurrence. It does NOT refute an arbitrary nonlinear histogram potential that handles both successors.

For a fringe with m nodes, both helpers have Delta D_A=-1; their B total-depth changes are -6 and m-6. Hence ANY fixed positive B-depth coefficient plus a uniformly bounded joint correction fails the required inequality for large enough m. RA03 gives the full all-size proof and its precise limits. An unbounded nonlinear repair or a different structural potential remains possible.

Verification:16 prescribed whole-access controls,48 exact StepEv profile identities covering both zigs and all four double orientations, two fully closed physical six-key walks, and independent polynomial/source replay all PASS. Existing Phi7 values were only READ at the m=1 points: -2->-3 on both branches. No finite fit, graph enlargement, solver invocation or Stage11G edit occurred.

The four-rule audit is preserved in RA00 and RA04. The unresolved universal step is an explicit F with signed bounds for all legal profile transports. The identity alone is not such a bound; no equivalent conjecture is substituted. Universal Coarse-Double and Dynamic Optimality remain OPEN.

Primary files: RA01_UNIFORM_ROTATION_IDENTITY.md; RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md; RA03_UNIFORM_MOMENT_REPAIR_OBSTRUCTION.md; RA04_NECESSARY_PROFILE_TESTS_AND_GATE.md; profile_transport_controls.json; six_key_closed_controls.json; independent_audit.json; proof_status_ledger.json; final_integrity.json.
""")
    save('RA06_REPRODUCIBILITY.md',r"""
# Reproduction and exact coverage

Copy only verify_profile_transport.py and verify_saved_controls.py to a fresh sibling directory at the same depth, and run from the pinned repository root:

    python -X utf8 -B <fresh-run>/verify_profile_transport.py
    python -X utf8 -B <fresh-run>/verify_saved_controls.py

Outputs use exclusive creation. No old artifact is overwritten. Python -B avoids caches; no dependencies are installed. The first script follows the exact pointer rotation order, verifies each profile change by the universal regional formula and cross-checks whole accesses with the independent tuple/frame engine. The second independently reruns full accesses through the ordinary pointer splay_trace and checks the formal difference in Z[z,w,C].

The prescribed controls are m=0,1,2,5, both branches and both orientations,16 accesses total. These are algebra/source regressions, not finite-fit or universality evidence. Universal quantification comes from the symbolic depth table and rigid-subtree proof. No collection of larger paired states is enumerated.

Two fixed six-key source cycles are replayed in full:11 and13 accesses, totals (A,Q)=(16,4),(20,5). A single-tree BFS located their connecting request words; no potential was fitted. Full words/states/costs are saved, not merely roots or abstract summaries.

Entry pins include the physical engines, historical mechanics/audit, the inherited seven-key potential, frozen Stage11G rule file and original low/high compilers. final_integrity.json compares those exact bytes and branch/HEAD/tracked state. Active unrelated untracked Stage11G work is left untouched and is not claimed frozen by this campaign.

Scope: source mechanics and the analytic no-go have arbitrary n. The positive CD-U theorem and any generic all-size nonlinear histogram invariant remain unproved. There is no negative physical Coarse-Double cycle claim.
""")
    save('proof_status_ledger.json',{'client_completion_date':'2026-10-31','timezone':'Asia/Karachi',
      'claims':[
       {'id':'RA-TRANSPORT','status':'PROVED UNIVERSAL SOURCE IDENTITY','scope':'physical primitive/StepEv depth-profile transport, arbitrary hanging trees','proof':'RA01_UNIFORM_ROTATION_IDENTITY.md','positive_signed_invariant':False},
       {'id':'RA-ZERO-HELPER-FRINGE','status':'PROVED UNIVERSAL FAMILY IDENTITY','scope':'six-core helpers with arbitrary paired fringe, all m','proof':'RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md'},
       {'id':'RA-DETERMINISTIC-HIST-UPDATE','status':'REFUTED EXACT','claim':'deterministic next histogram from complete input H,roots,key,source depths/costs','all_histogram_potentials_refuted':False},
       {'id':'RA-POSITIVE-B-MOMENT-BOUNDED-REPAIR','status':'REFUTED ANALYTICALLY ALL SIZE','scope':'fixed alpha, beta>0; repair oscillation bounded independently of n','proof':'RA03_UNIFORM_MOMENT_REPAIR_OBSTRUCTION.md'},
       {'id':'RA-CONTROLS','status':'FINITE EXACT','whole_accesses':16,'StepEvs':48,'closed_cycles':2,'new_fits':0},
       {'id':'RC-NONLINEAR-HIST-ALL','status':'OPEN'}, {'id':'RC-GENERAL','status':'OPEN'},
       {'id':'CD-U','status':'OPEN'}, {'id':'DYNAMIC-OPTIMALITY','status':'OPEN'}],
      'net_positive_CD_U_proof_advancement':0,'Stage11G_changed':False,
      'universal_positive_campaign_gate':'NOT PASSED: no constructed F or signed all-profile update bound'})
    entry=json.loads((OUT/'entry_source_pins.json').read_text(encoding='utf-8'))
    changes=[p for p,h in entry['files'].items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    good=not changes and git('rev-parse','HEAD')==entry['head'] and git('branch','--show-current')==entry['branch'] and not git('status','--porcelain=v1','--untracked-files=no')
    save('final_integrity.json',{'status':'PASS' if good else 'FAIL','source_files_compared':len(entry['files']),
         'source_changes':changes,'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
         'tracked_tree_clean':not git('status','--porcelain=v1','--untracked-files=no'),'Stage11G_modified':False})
    for p in OUT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
    save('delivery_manifest.json',{'main_report':'RA05_FINAL_REPORT.md','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}})
    print(json.dumps({'source_identity':'PROVED UNIVERSAL','moment_plus_bounded_repair':'REFUTED ANALYTICALLY','all_size_repayment':'OPEN','new_fits':0,'integrity':'PASS' if good else 'FAIL'}))

if __name__=='__main__':main()
