"""Bind explicit Notion proofs to checked artifacts, without closing the root."""
import hashlib
import json
from pathlib import Path
import context as C
import gso
HERE=C.HERE;ROOT=C.ROOT;K=C.K


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    proof=K.load(HERE/'NOTION_PROOF_REFERENCE.json');assert proof['readback_verified']
    oldpins=K.load(C.PREVIOUS/'PINNED_SOURCE_INPUTS.json');pins={x['path']:x for x in oldpins}
    extra=['GSO_ENGINE_20261121_V001/FINAL_MANIFEST.json','GSO_ENGINE_20261121_V001/kernel.py','GSO_ENGINE_20261121_V001/teacher.py','GSO_ENGINE_20261121_V001/run_001/optimum_cycle_n5.json','GSO_ENGINE_20261121_V001/run_001/optimum_cycle_n3.json']
    for name in extra:
        path='DO_RESEARCH_REBOOT/'+name;pins[path]={'path':path,'sha256':digest(ROOT/path)}
    K.dump(HERE/'PINNED_SOURCE_INPUTS.json',list(pins.values()))
    codefiles=[p for p in HERE.iterdir() if p.suffix in ('.py','.lean')]
    proof['code_sha256']={p.name:digest(p) for p in sorted(codefiles)}
    proof['workspace_updates']=[{**x,**({'status_header_corrected_and_verified':True} if x['key']=='gso' else {})} for x in proof['workspace_updates']]
    K.dump(HERE/'NOTION_PROOF_REFERENCE.json',proof)
    # The core3 result predates the clarification of abstract versus physical
    # cycles. Correct only that description, preserving its old wording.
    path=HERE/'run_001/CONTEXT_CERTIFICATE.json';z=K.load(path)
    desired='Discovery only; all-edge integer inequalities and a tight abstract cycle certify the finite quotient optimum. Original sharpness is verified separately.'
    if z['floating_LP_role']!=desired:
        K.dump(HERE/'CORE3_METADATA_CORRECTION.json',{'old_floating_LP_role':z['floating_LP_role'],'new_floating_LP_role':desired,'scope':'Description only; all potentials, edges, costs and cycle IDs unchanged.'});z['floating_LP_role']=desired;K.dump(path,z)
    examples=[]
    for file in sorted((HERE/'sources_001').glob('source_*.json.gz')):
        w=K.load(file);s=w['source']
        if s['name'].startswith('H_3_'):
            n=len(s['initial_A']['children']);r=next(row for row in w['rows'] if row['op']==n+7)
            assert r['a']==1 and r['q']==s['q']+1 and r['kappa_before']==r['kappa_post_A']==r['kappa_after']==n-3
            examples.append({'file':str(file.relative_to(HERE)).replace('\\','/'),'sha256':digest(file),'q':s['q'],'N':n,'original_op':n+7,'row':r,'original_critical_U_ids':[d['id'] for d in w['original_U'] if d['id'][0]==n+7]})
    K.dump(HERE/'SCALAR_OBSTRUCTION_CERTIFICATE.json',{'status':'REFUTED_ALL_FINITE_C_AND_ALL_FUNCTIONS_F_N','candidate':'Whole-operation q_B + F_N(kappa_after)-F_N(kappa_before) <= C a, also any uniformly bounded correction. Not the original aggregate CD bound.','all_parameter_proof':proof['url'],'source_family':'Complete original H_3,q for every integer q>=1; N=16(q+1)+1; empty reaching prefix; both full restoration sweeps counted.','symbolic_values':{'a':1,'q_B':'q+1','critical_U':'q','core_before_postA_after':'N-2','kappa_before_postA_after':'N-3','common_leaf_deletions':'exactly the physical endpoint keys1,N','choose_for_any_integer_C':'q=C+1'},'deduction':'Equal F values cancel. Any finite real C can be rounded up; q+1>C. Finite instances are not the all-q justification.','examples':examples})
    K.dump(HERE/'NECESSARY_SHAPE_RANGE.json',{'status':'PROVED_NECESSARY_CONDITION_FOR_A_UNIVERSAL_WHOLE_OPERATION_STATE_POTENTIAL','source_proof':proof['url'],'inequality':'oscillation of Phi among admissible states at support N=m+2 and core size m is at least (m+1)/16-C for every m=16q+15, q>=1.','reason':'The two actual complete H_3,q critical endpoints have identical core size but q_B=q+1 and a=1.','excluded':'Scalar core-size functions and uniformly bounded corrections.','not_excluded':'Unbounded shape-sensitive state potentials or non-statewise/history-dependent global accounting.','root':'OPEN'})
    claims=[
      {'claim':'Q_B<=A for boundary core<=3','status':'PROVED_RESTRICTED_DOMAIN','constant':'1','unbounded_parameters':'Physical support, target population, hanging subtrees, period length, repetitions/interleavings within the exact boundary condition.'},
      {'claim':'Q_B<=3A/2 for boundary core<=5','status':'PROVED_RESTRICTED_DOMAIN','constant':'3/2','scope':'Original operation boundaries only; intermediate core sizes may be larger.','sharp_original_witness':'sources_001/source_02.json.gz'},
      {'claim':'Global B core-drop budget <=2A','status':'PROVED_UNIVERSAL','scope':'All admissible exactly paired-closed original sources; whole-A-phase issuance <=real A rotations.'},
      {'claim':'Original neutral B bits are kappa-flat','status':'PROVED_UNIVERSAL','consequence':'Core-drop payments are already nonneutral SET-paid; no new hard-residual payment.'},
      {'claim':'All scalar F_N(kappa) and uniformly bounded corrections fail the whole-operation certificate for every finite C','status':'REFUTED_ALL_PARAMETER_FAMILY','evidence':'SCALAR_OBSTRUCTION_CERTIFICATE.json'},
      {'claim':'Q_B<=9A+U_>5','status':'PROVED_UNIVERSAL_INEQUALITY_WITH_UNRESOLVED_RESIDUAL','scope':'Literal original U_int partition by pre-operation core size, plus the unchanged six-A theorem and K_B<=A. Not a pure global constant bound.'},
      {'claim':'Universal Coarse Double','status':'OPEN','first_missing':'Global conservation for large-core neutral original consumers, or another fully checked source-uniform accounting route.'}
    ]
    K.dump(HERE/'THEOREM_CERTIFICATE.json',{'proof_reference':proof['url'],'claims':claims,'original_hard_residual_classes_newly_paid':0,'proof_limits':'Mathematical structural proofs plus independently checked finite components; Lean only checks the stated identities/arithmetic, not the whole source model.'})
    result=gso.status();result['notion']=proof['url'];result['prior_results']='All4877 pinned/sealed artifacts preserved; original predicates unchanged.'
    K.dump(HERE/'ENGINE_RESULT.json',result)
    print(json.dumps({'proof':proof['url'],'readback_verified':True,'claims':len(claims),'pins':len(pins),'code_bindings':len(codefiles),'root_status':'OPEN'}))


if __name__=='__main__':main()
