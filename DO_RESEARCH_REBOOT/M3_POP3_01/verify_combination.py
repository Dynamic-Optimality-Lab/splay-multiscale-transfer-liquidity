"""New dispatch/coverage check on saved evidence; no production root replay."""
import json
from pathlib import Path
from itertools import combinations
from combined_certificate import CombinedCoveredCertificate,UncoveredSignature
BASE=Path('DO_RESEARCH_REBOOT/M3_POP3_01')
def main():
    out=BASE/'combination_check.json';assert not out.exists();P=CombinedCoveredCertificate();s=json.loads((BASE/'source_audit.json').read_text());checked=0
    for file in s['root_files']:
        r=json.loads((BASE/file).read_text());a,b=r['source'],r['destination'];assert P.J(a)==r['source_potential']['value'] and P.J(b)==r['destination_potential']['value']
        if r['kind']=='LOW':assert r['weight']-P.ordinary(b)+P.ordinary(a)==r['residual']
        else:
            m=r['midpoint'];assert [r['weight']-P.midpoint(m)+P.ordinary(a),P.midpoint(m)-P.ordinary(b)]==r['residual']
        checked+=1
    leading=[(2,1,0),(1,1,1),(1,2,0),(2,0,1),(1,0,2),(0,2,1),(0,1,2)];covered=set()
    covered.add((0,)*10)
    for gap in range(10):
        for n in range(1,267):sig=[0]*10;sig[gap]=n;assert P.scope({'sigma':sig})=='single';covered.add(tuple(sig))
    for g,h in combinations(range(10),2):
        sig=[int(i in (g,h)) for i in range(10)];assert P.scope({'sigma':sig})=='unit_pair';covered.add(tuple(sig))
    for sig in leading:
        full=list(sig)+[0]*7
        for case in (full,list(reversed(full))):assert P.scope({'sigma':case})=='population3';covered.add(tuple(case))
    assert len(covered)==2720
    unresolved3=[]
    # Exact stars-and-bars enumeration of every total-three signature.
    for a in range(10):
        for b in range(a,10):
            for c in range(b,10):
                sig=[0]*10
                for i in (a,b,c):sig[i]+=1
                if tuple(sig) not in covered:
                    unresolved3.append(sig)
                    try:P.scope({'sigma':sig})
                    except UncoveredSignature:pass
                    else:raise AssertionError('uncovered total3 accepted')
    assert len(unresolved3)==196
    for sig in ([3,1]+[0]*8,[0,0,0,1,1,1]+[0]*4):
        try:P.scope({'sigma':sig})
        except UncoveredSignature:pass
        else:raise AssertionError('uncovered hard-deficit signature accepted')
    result={'status':'COMBINED_COVERED_DOMAIN_PASS_FULL_M3_INCOMPLETE','new_saved_root_value_checks':checked,'production_predicates_replayed':0,
      'covered_signature_vectors':len(covered),'covered_mask_signature_sectors':len(covered)*126,'new_population3_vectors':14,
      'new_population3_mask_sectors':1764,'total3_signatures_remaining':196,'uncovered_total3_signatures':unresolved3,
      'larger_total_multi_support_still_open':True,'uniform_walk_bound':-7,'closed_walk_bound':0,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='uncovered_total3_signatures'},indent=2),flush=True)
if __name__=='__main__':main()
