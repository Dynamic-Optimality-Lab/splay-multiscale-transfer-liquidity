"""Fixed FE02 source certificates; no search, size change or rigidity claim."""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from source_root_budget import return_budget
PG=HERE.parent/'route_c_pf_positive_gap_closure_20261101_v001'
FE=HERE.parent/'route_c_fe01_first_entry_20261101_v001'


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def direct(rows,donor):
    claims=[];usedU=set();usedD=set();residual=None
    def claim(d,u,kind):
        assert tuple(d) not in usedD and tuple(u) not in usedU
        usedD.add(tuple(d));usedU.add(tuple(u));claims.append(dict(demand=d,unit=u,kind=kind))
    for j,row in enumerate(rows):
        units=[[0,j,e,b] for e in range(row['a']) for b in [0,1]]
        demands=[[0,j,e] for e,ev in enumerate(row['B_events']) if ev[0]!='ZIG']
        for d,u in zip(demands,units):claim(d,u,'own')
        if row['delta']>0:
            assert j==0 and row['a']==1 and row['q']==3;residual=demands[2]
        if j==donor:
            assert row['q']<=2*row['a']-1 and residual is not None
            claim(residual,units[-1],'source_short_return_loan')
    assert len(claims)==sum(row['q'] for row in rows)==22
    return dict(donor_block=donor,assignments=claims,complete=True,paid_demands=22,
        physical_capacity=50,unused_units=28,startup_units_used=0,reused_units=0,
        selected_from='original-source return-gap/last-operation bound; not FE reservation')


def main():
    pg=read(PG/'closed_source_certificate.json');fe=read(FE/'FE_witness_certificate.json')
    result={}
    for orientation,rows in [('ordinary',pg['ordinary_rows']),('reflected',pg['reflected_rows'])]:
        budget=return_budget(rows)
        donors=[r for r in budget if rows[r['block']]['delta']<=0 and r['short_gap_donor']]
        donor=donors[0]['block'];assert donor==4
        assert budget[donor]['cyclic_gap']==3 and budget[donor]['eta']==1
        assert budget[donor]['B_double_source_bound']==1
        result[orientation]=dict(return_rows=budget,source_forced_donor=donor,direct_injection=direct(rows,donor),
            source_totals=dict(N=19,s=7,A=25,Q_B=22,E=1,negative_slack=29,
                positive_blocks=[0],sum_gaps=sum(r['cyclic_gap'] for r in budget),sum_eta=sum(r['eta'] for r in budget)),
            inherited_FE_cut0=fe['all_cut_trials'][orientation]['FE'][0])
    signature=dict(source_tree_status='NONE PROVIDED: formal integer signature only, NOT a source witness',
        N=4,s=4,a=[1,1,1,1],q=[3,2,2,2],L=[4,4,4,4],eta=[0,0,0,0])
    assert all(q<=L-1-eta for q,L,eta in zip(signature['q'],signature['L'],signature['eta']))
    assert sum(signature['L'])==signature['s']*signature['N']
    assert sum(signature['q'])-2*sum(signature['a'])==1
    assert 2*(sum(signature['a'])-signature['N'])+1+sum(signature['eta'])<= (signature['s']-3)*signature['N']
    save('root_return_certificate.json',dict(original_PG_sha256=sha(PG/'closed_source_certificate.json'),
        original_FE_sha256=sha(FE/'FE_witness_certificate.json'),source_formula_sha256=sha(HERE/'source_root_budget.py'),
        regression=result,formal_budget_noncontradiction_signature=signature,
        formal_signature_not_a_counterexample=True,actual_saturated_return_found=False,
        FE02_rigidity='OPEN',FE02_CD='OPEN',new_root_gap_subtheorem='PROVED—UNIVERSAL',
        repetitions='m=1 is the FE02 positive control; m>1 only inherited FE01 regression, not a FE02 theorem instance',
        new_key_counts=0,larger_finite_fits=0,source_searches=0,larger_repetitions_replayed=0))
    print(json.dumps(dict(status='FIXED_FE02_CERTIFICATES_WRITTEN',source_donor_block=4,
        source_donor_gap=3,source_donor_eta=1,source_bound=1,actual_A=25,actual_Q=22,
        formal_signature_has_no_source_trees=True,FE02_rigidity='OPEN'),indent=2))


if __name__=='__main__':main()
