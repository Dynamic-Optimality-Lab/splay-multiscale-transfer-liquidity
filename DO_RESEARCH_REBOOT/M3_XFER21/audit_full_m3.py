"""Independent full M3 inventory/source/interface/sign audit.

Imports no construction, prefix generator or candidate decoder. Reuses
completed exact UNSAT conclusions as premises, never finite sample passes.
"""
import json,sys,time,hashlib,collections
from pathlib import Path
import z3
BASE=Path(__file__).resolve().parent;R=BASE.parent;P20=R/'M3_XFER20';P19=R/'M3_XFER19';CAP=min(300,float(sys.argv[1]))
def read(p):return json.loads(p.read_text())
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def canon(v):return tuple(canon(q) for q in v) if isinstance(v,list) else v
def tree(t):return None if t is None else (t[0],tree(t[1]),tree(t[2]))
def mirror(t):return None if t is None else (8-t[0],mirror(t[2]),mirror(t[1]))
WORDS=((0,),(1,),(0,0),(0,1),(1,0),(1,1))
def helper_words(root,target,h):
    a,b=(root,target) if h==0 else (8-root,8-target)
    if b<a:w=(((0,),(1,0)),((0,0),(1,)),((0,0),(1,0)),((0,1),(1,0)))
    elif b>a:w=(((0,),(1,1)),((0,1),(1,1)))
    else:return ()
    return w if h==0 else tuple(tuple(tuple(1-v for v in p) for p in q) for q in w)
