"""New observable on the old exact C20 word, preserving every operation."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def material(t):return (t[0],material(t[1]),material(t[2])) if isinstance(t,list) else None
def main():
    global V
    base=P/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/rr7_source_candidate.json'
    recipe=P/'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20/saturated_source_word.json'
    old=json.loads(base.read_text());spec=json.loads(recipe.read_text());W=old['word'];word=[]
    for item in spec['word_recipe']:
        if 'base_range' in item:
            a,b=item['base_range'];word+=W[a-1:b]
        elif 'new_actual_operations' in item:word+=item['new_actual_operations']
        else:
            a,b=item['new_DELETE_operations_of_base_targets'];word+=[['D',x] for k,x in W[a-1:b]]
    assert len(word)==167 and [x for k,x in word if k=='K']==[x for k,x in W[:41] if k=='K']+[1,5,1,3]+[x for k,x in W[41:] if k=='K']
    sp=importlib.util.spec_from_file_location('C20_new_observable_source',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    A=material(old['initial_A']);BF=material(old['initial_BF']);a0,b0=A,BF;rows=[]
    for t,(kind,x) in enumerate(word,1):
        ab,bb=A,BF;A,h,_,ae=V.splay(A,x,True);q=0;be=[]
        if kind=='K':BF,_,q,be=V.splay(BF,x,True)
        rows.append({'t':t,'kind':kind,'key':x,'a':h,'qF':q,'genuine_F':kind=='K' and bb[0]!=x,
          'A_before':ab,'A_after':A,'BF_before':bb,'BF_after':BF,'A_events':ae,'BF_events':be})
    assert A==a0 and BF==b0 and sum(r['qF'] for r in rows)==66
    assert {r['key'] for r in rows if r['genuine_F']}==set(range(1,14,2))
    for t,h,q in ((72,1,2),(73,1,1),(74,1,6)):
        assert (rows[t-1]['a'],rows[t-1]['qF'])==(h,q)
    r={'status':'ORIGINAL_C20_WORD_FULL_A_B_SOURCE_REPLAY','word':word,'initial_A':a0,'initial_BF':b0,'period_rows':rows,
      'A':sum(r['a'] for r in rows),'QF':66,'r':7,'physical_keys':13,'A_B_closed':True,
      'reaching_prefix':'actual A-only canonical Gamma(initial_BF,initial_A) from a common diagonal',
      'paired_erased_and_chart_closure':'finite actual recurrence after full A/B closure, inherited source bridge; not newly replayed',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'JR35':'OPEN','old_source_or_owners_changed':False,
      'input_sha256':{str(p):sha(p) for p in (base,recipe,P/'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20/SATURATED_SOURCE_WITNESS.md',
        B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md')}}
    with (F/'C20_hybrid_source_control.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k not in ('word','initial_A','initial_BF','period_rows','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_core52_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
