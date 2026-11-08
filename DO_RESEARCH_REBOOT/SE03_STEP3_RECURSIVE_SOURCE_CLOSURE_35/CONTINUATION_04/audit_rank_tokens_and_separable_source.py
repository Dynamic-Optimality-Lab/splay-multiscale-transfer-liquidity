"""Distinct source controls for the uniform rank/return lemmas.
Global finite-graph/source-embedding arguments remain written proofs,
not an assertion that a finite source replay formally verifies them.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def keys(t):return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])
def depths(t):
    out={}
    def go(u,d):
        if u is not None:out[u[0]]=d;go(u[1],d+1);go(u[2],d+1)
    go(t,0);return out
def balanced(ks):
    if not ks:return None
    j=len(ks)//2;return (ks[j],balanced(ks[:j]),balanced(ks[j+1:]))
def audit_rotation(rot):
    before,after=tup(rot['before']),tup(rot['after']);u=before
    while u[0]!=rot['pivot']:u=u[1] if rot['pivot']<u[0] else u[2]
    p=u[0]
    if rot['direction']=='right':x=u[1][0];negative=set(keys(u[1][1]))|{x};positive=set(keys(u[2]))|{p}
    else:x=u[2][0];negative=set(keys(u[2][2]))|{x};positive=set(keys(u[1]))|{p}
    assert positive and negative and not positive&negative
    db,da=depths(before),depths(after);assert set(db)==set(da)
    order=sorted(db)
    for subset in (positive,negative):
        positions=sorted(order.index(k) for k in subset);assert positions==list(range(positions[0],positions[-1]+1))
    assert all(da[k]-db[k]==int(k in positive)-int(k in negative) for k in db)
    return {'bit':rot['bit'],'decrease':sorted(negative),'increase':sorted(positive)}
def main():
    global V
    sp=importlib.util.spec_from_file_location('RT35_return_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    r=1024;K=list(range(1,r+1));BF=balanced(K);g=BF[0];dep=depths(BF);x=min(k for k in K if dep[k]==max(dep.values()))
    assert dep[x]>=10 and 2**10-1<r
    if x<g:A=(g,(x,balanced([k for k in K if k<x]),balanced([k for k in K if x<k<g])),balanced([k for k in K if k>g]))
    else:A=(g,balanced([k for k in K if k<g]),(x,balanced([k for k in K if g<k<x]),balanced([k for k in K if k>x])))
    def mirror(t):return None if t is None else (r+1-t[0],mirror(t[2]),mirror(t[1]))
    controls=[];alltokens=[]
    for orientation,aa,bb,xx,gg in [('LR',A,BF,x,g),('RL',mirror(A),mirror(BF),r+1-x,r+1-g)]:
        asrc=V.Mutable(aa);bsrc=V.Mutable(bb);H=Q=0;rows=[]
        for t,k in enumerate((xx,gg),1):
            ab,bbefore=asrc.snapshot(),bsrc.snapshot();h,_,ev=asrc.splay(k,True);_,q,_=bsrc.splay(k,False)
            H+=h;Q+=q;assert h==1 and len(ev)==1 and ev[0]['pattern'] in ('L','R')
            tok=[audit_rotation(rot) for e in ev for rot in e['rotations']];alltokens.extend(tok)
            rows.append({'t':t,'key':k,'kind':'K','a':h,'qF':q,'A_before':ab,'BF_before':bbefore,
              'A_after':asrc.snapshot(),'BF_after':bsrc.snapshot(),'A_events':ev,'rank_tokens':tok})
        assert tup(asrc.snapshot())==aa and H==2 and Q>=5
        controls.append({'orientation':orientation,'physical_keys':r,'g':gg,'x':xx,'H':H,'Q':Q,'price':4-Q,
          'A_returns_exactly':True,'B_returns_only_root':True,'rows':rows,'full_period_replay_claimed':False})
    # Reuse the independently replayed dirty source: no repeated primitive run.
    dirty=json.loads((F/'cluster_collateral_closed_source.json').read_text());count=0;unitids=set();sum_delta={}
    for row in dirty['period_rows']:
        for event in row['A_events']:
            for rot in event['rotations']:
                token=audit_rotation(rot);unit=(row['t'],event['j'],rot['bit']);assert unit not in unitids;unitids.add(unit);count+=1
                for k in token['decrease']:sum_delta[k]=sum_delta.get(k,0)-1
                for k in token['increase']:sum_delta[k]=sum_delta.get(k,0)+1
    assert not any(sum_delta.values())
    docs=['BALANCED_SOURCE_RANK_TOKENS.md','SEPARABLE_SOURCE_POTENTIAL_OBSTRUCTION.md']
    report={'status':'PASS_DISTINCT_SOURCE_CONTROLS_AND_RANK_IDENTITIES','source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'large_source_controls':controls,'reused_dirty_period_rotations':count,'distinct_dirty_tokens':len(unitids),
      'closed_dirty_rank_vector':sum_delta,'universal_proofs':'written source rotation identities and finite sink-SCC proof; not formal verification',
      'JR35':'OPEN','new_funding_injection_proved':False,
      'input_sha256':{p:sha(F/p) for p in docs+['cluster_collateral_closed_source.json','independent_source_bridges_collateral_audit.json']}}
    with (F/'independent_rank_return_controls.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('large_source_controls','closed_dirty_rank_vector','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify114_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
