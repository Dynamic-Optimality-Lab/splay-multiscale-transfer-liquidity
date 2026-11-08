"""Reverse exact cost reachability for HIGH-envelope exceptions."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    cp=F/'global_probe11_H3_DAG_13.pkl';ep=F/'independent_probe11_HIGH_envelope_H3_13.json'
    env=json.loads(ep.read_text());assert env['input_sha256'][cp.name]==sha(cp)
    assert env['H_ge_4_failed_envelopes']==0
    failures=env['first_failures'];assert len(failures)==env['failed_envelopes']
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:small={k:v for k,v in pickle.load(f).items() if k in ('classes','roots')}
    with (F/'probe11_source_actions.pkl').open('rb') as f:prim={k:v for k,v in pickle.load(f).items() if k in ('destination','H','Q','roots')}
    with cp.open('rb') as f:z=pickle.load(f)
    D,H,Q=prim['destination'],prim['H'],prim['Q'];n=len(H);roots=small['roots'];assert np.array_equal(roots,prim['roots'])
    assert len(z['nodes'])+n*8+len(z['columns'])<2000000
    def unpack(root,count):
        out=np.empty(count,dtype=np.int8)
        def write(i,a,b):
            if a>=count:return
            if i<0:out[a:min(count,b)]=-i-1;return
            x,y=z['nodes'][i];m=(a+b)//2
            write(x,a,m);write(y,m,b)
        write(root,0,1<<(count-1).bit_length())
        return out
    records=[];witnesses=[];tests=0
    for row in failures:
        b,bt,x,q=(row[k] for k in ('B_source','B_target','KEEP','Q'));xx=x-1;g=int(roots[b]);assert g!=x
        assert (int(D[b,xx]),int(Q[b,xx]))==(bt,q)
        aa=small['classes'][g-1];bb=small['classes'][x-1]
        ds=unpack(z['columns'][b],len(aa));dt=unpack(z['columns'][bt],len(bb))
        cost=6-q;viol=0;checks=[]
        for lev in range(cost+int(dt.min())+1,int(ds.max())+1):
            bad=np.zeros(n,dtype=np.bool_);bad[bb]=dt<lev-cost
            fin=bad[D[:,xx]]
            back=[None]
            for h in (1,2,3):
                r=fin&(H[:,xx]==h)
                for k in range(1,h):
                    for y in range(11):
                        r|=(H[:,y]==k)&back[h-k][D[:,y]]
                back.append(r)
            active=aa[ds==lev];hits=active[back[3][active]]
            tests+=len(active);viol+=len(hits)
            checks.append({'D_source':lev,'A_starts':len(active),'has_bad_endpoint_count':len(hits)})
            if len(hits):
                a=int(hits[0]);s=a;h=3;word=[]
                while h:
                    if int(H[s,xx])==h and fin[s]:word.append(('K',x));s=int(D[s,xx]);h=0;break
                    for y in range(11):
                        k=int(H[s,y]);t=int(D[s,y])
                        if 0<k<h and back[h-k][t]:
                            word.append(('D',y+1));s=t;h-=k;break
                    else:raise AssertionError('missing exact reverse witness')
                assert bad[s] and word[-1]==('K',x)
                j=int(np.flatnonzero(bb==s)[0]);assert cost+int(dt[j])-lev<0
                witnesses.append({'B_source':b,'B_target':bt,'A_source':a,'A_target':s,'H':3,'Q':q,
                  'D_source':lev,'D_target':int(dt[j]),'source_word':word})
        records.append({'B_source':b,'B_target':bt,'KEEP':x,'Q':q,'starts_with_actual_violation':viol,'threshold_checks':checks})
        assert time.process_time()-START<CAP-2
    report={'status':'ALL_ACTUAL_H3_INEQUALITIES_PASS_CHECKPOINT13' if not witnesses else 'ACTUAL_H3_INEQUALITY_FAILURES_CHECKPOINT13',
      'candidate':cp.name,'all_OTHER_H3_edges_from_checked_endpoint_envelope':True,
      'reused_independent_source_primitives':True,
      'exception_method':'reverse DP on exact positive A-cost compositions ending at x; all intervening original zero actions retain costs/endpoints',
      'exception_edges':len(records),'tested_relevant_A_starts':tests,'exception_checks':records,
      'actual_H3_failure_controls':witnesses,'H_ge_4_minimum_margin':env['H_ge_4_minimum_margin'],
      'LOW_quiescent':False,'pending_LOW_B_columns':len(z['pending']),
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','not_a_closed_source_counterexample':True,
      'input_sha256':{p.name:sha(p) for p in [cp,ep,F/'independent_probe11_source_actions.json',F/'probe11_source_actions.pkl']}}
    with (F/'independent_probe11_H3_actual_signs_13.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('exception_checks','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify131_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
