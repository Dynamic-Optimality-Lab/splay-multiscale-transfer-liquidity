"""Independent component-set and reverse-walk audit; no producer import.
Checks a symbolic relay countermodel and affine identities separately from
the actual accepted source ledgers. Not a universal source proof checker.
"""
import hashlib,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'FINAL_C33';START=time.process_time();CAP=float(sys.argv[1])
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mp(v):return {tuple(r['demand']):tuple(r['unit']) for r in v}
def nd(n):return n[0],tuple(n[1])
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))

def audit_stage(claim,D,U,a,h0,full):
    R=D-set(h0);S=U-set(h0.values());P=D-set(a);T=U-set(a.values())
    verts={('d',d) for d in D}|{('u',u) for u in U};adj={v:set() for v in verts};edges=set()
    for d,u in h0.items():edges.add((('d',d),('u',u)))
    for d,u in a.items():edges.add((('u',u),('d',d)))
    for x,y in edges:adj[x].add(y);adj[y].add(x)
    starts={('d',p) for p in P}|{('u',s) for s in S}
    stops={('d',r) for r in R}|{('u',t) for t in T}
    unseen=set(verts);components=[]
    while unseen:
        component=set();stack=[next(iter(unseen))]
        while stack:
            v=stack.pop()
            if v in component:continue
            component.add(v);stack.extend(adj[v]-component)
        unseen-=component;components.append(component)
    produced={frozenset(nd(n) for n in x['path']):x for x in claim['components']}
    cycles={frozenset(nd(n) for n in z) for z in claim['cycles']}
    assert set(produced)|cycles=={frozenset(c) for c in components} and not set(produced)&cycles
    rho={};alpha={};direct={}
    for component in components:
        aa=component&starts;bb=component&stops
        if not aa:
            assert not bb and frozenset(component) in cycles;continue
        assert len(aa)==len(bb)==1
        st=next(iter(aa));en=next(iter(bb));pr=produced[frozenset(component)]
        assert nd(pr['start'])==st and nd(pr['end'])==en
        pp=[nd(n) for n in pr['path']];assert len(pp)==len(component) and pp[0]==st and pp[-1]==en
        assert all((x,y) in edges for x,y in zip(pp,pp[1:]))
        if st[0]=='u':rho[st[1]]=en
        elif en[0]=='d':alpha[st[1]]=en[1]
        else:direct[st[1]]=en[1]
    k={r[1]:s for s,r in rho.items() if r[0]=='d'}
    assert set(k)==R-set(alpha.values())
    assert rho=={tuple(x['seed']):nd(x['end']) for x in claim['rho']}
    assert alpha=={tuple(x['root']):tuple(x['hole']) for x in claim['alpha']}
    assert k=={tuple(x['hole']):tuple(x['seed']) for x in claim['virtual_k']}
    M={tuple(x['hole']):tuple(x['seed']) for x in claim['covering_virtual_matching']}
    L={tuple(x['hole']):tuple(x['seed']) for x in claim['licensed_L']}
    assert set(M)==R and len(set(M.values()))==len(M)
    assert all(M[r]==L[r] or M[r]==k.get(r) for r in R)
    extra={}
    for q in claim['quotient_repair_paths']:
        for step in q['quotient_path']:
            r=tuple(step['hole']);s=tuple(step['seed']);assert L[r]==s
            assert r not in extra;extra[r]=s
    comparison={**h0,**extra};assert len(set(comparison.values()))==len(comparison)
    ih={u:d for d,u in comparison.items()};claimed_new=mp(claim['new_actual_pairs']);reverse_seen=set()
    for root,terminal in claimed_new.items():
        assert terminal in T;u=terminal
        while True:
            assert u in ih and ('u',u) not in reverse_seen;reverse_seen.add(('u',u));d=ih[u]
            assert ('d',d) not in reverse_seen;reverse_seen.add(('d',d))
            if d not in a:
                assert d==root;break
            u=a[d]
    assert set(claimed_new)==P and {**a,**claimed_new}==full
    assert len(set(claimed_new.values()))==len(claimed_new)
    assert len(T)-len(P)==len(S)-len(R)==len(U)-len(D)
    return {'name':claim['name'],'components':len(components),'R':len(R),'B':len(alpha),'k':len(k),'P':len(P),'all_actual_values_preserved':True}

