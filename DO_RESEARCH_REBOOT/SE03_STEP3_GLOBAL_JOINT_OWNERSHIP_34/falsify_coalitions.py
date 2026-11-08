"""Candidate-directed GPR falsification on two nonmonotone source words.
All new primitive splays are charged; this is not a universal proof.
"""
import importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import retirement_pools as R
CAP=float(sys.argv[1]);QCAP=min(540,int(sys.argv[2]));START=time.process_time()
spec=importlib.util.spec_from_file_location('accepted_functional_source',B/'audit_core39.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
S.CAP=CAP;S.QCAP=QCAP;S.START=START;S.CALLS=0
def save(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def construct(helper):
    M=list(range(1,14,2));prefix=[13,5,11,3,9,1,7];keeps=prefix+M+list(reversed(M))
    word=[]
    for x in keeps:
        if x!=helper:word.append(('D',helper))
        word.append(('K',x))
    word.extend(('D',x) for x in list(range(1,14))+list(range(12,0,-1)))
    A=BF=BE=S.vine(1,13);initial=A;cf=ce=();seen={(A,BF,BE,cf,ce):0};copies=[];boundaries=[(A,BF,BE,cf,ce)]
    for c in range(3):
        if S.CALLS+sum(1+(k=='K')+(k=='K' and x!=3) for k,x in word)>QCAP:return {'status':'BATCH_LIMIT_BEFORE_NEXT_COMPLETE_COPY','helper':helper,'copies':len(copies)}
        rr=[]
        for i,(kind,x) in enumerate(word):
            old=A,BF,BE;A,a,_,_=S.splay(A,x);q=qe=0
            if kind=='K':
                gen=BF[0]!=x;BF,_,q,_=S.splay(BF,x)
                if gen:cf=(x,)+tuple(y for y in cf if y!=x)
                if x!=3:
                    egen=BE[0]!=x;BE,_,qe,_=S.splay(BE,x)
                    if egen:ce=(x,)+tuple(y for y in ce if y!=x)
            rr.append(dict(t=c*len(word)+i+1,kind=kind,key=x,a=a,qF=q,qE=qe,A_before=old[0],BF_before=old[1],BE_before=old[2],A_after=A,BF_after=BF,BE_after=BE,chart_F=cf,chart_E=ce))
        copies.append(rr);state=A,BF,BE,cf,ce;boundaries.append(state)
        if state in seen:
            u=seen[state];period=sum(copies[u:c+1],[]);zz=dict(status='ORIGINAL_TRIPLE_AND_CHART_CLOSED_CANDIDATE_CONTROL',helper=helper,initial_diagonal=initial,erase=3,word=word,prefix_rows=sum(copies[:u],[]),period_rows=period,period=[period[0]['t'],period[-1]['t']],period_start=boundaries[u],period_end=state)
            rows=R.normalize(zz,'c33');model=R.build(rows);zz['scope']=model['scope'];zz.update(r=model['r'],core=model['core'])
            if model['scope']=='MAXIMAL_CORE':
                zz['pool_test']=R.cover(model);zz['natural_prior_test']=R.cover(model,model['h0']);zz['macros']=model['macros'];zz.update(D=len(model['D']),U=len(model['U']),H=sum(r['a'] for r in period),Q=sum(r['qF'] for r in period))
            return zz
        seen[state]=c+1
    return {'status':'NO_FULL_RECURRENCE_IN_THREE_COPIES','helper':helper,'copies':len(copies)}
def main():
    results=[]
    for helper in (7,4):
        z=construct(helper);results.append(z)
        print(json.dumps({k:z.get(k) for k in ('helper','status','scope','r','core','D','U')}|{'fresh_source_queries_cumulative':S.CALLS,'pool_complete':z.get('pool_test',{}).get('complete')}),flush=True)
        if not z.get('pool_test',{}).get('complete',True):break
    save('nonmonotone_source_controls.json',dict(status='BOUNDED_GPR_FALSIFICATION_ONLY',cases=results,source_engine_calls=S.CALLS,source_queries=S.CALLS,universal_JIO34='OPEN',engine_sha256=R.pin(B/'audit_core39.py')))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_core40_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=S.CALLS,source_engine_calls=S.CALLS),f)
