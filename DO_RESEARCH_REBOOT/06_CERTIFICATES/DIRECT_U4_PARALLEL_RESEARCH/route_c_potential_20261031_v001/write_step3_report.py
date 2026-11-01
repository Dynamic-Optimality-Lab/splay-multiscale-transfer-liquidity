"""Append-only report of one explicit Step3 candidate and its analytic refutation."""
from pathlib import Path
import json,hashlib,subprocess,ast,datetime
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]

def save(name,value):
    with (OUT/name).open('x',encoding='utf-8') as f:
        if isinstance(value,str):f.write(value.strip()+'\n')
        else:json.dump(value,f,indent=2)

def main():
    cert=json.loads((OUT/'explicit_potential_countercertificate.json').read_text(encoding='utf-8'))
    audit=json.loads((OUT/'independent_audit.json').read_text(encoding='utf-8'))
    if audit['status']!='PASS':raise AssertionError('independent audit required')
    save('SP01_EXPLICIT_UNIFORM_DEFINITION.md',r"""
# One explicit uniform A/B potential candidate

Fix r=1/8. For same-key finite BSTs define

    G(A,B)=sum_y 8^{-d_A(y)} d_B(y),
    Psi(A,B)=max_T [G(T,B)-rho(A,T)],

where T ranges over all BSTs on the SAME ordered key set and rho is the undirected unit-cost primitive rotation distance. No coefficient, potential label or distribution is fitted. Primitive rotations connect the finite BST set, for example by transformation through a right vine, so the maximum is finite and attained. This is one constructive function for every n; computational efficiency is not a proof premise.

This formula is an explicit static optimization, not maximum future Pair Access excess. Its data are only the current A,B and a separately specified primitive metric. No cycle-sign/feasibility assumption is embedded in the definition. It uses full A geometry, not just its root or a fixed shadow.

G itself lies in the historically refuted additive joint-depth family and is NOT proposed as a complete potential. Its useful partial bounds are proved separately in SP02. Psi is the nonlinear repair being audited: it is not rho(A,B), and it is not an arbitrary assignment of unknown potential values.

The max-envelope construction was not found in the inspected repository sources. This is a scoped repository observation, not a literature novelty claim. Old failures and constraints were read before this test: PIVOT_CONSTRAINT_GUIDED_DUAL.md, REWEIGHTING_BRIDGE_AUDIT.md, wp6_rotdist.py and the existing Route C analytic reports.

Raw G is not the final answer. The principal question is whether its root-conditioned B repayment survives the repair that guarantees the A/DELETE law. SP03 gives both the successful A law and an analytic NO for that transfer.
""")
    save('SP02_RAW_GEOMETRIC_RESERVE_LEMMAS.md',r"""
# Uniform positive bounds for the raw geometric reserve, and its precise failure

These are source-exact ALL-SIZE partial laws. They do not make G a complete potential.

## 1. Finite binary mass budget

For r=1/8, at depth j a binary A tree has at most2^j nodes. Therefore

    sum_y r^{d_A(y)} < sum_{j>=0}(2r)^j = 4/3,
    sum_{y!=root(A)} r^{d_A(y)} < 1/3.

No key-count or balanced-tree assumption enters this bound.

## 2. Every root-conditioned B splay repays q

Assume A is rooted at the accessed key x. Keep A frozen and splay x in B, whose initial x-depth is d. The banked physical source lemma 26AL-L1 states that every other key's B depth increases by at most2 under one whole splay. Key x, of A-weight1, drops its B depth by d. Thus, for d>=1,

    G(A,S_xB)-G(A,B) <= -d + 2*sum_{y!=x} r^{d_A(y)}
                     <= -d+2/3
                     <= -floor(d/2)-1/3.

For d=0 the B tree is unchanged. Hence every starved KEEP, including a zero-demand B zig, is paid by G, uniformly in n and every fringe configuration.

Source dependency: DO_RESEARCH_REBOOT/02_PROVED/26AL_generalized_signed_repayment.md, 26AL-L1, derived there from the bottom-up frame/source rotation geometry. No Coarse-Double or U4 claim is a premise.

This directly handles the CONSUMER part of every overwritten-setup family: no latest-arrival credit pool is used. It does not say that the preparatory DELETEs obey G's budget.

## 3. Both arbitrary-fringe zero-helper branches are safe for G

Use the source-exact H0(C),HL(C),HR(C) family of route_c_analytic_20261030_v001/RA02. Since G(A,B)=partial_w H(r,1), its exact whole-access changes are

    Delta G_L = -r-5r^2 = -13/64,
    Delta G_R = -r-6r^2+r^3+C(r,1).

The fringe is attached at A depth5, so C(r,1)=r^5 sum_{y in U}r^{d_U(y)} <= r^5/(1-2r)=1/24576. Consequently

    Delta G_R <= -111/512+1/24576 = -5327/24576 < 0.

Both helpers have a=1,q=2 and require nonincrease. These inequalities hold for arbitrary m and arbitrary internal A/B fringe shapes, also after reflection. Exponential A-depth damping defeats the earlier unbounded passive-fringe DEPTH-MOMENT increase here. No fringe-size fit is used.

## 4. G still fails the DELETE law

Let n>=6, let M be ANY BST on2..n-1, and set

    A = 1(empty,n(M,empty)),
    B = 2(1, right-vine on3..n).

DELETE n is one A zig. The middle subtree M keeps its A depths, while weights at1 and n swap1 and r. Since d_B(1)=1 and d_B(n)=n-2,

    Delta G=(1-r)(n-3)=7(n-3)/8.

This exceeds the2a=2 budget at n>=6 (n6 gives21/8). Thus G is NOT a potential satisfying the complete source inequality. Its starved-consumer and specific zero-helper successes cannot be promoted to survival of whole overwritten-setup histories.

The repair Psi addresses exactly this missing A-motion budget. The next document proves that repair's law and exposes its failure on B repayment.
""")
    save('SP03_ENVELOPE_LAW_AND_ALL_SIZE_REFUTATION.md',r"""
# The envelope has the universal DELETE law but loses B repayment

## 1. Universal A-motion law

Each function A->G(T,B)-rho(A,T) is1-Lipschitz in the rotation metric by triangle inequality. The maximum over T is therefore1-Lipschitz:

    |Psi(A',B)-Psi(A,B)| <= rho(A,A').

Taking T=A also proves Psi>=G>=0. Since G(T,B)<(4/3)max_y d_B(y), Psi is finite with range allowed to grow with n. It is the least1-Lipschitz majorant of G in the A variable: any such majorant dominates every term G(T,B)-rho(A,T), hence dominates their maximum.

An ordinary source splay from A to S_xA uses exactly d_A(x) primitive rotations. Thus

    Psi(S_xA,B)-Psi(A,B) <= d_A(x) <=2 ceil(d_A(x)/2).

This proves the required DELETE inequality for EVERY finite A,B and present x.

If the root-conditioned B-splay law also held for Psi, the actual A-then-B execution of a KEEP would give the whole source bound by addition. There is no extra unknown capacity theorem. But the B law is false.

## 2. Analytic counterexample for every n>=6

Use the same A,B family as SP02: A root1, its right child n, arbitrary M on2..n-1 below n.left; B root2,left child1,right vine3..n. Access x=1 with KEEP. Then a=0, d_B(1)=1, q=0,z=1. The required potential change is<=0.

Let T* maximize the SOURCE value G(T,B)-rho(A,T). We first show root(T*)!=1.

For any T rooted at1, its root contribution is d_B(1)=1. The remaining A-style weights total<1/3, and every B depth is<=n-2. Therefore

    G(T,B)-rho(A,T) <=1+(n-2)/3.

On the other hand, let Tn be obtained from A by the single root zig splaying n. Its rotation distance from A is1 and its G value is at least d_B(n)=n-2. Hence

    Psi(A,B) >= n-3.

For n>=6, n-3>1+(n-2)/3. Every maximizing T* is therefore rooted away from1.

After the B zig at1, key1 rises one level and EVERY other B key descends one level. For ANY T rooted away from1, r^{d_T(1)}<=r while total weight is>=1. Consequently

    G(T,S_1B)-G(T,B)
      = sum_y r^{d_T(y)} -2r^{d_T(1)}
      >=1-2r=3/4.

Evaluate the DESTINATION maximum at the old maximizer T*. The metric penalty uses the same A and cancels:

    Psi(A,S_1B) >= Psi(A,B)+3/4.

This violates the required nonincrease for a=q=0. The failure is a genuine legal whole KEEP, not a proposed micro-step condition or a mismatched symbolic endpoint. It is analytically uniform in n>=6 and arbitrary M. A fixed n6 source replay embeds it in an exactly closed Pair Access walk from a diagonal.

Mechanism: the Lipschitz maximum suppresses expensive A-root changes by allowing a different auxiliary root to dominate the reserve. That root does not equal the access target. Its positive bystander motion reverses the raw reserve's target-conditioned repayment. The same maximizing T can be reused at the destination, so no compatibility or existence gap remains in the contradiction.

## 3. Same-family parameter corollary, without tuning or another search

For any fixed0<r<1/4 and fixed metric coefficient lambda>=0, the envelope max_T[G_r(T,B)-lambda rho(A,T)] fails for sufficiently large n. Put s=2r/(1-2r)<1. Root1 candidates score at most1+s(n-2), while the one-rotation root-n candidate scores at least n-2-lambda. Choose (1-s)(n-2)>1+lambda. A maximizing root is again different from1, and the B zig increases its score by at least1-2r>0.

This is an immediate algebraic corollary of the same witness, not a parameter fit or a second campaign. The fixed audited candidate remains r=1/8,lambda=1. No replacement parameters were tested.

## 4. Scope

This refutes this explicit least-majorant construction and the stated fixed-parameter family. It does not refute every A-Lipschitz potential, every possible nonlinear repair, an unbounded structural reserve, or Route C. Pointwise domination Psi>=G does NOT preserve transition differences. A larger majorant could have different differences; no such construction is asserted.

The raw positive lemmas and the envelope's positive DELETE lemma are separate true statements. Combining them across two different functions is invalid. Universal Coarse-Double remains OPEN.
""")
    word=' '.join(mode+str(x) for mode,x in cert['closed_physical_witness']['word'])
    save('SP04_EXACT_COUNTEREXAMPLE.md',r"""
# Exact source countercertificate for the explicit candidate

Use keys1..6. Let M be the median-recursive BST on2..5 (root4,left3 with left2,right5), and

    A = 1(empty,6(M,empty)),
    B = 2(1,3(empty,4(empty,5(empty,6)))).

KEEP1 leaves A unchanged and makes B the right vine1..6. It has a0,q0,z1.

Exact function evaluation gives

    Psi(source)=405/128,
    Psi(destination)=16625/4096,
    increase=3665/4096 >0.

Thus the whole-access signed inequality fails. The raw G DELETE6 comparison increases by21/8, exceeding its budget2, whereas Psi's DELETE budget is already guaranteed analytically.

The evaluation enumerates exactly132 SINGLE-tree BSTs and660 directed primitive-rotation arcs. It does not fit any potential label or scan a larger Pair Access graph. There are no free parameters. Distances are proved exact by actual predecessor paths plus1-Lipschitz inequalities on every rotation edge. The independent verifier rebuilds those edges from the pointer source and recomputes all264 source/destination expression values.

The failed edge occurs inside this complete original closed word, starting both trees at B:

    """+word+r"""

The certificate includes every source/destination tree, source event trace and cost. Total A=15,Q_B=0,Z_B=2, with exact paired closure. It is not a Coarse-Double counterexample; it is a counterexample to the frozen candidate. No B zig or weight-zero operation was erased.

Files: explicit_potential_countercertificate.json contains all states, all formula terms, complete metric certificate, maximizing trees, failed edge and closed word. independent_audit.json verifies these without importing the candidate evaluator. The all-n proof is in SP03; this fixed evaluation is an independent control, not its universality argument.
""")
    save('SP05_FINAL_VERDICT_AND_GATE.md',r"""
# Step3 verdict — explicit candidate constructed and refuted

**CANDIDATE REFUTED. No valid complete uniform Route C potential found.**

The written four-rule gate preceded execution. The fixed construction was

    G(A,B)=sum_y8^{-d_A(y)}d_B(y),
    Psi(A,B)=max_T[G(T,B)-rho(A,T)].

New analytic conclusions at their precise scope:

- G pays EVERY B splay once A is rooted at its target, uniformly in n. This covers overwritten-setup CONSUMERS without eligibility matching.
- G's two prior arbitrary-fringe zero-helper changes are negative uniformly in fringe size and internal geometry.
- G fails cheap preparatory DELETEs, so the preceding successes do not make it a complete potential.
- Psi is an explicit uniform function and satisfies every DELETE bound by metric Lipschitzness.
- Psi loses the B law: a starved weight-zero B zig increases it, analytically for every n>=6. The n6 increase3665/4096 is independently certified.

The first failed bridge is therefore concrete:

    root-conditioned B repayment of G
      does NOT transfer through its least rotation-Lipschitz majorant in A.

The optimizer can select an auxiliary root different from the accessed root. Assuming those roots coincide would hide the missing—and false—implication. No such assumption is retained.

Four-rule outcome: the bounded fixed-candidate audit is COMPLETE with an exact refutation. Its positive universal premises are exposed separately and not combined across different functions. Net positive CD-U proof advancement0; strategic elimination of one explicit repair mechanism. The gate's first-refutation stop is obeyed: no coefficient changes, larger fits, replacement envelopes or equivalent new existence premise were executed.

Both original Step3 acceptance families are now more precise tests for a future construction. It must keep preparatory work without relying on latest setup IDs, damp passive fringes, and preserve ACCESS-TARGET alignment while maintaining the actual DELETE budget. Those are design constraints, not an asserted solution or a newly sufficient theorem. No further positive campaign is launched without a concrete mechanism passing the gate.

U4-M remains refuted, the nonlinear seven-key certificate remains valid, the prior profile identities remain valid, and general nonlinear/source-exact Route C and CD-U remain OPEN. Stage11G was read-only throughout; no graph, solver, coordinate, accepted certificate, branch, tracked source or proof-status file was changed.
""")
    save('SP06_REPRODUCIBILITY.md',r"""
# Reproduction and coverage

Copy evaluate_explicit_potential.py and independent_verify.py to a NEW sibling directory at the same depth. From the pinned repository root run:

    python -X utf8 -B <fresh-run>/evaluate_explicit_potential.py
    python -X utf8 -B <fresh-run>/independent_verify.py

Every output uses exclusive creation. No installation, solver or fitted label assignment is required. Exact integer scaling8^5 represents every six-key G term and metric penalty; rational display is reduced exactly.

The evaluator uses immutable single-rotation construction and validates all graph arcs against the pointer primitives. The independent verifier regenerates the full graph with those pointer operations, proves the supplied distance values using upper/lower path bounds, then recomputes every expression term. The closed source word is independently replayed with tuple/frame splay, including full paired states and actual q/a/z costs.

This is one fixed six-key function evaluation:132 single trees,660 directed arcs and264 expression terms. It is not a larger finite fit or all-size numerical extrapolation. SP02/SP03 contain the arbitrary-n analytic arguments. No evidence from a floating solver, timeout or unknown status is used.

entry_source_pins.json and final_integrity.json pin/check all used physical/proof inputs and the Stage11G rule/low/high sources. Active unrelated untracked work is not claimed frozen. All writes remain in this fresh append-only directory; Python -B prevents cache writes.
""")
    save('proof_status_ledger.json',{'date':'2026-10-31','timezone':'Asia/Karachi',
      'claims':[
       {'id':'SP-RAW-B-PAYMENT','status':'PROVED UNIVERSAL CONDITIONAL ON A ROOTED AT TARGET','function':'G','proof':'SP02_RAW_GEOMETRIC_RESERVE_LEMMAS.md','complete_potential':False},
       {'id':'SP-RAW-PRIOR-FRINGE-HELPERS','status':'PROVED UNIVERSAL RESTRICTED FAMILY','function':'G','arbitrary_fringe_size_and_shape':True},
       {'id':'SP-RAW-DELETE','status':'REFUTED ANALYTICALLY','claim':'G is a complete source potential'},
       {'id':'SP-ENVELOPE-DELETE','status':'PROVED UNIVERSAL','function':'Psi','proof':'SP03_ENVELOPE_LAW_AND_ALL_SIZE_REFUTATION.md'},
       {'id':'SP-ENVELOPE-COMPLETE','status':'REFUTED EXACT AND ANALYTICALLY','all_n_family':'n>=6','finite_control':'explicit_potential_countercertificate.json'},
       {'id':'SP-PARAMETER-COROLLARY','status':'REFUTED ANALYTICALLY','scope':'fixed 0<r<1/4, fixed lambda>=0; same envelope construction'},
       {'id':'ROUTE-C-GENERAL','status':'OPEN'}, {'id':'CD-U','status':'OPEN'}, {'id':'DYNAMIC-OPTIMALITY','status':'OPEN'}],
      'new_fitted_parameters':0,'larger_finite_fits':0,'net_positive_CD_U_proof_advancement':0,'Stage11G_modified':False})
    save('SP07_DELIVERY_REPORT.md',r"""
# Step3 explicit-potential audit — 2026-10-31

**One explicit uniform candidate was constructed, proved to satisfy the DELETE law, and refuted analytically on a starved zero-weight KEEP. No complete Route C potential is claimed.**

The promising raw reserve is G=sum_y8^{-d_A(y)}d_B(y). Binary mass summability plus the inherited source +2 displacement bound proves that G pays every B splay when A is rooted at the target. The exact prior arbitrary-fringe zero-helper identities also give strictly negative G changes uniformly in fringe size. These are usable partial laws; G still fails preparatory DELETEs.

The repair Psi=max_T[G(T,B)-rho(A,T)] is a fixed constructive function for every n, with no fitted coefficients. Triangle inequality proves the full DELETE budget. However the maximizer may be rooted away from the accessed A-root. On an explicit family for every n>=6, a zero-demand B zig increases Psi by at least3/4 while a=q=0 requires nonincrease.

The exact six-key control has Psi405/128 ->16625/4096, increase3665/4096. It lies inside an11-access exactly closed physical walk from a diagonal, with A15,Q_B0,Z_B2. A complete independent verifier checks all132 single-tree metric states,660 directed rotations,264 expression values and the full source replay. No larger finite fit or source-pair graph scan occurred.

The missing bridge is now explicit: the nonlinear Lipschitz majorant does not preserve the raw target-conditioned B repayment. Separate valid halves for DIFFERENT functions cannot be combined into a proof. The gate stops this construction at its exact failure; no parameter tuning or replacement existence conjecture is introduced.

Source/proof details: SP01 (definition), SP02 (raw uniform lemmas), SP03 (DELETE proof and all-size refutation), SP04 (exact witness), SP05 (gate/verdict), SP06 (reproduction). Source preservation is recorded in final_integrity.json. Stage11G and all old research remain unchanged. General Route C and Universal Coarse-Double are OPEN.
""")
    entry=json.loads((OUT/'entry_source_pins.json').read_text(encoding='utf-8'))
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    changes=[p for p,h in entry['files'].items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    ok=not changes and git('rev-parse','HEAD')==entry['head'] and git('branch','--show-current')==entry['branch'] and not git('status','--porcelain=v1','--untracked-files=no')
    save('final_integrity.json',{'status':'PASS' if ok else 'FAIL','source_files_compared':len(entry['files']),
      'source_changes':changes,'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'tracked_tree_clean':not git('status','--porcelain=v1','--untracked-files=no'),'Stage11G_modified':False})
    for p in OUT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
    save('delivery_manifest.json',{'main_report':'SP07_DELIVERY_REPORT.md','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}})
    print(json.dumps({'candidate':'REFUTED EXACT AND ANALYTICALLY','raw_partial_laws':'PROVED at stated scope','all_size_complete_potential':'OPEN','fitted_parameters':0,'integrity':'PASS' if ok else 'FAIL'}))

if __name__=='__main__':main()
