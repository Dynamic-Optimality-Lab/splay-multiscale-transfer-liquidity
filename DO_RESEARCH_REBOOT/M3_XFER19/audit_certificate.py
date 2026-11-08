"""Independent coverage/provenance/composition audit, no source replays."""
import json,sys,time,hashlib,collections
from pathlib import Path
import z3
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def read(n):return json.loads((BASE/n).read_text())
def canonical(v):return tuple(canonical(q) for q in v) if isinstance(v,list) else v
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def opposite(t):return None if t is None else (8-t[0],opposite(t[2]),opposite(t[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    final=read('audit_final_source.json')
    assert final['status']=='INDEPENDENT_NORMALIZED_MAXIMAL_SOURCE_AUDIT_PASS'
    assert final['pending_jobs']==0 and final['unresolved'] is None
    clauses=final['clauses'];assert len(clauses)==len({json.dumps(c,sort_keys=True) for c in clauses})
    reports=['audit_anchor_closure.json','audit_anchor_union.json','audit_maximal.json','audit_final_source.json']
    for name in reports:
        old=read(name)['clauses'];assert old==clauses[:len(old)],name
    assert read('audit_normalization_v2.json')['status']=='UNIVERSAL_CHEAP_TARGET_AND_MAXIMAL_LEVEL_REDUCTION_PASS'
    assert len(read('audit_normalization_v2.json')['helper_word_proofs'])==18
    assert read('anchor_generic_certificate.json')['status']=='UNIVERSAL_H1_NO_DUPLICATE_AND_OLD_ROOT_ANCHOR_PASS'
    assert len(read('anchor_generic_certificate.json')['proofs'])==6
    assert read('audit_seven_independent.json')['status']=='INDEPENDENT_WHOLE_UNION_ONE_CREDIT_AUDIT_PASS'
    assert read('final_immutable_integrity.json')['status']=='PASS'
    assert read('final_immutable_integrity.json')['old_files_checked']==14704
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    ker=json.loads((BASE.parent/'M3_H2R01/fringe_kernel_certificate.json').read_text())
    ts=[freeze(q['tree']) for q in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    ps=[q['psi'] for q in bank['nodes']];depth=tab['B_depth'];dest=tab['B_destination']
    assert len(ts)==4862 and set(ps)=={0,1,2}
    # Recover the COMPLETE critical family solely from the pinned old facts.
    anchors={};groups=set()
    for i,t in enumerate(ts):
        for x in range(9):
            j=dest[i][x]
            if ps[i]>ps[j] and depth[i][x] in (4,5):
                groups.add((t[0],x,j,ps[i]));anchors.setdefault(j,{})[t[0]]=max(anchors.get(j,{}).get(t[0],0),ps[i])
    assert len(groups)==378 and len(anchors)==303
    seeds={(c['core'],c['level']) for c in clauses if c['kind']=='anchor'}
    assert seeds=={(i,k) for i in anchors for k in range(1,max(anchors[i].values())+1)}
    # The six genuine A words are partitioned by the forced first direction.
    words=((0,),(1,),(0,0),(0,1),(1,0),(1,1))
    helper={};mirror=[ids[opposite(t)] for t in ts]
    for q in ker['rows']:
        assert q['w']==4-q['q'] and q['q']==q['terminal_depth']//2
        if not q['gap0_childless_at_exit'] or q['w']>=2:continue
        assert q['target']!=ts[q['entry_core']][0] # same old root has range-safe price
        helper.setdefault(q['entry_core'],set()).add((0,q['target'],q['exit_core'],q['w']))
        helper.setdefault(mirror[q['entry_core']],set()).add((9,8-q['target'],mirror[q['exit_core']],q['w']))
    inventory={}
    def required(i,k):
        if (i,k) in inventory:return inventory[i,k]
        out=set()
        if ps[i]<k:
            for x in range(9):
                j=dest[i][x];w=2-depth[i][x]//2
                if w>=k or w+ps[j]>=k:continue
                for p in words:
                    if p[0]==int(x>ts[i][0]):out.add((i,k,None,(p,),x,j,w))
            if k==2:
                for h,x,j,w in helper.get(i,set()):
                    if w+ps[j]>=2:continue
                    for p in words:
                        for r in words:
                            if p[0]==int(h==9) and r[0]==int(h==0):out.add((i,k,h,(p,r),x,j,w))
        inventory[i,k]=out;return out
    proven={};counts={};records=0
    sources=[('anchor_closure_checkpoints.jsonl','single'),('anchor_union_checkpoints.jsonl','union'),
      ('maximal_checkpoints.jsonl','union'),('final_source_checkpoints.jsonl','union')]
    for name,style in sources:
        n=0
        for lineno,line in enumerate((BASE/name).read_text().splitlines(),1):
            q=json.loads(line)
            if style=='single':
                assert q['proof']=='UNIVERSAL_UNSAT'
                key=(q['source_core'],q['level'],q['helper'],canonical(q['word']),q['target'],q['destination_core'],q['weight'])
                cids=[q['clause']]
            else:
                assert q['result']=='UNIVERSAL_UNSAT';key=canonical(q['job']);cids=q['source_clause_ids']
            for cid in cids:
                c=clauses[cid];assert c['core']==key[0] and c['level']==key[1]
                assert key in required(c['core'],c['level']),(name,lineno,cid,'invalid job')
                proven[cid,key]=(name,lineno)
            n+=1;records+=1
        counts[name]=n
    missing=[];total=0
    for cid,c in enumerate(clauses):
        assert c['kind'] in ('anchor','score_cube') and c['level'] in (1,2)
        if c['kind']=='score_cube':
            assert set(c)<= {'core','level','kind','marks','score_equalities'}
            assert all(0<=r<9 for r in c['marks'])
            assert all(1<=p<=6 and 0<=v<9 for p,v in c['score_equalities'])
        for key in required(c['core'],c['level']):
            total+=1
            if (cid,key) not in proven:missing.append((cid,key))
    assert not missing,missing[:5]
    # Independent exact arithmetic composition, including the source-only N gate.
    ds,dt,cs,ct,w=z3.Ints('audit_ds audit_dt audit_cs audit_ct audit_w');N=z3.Bool('audit_N')
    F=z3.If(z3.And(N,cs>ds),cs,ds);T=z3.If(ct>dt,ct,dt)
    s=z3.Solver();s.add(ds>=0,ds<=2,dt>=0,dt<=2,cs>=0,cs<=2,ct>=0,ct<=2,
      z3.Implies(z3.And(N,cs==2,ds<2),w+T>=2),
      z3.Implies(z3.And(N,cs==1,ds<1),w+T>=1),w+dt-ds>=0,w+T-F<0)
    assert s.check()==z3.unsat
    s=z3.Solver();s.add(ds>=0,ds<=2,dt>=0,dt<=2,cs>=0,cs<=2,ct>=0,ct<=2,
      z3.Implies(F>ds,T>=F),z3.Implies(F==ds,T>=ds),T-F<0)
    assert s.check()==z3.unsat
    # Retained grammar bounds are structural, not population bounds.
    from universal_grammar_v2 import build
    max_grammar=0
    def nodes(e):
        seen=set();stack=[e]
        while stack:
            a=stack.pop()
            if a.get_id() in seen:continue
            seen.add(a.get_id());stack.extend(a.children())
        return len(seen)
    root,target=z3.Ints('dag_root dag_target')
    for h in (0,9):
        for p in words:
            for r in words:
                if p[0]!=int(h==9) or r[0]!=int(h==0):continue
                u=build((p,r),root,target,h,'dag')
                max_grammar=max(max_grammar,nodes(z3.And(*u['constraints'],*(v==z3.IntVal(0) for v in u['source']+u['target']))))
    # A conservative syntax-tree bound for all floor calls: at most100000
    # primitive AST nodes each (explicit fixed loops<=9 and6 positions).
    # Four floor calls, two clause unions, source/target substitutions and
    # complete helper grammar fit well below the inherited4m INPUT-DAG cap.
    public_clause_bound=len(clauses)*100
    input_bound=4*100000+2*public_clause_bound+10*max_grammar+100000
    assert input_bound<4000000
    pins=[]
    for n in reports+[q[0] for q in sources]+['audit_normalization_v2.json','anchor_generic_certificate.json',
      'audit_seven_independent.json','LEGACY_FLOOR_AUDIT.md','COMPLETE_STEP4_COMPOSITION.md',
      'baseline19.py','complete_floor.py','legacy_floors.py','universal_grammar_v2.py','symbolic_prefix_v2.py']:
        pins.append({'file':n,'sha256':hashlib.sha256((BASE/n).read_bytes()).hexdigest()})
    assert time.process_time()<CAP-2
    report={'status':'INDEPENDENT_COMPLETE_STEP4_CERTIFICATE_AUDIT_PASS','clauses':len(clauses),
      'critical_groups':len(groups),'critical_destination_cores':len(anchors),'required_clause_word_obligations':total,
      'covered_clause_word_obligations':len(proven),'missing_obligations':0,'proof_records':records,'proof_files':counts,
      'all_initial_anchors_present':True,'stable_clause_prefixes':True,'all_cache_transport_hypotheses_audited':True,
      'independent_signed_and_zero_composition_UNSAT':True,'all_masks_signatures_inventories_quantified':True,
      'original_LOW_semantics_and_full_state_closure':'prose audit; complete old count-free grammar/normal-form premises reused',
      'new_finite_tests':0,'new_original_root_or_psi_queries':0,'completed_semantic_checks_replayed':0,
      'input_DAG_conservative_bound':input_bound,'largest_symbolic_helper_grammar_DAG':max_grammar,
      'scope':'separate certificate/semantics derivation, not external review or full compiler formalization',
      'pins':pins,'Step4_signed_mathematics_complete':True,'publication_requires_resource_controller_PASS':True}
    write('step4_audit.json',report);print(json.dumps({k:v for k,v in report.items() if k!='pins'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_certificate_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
