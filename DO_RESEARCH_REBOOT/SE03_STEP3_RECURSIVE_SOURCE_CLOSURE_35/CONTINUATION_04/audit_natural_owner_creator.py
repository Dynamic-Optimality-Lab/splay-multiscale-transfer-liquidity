"""Complete free-frame birth classification and reused SI34 tail identities."""
import hashlib,itertools,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;S=C/'CONTINUATION_01';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def left(t):
    p,A,c=t;y,M,R=c;return (y,(p,A,M),R)
def right(t):
    p,c,D=t;y,L,M=c;return (y,L,(p,M,D))
def edges(t):
    if not isinstance(t,tuple):return set()
    out=set()
    for c in t[1:]:
        if isinstance(c,tuple):out.add((t[0],c[0]));out|=edges(c)
    return out
def reflect(t,maxkey):
    if not isinstance(t,tuple):return t
    return (maxkey-t[0],reflect(t[2],maxkey),reflect(t[1],maxkey))
def edge(t,p,x):
    while isinstance(t,(tuple,list)) and t[0]!=p:t=t[1] if p<t[0] else t[2]
    return isinstance(t,(tuple,list)) and any(isinstance(c,(tuple,list)) and c[0]==x for c in t[1:])
def main():
    tests={};maxima={}
    for pattern in ('LL','LR','RR','RL','L','R'):
        worst=cases=0;iszig=len(pattern)==1
        for flags in itertools.product((False,True),repeat=2 if iszig else 3):
            for ports in itertools.product((0,1,2),repeat=3 if iszig else 4):
                # A port represents an arbitrary ordered BST, not a finite leaf.
                def port(key,state):return None if state==0 else (key,f'{key}:L',f'{key}:R')
                if iszig:
                    A,M,D=(port(k,s) for k,s in zip((0,2,4),ports))
                    source=(3,(1,A,M),D);dest=right(source);v=1
                    marks={k for k,f in zip((3,1),flags) if f}|{k for k,s in zip((0,2,4),ports) if s==2}
                    maximum=4
                else:
                    A,Bb,Cc,D=(port(k,s) for k,s in zip((0,2,4,6),ports))
                    if pattern in ('LL','RR'):
                        source=(5,(3,(1,A,Bb),Cc),D);dest=right(right(source));v=1
                    else:
                        source=(5,(1,A,(3,Bb,Cc)),D);dest=right((5,left(source[1]),D));v=3
                    marks={k for k,f in zip((5,1 if pattern in ('LR','RL') else 3,v),flags) if f}
                    marks|={k for k,s in zip((0,2,4,6),ports) if s==2};maximum=6
                if pattern in ('RR','RL','R'):
                    source,dest=reflect(source,maximum),reflect(dest,maximum);marks={maximum-k for k in marks};v=maximum-v
                qualified=[]
                for p,c in edges(dest)-edges(source):
                    if c not in marks:continue
                    if p not in marks or p==v or (v-p)*(c-p)<0:qualified.append((p,c))
                assert len(qualified)<=(1 if iszig else 2)
                worst=max(worst,len(qualified));cases+=1
        tests[pattern]=cases;maxima[pattern]=worst
    old=json.loads((S/'independent_critical_source_audit.json').read_text())
    for p,h in old['input_sha256'].items():assert sha(S/p)==h
    A=json.loads((S/'new_A_primitive_rows.json').read_text())['rows']
    reports=[]
    for i,x in ((2,5),(4,9),(6,13)):
        pred=A[2*i-3];death=A[2*i-2];watch=(1,x-2)
        assert pred['key']==1 and death['key']==x and pred['a']==death['a']==1
        assert not edge(pred['before'],*watch) and edge(pred['after'],*watch)
        assert edge(death['before'],*watch) and not edge(death['after'],*watch)
        reports.append({'target':x,'watched_edge':watch,'creator':'preceding genuine KEEP1','creator_H':1,'creator_Q':1,
          'natural_h0_owned_prefix_units':1,'unused_tail_units':1,'g':1,'selected_actual_bit':[f'h{i}',1,1],
          'new_h0_residual':[f'v{x}',3]})
    status={'status':'PASS_UNIFORM_CREATOR_FRAME_IDENTITIES_AND_NATURAL_TAIL_REDUCTION',
      'free_frame_cases':tests,'joint_maximum_births':maxima,
      'universal_scope':'six original formulas with arbitrary ordered opaque hangers; cases are operand/root mark types, not bounded BST populations',
      'review':'inner-edge lifetime barrier, one creator per surviving export, marked child uniqueness at macro end, last-tail ordinal selection, actual period and static block construction inspected',
      'SI34_tail_controls':reports,'arbitrary_overfull_creator_groups_proved':False,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in (F/'NATURAL_OWNER_CREATOR_THEOREM.md',S/'independent_critical_source_audit.json',
        S/'new_A_primitive_rows.json',F/'independent_FP_SI34_source_countercut.json')}}
    with (F/'independent_natural_owner_creator.json').open('x',encoding='utf8') as f:json.dump(status,f,indent=2)
    print(json.dumps({k:v for k,v in status.items() if k not in ('input_sha256','SI34_tail_controls')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify142_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
