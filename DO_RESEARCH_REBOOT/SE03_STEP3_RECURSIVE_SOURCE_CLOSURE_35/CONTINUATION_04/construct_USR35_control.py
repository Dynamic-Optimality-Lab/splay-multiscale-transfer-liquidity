"""m=4 control of a separately written uniform proof; cached source substitutions only."""
import hashlib,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
sys.path.insert(0,str(F));import ranked_source_bst as R
CAP=float(sys.argv[1]);START=time.process_time()
def N(k,l=None,r=None):return (k,l,r)
def vine(a,b,right=True):
    t=None
    for x in (range(b,a-1,-1) if right else range(a,b+1)):t=N(x,None,t) if right else N(x,t,None)
    return t
def path(t,x):
    p=[]
    while True:
        p.append(t[0])
        if t[0]==x:return p
        t=t[1] if x<t[0] else t[2]
def inv(a):return [] if not a else [a[0]]+[z for x in inv(a[1:]) for z in (x,a[0])]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'probe11_source_actions.pkl').open('rb') as f:lift=R.Lift(pickle.load(f))
    m=4;size=6*m+3;y=2*m+1;u=y+1;g=2*m-1;marks=set(range(1,size+1,2))
    b0=N(g,vine(1,g-1,False),N(u,N(y-1,None,N(y)),vine(y+2,size)))
    initial,h,q=lift.action(b0,size,g-2);assert (h,q)==(1,1)
    word=[z for i in range(m,0,-1) for z in (2*i-1,6*m+7-4*i)]+[y]+list(range(1,2*m,2))
    expect=[1,3]+[z for _ in range(m-1) for z in (2,3)]+[m+1,1]+[2]*(m-1)
    current=initial;rows=[];forward=[]
    def action(x,role):
        nonlocal current
        before=current;p=path(before,x);assert len(p)%2==1 and len(p)>1
        for j in range(len(p)-3,-1,-2):
            G,P=p[j:j+2];assert G in marks and P not in marks and (x<G)==(x<P)
        current,h,q=lift.action(before,size,x);assert h==q==(len(p)-1)//2
        assert set().union(*(set(path(current,z)) for z in marks))==set(range(1,size+1))
        row={'target':x,'before':before,'after':current,'Q':q,'ancestors':p[:-1:2],'role':role};rows.append(row);return row
    for x,q in zip(word,expect):
        row=action(x,'forward');assert row['Q']==q;forward.append(row)
    for r in reversed(forward):
        assert current==r['after']
        for x in inv(r['ancestors']):action(x,'inverse')
        assert current==r['before']
    M=16*m-4+2**(m+1);Q=26*m-10+2**(m+2)
    assert current==initial and len(rows)==M and sum(r['Q'] for r in rows)==Q
    assert {r['target'] for r in rows}==marks
    critical=[]
    starts=[initial]
    for i in range(m,0,-1):
        G=2*i-1;X=6*m+7-4*i
        a=N(G,vine(1,G-1),N(G+1,None,N(X,vine(G+2,X-1),vine(X+1,size))))
        after,h,_=lift.action(a,size,X);assert h==1
        want=N(X,N(G+1,N(G,vine(1,G-1),None),vine(G+2,X-1)),vine(X+1,size))
        assert after==want
        d=len(path(starts[-1],G))-1;assert d==(2 if i==m else 2*i+1)
        tail=2*((d+1)//2)-(1 if i==m else 2);assert tail==(1 if i==m else 2*i)
        critical.append({'G':G,'X':X,'A_before':a,'A_after':after,'prep_start':starts[-1],'prep_depth':d,'tail_lower':tail})
        starts.append(after)
    a=N(y,N(y-1,vine(1,y-2,False),None),vine(y+1,size));contact=a;controls=[]
    for kind,x in [('DELETE',y-1)]+[('KEEP',z) for z in range(1,2*m,2)]:
        before=a;a,h,_=lift.action(a,size,x);controls.append({'kind':kind,'target':x,'before':before,'after':a,'H':h})
    paths=[F/'UNBOUNDED_SHARED_RETURN_SOURCE_FAMILY.md',F/'construct_USR35_control.py',F/'probe11_source_actions.pkl',F/'independent_probe11_source_actions.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md']
    out={'status':'PRODUCER_USR35_M4_CONTROL','m':m,'size':size,'y':y,'initial':initial,'B_rows':rows,'forward_count':len(word),'M':M,'Q':Q,'critical':critical,'A_contact':contact,'controls':controls,'source_queries':0,'source_engine_calls':0,'cached_leaf_substitutions':lift.substitutions,'JR35':'OPEN','input_sha256':{str(p):sha(p) for p in paths}}
    with (F/'USR35_m4_control.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('initial','B_rows','critical','A_contact','controls','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof292_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
