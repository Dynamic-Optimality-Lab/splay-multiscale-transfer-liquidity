"""Capped symbolic theorem interfaces and new reservation-composition regression."""
import hashlib,itertools,json,sys,time
from collections import Counter
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def N(k,l,r):return (k,l,r)
def pointers(t):
    if isinstance(t,str):return {}
    k,l,r=t
    return {k:(l[0] if not isinstance(l,str) else l,r[0] if not isinstance(r,str) else r),**pointers(l),**pointers(r)}
def main():
    previous=read(C/'CONTINUATION_02/campaign_manifest.json')
    for n,h in previous['artifacts'].items():assert sha(C/'CONTINUATION_02'/n)==h
    deps=[]
    for n in ['SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md',
      'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md',
      'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/FROZEN_OWNER_EXCHANGE.md',
      'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FROZEN_OWNER_COMPATIBILITY.md',
      'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CHART_SIGNED_CORRECTIONS.md',
      'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md',
      'SE03_STEP3_GLOBAL_JOINT_OWNERSHIP_34/EXACT_RESIDUAL_SOURCE_OWNERSHIP.md',
      'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01/DIRTY_OWNER_COURSE_CORRECTION/FROZEN_OWNER_BLOCKING_STRUCTURE.md']:
        p=P/n;deps.append({'path':str(p),'sha256':sha(p),'inspected':True})
    put('dependency_manifest.json',{'inherited':deps,'prior_manifest_sha256':sha(C/'CONTINUATION_02/campaign_manifest.json'),
      'controller_sha256':sha(B/'run_phase_1440.py'),'resource_entry_sha256':sha(C/'CONTINUATION_02/resources_checkpoint.json')})
    # Universal linear identity: q=l+b, DeltaL=l-kappa.
    terms=Counter({'c':2,'l':-1,'b':-1});terms.update({'l':1,'kappa':-1})
    assert {k:v for k,v in terms.items() if v}=={'c':2,'b':-1,'kappa':-1}
    # COMPLETE finite integer case partition from q+2b+d<=6. No trees or accesses.
    bad=set();profiles=[]
    for q in range(1,7):
        for d in range(7):
            for b in range(q+1):
                if q+2*b+d>6:continue
                kappa=min(q,max(2-d,0))
                assert b<=2 and kappa<=2
                if b+kappa>2:bad.add((q,b,d,kappa))
    assert bad=={(2,1,0,2),(2,2,0,2),(3,1,0,2),(4,1,0,2)}
    for q,b,d,kappa in sorted(bad):
        ds=set()
        for row in itertools.product(range(1,7),repeat=q):
            if sum(row)+d<=6 and sum(v>2 for v in row)==b:ds.add(tuple(sorted(row)))
        profiles.append({'q':q,'b':b,'d':d,'kappa':kappa,'degree_multisets':sorted(ds),'holes':b})
    # Generic root-local pointer footprint, including both mixed doubles.
    A,D,E,H='A D E H'.split();g,p,x='g p x'.split()
    frames={
      'LL':(N(g,N(p,N(x,A,D),E),H),N(x,A,N(p,D,N(g,E,H)))),
      'LR':(N(g,N(p,A,N(x,D,E)),H),N(x,N(p,A,D),N(g,E,H))),
      'RL':(N(g,A,N(p,N(x,D,E),H)),N(x,N(g,A,D),N(p,E,H))),
      'RR':(N(g,A,N(p,D,N(x,E,H))),N(x,N(p,N(g,A,D),E),H)),
      'L':(N(g,N(x,A,D),E),N(x,A,N(g,D,E))),
      'R':(N(g,A,N(x,D,E)),N(x,N(g,A,D),E))}
    for name,(before,after) in frames.items():
        a,bp=pointers(before),pointers(after)
        assert set(a)==set(bp)
        changed={v for v in a if a[v]!=bp[v]}
        assert changed<=({g,x} if name in ('L','R') else {g,p,x})
        if name not in ('L','R'):assert x in a[p]
    put('new_symbolic_certificate.json',{'status':'SYMBOLIC_INTERFACES_CHECKED_NOT_UCF35',
      'source_queries':0,'source_engine_calls':0,'DL35_identity':'2c-q+Delta Lk=2c-bk-kappa',
      'r7_exceptions':profiles,'r7_nonexception_source_D_width':4,'r7_nonexception_working_bound':10,
      'OR35_frames':frames,'OR35_anonymous_operand_bound':'r-1','OR35_A_shadow_bound':'3*r-3',
      'OR35_union_explicit_view_labels_bound':'4*r-4; with arbitrary rigid ordered contexts',
      'OR35_not_a_global_credit_theorem':True,'UCF35':'OPEN'})
    # New reservation composition on a SAVED historical construction; no source replay.
    hist=B/'SOURCE_JOINT_REPAIR_03'
    s=read(hist/'actual_monotone_return_source.json');o=read(hist/'actual_auxiliary_owner_extension.json')
    def mapping(rows):return {tuple(z['demand']):tuple(z['unit']) for z in rows}
    h=mapping(s['funding']['full_h']);a=mapping(o['old_canonical_effective_a0'])
    current=mapping(o['full_allocation']);new=mapping(o['new_actual_pairs'])
    reservation=dict(list(new.items())[::2]);aplus={**a,**reservation}
    assert len(aplus)==len(a)+len(reservation) and len(set(aplus.values()))==len(aplus)
    inv={u:d for d,u in aplus.items()};result=dict(aplus);paths=[]
    for root in sorted(set(h)-set(aplus)):
        d=root;seen=set();path=[]
        while True:
            assert d not in seen;seen.add(d);u=h[d];path.append((d,u))
            if u not in inv:break
            d=inv[u]
        result[root]=u;paths.append({'root':root,'steps':path,'terminal':u})
    assert result==current and all(result[d]==u for d,u in a.items())
    assert len(set(result.values()))==len(result)==36
    put('claim_reservation_composition.json',{'status':'PASS_NEW_TYPED_RESERVATION_REGRESSION',
      'scope':'archived32-to36 construction only; actual current36 map remains unchanged',
      'historical_a0_count':len(a),'claim_bound_reservations':[{'demand':d,'unit':u} for d,u in reservation.items()],
      'frozen_augmented_count':len(aplus),'final_count':len(result),'new_paths':paths,
      'equals_existing_current_full36':True,'current_frozen_input_rolled_back':False,
      'source_queries':0,'source_engine_calls':0,
      'input_sha256':{str(p.relative_to(P)):sha(p) for p in [hist/'actual_monotone_return_source.json',hist/'actual_auxiliary_owner_extension.json']}})
    print('DL35_OR35_AND_CLAIM_RESERVATION_INTERFACES; SOURCE_CREDIT_STILL_OPEN',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof177_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
