"""New blocking/reservation analysis of an accepted legitimate owner control.
No old source replay or old coefficient audit is repeated.
"""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;C=B/'DIRTY_OWNER_COURSE_CORRECTION';START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (C/n).open('x') as f:json.dump(z,f,indent=2)
def mp(v):return {tuple(r['demand']):tuple(r['unit']) for r in v}
def walk(D,a,h,h0):
    inv={u:d for d,u in a.items()};reserved={u:d for d,u in h0.items()};paths=[];seen=set()
    for root in sorted(D-set(a)):
        d=root;steps=[]
        while d in h:
            assert d not in seen;seen.add(d);u=h[d];owner=inv.get(u);steps.append({'demand':d,'unit':u,'frozen_owner':owner,'natural_reservation':reserved.get(u)})
            if owner is None:paths.append({'root':root,'steps':steps,'terminal':u,'hole':None});break
            d=owner
        else:paths.append({'root':root,'steps':steps,'terminal':None,'hole':d})
    return paths
def main():
    file='one_helper_original_source_and_owners.json';pin=json.loads((B/'one_helper_original_source_independent_audit.json').read_text());assert pin['status']=='PASS_ORIGINAL_R7_CORE9_ONE_HELPER_SOURCE_OWNER_AND_BANK' and hashlib.sha256((B/file).read_bytes()).hexdigest()==pin['input_sha256'][file]
    z=json.loads((B/file).read_text());a=mp(z['old_effective_a']);h0=mp(z['h0']);h=mp(z['h']);f=mp(z['full_f']);fe=mp(z['actual_fE6']);D=set(f);E=set(fe);U={(r['occurrence'],j,b) for r in z['rows'] for j in range(1,r['a']+1) for b in (0,1)};common=D&E;N=E-D;F=D-E;X=set(a)-common;P=D-set(a);assert len(a)==30 and len(P)==2 and all(a[d]==fe[d] for d in common)
    raw=U-set(fe.values());retired={fe[d] for d in N};extra={a[d] for d in X};free=U-set(a.values());assert not raw&retired and free==(raw|retired)-extra and P==F-X and len(free)-len(P)==len(U)-len(D)
    natural=walk(D,a,h0,h0);complete=walk(D,a,h,h0);expected=mp(z['extension']);actual={tuple(p['root']):tuple(p['terminal']) for p in complete if p['terminal'] is not None};assert actual==expected
    reservation_releases=[]
    for p in complete:
        assert p['terminal'] is not None and p['hole'] is None and p['terminal'] in free
        q={u:d for d,u in h0.items()}.get(p['terminal'])
        if q is not None:
            assert p['steps'][-1]['demand']==q and (q==p['root'] or q in a)
            reservation_releases.append({'new_root':p['root'],'terminal':p['terminal'],'natural_reserved_demand':q,'already_frozen_owner_unit':a.get(q),'old_owner_not_moved':True})
    assert all(p['hole'] is None or p['hole'] in D-set(h0) for p in natural)
    out('accepted_core9_blocking_analysis.json',{'status':'PRODUCER_NEW_OWNER_FRONTIER_AND_RESERVE_ANALYSIS','source':file,'period':z['period'],'legitimate_parent_input':'archived actual certified six-key fE, normalized natural effective a; old source/owner audit reused by hash','frozen_owner_count':30,'unpaid_root_count':2,'natural_excess_slots':sorted(D-set(h0)),'natural_comparison_paths':natural,'complete_comparison_paths':complete,'actual_new_assignments':[{'demand':d,'unit':u} for d,u in sorted(actual.items())],'natural_reservation_release_examples':reservation_releases,'exact_inventory_partition':{'original_units':len(U),'full_demands':len(D),'auxiliary_demands':len(E),'common':len(common),'full_only':len(F),'auxiliary_only_retired':len(N),'additional_frozen_successes':len(X),'raw_auxiliary_unused':len(raw),'retired_units':len(retired),'actual_unowned_after_frozen_successes':len(free),'unpaid':len(P),'raw_balance':len(free)-len(P)},'no_old_source_or_owner_audit_repeated':True,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','input_sha256':{file:hashlib.sha256((B/file).read_bytes()).hexdigest(),'one_helper_original_source_independent_audit.json':hashlib.sha256((B/'one_helper_original_source_independent_audit.json').read_bytes()).hexdigest(),'OWNER_COUPLED_RESERVE_IDENTITY.md':hashlib.sha256((C/'OWNER_COUPLED_RESERVE_IDENTITY.md').read_bytes()).hexdigest()}})
    assert time.process_time()-START<CAP-1
    print(json.dumps({'status':'ACCEPTED_CORE9_NEW_BLOCKING_ANALYSIS','P':sorted(P),'natural_holes':[p['hole'] for p in natural],'new_endpoints':sorted(actual.values()),'reservation_release_examples':reservation_releases,'source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof163_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
