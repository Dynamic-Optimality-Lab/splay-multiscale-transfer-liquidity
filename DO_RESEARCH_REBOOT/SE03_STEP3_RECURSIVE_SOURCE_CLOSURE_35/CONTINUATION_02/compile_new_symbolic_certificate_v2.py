"""Charged free-term identities and source-schema assembly; zero source queries."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent
B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def put(n,v):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def N(x,l,r):return (x,l,r)
def left(t):
    x,l,(y,m,r)=t
    return N(y,N(x,l,m),r)
def right(t):
    y,(x,l,m),r=t
    return N(x,l,N(y,m,r))
def leaves(t):
    return [t] if isinstance(t,str) else leaves(t[1])+[t[0]]+leaves(t[2])
def main():
    a,p,x,y='a p x y'.split();z,L,E,O,R='z L E O R'.split()
    s=N(a,z,N(p,L,N(x,E,R)))
    rr=left(left(s));want=N(x,N(p,N(a,z,L),E),R)
    assert rr==want and leaves(rr)==leaves(s)
    ll=right(right(rr));assert ll==s
    d=N(a,z,N(p,L,N(x,E,N(y,O,R))))
    # The bottom RR is entirely in a.right, then the root zig.
    rr3=left(N(a,z,left(left(d[2]))))
    want3=N(y,N(a,z,N(x,N(p,L,E),O)),R)
    assert rr3==want3 and leaves(rr3)==leaves(d)
    back=right(rr3)
    assert back==N(a,z,N(y,N(x,N(p,L,E),O),R))
    # Endpoint cluster inventories, not splay/access dispatches.
    src=json.loads((F.parent/'CONTINUATION_01/SI34_source_countercertificate.json').read_text())
    def clusters(t):
        if t is None:return set(),frozenset()
        c1,k1=clusters(t[1]);c2,k2=clusters(t[2]);k=k1|k2|{t[0]}
        return c1|c2|{frozenset(k)},frozenset(k)
    old,_=clusters(src['source']['desired_A_before_forward'])
    new,_=clusters(src['source']['initial_A'])
    missing=sorted([sorted(k) for k in new-old])
    assert len(missing)==8
    cert={'status':'FREE_TERM_IDENTITIES_AND_REUSED_SOURCE_ENDPOINTS_CHECKED',
          'source_queries':0,'source_engine_calls':0,
          'free_frames':{'even_consumer_RR':{'before':s,'after':rr},
                         'following_anchor_LL':{'before':rr,'after':ll},
                         'odd_consumer_RR_then_zig':{'before':d,'after':rr3},
                         'following_anchor_zig':{'before':rr3,'after':back}},
          'SI34_missing_reset_clusters':missing,'SI34_reset_H_lower_bound':4,
          'arbitrary_r_schema':{'r_min':4,'n':'2*r-1','m':'2*r-3',
            'missing_reset_clusters':'r','reset_H_lower_bound':'ceil(r/2)',
            'full_Q':'8*r-18','full_KEEP_count':'4*r-8',
            'source_family_only':True,'complete_h':True,'bank_bound':2,
            'global_frozen_input_compatibility':'CONDITIONAL; not supplied for arbitrary r'},
          'universal_UCF35':'OPEN','SI34':'REFUTED',
          'input_sha256':{str(p.relative_to(F.parents[2])):sha(p) for p in (
              F/'RESET_CLUSTER_LOWER_BOUND.md',F/'DESCENDING_SWEEP_RETURN.md',
              F/'ANCHORED_FAMILY_COMPLETE_FUNDING.md',
              F.parent/'CONTINUATION_01/SI34_source_countercertificate.json')}}
    put('new_symbolic_source_certificate.json',cert)
    print('AF35_FREE_FRAME_AND_ENDPOINT_CERTIFICATE; UNIVERSAL_ROOT_OPEN',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof175_exit.json').open('x',encoding='utf-8') as f:
            json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
