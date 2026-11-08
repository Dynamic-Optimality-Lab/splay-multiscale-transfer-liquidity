"""Final source ownership/provenance audit and bounded stronger NEG2 check."""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as f
account={'source_engine_calls':0,'new_finite_tests':0};M=(1,3,5,7,9,11)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as g:json.dump(v,g,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def term(t):return ('leaf',t) if isinstance(t,str) else f.node(t[0],term(t[1]),term(t[2]))
def step(t,x):
    account['source_engine_calls']+=1;return f.trace(t,x)
def main():
    physical=[];family_results=[]
    for filename in ('entry_family.json','e1_family.json'):
        fam=json.loads((B/filename).read_text());owners={};bits=[];demands=[]
        for i,p in enumerate(fam['packets']):
            for occ in p['occurrences']:
                assert occ not in owners;owners[occ]=i
        assert set(owners)==set(range(1,len(fam['rows'])+1))
        offset=len(fam['reaching_prefix']);operations=[]
        for r in fam['rows']:
            absocc=offset+r['occurrence']
            aa=[{'family':filename,'absolute_occurrence':absocc,'A_StepEv':j,'bit':b}
                for j in range(1,r['a']+1) for b in (0,1)]
            bb=[{'family':filename,'absolute_occurrence':absocc,'BF_StepEv':j}
                for j,e in enumerate(r['BF_events'],1) if e['kind']=='DOUBLE']
            bits+=aa;demands+=bb
            operations.append({'absolute_occurrence':absocc,'period_occurrence':r['occurrence'],
                'mode':r['mode'],'key':r['target'],'packet_owner':owners[r['occurrence']],
                'A_bit_units':aa,'BF_double_demands':bb})
        assert len(bits)==2*fam['costs']['A'] and len(demands)==fam['costs']['QF']
        assert len({json.dumps(v,sort_keys=True) for v in bits})==len(bits)
        assert len({json.dumps(v,sort_keys=True) for v in demands})==len(demands)
        assert fam['charts'][0]['recent_before']==fam['charts'][-1]['recent_after']
        assert sum(p['H'] for p in fam['packets'])==fam['costs']['A']
        assert sum(p['Q'] for p in fam['packets'])==fam['costs']['QF']
        assert all(p['Q']!=5 for p in fam['packets'])
        physical.append({'family':filename,'reaching_prefix_length':offset,'period_operations':operations,
            'all_operations_covered_once':True,'no_unit_assigned_or_spent':True})
        family_results.append({'family':filename,'period':len(fam['rows']),'prefix':offset,
            'A_bit_units':len(bits),'BF_demands':len(demands),'cold_negative':True,'entry':fam['critical'][0]['entry_class']})
    out('absolute_source_ids.json',{'families':physical,'physical_allocation_created':False})
    # Check the stronger all-NEG2-source predicate on the SAME closed suffix
    # cells, to avoid silently overlooking a hot negative-two obstruction.
    suffix=json.loads((B/'suffix_analysis.json').read_text());hot=[]
    for rep in suffix['reports']:
        for i,row in enumerate(rep['states']):
            a,b,e,r=row['state'];a,b=term(a),term(b)
            for x in M:
                if x==b[1]:continue
                aa,ae=step(a,x);bb,be=step(b,x)
                q=sum(v[0]!='ZIG' for v in be)
                if len(ae)!=1:continue
                if q==4:hot.append({'family':rep['family'],'state':i,'target':x,'cold':x==r[-1]})
                if q==5:
                    for y in (1,11):
                        if y==x:continue
                        _,ev=step(aa,y);_,bv=step(bb,y)
                        if len(ev)==1 and sum(z[0]!='ZIG' for z in bv)==1:
                            hot.append({'family':rep['family'],'state':i,'target':x,'successor':y,'cold':x==r[-1]})
    out('all_negative_two_suffix_check.json',{'scope':'the two explicit suffix certificates only',
        'negative_two_source_hits':hot,'not_a_new_universal_graph':True})
    assert not hot,'a stronger potential obstruction needs separate source closure audit'
    pins=json.loads((B/'dependency_pins.json').read_text());bad=[]
    for p in pins['pins']:
        q=ROOT/p['path']
        if not q.is_file() or sha(q)!=p['sha256']:bad.append(p['path'])
    for p in pins['external_pins']:
        if sha(Path(p['path']))!=p['sha256']:bad.append(p['path'])
    assert not bad
    required=['SOURCE_SPEC.md','NEG2_EXIT_GEOMETRY.md','FIRST_LOWERING_ENTRY.md','NEUTRAL_ZERO_PREFIX.md',
        'PLUS_ONE_INTERVENTION.md','ENTRY_BARRIER.md','POST_LOWERING_RESIDUAL.md','SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md']
    assert all((B/n).is_file() for n in required)
    audit=json.loads((B/'independent_audit.json').read_text());assert audit['status']=='PASS_BOTH_ENTRY_CLASSES_AND_EXAMPLE_SUFFIX_CLOSURES'
    out('dependency_revalidation.json',{'status':'PASS','pins_verified':len(pins['pins']),
        'external_pins_verified':len(pins['external_pins']),'mismatches':bad})
    out('seal_audit.json',{'status':'PASS_OUTCOME_B_ONLY','outcome':'B','witness_families':family_results,
        'all_physical_operation_and_period_interfaces':True,'independent_engine_and_reflections':'PASS',
        'generic_exit_source_proof_review':{
            'singleton_q4':'five path marks plus one mass-zero offpath block; extra mark parent determines S5/S4',
            'paired_q5_q1':'six-mark fan then extreme marked leaf return; sole-child marked root P4',
            'zero_length':'T root degrees1,4,5 cannot equal loss-source degrees2,3',
            'N_prefix':'S4/P4 actual q2 outputs D4; all D4 q2 accesses lower; source paths only narrowed by legality',
            'A_no_invented_normalform':'original six one-event cases, actual source inventories preserved',
            'witnesses':'E0/E1 full original closures and exact charts independently checked',
            'post_loss':'restricted suffix guards and induction only; generic residual OPEN'},
        'Sigma_predecessor_leaf3_preserved':True,'new_potential_constructed':False,
        'width_two_obstruction':False,'original_CD_counterexample':False,'Step2':'OPEN','Universal_CD':'OPEN',**account})
    print(json.dumps({'status':'PASS_OUTCOME_B_ONLY','pins':len(pins['pins']),
        'family_interfaces':family_results,'all_negative_two_suffix_hits':len(hot),**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
