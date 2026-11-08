"""Partial combination and exact scope audit; no production predicates rerun."""
import json
from pathlib import Path
from itertools import combinations_with_replacement,combinations
from combined_certificate_partial import CombinedCoveredCertificate,UncoveredSignature
BASE=Path(__file__).resolve().parent

def main():
    out=BASE/'combination_check_partial.json';assert not out.exists();P=CombinedCoveredCertificate()
    source=json.loads((BASE/'source_audit_partial.json').read_text());checked=0
    for filename in source['root_files']:
        r=json.loads((BASE/filename).read_text());s,t=r['source'],r['destination']
        assert P.J(s)==r['source_potential']['value'] and P.J(t)==r['destination_potential']['value']
        if r['kind']=='LOW':assert r['weight']-P.ordinary(t)+P.ordinary(s)==r['residual']
        else:
            m=r['midpoint'];assert [r['weight']-P.midpoint(m)+P.ordinary(s),P.midpoint(m)-P.ordinary(t)]==r['residual']
        checked+=1
    covered={(0,)*10}
    for g in range(10):
        for n in range(1,267):sig=[0]*10;sig[g]=n;assert P.scope({'sigma':sig})=='single';covered.add(tuple(sig))
    for g,h in combinations(range(10),2):
        sig=[int(i in (g,h)) for i in range(10)];assert P.scope({'sigma':sig})=='unit_pair';covered.add(tuple(sig))
    old=json.loads((BASE.parent/'M3_POP3_01/certificate.json').read_text())['covered_signatures']
    for sig in old:assert P.scope({'sigma':sig})=='population3';covered.add(tuple(sig))
    run=json.loads((BASE/'run_result.json').read_text());new=set()
    for sig in run['completed_signatures']:new.update((tuple(sig),tuple(reversed(sig))))
    for sig in new:assert P.scope({'sigma':sig})=='new_population3';covered.add(sig)
    unresolved=[];covered3=[]
    for xs in combinations_with_replacement(range(10),3):
        sig=[xs.count(i) for i in range(10)]
        if tuple(sig) in covered:covered3.append(sig)
        else:
            unresolved.append(sig)
            try:P.scope({'sigma':sig})
            except UncoveredSignature:pass
            else:raise AssertionError('open signature promoted')
    assert len(covered)==2722 and len(unresolved)==194 and len(covered3)==26 and len(new)==2
    masks=[sum(1<<i for i in c) for c in combinations(range(9),5)];assert len(masks)==126
    for sig in ([3,1]+[0]*8,[2,2]+[0]*8):
        try:P.scope({'sigma':sig})
        except UncoveredSignature:pass
        else:raise AssertionError('larger open population promoted')
    obj={'status':'PARTIAL_COMBINED_DOMAIN_AUDIT_PASS_FULL_CAMPAIGN_STOPPED','new_saved_root_value_checks':checked,
      'production_predicates_replayed':0,'new_certified_signatures':sorted(new),'new_signature_count':2,'new_mask_sectors':252,
      'combined_signature_vectors':len(covered),'combined_mask_sectors':len(covered)*126,'total3_covered':26,'total3_remaining':194,
      'unresolved_total3_signatures':unresolved,'all_legal_masks':126,'uniform_walk_bound':-7,'closed_walk_bound':0,
      'larger_multi_support_population_still_open':True,'full_M3_proved':False}
    with out.open('x') as f:json.dump(obj,f,indent=2)
    print(json.dumps({k:v for k,v in obj.items() if k!='unresolved_total3_signatures'},indent=2),flush=True)
if __name__=='__main__':main()