def model_check():
    # Pure symbolic injective-map model, deliberately no Pair Access claim.
    L={'r1':{'s3'},'r2':{'s3'},'r3':{'s1','s2'}};rho={'s3':'r3','s1':'u1','s2':'u2'};k={'r3':'s3'}
    endpoints={}
    for root in ('r1','r2'):
        stack=[root];seen=set();ends=set()
        while stack:
            r=stack.pop()
            if r in seen:continue
            seen.add(r)
            for s in L[r]:
                if rho[s].startswith('u'):ends.add(rho[s])
                else:stack.append(rho[s])
        endpoints[root]=ends;assert ends=={'u1','u2'}
    for rootset in ({'r1'},{'r2'},{'r1','r2'}):
        assert len(set().union(*(endpoints[r] for r in rootset)))>=len(rootset)
    X={'r1','r2'};NJ=set().union(*(L[r]|({k[r]} if r in k else set()) for r in X))
    assert NJ=={'s3'} and len(NJ)==len(X)-1
    return {'status':'ENDPOINT_HALL_SHORTCUT_REFUTED_IN_SYMBOLIC_MODEL','source_reachability_claim':False,'X':sorted(X),'N_J_X':sorted(NJ),'individually_reachable_endpoints':{r:sorted(v) for r,v in endpoints.items()}}

def main():
    source=B/'one_helper_original_source_and_owners.json';oldreceipt=B/'one_helper_original_source_independent_audit.json'
    ar=json.loads(oldreceipt.read_text());assert pin(source)==ar['input_sha256'][source.name]
    assert ar['status']=='PASS_ORIGINAL_R7_CORE9_ONE_HELPER_SOURCE_OWNER_AND_BANK'
    cert=F/'actual_owner_quotient_certificate.json';z=json.loads(cert.read_text())
    for pp,sha in z['input_sha256'].items():assert pin(Path(pp))==sha
    v=json.loads(source.read_text());h0=mp(v['h0']);full=mp(v['full_f']);D=set(full)
    U={(r['occurrence'],j,b) for r in v['rows'] for j in range(1,r['a']+1) for b in (0,1)}
    inputs={'historical30':mp(v['old_effective_a']),'current32':full}
    stats=[audit_stage(c,D,U,inputs[c['name']],h0,full) for c in z['stages']]
    assert stats[1]['P']==0 and len(full)==32
    # Exact affine identities on arbitrary component counts (p,a,b,c,n).
    P=(1,1,0,0,0);T=(1,0,0,1,0);R=(0,1,1,0,0);S=(0,0,1,1,0);n=(0,0,0,0,1)
    assert sub(T,P)==sub(S,R)==sub(add(S,n),add(R,n))
    # Bank slack: K=23-x, extra=2-y, slack=x+y, x,y>=0.
    K=(23,-1,0);extra=(2,0,-1)
    assert sub((25,0,0),add(K,extra))==(0,1,1)
    # Net Hall margin: (paid+extra)-(paid+roots)=extra-roots.
    assert sub((1,0,1),(1,1,0))==(0,-1,1)
    model=model_check();out('symbolic_shared_relay_countermodel.json',model)
    docs=('GENUINE_EXCESS_FRONTIER_DEFINITION.md','JOINT_FRONTIER_FEASIBILITY_MODEL.md','MINIMAL_JOINT_OBSTRUCTION.md','BANK25_SCHEDULE_PROOF.md','SOURCE_FORCED_JOINT_REPAIR_THEOREM.md')
    result={'status':'PASS_ACTUAL_OWNER_QUOTIENT_REVERSE_AUDIT_AND_SYMBOLIC_KERNELS','actual_ledger_stages':stats,
      'affine_component_and_bank_identities':'PASS_ALL_PARAMETER_COEFFICIENTS','symbolic_model':model['status'],
      'audit_scope':'independent component sets/reverse expansion on accepted actual ledgers; exact symbolic identities and countermodel; written uniform matching proof is not formalized',
      'universal_source_eligibility_or_expansion_proved':False,'universal_hard_bank_trace_proved':False,
      'same_agent_distinct_implementation':True,'external_peer_review_or_formal_verification':False,
      'source_queries':0,'source_engine_calls':0,'principal_C33':'OPEN',
      'input_sha256':{str(cert):pin(cert),str(source):pin(source),str(oldreceipt):pin(oldreceipt),**{d:pin(F/d) for d in docs}}}
    out('quotient_independent_audit.json',result);assert time.process_time()-START<CAP-1
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify77_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
