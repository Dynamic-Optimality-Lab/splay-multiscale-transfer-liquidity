"""Append-only publication metadata after all mathematical audits pass."""
import json,hashlib,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
def read(n):return json.loads((BASE/n).read_text())
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    audit=read('step4_audit.json');scope=read('step4_scope_audit.json');final=read('audit_final_source.json')
    assert audit['status']=='INDEPENDENT_COMPLETE_STEP4_CERTIFICATE_AUDIT_PASS'
    assert scope['status']=='INDEPENDENT_TWO_SORT_AND_HIGH_H0_SCOPE_AUDIT_PASS'
    assert final['status']=='INDEPENDENT_NORMALIZED_MAXIMAL_SOURCE_AUDIT_PASS'
    assert final['pending_jobs']==0 and final['unresolved'] is None
    for n in ('certificate','scope','final_source'):assert read('run_'+n+'_result.json')['status']=='PASS'
    assert read('final_immutable_integrity.json')['status']=='PASS'
    runs={};charges={}
    for p in BASE.glob('run_*_result.json'):
        q=json.loads(p.read_text());n=q['phase'];ctrl=read('controller_'+n+'_exit.json')
        assert q['child_CPU']<=q['allocated_CPU_cap']
        runs[n]=q;charges[n]=q['child_CPU']+ctrl['whole_process_CPU_seconds']
    groups=[('global_quantified_construction',300,['quantified','quantified_shared']),
      ('reduced_correction_construction',300,['correction','correction_v2','correction_v3']),
      ('original_anchor_source_audit',300,['anchor','anchor_r1','anchor_r2','anchor_r3','anchor_closure']),
      ('original_union_independent_audit',300,['anchor_union']),
      ('seven_family_source_audit',300,['seven','seven_closure']),
      ('seven_family_independent_audit',300,['seven_independent']),
      ('normalized_maximal_source_theorem',300,['maximal']),
      ('normalized_independent_final_audit',300,['final_source','certificate','scope']),
      ('pair_symbolic',120,['pair','pair_v2']),('lower_return_symbolic',120,['lower_return','lower_return_v2']),
      ('normalization_symbolic',120,['normalization','normalization_v2'])]
    used=set();phase_groups=[]
    for name,cap,names in groups:
        value=sum(charges[n] for n in names);assert value<=cap,(name,value)
        used.update(names);phase_groups.append({'name':name,'cap':cap,'charged_CPU':value,'phases':names})
    for n in sorted(set(charges)-used):
        assert charges[n]<=120;phase_groups.append({'name':n,'cap':120,'charged_CPU':charges[n],'phases':[n]})
    prior=766.703125;new=sum(charges.values());total=prior+new;assert total+5<=7200
    resources={'prior_uniform_CPU':prior,'new_CPU_including_all_failed_attempts_and_controllers':new,
      'cumulative_uniform_CPU':total,'global_CPU_allowance':7200,'remaining_CPU_including_reserve':7200-total,
      'required_reserve':5,'phase_groups':phase_groups,'all_phase_caps_preserved':True,
      'original_signature_ledger_unchanged':7195.203125,
      'canonical_query_cap':2000000,'live_record_cap':2000000,'largest_published_clause_formula':len(final['clauses']),
      'input_DAG_cap':4000000,'input_DAG_conservative_bound':audit['input_DAG_conservative_bound'],
      'stored_edge_cap':5000000,'proof_records':audit['proof_records'],
      'peak_working_set_bytes_observed':max(q['peak_working_set_bytes_observed'] for q in runs.values()),
      'memory_cap_bytes':32*1024**3,'per_phase_wall_limit_hours':12,
      'no_finite_tests':True,'no_completed_semantic_replays':True,
      'metadata_CPU_excluded_by_inherited_convention':True}
    assert resources['peak_working_set_bytes_observed']<=resources['memory_cap_bytes']
    write('resources_final.json',resources)
    # Explicit anchor coefficients, copied/derived only from old completed facts.
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text());anchors={}
    for i,q in enumerate(bank['nodes']):
        for x in range(9):
            j=tab['B_destination'][i][x]
            if tab['B_depth'][i][x] in (4,5) and q['psi']>bank['nodes'][j]['psi']:
                anchors.setdefault(j,{})[q['tree'][0]]=max(anchors.get(j,{}).get(q['tree'][0],0),q['psi'])
    assert len(anchors)==303
    formula={'status':'PROVED_UNIVERSAL_STEP4_ZERO_LOW_SIGNED_REPAYMENT',
      'domain':'original full ordinary states; all legal five-bit masks and arbitrary admissible sigma in the frozen nine-core M3 domain',
      'equation':'F=max(D0, 1_(P AND N AND C1), 2*1_(P AND N AND C2))',
      'D0':'fixed XFER18 D_current plus the proved Bad/reset/paired/lower-return/seven-anchor augmentations',
      'D0_definition_sources':['../M3_XFER18/debt_definition.json','STATIC_BOUNDARY_THEOREM.md',
        'COMPATIBLE_RESET_PROOF.md','PAIRED_UPPER_FAMILY.md','LOWER_RETURN_FAMILY.md','SEVEN_CLOSURE_RESULT.md'],
      'P':'proper listed B core; A root Score synchronized to B root and marked; root.kind UNUSED',
      'N':'for every nonroot alpha position p, NOT ScoreAt(p,Broot)',
      'ScoreAt':'original kind0 AND isS=true AND index=role, with all unused fields free',
      'Ck':'union of clauses below with level>=k at the specified exact B core',
      'anchor_guard':'N AND OR_r(mark[r] AND (ScoreAt(L,r) OR ScoreAt(LL,r) if r<root else ScoreAt(R,r) OR ScoreAt(RR,r))), only r with coefficient>=level',
      'score_cube_guard':'all listed ScoreAt equalities AND all listed positive mask bits; every omitted field free',
      'anchor_coefficients':anchors,'clauses':final['clauses'],
      'core_index_source':'../M3_LDR01/negative_run_census.json, already independently completed4862-core facts',
      'core_index_sha256':sha(BASE.parent/'M3_LDR01/negative_run_census.json'),
      'Step4_complete':True,'M3_complete':False,'Dynamic_Optimality_proved':False,
      'all_old_valid_LOW_rows_preserved':True,'newly_raised_H1_and_Gamma1_sources_proved':True,
      'all_original_zero_LOW_rows_proved':True,'R1_R2_R3_R4_preserved':True,
      'HIGH_h0_scope':'TWO_SORT_SCOPE_CORRECTION.md and step4_scope_audit.json',
      'independent_audit':'step4_audit.json, FINAL_PROOF_AUDIT.md, step4_scope_audit.json',
      'audit_scope':'separate campaign derivation/checker, not external review or full compiler formalization'}
    write('STEP4_CERTIFICATE.json',formula)
    h1=[]
    for drop in ('1_to_0','2_to_0','2_to_1'):
        for d in (4,5):
            for word in ('L','R','LL','LR','RL','RR'):
                h1.append({'seed_drop':drop,'B_depth':d,'A_word':word,'status':'CLOSED_UNIVERSALLY',
                  'proof':'exact-source debt + generic marked old-root anchor + complete signed closure'})
    write('partition_closure.json',{'Step4_complete':True,'marked_H1_slots':h1,
      'Gamma1_visible_profiles':{'count':8,'status':'CLOSED_INHERITED_AND_PRESERVED'},
      'Gamma1_hidden_profiles':{'count':8,'status':'CLOSED_INHERITED_AND_PRESERVED'},
      'Gamma0':'CLOSED_INHERITED_AND_PRESERVED','unmarked_source_zero_H1':'CLOSED_SOURCE_ZERO',
      'remaining_Step4_cases':0,'not_a_signature_or_population_partition':True})
    result=f'''# Step4 closed: universal zero-weight LOW repayment

Step4 is PROVED—UNIVERSAL on the frozen original M3 domain. Every
remaining marked zero-H1 edge is paid for arbitrary admissible sigma,
all legal masks and every original private completion. Together with
preserved Gamma0/Gamma1 and unmarked-source results, this covers ALL
original zero-weight LOW edges. No finite population tests were used.

The new explicit ordinary debt is

    F=max(D0, 1_(P AND N AND C1), 2*1_(P AND N AND C2)).

Its3413 public clauses are saved in STEP4_CERTIFICATE.json. N removes
nonroot ghost reads of the current root; every cheap genuine target
retains its correction credit. The source proof checks only the maximum
active debt and includes negative and +1 exits from every raised source.
Thus every old valid signed LOW row survives. This pays repeated signed
debt transfers, including anonymous exposures, without private inventories.

The independent inventory covers all36972 clause/word obligations through
6806 universal certificate records, with zero missing. Generic anchor
coverage then pays all378 critical core/role groups, closing all36 old
marked-H1 schematic slots. Old proofs were reused, not rerun. Failed and
cap-limited candidates remain unproved in their original artifacts.

The separate dependency/guard/signed-composition/full-state audit passed.
All14704 inherited files, HEAD and the tracked tree are unchanged. R1–R4,
original147-O/127-M interfaces, independent witnesses/SAME midpoint,
HIGH/free-v, weak LE/G/unused fields and corrected h0 are preserved.
The debt reads ordinary alpha fields only; the midpoint extension is
unchanged, as clarified in TWO_SORT_SCOPE_CORRECTION.md.

CPU including all failed attempts and controllers: {total}/7200 seconds;
remaining {7200-total}, including reserve5. All per-phase groups and the
2-million-query/other caps pass resources_final.json. Metadata bookkeeping
uses the inherited exclusion convention. No original root or new bank
census was executed.

Proof: FINAL_PROOF_AUDIT.md and COMPLETE_STEP4_COMPOSITION.md with
TWO_SORT_SCOPE_CORRECTION.md. Exact audit: step4_audit.json. Complete
statuses: partition_closure.json. This is a separate audit within the
campaign, not external review or full compiler formalization.

Full M3 remains open pending any remaining positive LOW obligations and
the subsequent complete M3 composition. Dynamic Optimality is not claimed.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(result)
    write('CURRENT_STATE.json',{'Step4':'PROVED_UNIVERSAL_CLOSED','remaining_Step4_cases':0,
      'M3':'OPEN_PENDING_REMAINING_POSITIVE_LOW_AND_FULL_COMPOSITION',
      'active_ordinary_debt':'STEP4_CERTIFICATE.json','audit':'step4_audit.json',
      'next':'audit/close any remaining weight+1 LOW rows, then combine full M3; do not repeat Step4',
      'CPU':total,'CPU_remaining':7200-total})
    entry=read('entry_baseline.json')
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==entry['head']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    pins=[{'file':p.name,'sha256':sha(p)} for p in sorted(BASE.iterdir()) if p.is_file()]
    write('final_manifest.json',{'status':'STEP4_CLOSED_ALL_PUBLICATION_GATES_PASS',
      'files':pins,'old_integrity':'final_immutable_integrity.json','old_files':14704,'head':entry['head'],
      'metadata_CPU_excluded':time.process_time(),'Step4_complete':True,'M3_complete':False})
    print(json.dumps({'Step4_complete':True,'obligations':audit['covered_clause_word_obligations'],
      'clauses':len(final['clauses']),'CPU':total,'remaining_CPU':7200-total,'files_pinned':len(pins)},indent=2),flush=True)
if __name__=='__main__':main()
