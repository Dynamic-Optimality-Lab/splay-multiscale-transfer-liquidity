"""Reproduce the one fixed failed membership proposal; no alternative word."""
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('fixed_membership_proposal',HERE/'build_closed_membership.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m);b=m.b


def main():
    five=b.read(HERE/'odd_boundary_obstruction_certificate.json')
    old=b.read(b.BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    startup=[(r['mode'],r['key']) for r in old['startup_rows']]
    fw=[tuple(v) for v in five['source_word']]
    w=[(r['mode'],r['key']) for r in old['ordinary_rows']]
    V=old['startup_rows'][0]['source_B']
    word=fw+startup+w+[('KEEP',x) for x in range(2,14)]+[('KEEP',x) for x in range(12,0,-1)]
    rows=b.execute(V,V,word)
    ps=[(i,r['key'],r['a'],r['q']) for i,r in enumerate(rows) if r['delta']>0]
    assert ps==[(16,7,1,3),(29,7,1,3)]
    assert rows[-1]['destination_A']==rows[-1]['destination_B']==V
    result=dict(status='FIXED_COMPOSITION_TARGET_FAILED',scope_sha256=b.sha(HERE/'UI00A_CLOSED_FE02_MEMBERSHIP_SCOPE.md'),
        rows=rows,source_word=word,expected_positive_index=len(fw)+len(startup),actual_positive_rows=ps,
        full_pair_closed=True,no_alternative_connector_searched=True,FE02_membership_claimed=False)
    b.save('fixed_composition_failure_certificate.json',result)
    print('FAILED MEMBERSHIP RETAINED: two positives, exact closure, no alternative word searched')


if __name__=='__main__':main()
