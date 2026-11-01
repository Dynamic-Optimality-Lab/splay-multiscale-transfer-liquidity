"""Write the scoped Route C result and explicit universal gate failure, append-only."""
from pathlib import Path
import json,hashlib,subprocess,ast
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]

def save(name,data):
    with (OUT/name).open('x',encoding='utf-8') as f:
        if isinstance(data,str):f.write(data.strip()+'\n')
        else:json.dump(data,f,indent=2)

def main():
    result=json.loads((OUT/'result.json').read_text(encoding='utf-8'))
    audit=json.loads((OUT/'independent_certificate_audit.json').read_text(encoding='utf-8'))
    ck=lambda x,msg: None if x else (_ for _ in ()).throw(AssertionError(msg))
    ck(result['status']=='FINITE_POTENTIAL_ONLY' and audit['status']=='PASS_FINITE_EXACT','exact finite outcome')
    save('RC01_SOURCE_AND_FAILURE_INHERITANCE.md',"""
# Source inheritance and novelty audit

Repository branch coarse-double-branch; HEAD fea2a25b05e97f726b6e1891cebb12c4cfca821a. Tracked tree clean at entry. Read-only sources include:

- python/liquidity/legacy_embedding.py: _depth_to, _rot_right, _rot_left, splay_trace.
- python/independent/splay.py: lookup, _rebuild, trace.
- scripts/wp6_staticR.py and scripts/wp6_j4shared.py: exact total-depth residual plus the old shared J-SELF/ROW construction. Its global assignment remains open; it was not renamed into a new invariant.
- audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md: C7/R-A through R-F record failed depth sums, rotation distance, symmetric interval difference and deletion alignment. P3 records additive separability; U2 refutes the additive per-key joint-depth template. U2 explicitly says nonlinear histogram functions are NOT excluded. U6-X/Y record the richer joint subtree-context finite-fit/exactification wall.
- audits/PIVOT_DUAL_UNIVERSAL.md: maximum B depth plus twin reserve fails through recharge/cancellation.
- audits/REWEIGHTING_BRIDGE_AUDIT.md: depth-tracking remass candidates have unproved/unbounded reweight costs; no theorem was imported from its unpinned external interfaces.
- DO_RESEARCH_REBOOT/02_PROVED/26AJ_direct_coarse_double_repayment.md and 26AL_generalized_signed_repayment.md: root-block and delayed-displacement theorems remain restricted. They do not provide all-size unrestricted coverage.
- Prior DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001 physical witnesses and Route C exclusion report.

All relevant tracked sources have SHA256 pins in entry_source_pins.json. No old constructors with hardcoded output paths were run. No package installation or solver call occurred.

The new architecture is genuinely broader than an additive sum f(dA,dB): an arbitrary function of the WHOLE paired-depth histogram may couple counts nonlinearly. Its information/range may grow with n, and it contains actual A-depth information beyond root/vine bits. It is not automatically covered by the old root_A+full_B or separability exclusion. This test does not claim that this broader class is universally sufficient.

No old failed candidate was renamed into a positive result. A finite table on the new summary is still a finite table. Its successful verification is evidence about representational viability at n7, not universal theorem advancement.
""")
    save('RC02_FINITE_EXACT_RESULT.md',"""
# Exact nonlinear joint-depth certificate at seven keys

**Status: FINITE-EXACT. No all-size invariant is proved.**

For actual BST pairs on seven ordered keys define

    alpha(A,B) = (7, root(A), root(B), H),
    H[u,v] = number of keys x with d_A(x)=u and d_B(x)=v.

All depths count edges. H is the COMPLETE multiset of paired depths, not separate marginal histograms. The exact root key labels are retained. The stored code is [rootA,rootB] followed by the sorted seven values 7*d_A(x)+d_B(x). This is a lossless encoding of this fixed-n summary; no probabilistic hashes or cell truncation are used.

There are 429 BSTs, 184,041 physical paired states and 90,812 distinct summaries. Every physical pair lies in the explicitly computed recurrent component of the right-vine diagonal anchor: both a reachability path and a path back exist. The transition table has 2,576,574 KEEP/DELETE edges. The two physical engines agree on all 3,003 shape/access transitions, including whole final trees and ordered StepEv traces.

For each exact summary edge, use the MAXIMUM reward q-2a among its concrete representatives, and retain a source representative. There are 1,842,798 summary edges. Thus a potential satisfying this quotient's inequalities covers every concrete transition; this direction does not require lifting abstract cycles to physical ones.

Exact integer label correction completed in five passes, 9,213,990 edge scans. The result is the explicit table Phi7 in {-3,-2,-1,0} saved in finite_summary_potential.json. Every original seven-key transition satisfies

    q(e)-2a(e) <= Phi7(alpha(source))-Phi7(alpha(destination)).

An independent checker rebuilt all source transitions with the pointer engine, independently regenerated all features and checked EVERY one of the 2,576,574 concrete inequalities. Minimum residual0, maximum9. It imports neither the quotient generator nor its label-correction code. This finite certificate is exact; no floating solver or rounded value is involved.

Summing gives the finite theorem for ANY length and any seven-key physical path:

    Q_B(path)-2A(path) <= Phi7(start)-Phi7(end) <= 3.

For an exactly closed paired walk the potential boundary is zero, so Q_B<=2A. This holds for repeated/nonprimitive walks and arbitrary occurrence masks in that seven-key domain. Order-preserving relabeling transfers the finite theorem to any seven-element totally ordered set. It does not transfer it to a larger key count.

This is NOT new coverage of Coarse-Double: the repository already has finite seven-key certificates. The new finite observation is that a complete nonlinear joint-depth summary suffices here; full keyed tree state need not be retained at n7. Its all-size sufficiency remains unproved and unrefuted by this run.
""")
    walk=audit['overwritten_setup_walk']
    table='\n'.join('|'+ '|'.join(str(r[k]) for k in ('operation','a','q','potential_source','potential_destination','residual'))+'|' for r in walk)
    save('RC03_OVERWRITTEN_SETUP_REPAYMENT.md',"""
# Actual-state repayment on the overwritten-setup witness

**Scope: the seven-key saved source witness; this is a finite pointwise consequence of the complete certificate.**

The original eligibility graph still fails at K7: its three demands have only the two D7 setup units. The new state potential does not use that eligibility graph or latest-setup identifiers.

|Operation|a|q|Phi source|Phi destination|drop-(q-2a)|
|---|---|---|---|---|---|
"""+table+"""

At the beginning Phi=-2. D6 has a=3 and raises Phi from -2 to0; the following D7 has a=1 and leaves Phi0 unchanged. K7 has a=0,q=3 and drops Phi from0 to-3, paying its entire demand. Thus the D6 state change remains visible through the overwritten D7 setup. Nothing restricts payment to D7's two units.

Equivalently, the shifted bank Phi+3 starts at1, receives2 during D6, stays at3 during D7 and consumes3 at K7. These are potential values, not an asserted injection into specific historical credit IDs. No credit matching theorem is inferred from this bank description.

The entire closed word has reward Q-2A=-16 and total potential drop0. Every inequality was checked independently. Potential decreases on some weight-zero operations too: K4 has a=q=0 but executes a B zig and drops the potential by2. Weight zero does not mean inert state or neutral future reserve.

The five-KEEP/nine-core physical witness was independently replayed as an INPUT REGRESSION only (32 accesses,A34,Q18,exact closure). Phi7 is undefined for its nine-key states. Its potential payment was NOT checked or claimed. The all-n overwritten-setup family likewise remains an all-size acceptance test, not a domain covered by this finite table.
""")
    save('RC04_UNIVERSAL_GATE_AND_STOP.md',"""
# Universal Route C gate — not passed

The user authorized seeking an all-size source-exact A/B invariant. RC00_PRE_EXECUTION_GATE.md authorized exactly one bounded test of a previously open nonlinear summary architecture. That test completed with a finite potential and no summary countercycle. Its registered stopping condition now applies: no larger-size scan, feature refinement, fresh fit or automatic successor is executed.

The all-size proposal would require an EXPLICIT uniform construction F(n,rootA,rootB,H), or another source-defined invariant, and a universally proved update law. A separate label vector for each n supplied by a finite difference solver does not meet that requirement. Defining F as maximum future excess or assuming every quotient has nonnegative cycles would merely move the original open obligation.

The first unsupported implication is:

    finite seven-key nonlinear histogram certificate
        => a uniform source-defined all-size repayment law.

No source induction, closed formula, bounded recurrence, or all-size summary-lifting theorem presently discharges it. Even feasibility of this summary architecture at n>=8 is unproved by this run. There is no claim that histogram feasibility would be necessary for unrestricted Route C.

Four-rule assessment for a NEW positive universal campaign:

1. Smaller structural target: not yet identified beyond the explicitly bounded representation test.
2. Concrete universal construction/induction: MISSING. Numerical or finite feasibility is not a mechanism.
3. One bounded principal theorem: cannot presently be specified without an additional independent open construction theorem.
4. Deleted original CD-U obligation: NONE from this finite certificate; existing finite n7 coverage already supplied the scalar bound.

Therefore a universal proof campaign is NOT launched. This is compliance with RESEARCH_RULES.md, especially “A new equivalent existence premise ... finite fit ... does not count” and “Do not automatically proceed after OPEN.” No new approval request is needed or made; there simply is no passing positive theorem gate to execute.

BEFORE: original U4-M refuted; additive and several geometric scalar candidates already failed; nonlinear histogram architecture explicitly open.
RESULT: exact nonlinear histogram potential at n7, covering the complete physical domain and the seven-key overwritten-setup witness, independently verified.
AFTER: all-size architecture still OPEN, general Route C still OPEN, CD-U still OPEN. Net new positive CD-U proof advancement:0. New finite source-exact evidence: the nonlinear coupled summary survives a complete n7 test.

The next justified operation is analytic, not graph enlargement: a concrete source rotation identity must specify how a retained A/B reserve behaves when a setup is overwritten, when an off-path subtree moves, and when a zero-weight helper changes the future. No such identity is asserted here. Its gate must identify an actual smaller theorem and prove why it removes an original obligation before execution.
""")
    save('RC05_FINAL_REPORT.md',"""
# Route C continuation — finite coupled repayment found; universal construction open

**Verdict: FINITE-EXACT COUPLED CERTIFICATE. No all-size Route C proof completed.**

The written four-rule gate preceded experiments. Existing failed additive/separable/depth/interval/distance candidates were audited before selecting a different class: arbitrary nonlinear functions of the complete joint A/B depth histogram, with exact root labels and size-dependent information/range.

This class passed the complete seven-key source graph. The saved exact potential has values -3..0 on90,812 summaries of184,041 physical pairs. All2,576,574 source transitions satisfy q-2a<=Phi(source)-Phi(destination). Independent full concrete-edge verification passes.

On the overwritten-setup word, the preparatory D6 raises Phi from-2 to0; D7 keeps it0; K7 drops it to-3 and pays all three B doubles. The false original U4 matching is neither assumed nor repaired. The nine-key/five-KEEP witness was replayed but is outside this potential's domain.

What remains unsupported is an explicit uniform source invariant and universal transition proof. A table at one n cannot supply it. The gate does not authorize escalating finite fits after this result, so the campaign stops with the all-size obligation exposed. Coarse-Double and Dynamic Optimality remain open.

Artifacts:

- RC00_PRE_EXECUTION_GATE.md — exact registered scope and stopping conditions.
- RC01_SOURCE_AND_FAILURE_INHERITANCE.md — old failures and novelty limits.
- RC02_FINITE_EXACT_RESULT.md — exact potential, graph semantics and finite theorem.
- RC03_OVERWRITTEN_SETUP_REPAYMENT.md — every witness payment and zero-weight behavior.
- RC04_UNIVERSAL_GATE_AND_STOP.md — first unsupported implication and four-rule assessment.
- finite_summary_potential.json — complete integer table and exact summary encoding.
- independent_certificate_audit.json — independent all-edge check and per-access witness values.
- result.json, entry_source_pins.json, integrity.json and proof_status_ledger.json.

Stage11G was read-only throughout. No frozen graph, solver architecture, coordinate, accepted certificate, branch or tracked source was changed. Active untracked Stage11G files were not claimed frozen or redirected. This campaign writes only inside its new append-only directory.
""")
    save('RC06_REPRODUCIBILITY.md',"""
# Reproduction

From the repository root, use a NEW sibling directory at the same depth. Copy only the two new test scripts there. They compute ROOT by parent depth and exclusively create their outputs; never rerun a writer against an existing result path.

    python -X utf8 -B <fresh-run>/rc_histogram_test.py
    python -X utf8 -B <fresh-run>/verify_histogram_certificate.py

No dependency installation is required. Both physical engines are existing repository modules. The first script constructs all429 BSTs independently of saved graph files, verifies3,003 tuple/pointer splay destinations AND event traces, computes concrete reachability/recurrence, builds exact complete summaries and every maximal reward edge, and verifies the produced integer inequalities. The second imports only the pointer engine and independently regenerates all concrete rows; it does not trust graph construction, solver termination or sampling.

The summary uses all joint depth cells, not separate marginals. Parallel source transitions are combined by MAX reward, preserving the strongest required inequality. Solver labels are negated exactly: if d[v]>=d[u]+reward, Phi=-d gives Phi[u]-Phi[v]>=reward. No floating signs/rounding are involved.

result.json records dimensions, passes, edge scans and CPU time. independent_certificate_audit.json records all2,576,574 checks, residual histogram, full saved-word potential values and certificate SHA256. The original U4 matching and symbolic Stage11G certificates are not test dependencies or proof premises.

entry_source_pins.json pins1,888 pre-existing source/input files. integrity.json compares those hashes and branch/HEAD/tracked state. Active untracked Stage11G population work is outside the source-freeze claim. New scripts use Python -B to avoid bytecode caches. No old result path is written.

Coverage limits: n=7 finite source domain only. Arbitrary path lengths follow by exact telescoping inside this domain. No nine-key potential, all-size formula, general histogram theorem, Coarse-Double counterexample or new universal Dynamic Optimality theorem is claimed.
""")
    ledger={'date':'2026-10-30','timezone':'Asia/Karachi','head':'fea2a25b05e97f726b6e1891cebb12c4cfca821a',
      'claims':[
       {'id':'RC-NONLINEAR-HIST-7','status':'FINITE EXACT','domain':'all seven-key physical Pair Access transitions','certificate':'finite_summary_potential.json','independent_check':'independent_certificate_audit.json'},
       {'id':'RC-OVERWRITTEN-7','status':'FINITE EXACT','claim':'K7 has potential drop3; all15 witness inequalities hold','eligibility_matching_claim':False},
       {'id':'RC-OVERWRITTEN-9','status':'SOURCE REPLAY REGRESSION ONLY','potential_defined':False},
       {'id':'RC-NONLINEAR-HIST-ALL','status':'OPEN','claim':'uniform all-size construction and update law absent'},
       {'id':'RC-GENERAL','status':'OPEN','claim':'no all-size source potential or complete repayment law proved'},
       {'id':'CD-U','status':'OPEN'}, {'id':'U4-M','status':'REFUTED EXACT','inherited':True},
       {'id':'DYNAMIC-OPTIMALITY','status':'OPEN'}],
      'net_new_CD_U_proof_advancement':0,'four_rule_gate_for_new_universal_campaign':'NOT PASSED: no concrete uniform mechanism',
      'registered_bounded_test':'COMPLETE; stopping condition observed','Stage11G_changed':False}
    save('proof_status_ledger.json',ledger)
    entry=json.loads((OUT/'entry_source_pins.json').read_text(encoding='utf-8'))
    changed=[p for p,h in entry['files'].items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    tracked=subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain=v1','--untracked-files=no']).decode().strip()
    save('final_integrity.json',{'status':'PASS' if not changed and not tracked else 'FAIL','source_files_compared':len(entry['files']),
        'source_changes':changed,'tracked_status':tracked,'Stage11G_modified':False})
    for p in OUT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'))
    save('delivery_manifest.json',{'main_report':'RC05_FINAL_REPORT.md','files':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}})
    print(json.dumps({'report':'RC05_FINAL_REPORT.md','finite_edges_verified':audit['concrete_edge_inequalities_checked'],'all_size_proof':False,'source_files_unchanged':len(entry['files']) if not changed else False,'universal_gate':'NOT PASSED'}))

if __name__=='__main__':main()
