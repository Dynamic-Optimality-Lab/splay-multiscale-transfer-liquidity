"""Durable exact chronology of credits, including original cyclic restoration."""
import sys
import json
import gzip
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def load(name):
    p=HERE/name
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8')) as f:return json.load(f)


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    cases=[]
    for row in load('COMPLETE_SOURCE_AUDIT.json')['cases']:
        bank=load(row['global_credit']);m=row['carrier_support'];q=row['q']
        def phase(op):return 'preparation' if op<m else 'descending' if op<2*m else 'forward_restoration' if op<3*m else 'reverse_restoration'
        critical=[]
        for operation in (m,m+1,m+3,m+7):
            chosen=[a for a in bank['credit_assignments'] if a['B'][1]==operation]
            credits=Counter(phase(a['A_credit'][1]) for a in chosen)
            critical.append({'B_operation':operation,'paid_doubles':len(chosen),'original_A_credit_phases':dict(credits),
                'cyclic_from_later_original_operation':sum(a['A_credit'][1]>operation for a in chosen),
                'distinct_original_A_units':len({tuple(a['A_credit'][:-1]) for a in chosen}),
                'max_slots_from_one_A_unit':max(Counter(tuple(a['A_credit'][:-1]) for a in chosen).values(),default=0)})
        assert critical[0]['paid_doubles']==8*(q+1)
        assert critical[0]['cyclic_from_later_original_operation']==8*(q+1)
        assert all(r['max_slots_from_one_A_unit']<=4 for r in critical)
        cases.append({'q':q,'physical_support':row['physical_support'],'carrier_support':m,
            'global_reserve_capacity':bank['capacity'],'total_issued_equals_total_paid':bank['issued'],
            'critical':critical})
    result={'cases':cases,'scope':'Exact source chronology. The closed seam permits earlier-lap real A credit; no reaching-prefix credit or virtual A bit.',
        'observation':'In the greatest cyclic C=4 reserve, the first B maximum burst is paid by actual A issuance from the preceding lap. The FIFO provenance is mostly forward restoration; the q=9 source also uses one descending-phase credit. Reverse restoration may preserve an already full balance and need not issue new credit. Rigid-gap growth does not change this cost-word credit law.',
        'not_proved':'A uniform mean-cost or reserve invariant on arbitrary original paired sources.','universal_CD':'OPEN'}
    p=HERE/'CREDIT_CHRONOLOGY.json';assert not p.exists();p.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'cases':len(cases),'first_burst_funded_by_previous_lap_real_A':True,'universal_CD':'OPEN'}))


if __name__=='__main__':main()
