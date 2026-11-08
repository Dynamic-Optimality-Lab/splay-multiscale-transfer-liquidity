"""Independent interval grammar and mutable-parent original B replay."""
import functools,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time()
sp=importlib.util.spec_from_file_location('independent_pointer_B_core13',B/'audit_verify79.py')
V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V);V.CAP=CAP;V.QCAP=QCAP;V.START=START;V.CALLS=0
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fr(t):return None if t is None else (t[0],fr(t[1]),fr(t[2]))
@functools.lru_cache(None)
def interval(lo,hi):
    if lo>hi:return (None,)
    mass=sum(1 if k%2 else -1 for k in range(lo,hi+1))
    if mass not in (0,1):return ()
    out=[]
    for root in range(lo,hi+1):
        if (root%2)!=mass:continue
        for l in interval(lo,root-1):
            for r in interval(root+1,hi):out.append((root,l,r))
    return tuple(out)
def main():
    grammar=read(F/'maximal_B_grammar.json');table=read(F/'full_B_actions.json');old=read(F/'cached_product_inputs.json')
    for n,h in table['input_sha256'].items():assert sha(F/n)==h
    ts=list(map(fr,grammar['trees']));idx={t:i for i,t in enumerate(ts)}
    assert set(interval(1,13))==set(ts) and len(ts)==3876
    cache={}
    for e in old['B_edges']:cache[idx[fr(old['B_trees'][e['source']])],e['key']]=(idx[fr(old['B_trees'][e['target']])],e['q'])
    reused=eligible=0;assert QCAP>=table['fresh_genuine_actions']
    for i,t in enumerate(ts):
        for j,x in enumerate(grammar['marks']):
            row=table['actions'][i][j]
            if x==t[0]:assert row['origin']=='ROOT_IDENTITY' and row['destination']==i and row['q']==row['H']==0;continue
            if (i,x) in cache:
                di,q=cache[i,x];assert row['origin']=='ACCEPTED_CACHE' and row['destination']==di and row['H']==row['q']==q
                reused+=1;eligible+=1;continue
            assert row['origin']=='NEW_ORIGINAL_SPLAY'
            tr=V.Mutable(t);h,q,ev=tr.splay(x,False);after=tr.snapshot()
            ok=h==q and all(e['pattern'] in ('LL','RR') and e['grandparent']%2 and e['parent'] is not None and not e['parent']%2 for e in ev)
            assert (h,q)==(row['H'],row['q']) and row['patterns']==[e['pattern'] for e in ev] and bool(ok)==row['admissible']
            if ok:assert after in idx and idx[after]==row['destination'];eligible+=1
            else:assert after not in idx and row['destination']==-1
    assert reused==136 and V.CALLS==table['fresh_genuine_actions']==23120 and eligible==table['admissible_genuine_edges']==13184
    oldctl=(B/'run_phase_1440.py').read_text();newctl=(B/'run_phase_3050000.py').read_text()
    assert newctl.replace('entry_authorized3050000.json','entry_authorized1440.json')==oldctl
    en=read(B/'entry_authorized3050000.json');eo=read(B/'entry_authorized1440.json')
    assert en['remaining_conservative_queries']==eo['remaining_conservative_queries']+50000 and en['query_limit']==3050000
    assert all(en[k]==eo[k] for k in eo if k not in ('remaining_conservative_queries','query_limit'))
    report={'status':'PASS_COMPLETE_CORE13_ORIGINAL_B_ACTIONS_AND_GRAMMAR',
      'static_states':3876,'all_candidate_genuine_actions':23256,'accepted_actions_reused':reused,
      'fresh_pointer_source_actions':V.CALLS,'admissible_genuine_edges':eligible,
      'independent_static_grammar':'all interval root choices with signed mass constraints, no producer grammar import',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'coverage':'every original closed maximal-core13 B source; no claim each static state is recurrent',
      'controller_amendment':'entry filename and explicitly authorized query allowance only',
      'trust':'separate mutable-parent implementation, same research agent; not external or formal review',
      'JR35':'OPEN_PENDING_PRODUCT_SOURCE_ANALYSIS',
      'input_sha256':{'maximal_B_grammar.json':sha(F/'maximal_B_grammar.json'),'full_B_actions.json':sha(F/'full_B_actions.json'),
        'query_authorization.json':sha(F/'query_authorization.json'),'MAXIMAL_CORE_GRAMMAR.md':sha(F/'MAXIMAL_CORE_GRAMMAR.md')},
      'engine_sha256':sha(B/'audit_verify79.py')}
    with (F/'independent_full_B_actions_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify96_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':V.CALLS,'source_engine_calls':V.CALLS},f)
