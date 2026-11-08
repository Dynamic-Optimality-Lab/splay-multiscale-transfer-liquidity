"""Actual-ID natural/frozen quotient; accepted source ledgers reused by hash.
No source engine, source enumeration, or universal eligibility assumption.
"""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'FINAL_C33'
START=time.process_time();CAP=float(sys.argv[1])
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def node(kind,v):return kind,tuple(v)

def compress(D,U,a,h0):
    inv={u:d for d,u in a.items()};R=D-set(h0);S=U-set(h0.values())
    P=D-set(a);T=U-set(a.values());succ={node('d',d):node('u',u) for d,u in h0.items()}
    succ.update({node('u',u):node('d',d) for d,u in a.items()})
    vertices={node('d',d) for d in D}|{node('u',u) for u in U}
    starts=sorted({node('d',p) for p in P}|{node('u',s) for s in S})
    components=[];used=set();ends=set();root_holes={};root_free={};rho={}
    for st in starts:
        v=st;path=[]
        while True:
            assert v not in used;used.add(v);path.append(v)
            if v not in succ:break
            v=succ[v]
        assert v not in ends;ends.add(v)
        if st[0]=='d':
            (root_holes if v[0]=='d' else root_free)[st[1]]=v[1]
        else:rho[st[1]]=v
        components.append({'start':st,'end':v,'path':path})
    cycles=[]
    while vertices-used:
        st=min(vertices-used);v=st;path=[]
        while v not in used:
            used.add(v);path.append(v);assert v in succ;v=succ[v]
        assert v==st;cycles.append(path)
    assert ends=={node('d',r) for r in R}|{node('u',t) for t in T}
    holes=set(root_holes.values());k={v[1]:s for s,v in rho.items() if v[0]=='d'}
    assert set(k)==R-holes and len(set(k.values()))==len(k)
    assert {v for v in rho.values()}==({node('d',r) for r in R-holes}|{node('u',t) for t in T-set(root_free.values())})
    assert len(S)-len(R)==len(U)-len(D)==len(T)-len(P)
    return R,S,P,T,root_holes,root_free,rho,k,components,cycles

def covering(R,L,k):
    J={r:set(L.get(r,set()))|({k[r]} if r in k else set()) for r in R}
    M=dict(k);inv={s:r for r,s in M.items()}
    def aug(r,seen):
        for s in sorted(J[r]):
            if s in seen:continue
            seen.add(s);old=inv.get(s)
            if old is None or aug(old,seen):
                M[r]=s;inv[s]=r;return True
        return False
    for r in sorted(R-set(k)):
        assert aug(r,set())
    assert set(M)==R and len(set(M.values()))==len(M)
    return M

def stage(name,D,U,a,h0,h,expected):
    R,S,P,T,alpha,own,rho,k,components,cycles=compress(D,U,a,h0)
    # This ONE relation is the accepted, simultaneously licensed full h's
    # actual seed choices. It is NOT a union over competing source rules.
    L={r:{h[r]} for r in R};assert all(L[r]<=S for r in R)
    M=covering(R,L,k);ik={s:r for r,s in k.items()};b={};added=dict(own);qpaths=[]
    ialpha={r:p for p,r in alpha.items()};seen=set()
    for root in sorted(set(alpha.values())):
        r=root;path=[]
        while True:
            assert r not in seen;seen.add(r);s=M[r];assert s in L[r]
            b[r]=s;path.append({'hole':r,'seed':s,'rho':rho[s]})
            if s not in ik:
                assert rho[s][0]=='u' and rho[s][1] in T
                added[ialpha[root]]=rho[s][1];break
            r=ik[s]
        qpaths.append({'root':ialpha[root],'quotient_path':path,'terminal':added[ialpha[root]]})
    assert set(added)==P and len(set(added.values()))==len(added) and set(added.values())<=T
    assert {**a,**added}==expected
    return {'name':name,'current_live_gap':False,'scope':'CURRENT_COMPLETE_POLICY' if name=='current32' else 'ARCHIVED30_ALGORITHM_CONTROL_NOT_REOPENED',
      'counts':{'D':len(D),'U':len(U),'R':len(R),'S':len(S),'P':len(P),'T':len(T),'B':len(alpha),'virtual_paid_holes':len(k),'raw_balance':len(U)-len(D)},
      'components':components,'cycles':cycles,'alpha':[{'root':p,'hole':r} for p,r in sorted(alpha.items())],
      'natural_successes':[{'root':p,'terminal':u} for p,u in sorted(own.items())],
      'rho':[{'seed':s,'end':v} for s,v in sorted(rho.items())],
      'virtual_k':[{'hole':r,'seed':s} for r,s in sorted(k.items())],
      'licensed_L':[{'hole':r,'seed':h[r]} for r in sorted(R)],
      'covering_virtual_matching':[{'hole':r,'seed':s} for r,s in sorted(M.items())],
      'quotient_repair_paths':qpaths,'new_actual_pairs':[{'demand':p,'unit':u} for p,u in sorted(added.items())],
      'all_old_actual_values_preserved':True}

def main():
    source=B/'one_helper_original_source_and_owners.json'
    receipt=B/'one_helper_original_source_independent_audit.json';audit=json.loads(receipt.read_text())
    assert audit['status']=='PASS_ORIGINAL_R7_CORE9_ONE_HELPER_SOURCE_OWNER_AND_BANK'
    assert pin(source)==audit['input_sha256'][source.name]
    z=json.loads(source.read_text());h0=mp(z['h0']);h=mp(z['h']);old=mp(z['old_effective_a']);full=mp(z['full_f']);D=set(full)
    U={(r['occurrence'],j,b) for r in z['rows'] for j in range(1,r['a']+1) for b in (0,1)}
    assert set(h)==D and len(set(h.values()))==len(h) and all(h[d]==u for d,u in h0.items())
    assert len(old)==30 and len(full)==32
    for a in (old,full):assert set(a)<=D and len(set(a.values()))==len(a) and set(a.values())<=U
    stages=[stage('historical30',D,U,old,h0,h,full),stage('current32',D,U,full,h0,h,full)]
    result={'status':'PRODUCER_ACTUAL_SOURCE_OWNER_QUOTIENT','stages':stages,
      'no_splay_or_old_source_audit_repeated':True,'source_queries':0,'source_engine_calls':0,
      'new_mathematical_scope':'uniform component/conditional static-fiber theorems, not universal source feasibility',
      'universal_source_factorization_and_expansion':'OPEN','principal_C33':'OPEN',
      'input_sha256':{str(source):pin(source),str(receipt):pin(receipt)}}
    out('actual_owner_quotient_certificate.json',result)
    assert time.process_time()-START<CAP-1
    print(json.dumps({'status':result['status'],'counts':[s['counts'] for s in stages],'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof164_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
