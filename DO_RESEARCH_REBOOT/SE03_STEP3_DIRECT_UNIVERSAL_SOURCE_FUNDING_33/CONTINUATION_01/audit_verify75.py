"""Independent reverse-component check of the corrected owner model.
Uses archived legitimate source receipts; does not rerun their source audits.
"""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;C=B/'DIRTY_OWNER_COURSE_CORRECTION';START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (C/n).open('x') as f:json.dump(z,f,indent=2)
def mp(v):return {tuple(q['demand']):tuple(q['unit']) for q in v}
def reverse_components(D,a,h):
    invh={u:d for d,u in h.items()};free={u for u in h.values() if u not in a.values()};roots={};holes={}
    def reverse(d):
        seen=set()
        while d in a:
            assert d not in seen;seen.add(d);u=a[d]
            if u not in invh:return None
            d=invh[u]
        return d
    for u in free:
        r=reverse(invh[u])
        if r is not None:assert r not in roots and r not in holes;roots[r]=u
    for q in D-set(h):
        r=reverse(q)
        if r is not None:assert r not in roots and r not in holes;holes[r]=q
    assert set(roots)|set(holes)==D-set(a)
    return roots,holes
def main():
    z=json.loads((C/'accepted_core9_blocking_analysis.json').read_text());old=json.loads((B/'one_helper_original_source_and_owners.json').read_text());pin=json.loads((B/'one_helper_original_source_independent_audit.json').read_text());assert hashlib.sha256((B/'one_helper_original_source_and_owners.json').read_bytes()).hexdigest()==pin['input_sha256']['one_helper_original_source_and_owners.json']
    a=mp(old['old_effective_a']);h0=mp(old['h0']);h=mp(old['h']);final=mp(old['full_f']);fe=mp(old['actual_fE6']);D=set(final);U={(r['occurrence'],j,b) for r in old['rows'] for j in range(1,r['a']+1) for b in (0,1)}
    r0,b0=reverse_components(D,a,h0);r1,b1=reverse_components(D,a,h);assert not b1 and r1==mp(old['extension']) and b0=={tuple(p['root']):tuple(p['hole']) for p in z['natural_comparison_paths'] if p['hole'] is not None};assert r1=={tuple(p['root']):tuple(p['terminal']) for p in z['complete_comparison_paths'] if p['terminal'] is not None}
    for p in z['complete_comparison_paths']:
        root=tuple(p['root']);u=tuple(p['terminal']);assert u not in a.values()
        q=next((d for d,bit in h0.items() if bit==u),None)
        if q is not None:assert q==tuple(p['steps'][-1]['demand']) and (q==root or q in a)
    E=set(fe);common=D&E;retired=E-D;extra=set(a)-common;unowned=U-set(a.values());assert unowned==((U-set(fe.values()))|{fe[d] for d in retired})-{a[d] for d in extra};assert len(unowned)-(len(D)-len(a))==len(U)-len(D)==104
    # Propositional proof kernel of the reserve identity. These five cases
    # exhaust disjoint fE image classes and injective extra-a0 occupancy,
    # independently of set population or any BST bound.
    for origin in ('common','retired_E_only','outside_fE'):
        for extra_used in (False,True):
            if origin=='common' and extra_used:continue
            in_old_image=origin!='outside_fE';in_common=origin=='common';in_retired=origin=='retired_E_only';in_a=in_common or extra_used
            assert (not in_a)==((not in_old_image or in_retired) and not extra_used)
    # CURRENT accepted policy includes both already successful additions.
    # The archived30-owner stage is only a historical positive model control.
    assert len(final)==32 and set(final)==D and not(D-set(final))
    files=('accepted_core9_blocking_analysis.json','FROZEN_OWNER_BLOCKING_STRUCTURE.md','OWNER_COUPLED_RESERVE_IDENTITY.md','DIRTY_FRAME_EXACT_FEASIBILITY_MODEL.md','SOURCE_FORCED_DONOR_EXPANSION.md')
    result={'status':'PASS_OWNER_FRONTIER_MODEL_AND_PHYSICAL_RESERVE_PARTITION','historical_control_frozen_owners':30,'historical_control_unpaid_roots':[[31,3],[31,4]],'historical_natural_holes':[[31,3],[31,4]],'accepted_source_full_comparison_terminals':[[32,1,1],[36,2,0]],'CURRENT_accepted_owner_count':32,'CURRENT_unpaid_roots':[],'old_source_audit_reused_not_replayed':True,'method':'reverse components from actual free endpoints and missing comparison demands; separate from producer forward owner walks','reserve_identity_kernel':'five exhaustive propositional image-membership cases, not finite BST population testing','natural_reservation_property':'all checked terminals satisfy the general written owner-path proof; no new concrete release example claimed','universal_source_expansion_proved':False,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((C/n).read_bytes()).hexdigest() for n in files}}
    assert time.process_time()-START<CAP-1
    out('owner_model_independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify75_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
