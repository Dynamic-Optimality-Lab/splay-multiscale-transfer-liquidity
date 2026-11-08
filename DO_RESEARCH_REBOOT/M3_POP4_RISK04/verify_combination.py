"""Scope, source-completion and saved-value audit; no old predicates rerun."""
import json
from pathlib import Path
from itertools import combinations_with_replacement
from combined_certificate import CombinedCoveredCertificate,UncoveredSignature
BASE=Path(__file__).resolve().parent

def read(p):return json.loads(p.read_text())
def signatures(total):
    for xs in combinations_with_replacement(range(10),total):yield tuple(xs.count(i) for i in range(10))
def main():
    out=BASE/'combination_check.json';assert not out.exists();P=CombinedCoveredCertificate();cert=read(BASE/'certification_run.json');checked=0
    for batch in cert['source_batches']:
        source=read(Path(batch['report']));folder=Path(batch['report']).parent
        for filename in source['root_files']:
            r=read(folder/filename);s,t=r['source'],r['destination']
            assert P.J(s)==r['source_potential']['value'] and P.J(t)==r['destination_potential']['value']
            if r['kind']=='LOW':assert r['weight']-P.ordinary(t)+P.ordinary(s)==r['residual']
            else:
                m=r['midpoint'];assert [r['weight']-P.midpoint(m)+P.ordinary(s),P.midpoint(m)-P.ordinary(t)]==r['residual']
            checked+=1
    old={(0,)*10}
    for gap in range(10):
        for n in range(1,267):s=[0]*10;s[gap]=n;assert P.scope({'sigma':s})=='single';old.add(tuple(s))
    for total in (2,3):
        for s in signatures(total):P.scope({'sigma':s});old.add(s)
    prior=read(BASE.parent/'M3_POP4_RISK01/combination_check.json')['new_total4_signatures']
    for s in prior:assert P.scope({'sigma':s})=='population4';old.add(tuple(s))
    prior2=read(BASE.parent/'M3_POP4_RISK02/combination_check.json')['new_certified_signatures']
    for s in prior2:assert P.scope({'sigma':s})=='renewed_population4';old.add(tuple(s))
    prior3=read(BASE.parent/'M3_POP4_RISK03/combination_check.json')['new_certified_signatures']
    for s in prior3:assert P.scope({'sigma':s})=='renewal3_population4';old.add(tuple(s))
    assert len(old)==3437
    cases=cert['source_certified_signatures'];new={v for s in cases for v in (tuple(s),tuple(reversed(s)))}
    assert not(old&new)
    for s in new:assert P.scope({'sigma':s})=='renewal4_population4'
    remaining=[];covered=[]
    for s in signatures(4):
        if s in old or s in new:covered.append(s)
        else:
            remaining.append(s)
            try:P.scope({'sigma':s})
            except UncoveredSignature:pass
            else:raise AssertionError('uncertified total4 accepted')
    assert len(remaining)==184-len(new) and len(covered)==531+len(new)
    fixed=sum(s==list(reversed(s)) for s in cases);assert len(new)==2*len(cases)-fixed
    for s in ([4,1]+[0]*8,[1,1,1,1,1]+[0]*5):
        try:P.scope({'sigma':s})
        except UncoveredSignature:pass
        else:raise AssertionError('larger uncertified signature accepted')
    r={'status':'RENEWED_COMBINED_COVERAGE_AUDIT_PASS_FULL_M3_OPEN','new_certified_signatures':sorted(new),'new_signature_count':len(new),
      'source_complete_canonical_tables':len(cases),'self_reflecting_new_sectors':fixed,'new_mask_sectors':126*len(new),'saved_new_root_value_checks':checked,
      'production_predicates_replayed':0,'old_signature_vectors_reused':3437,'combined_signature_vectors':3437+len(new),
      'combined_mask_sectors':126*(3437+len(new)),'total4_vectors_covered':531+len(new),'total4_vectors_remaining':184-len(new),
      'unresolved_total4_signatures':remaining,'all_total3_still_covered':True,'uniform_walk_bound':-7,'closed_walk_bound':0,'full_M3_proved':False}
    with out.open('x') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k not in ('new_certified_signatures','unresolved_total4_signatures')},indent=2),flush=True)
if __name__=='__main__':main()
