"""Formal arbitrary-multiplicity upper-private LOW source classification.
No actual source query, no finite population tested: free-term normal forms.
"""
import json,time,sys,itertools,math
from pathlib import Path
from audit_verify35 import formal_path,at,splay,project,node
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def keys(t):return [] if not node(t) else keys(t[1])+[t[0]]+keys(t[2])
def pi(t,private):
    if not node(t):return t
    return pi(t[1],private) if t[0] in private else (t[0],pi(t[1],private),pi(t[2],private))
def main():
    rows=[];failures=[]
    for d in range(1,5):
        for directions in itertools.product('LR',repeat=d):
            word=''.join(directions);t,x=formal_path(word);pathkeys=[at(t,[1 if v=='L' else 2 for v in word[:j]])[0] for j in range(d+1)]
            for mask in range(1,1<<(d-1)):
                private={pathkeys[j+1] for j in range(d-1) if mask>>j&1};marked=set(pathkeys)-private
                if min(private)<max(marked):continue
                assert all(word[j]=='L' for j,k in enumerate(pathkeys[:-1]) if k in private)
                old=pi(t,private);actual,h=splay(t,x);native,h0=splay(old,x);p=pi(actual,private);kind=None
                if p==native:kind='COMMUTING'
                elif len(marked)==3 and h==h0+1:
                    xx,left,right=native
                    if node(left) and node(left[1]):
                        pp,gg,C=left;g,A,BB=gg
                        if p==(xx,(g,A,(pp,BB,C)),right):kind='RR_EXTRA_EVENT_CRITICAL_QUARTET'
                elif len(marked)==4 and h==h0==2:
                    g,A,pr=old;pp,BB,ur=pr;u,ul,rr=ur
                    if x>u:
                        xx,dd,ee=rr;expected=(xx,(pp,(g,A,BB),(u,ul,dd)),ee);kind='INTERNAL_RRR'
                    else:
                        xx,cc,dd=ul;expected=(xx,(pp,(g,A,BB),cc),(u,dd,rr));kind='INTERNAL_RRL'
                    if p!=expected:kind=None
                row={'actual_path':word,'private_path_positions':[j for j,k in enumerate(pathkeys) if k in private],'private_path_keys':sorted(private),'source_term':t,'actual_target':actual,'old_source':old,'native_target':native,'projected_actual_target':p,'actual_H':h,'old_H':h0,'class':kind}
                rows.append(row)
                if kind is None:failures.append(row)
    assert not failures
    out('upper_private_low_source_normal_forms.json',{'status':'COMPLETE_FORMAL_LOW_DIRECT_CLASSIFICATION','direct_schemas':rows,'class_counts':{k:sum(r['class']==k for r in rows) for k in sorted({r['class'] for r in rows})},'source_queries':0,'source_engine_calls':0,'population_scope':'arbitrary number; only the at-most-three private path vertices in any H<=2 access are exposed, all other source subtrees remain free terms','principal_U33':'OPEN'})
    print(json.dumps({'status':'COMPLETE_FORMAL_LOW_DIRECT_CLASSIFICATION','schemas':len(rows),'class_counts':{k:sum(r['class']==k for r in rows) for k in sorted({r['class'] for r in rows})}}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof81_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
