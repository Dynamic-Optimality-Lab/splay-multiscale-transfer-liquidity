"""Strengthen creator predicates: a fringe owns the entire anchor prefix/suffix."""
import json,time,sys,itertools
from pathlib import Path
from audit_proof130 import phi,spines
from audit_verify35 import splay,node
B=Path(__file__).resolve().parent
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def atoms(t,P):
    if not node(t):return set() if t=='E' else {('X',int(t[1:]))}
    return atoms(t[1],P)|atoms(t[2],P)|({('K',t[0])} if t[0] not in P else set())
def permitted(t,P):
    total=atoms(t,P);result={}
    def walk(v):
        if not node(v):return
        if v[0] in P:
            k=v[0];L,R=atoms(v[1],P),atoms(v[2],P);below={a for a in total if (a[1]<k if a[0]=='K' else a[1]<=k)};above=total-below
            result[k]=({'L'} if L==below else set())|({'R'} if R==above else set()) if L and R else {'L','R'}
        walk(v[1]);walk(v[2])
    walk(t);return result
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'unary_helper_protected_activation_forms.json').read_text());rows=[];bad=[]
    for row in Z['schemas']:
        t=fr(row['source']);a=fr(row['actual_after']);s=fr(row['projected_old_source']);P={k for k in range(row['m']) if row['private_mask']>>k&1};allowed=permitted(a,P);LS,RS=spines(a);witness=None
        for bits in itertools.product('LR',repeat=len(P)):
            tags=dict(zip(sorted(P),bits))
            if any(tags[k] not in allowed[k] for k in P):continue
            p=phi(a,P,tags,LS,RS)
            if p is None:continue
            for z in range(row['m']):
                if z in P:continue
                old,c1=splay(s,z);old,c2=splay(old,row['terminal'])
                if old==p and c1<=1 and c2<=1:witness={'tags':tags,'old_DELETE_proxy':z,'old_event_costs':[c1,c2],'old_after':p};break
            if witness:break
        r=dict(row);r['saturated_witness']=witness;rows.append(r)
        if witness is None:bad.append(r)
    out('unary_activation_saturated_creator_forms.json',{'status':'UNARY_ACTIVATION_SATURATED_FRINGE_DERIVATION' if not bad else 'SATURATED_CREATOR_REFINEMENT_HAS_EXCEPTIONS','schemas':rows,'exceptions':bad,'free_term_schemas':len(rows),'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'});print(json.dumps({'status':'SATURATED_CREATOR_REFINEMENT','schemas':len(rows),'exceptions':len(bad),'first_exception':bad[0] if bad else None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof133_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
