"""Exact old/new scope and saved-witness audit; no production root replays."""
import json
from pathlib import Path
from itertools import combinations,combinations_with_replacement
from combined_certificate import CombinedCoveredCertificate,UncoveredSignature
BASE=Path(__file__).resolve().parent

def sigs(total):
    for xs in combinations_with_replacement(range(10),total):yield tuple(xs.count(g) for g in range(10))
def main():
    out=BASE/'combination_check.json';assert not out.exists();P=CombinedCoveredCertificate();source=json.loads((BASE/'source_audit.json').read_text());checked=0
    for filename in source['root_files']:
        r=json.loads((BASE/filename).read_text());s,t=r['source'],r['destination']
        assert P.J(s)==r['source_potential']['value'] and P.J(t)==r['destination_potential']['value']
        if r['kind']=='LOW':assert r['weight']-P.ordinary(t)+P.ordinary(s)==r['residual']
        else:
            m=r['midpoint'];assert [r['weight']-P.midpoint(m)+P.ordinary(s),P.midpoint(m)-P.ordinary(t)]==r['residual']
        checked+=1
    old={(0,)*10}
    for gap in range(10):
        for n in range(1,267):s=[0]*10;s[gap]=n;assert P.scope({'sigma':s})=='single';old.add(tuple(s))
    for total in (2,3):
        for s in sigs(total):P.scope({'sigma':s});old.add(s)
    assert len(old)==2916
    run=json.loads((BASE/'run_result.json').read_text());new={v for s in run['completed_signatures'] for v in (tuple(s),tuple(reversed(s)))}
    for s in new:assert P.scope({'sigma':s})=='population4'
    unresolved=[];covered4=[]
    for s in sigs(4):
        if s in old or s in new:covered4.append(s)
        else:
            unresolved.append(s)
            try:P.scope({'sigma':s})
            except UncoveredSignature:pass
            else:raise AssertionError('uncertified total4 accepted')
    fixed=sum(s==list(reversed(s)) for s in run['completed_signatures'])
    assert len(new)==2*len(run['completed_signatures'])-fixed
    assert len(covered4)==10+len(new) and len(unresolved)==705-len(new) and not(old&new)
    for s in ([4,1]+[0]*8,[0,0,1,1,1,1,1,0,0,0]):
        try:P.scope({'sigma':s})
        except UncoveredSignature:pass
        else:raise AssertionError('larger uncertified support accepted')
    result={'status':'COMBINED_COVERED_DOMAIN_AUDIT_PASS_FULL_M3_OPEN','saved_new_root_value_checks':checked,'production_predicates_replayed':0,
      'new_total4_signatures':sorted(new),'new_signature_count':len(new),'new_mask_sectors':126*len(new),'self_reflecting_new_sectors':fixed,
      'total4_vectors_covered':len(covered4),'total4_vectors_remaining':len(unresolved),'unresolved_total4_signatures':unresolved,
      'prior_signature_vectors_reused':2916,'all_total3_still_covered':True,'combined_signature_vectors':2916+len(new),
      'combined_mask_sectors':126*(2916+len(new)),'legal_masks':126,'uniform_walk_bound':-7,'closed_walk_bound':0,'full_M3_proved':False}
    with out.open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('new_total4_signatures','unresolved_total4_signatures')},indent=2),flush=True)
if __name__=='__main__':main()
