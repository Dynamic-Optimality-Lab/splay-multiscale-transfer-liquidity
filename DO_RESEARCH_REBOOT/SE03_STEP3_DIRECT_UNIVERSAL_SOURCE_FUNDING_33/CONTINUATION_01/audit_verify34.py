"""Independent forward source check of the two immutable private-max candidates.
Reads the JSON coefficient export, not the producer pickle. No solver/repair.
Only reuses already checked original primitive identities.
"""
import json,time,sys,hashlib,collections
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    basis=B/'native10_source_actions.json';raw=basis.read_bytes();Z=json.loads(raw);R=json.loads((B/'native10_source_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==R['input_sha256'];del raw
    export=B/'native10_credit_certificate.json';raw=export.read_bytes();E=json.loads(raw);assert E['source_actions_sha256']==hashlib.sha256(basis.read_bytes()).hexdigest();L=dict(E['nonzero_debt']);assert len(L)==1769616 and E['width']==3;del E,raw
    T=list(map(fr,Z['trees']));N=len(T);idx={t:i for i,t in enumerate(T)};dest=Z['destination'];Q=Z['Q'];mir=Z['mirror']
    def debt(a,b):return L.get(min(a*N+b,mir[a]*N+mir[b]),0)
    # B preimages grouped by actual old root and accessed key, independently forward.
    byroot=collections.defaultdict(list)
    for b,t in enumerate(T):
        for x,q in enumerate(Q[b],1):
            if q>=2:byroot[t[0],x].append((b,dest[b][x-1],q))
    # Required target comparison rows are sparse D=3 states with their raw mirrors.
    positive=collections.defaultdict(list)
    d3=collections.defaultdict(set)
    for code,v in L.items():
        a,b=divmod(code,N);positive[a].append((b,v));positive[mir[a]].append((mir[b],v))
        if v==3:d3[a].add(b);d3[mir[a]].add(mir[b])
    quartet=[];internal=[];rows=0;source_motifs=0
    for a,t in enumerate(T):
        g=t[0]
        for x in range(g+1,11):
            v=t;directions=''
            while v[0]!=x:
                k=1 if x<v[0] else 2;directions+='L' if k==1 else 'R';v=v[k]
            if len(directions) not in (2,4) or not directions.startswith('RR'):continue
            h=len(directions)//2;at=dest[a][x-1];xx,left,right=T[at];p,gg,C=left;ggkey,A,BB=gg;assert xx==x and ggkey==g
            pt=idx[(x,(g,A,(p,BB,C)),right)];rows+=1
            targets={bt for bt in d3[at] if debt(pt,bt)==0}
            if not targets:continue
            for b,bt,q in byroot[g,x]:
                if bt not in targets:continue
                required=2*h-q+3
                if not 0<=required<=3:continue
                ds=debt(a,b);assert ds!=required
                quartet.append([a,b,x,h,q,ds,at,bt,pt])
        # Independently classify source depth-three prefixes; avoid producer motif loop.
        for x in range(1,11):
            v=t;path=[]
            while v[0]!=x:path.append(v);v=v[1 if x<v[0] else 2]
            if len(path)!=3 or not (path[0][0]<path[1][0]<path[2][0]):continue
            g,A,pr=path[0];p,BB,ur=pr;u,ul,rr=ur
            if x>u:
                xx,dd,ee=rr;projected=(x,(p,(g,A,BB),(u,ul,dd)),ee);kind='RRR'
            else:
                xx,cc,dd=ul;projected=(x,(p,(g,A,BB),cc),(u,dd,rr));kind='RRL'
            assert xx==x;pt=idx[projected];source_motifs+=1
            for b,ds in positive[a]:
                q=Q[b][x-1];w=4-q
                if w>=ds:continue
                bt=dest[b][x-1];dt=debt(pt,bt);assert w+dt-ds>=0
                internal.append([a,b,x,kind,q,ds,pt,bt,dt])
        if a%512==0 and time.process_time()-START>CAP-2:raise TimeoutError('STATIC_AUDIT_CPU')
    p=json.loads((B/'private_max_pullback_critical_quartet.json').read_text());i=json.loads((B/'internal_max_unary_pullback_source_candidate.json').read_text());assert p['failure'] is None and i['failure'] is None
    assert rows==p['A_RR_even_inverse_rows']==13624 and len(quartet)==p['source_pair_candidates_inspected']==66
    assert source_motifs==i['A_source_motifs']==7280 and len(internal)==i['source_candidates_inspected']==2811
    result={'status':'PASS_COMPLETE_PRIVATE_MAX_COEFFICIENT_OBLIGATIONS','canonical_wrapper_critical_rows':rows,'critical_quartet_candidate_cases':quartet,'depth_two_internal_source_motifs':source_motifs,'internal_positive_source_cases':internal,'source_queries':0,'source_engine_calls':0,'method':'independent forward prefix classification and immutable JSON coefficient export; accepted source primitives reused; no solver or debt repair','not_fresh_source_replays':True,'source_formulas_need_symbolic_assembly':True,'principal_U33':'OPEN','external_or_formal_verification':False,'producer_core19_logging_error':'candidate artifact verified despite final print exception; failed CPU remains charged','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_source_actions.json','native10_credit_certificate.json','private_max_pullback_critical_quartet.json','internal_max_unary_pullback_source_candidate.json')}}
    out('private_max_pullback_independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('critical_quartet_candidate_cases','internal_positive_source_cases','input_sha256')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify34_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