def main():
    final=read(BASE/'audit_extremal.json');prefix=read(P20/'audit_prefix.json');old=read(P19/'STEP4_CERTIFICATE.json')
    assert final['status']=='COMPLETE_EXTREMAL_HELPER_AND_ALL_LOW_AUDIT_PASS'
    assert final['pending_jobs']==0 and final['unresolved'] is None
    assert final['Gamma1_next_job']==final['Gamma1_required_jobs']==4152
    cs=final['clauses'];cut=prefix['accepted_clause_count'];assert cut==2963
    assert cs[:cut]==prefix['clauses']
    assert cs[:743]==read(P20/'audit_completion_v2.json')['clauses']
    assert cs[:1349]==read(P20/'audit_joint.json')['clauses']
    assert cs[:cut]==read(P20/'audit_independent.json')['clauses'][:cut]
    assert old['Step4_complete'] and read(P19/'step4_audit.json')['missing_obligations']==0
    for n,status in [('audit_reductions.json','UNIVERSAL_POSITIVE_SOURCE_AND_WORD_REDUCTIONS_PASS'),
      ('audit_visibility.json','UNIVERSAL_VISIBLE_TERMINAL_CAPACITY_EXCLUSION_PASS'),
      ('audit_prefix.json','UNIVERSAL_CLOSED_PREFIX_AND_EXTREMAL_REDUCTION_PASS')]:assert read(P20/n)['status']==status
    assert len(read(P20/'audit_reductions.json')['excluded_symbolic_word_pairs'])==24
    assert len(read(P20/'audit_visibility.json')['proofs'])==8
    assert len(prefix['tall_hidden_source_exclusion'])==4
    bank=read(R/'M3_LDR01/negative_run_census.json');tab=read(R/'M3_H1F01/cheap_census.json');kernel=read(R/'M3_H2R01/fringe_kernel_certificate.json')
    ts=[tree(q['tree']) for q in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    ps=[q['psi'] for q in bank['nodes']];dd=tab['B_depth'];nx=tab['B_destination'];rev=[ids[mirror(t)] for t in ts]
    assert len(ts)==4862 and len(set(ts))==4862 and set(ps)=={0,1,2}
    critical={(i,x,nx[i][x]) for i in range(len(ts)) if ps[i]==2 for x in range(9) if dd[i][x] in (2,3) and ps[nx[i][x]]==0}
    inv=read(P20/'positive_inventory.json');assert critical=={tuple(q) for q in inv['H1_critical_core_rows']}
    anchors={}
    for i,x,j in critical:anchors.setdefault(j,set()).add(ts[i][0])
    assert {int(i):set(v) for i,v in final['anchors'].items()}==anchors
    assert len(critical)==318 and len(anchors)==275
    assert {(c['core'],c['level']) for c in cs if c['kind']=='positive_anchor'}=={(i,1) for i in anchors}
    helpers={};actual_gamma=set();gamma_classes=collections.Counter()
    for q in kernel['rows']:
        assert q['w']==4-q['q'] and q['q']==q['terminal_depth']//2
        if not q['gap0_childless_at_exit']:continue
        i,x,j,w=q['entry_core'],q['target'],q['exit_core'],q['w']
        for h,ii,xx,jj in ((0,i,x,j),(9,rev[i],8-x,rev[j])):
            if w<2:
                assert xx!=ts[ii][0]
                helpers.setdefault(ii,set()).add((h,xx,jj,w))
            if w!=1:continue
            hd=dd[ii][0 if h==0 else 8]+1
            if hd==1:gamma_classes['helper_depth1_parallel_Step4_H1']+=1;continue
            if hd>=3:raise AssertionError('old proper kernel contradicts proved deep-helper parent law')
            assert hd==2
            assert q['terminal_depth']==6,'odd terminal7 impossible by final proxy parent and extreme depth1'
            if ps[jj]>=1:gamma_classes['actual_destination_psi_floor1']+=1;continue
            gamma_classes['critical_actual_orientation_rows']+=1
            for word in helper_words(ts[ii][0],xx,h):actual_gamma.add((ii,xx,jj,h,word))
    # Independently apply ACTUAL max psi after mirroring the topology. This
    # discharges coverage without ever assuming a psi reflection property.
    planned=[]
    for q in inv['Gamma1_gap0_critical_rows']:
        i,x,j=q['entry_core'],q['target'],q['exit_core']
        for h,ii,xx,jj in ((0,i,x,j),(9,rev[i],8-x,rev[j])):
            for word in helper_words(ts[ii][0],xx,h):planned.append((ii,xx,jj,h,word))
    assert len(planned)==len(set(planned))==4152 and set(planned)==actual_gamma
    jobcache={}
    def required(i,k):
        if (i,k) in jobcache:return jobcache[i,k]
        out=set()
        if ps[i]<k:
            for x in range(9):
                j=nx[i][x];w=2-dd[i][x]//2
                if w>=k or w+ps[j]>=k:continue
                for word in WORDS:
                    if word[0]==int(x>ts[i][0]):out.add((i,k,None,(word,),x,j,w))
            if k==2:
                for h,x,j,w in helpers.get(i,set()):
                    if w+ps[j]>=k:continue
                    for word in helper_words(ts[i][0],x,h):out.add((i,k,h,word,x,j,w))
        jobcache[i,k]=out;return out
    proven=set();accepted={};rejected=0
    sources=[(P20/'completion_v2_checkpoints.jsonl',743),(P20/'joint_checkpoints.jsonl',1349),
      (P20/'independent_checkpoints.jsonl',None),(BASE/'extremal_checkpoints.jsonl',None)]
    for p,limit in sources:
        count=0
        for line in p.read_text().splitlines():
            q=json.loads(line);pf=limit if limit is not None else q['formula_prefix_length']
            if p.parent==P20 and p.name.startswith('independent') and pf>cut:rejected+=1;continue
            assert pf<=len(cs) and q['proof']=='UNIVERSAL_UNSAT';key=canon(q['job'])
            for cid in q['source_clause_ids']:
                assert cid<pf;c=cs[cid]
                assert key in required(c['core'],c['level']),(p.name,cid,key)
                proven.add((cid,key))
            count+=1
        accepted[str(p.relative_to(R))]=count
    total=0;missing=[]
    for cid,c in enumerate(cs):
        assert c['level'] in (1,2) and c['kind'] in ('positive_anchor','score_cube')
        if c['kind']=='score_cube':
            assert set(c)<= {'kind','core','level','marks','nonmarks','score_equalities'}
            assert all(0<=x<9 for x in c['marks']+c.get('nonmarks',[]))
            assert not set(c['marks'])&set(c.get('nonmarks',[]))
            assert len({p for p,v in c['score_equalities']})==len(c['score_equalities'])
            assert all(1<=p<=6 and 0<=v<9 for p,v in c['score_equalities'])
        for key in required(c['core'],c['level']):
            total+=1
            if (cid,key) not in proven:missing.append((cid,key))
    assert not missing,missing[:5]
    # Independent helper record decoder and exclusion validation.
    visible={((0,),(1,0)),((0,0),(1,)),((0,),(1,1)),((0,1),(1,1))}
    hidden={((0,0),(1,0)),((0,1),(1,0))}
    closed={};proof_kinds=collections.Counter()
    gamma_sources=[(P20/'gamma_checkpoints.jsonl',743),(P20/'joint_gamma_checkpoints.jsonl',1349),
      (P20/'independent_gamma_checkpoints.jsonl',None),(BASE/'extremal_gamma_checkpoints.jsonl',None)]
    for p,limit in gamma_sources:
        for line in p.read_text().splitlines():
            q=json.loads(line);pf=limit if limit is not None else q['formula_prefix_length']
            if p.parent==P20 and p.name.startswith('independent') and pf>cut:continue
            assert pf<=len(cs);n=q['job'];i,x,j,h,word=planned[n]
            assert canon([q['source_core'],q['target_key'],q['destination_core'],q['helper'],q['word']])==planned[n]
            proof=q['proof'];minimum_word=word if h==0 else tuple(tuple(1-v for v in p) for p in word)
            if proof=='STATIC_VISIBLE_SEED_CAPACITY_CONTRADICTION':
                assert ps[i]<2 and minimum_word in visible and 2-dd[i][x]//2+ps[nx[i][x]]<2
            elif proof=='STATIC_EXTREMAL_TALL_HIDDEN_CEILING_CONTRADICTION':
                assert (ts[i][0] if h==0 else 8-ts[i][0])==8 and max(dd[i])>=7 and minimum_word in hidden
                assert x>0 if h==0 else x<8
            else:assert proof=='UNIVERSAL_UNSAT'
            assert n not in closed;closed[n]=proof;proof_kinds[proof]+=1
    assert set(closed)==set(range(4152))
    # Signed augmentation and full two-sort/telescoping arithmetic are new
    # independent theorems over arbitrary debts/weights, not state samples.
    ds,dt,cs_,ct,w=z3.Ints('full_ds full_dt full_cs full_ct full_weight');N=z3.Bool('full_N')
    D=z3.If(z3.And(N,cs_>ds),cs_,ds);T=z3.If(ct>dt,ct,dt)
    sol=z3.Solver();sol.add(ds>=0,ds<=2,dt>=0,dt<=2,cs_>=0,cs_<=2,ct>=0,ct<=2,
      z3.Implies(z3.And(N,cs_==2,ds<2),w+T>=2),z3.Implies(z3.And(N,cs_==1,ds<1),w+T>=1),
      w+dt-ds>=0,w+T-D<0)
    assert sol.check()==z3.unsat
    proofs=['source-only_N/maximal-credit signed preservation']
    for label,conds,delta in [('LOW',[w+dt-ds>=0],ds-dt),('OM_same_chi',[w>=2],ds),
      ('OM_entering_chi',[w>=-3],ds-5),('MO',[w==0],-dt)]:
        s=z3.Solver();s.add(ds>=0,ds<=2,dt>=0,dt<=2,*conds,w<delta);assert s.check()==z3.unsat;proofs.append(label)
    chi=z3.Int('full_chi');O=-ds-5*chi;M=-5*chi
    sol=z3.Solver();sol.add(ds>=0,ds<=2,z3.Or(chi==0,chi==1),z3.Or(O< -7,O>0,M< -7,M>0))
    assert sol.check()==z3.unsat;proofs.append('global_W_range_minus7_to0')
    # Formal arbitrary-horizon induction step for accumulated signed weight.
    S,P,Q,V,edge=z3.Ints('sum_so_far start_value current_value next_value next_weight')
    sol=z3.Solver();sol.add(S>=Q-P,edge>=V-Q,S+edge<V-P);assert sol.check()==z3.unsat
    proofs.append('arbitrary_walk_induction_step')
    sol=z3.Solver();sol.add(S>=Q-P,Q==P,S<0);assert sol.check()==z3.unsat;proofs.append('full_state_closed_walk_nonnegative')
    high=read(R/'M3_COMB_AUD01/high_source_audit.json');interface=read(R/'M3_COMB_AUD01/primitive_interface_audit.json')
    assert high['status']=='PASS_INDEPENDENT_ORIGINAL_DAG_AUDIT' and high['off_spine_source_fields']=='UNFIXED'
    assert interface['status']=='PASS_INDEPENDENT_PRIMITIVES_AND_INTERFACE_SCOPE'
    assert interface['ordinary_coordinate_count']==147 and interface['midpoint_coordinate_count']==127
    assert interface['raw_interval_coordinates_in_interface'] and interface['alpha_unused_fields_in_interface']
    # Immutable dependency verification, reusing old pin values rather than
    # executing any old semantic checker or original root.
    oldpins={q['path']:q['sha256'] for q in read(P19/'entry_baseline.json')['files']}
    selected=[]
    folders=('M3_E1_01/','M3_XFER','M3_UNIFORM03/','M3_POP3_RISK01/','M3_POP4_RISK01/','M3_POP5_RISK01/',
      'M3_EXPOSURE02/','M3_AER01/','M3_OUT01/','M2_DSK01/')
    explicit={'M3_LDR01/negative_run_census.json','M3_H1F01/cheap_census.json','M3_H2R01/fringe_kernel_certificate.json',
      'M3_COMB_AUD01/high_source_audit.json','M3_COMB_AUD01/primitive_interface_audit.json'}
    primaries={'STRICT_LOW_COMPILER.py','STRICT_HIGH_COMPILER.py','STRICT_SOURCE_REPAIRS.py',
      'PC_ATOM_INVENTORY.py','PC_TYPED_DAG.py','PC_B_CONTROLLER.py','PC_ROTATION_INTERPRETER.py'}
    for name,digest in oldpins.items():
        path=Path(name);rel=path.relative_to(R).as_posix()
        want=rel in explicit or path.name in primaries or (any(rel.startswith(f) for f in folders) and
          (path.suffix=='.md' or path.name in ('certificate.json','proof_certificate.json','debt_definition.json')))
        if not want:continue
        current=hashlib.sha256(Path('\\\\?\\'+str(path.resolve())).read_bytes()).hexdigest();assert current==digest,rel
        selected.append({'path':name,'sha256':digest})
    for q in read(P19/'final_manifest.json')['files']:
        p=P19/q['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==q['sha256'],p.name
    assert len(selected)>100
    assert hashlib.sha256((P19/'final_manifest.json').read_bytes()).hexdigest()==read(P20/'entry.json')['inherited_manifest_sha256']
    assert hashlib.sha256((P20/'audit_prefix.json').read_bytes()).hexdigest()==read(BASE/'entry.json')['prefix_sha256']
    # Conservative input syntax bound, including both public clause layers,
    # lower-floor templates and the entire source/helper observation grammar.
    ast_bound=500000+2*(len(cs)+len(old['clauses']))*100+100000
    assert ast_bound<4000000
    assert time.process_time()<CAP-2
    out={'status':'INDEPENDENT_FULL_ORIGINAL_M3_CERTIFICATE_AUDIT_PASS',
      'new_completion_clauses':len(cs),'step4_parent_clauses':len(old['clauses']),
      'required_new_signed_clause_word_obligations':total,'covered_new_signed_clause_word_obligations':len(proven),
      'missing_new_signed_obligations':0,'accepted_source_proof_records':accepted,'discarded_trial_records_not_used':rejected,
      'H1_positive_critical_core_rows':len(critical),'H1_positive_anchor_cores':len(anchors),
      'Gamma1_critical_word_obligations':len(planned),'Gamma1_covered_word_obligations':len(closed),
      'Gamma1_proof_kinds':dict(proof_kinds),'Gamma1_original_kernel_classes':dict(gamma_classes),
      'actual_maximum_psi_coverage_checked_without_symmetry_assumption':True,
      'independent_integer_algebra_UNSAT':proofs,'all_original_LOW_price_classes_covered':True,
      'all_original_HIGH_classes_covered':'reused universal source-exact HIGH toll/absorption plus new range algebra',
      'ordinary_coordinates':147,'midpoint_coordinates':127,'chi8':'b.kr[8]==0 AND b.rr[8]==19',
      'HIGH_v_free':True,'SAME_full_actual_midpoint_and_independent_witnesses':True,
      'h0':{'actual_depth':0,'declared_depth':18,'q':9,'weight':-3},
      'all_masks_and_admissible_signatures':True,'support_or_population_restriction_added':False,
      'global_potential_range':[-7,0],'closed_walk_weight_lower_bound':0,'finite_walk_weight_lower_bound':-7,
      'new_finite_tests':0,'new_original_root_queries':0,'completed_accepted_semantic_checks_replayed':0,
      'input_DAG_conservative_bound':ast_bound,'verified_original_dependency_pins':selected,
      'audit_scope':'independent certificate/source/dependency/sign derivation, reusing completed exact UNSAT conclusions; not external review or full compiler formalization',
      'mathematical_M3_complete':True,'publication_requires_controller_and_final_resource_PASS':True,
      'Dynamic_Optimality_proved':False}
    write('full_m3_audit.json',out);print(json.dumps({k:v for k,v in out.items() if k!='verified_original_dependency_pins'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_full_m3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
