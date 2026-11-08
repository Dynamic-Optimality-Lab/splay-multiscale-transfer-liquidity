"""Exact closed provenance and one-period distinct physical injections."""
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('closed_base',HERE/'build_discharge.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)


def mirror(t):
    return None if t is None else b.N(14-t[0],mirror(t[2]),mirror(t[1]))


def inject(rows):
    positive=[i for i,r in enumerate(rows) if r['delta']>0]
    assert len(positive)==1
    p=positive[0];assert (rows[p]['a'],rows[p]['q'])==(1,3)
    assert all(rows[i]['key']!=rows[(i+1)%len(rows)]['key'] for i in range(len(rows)))
    order=[(p+j)%len(rows) for j in range(len(rows))]
    donor=next(i for i in order[1:] if rows[i]['delta']<=-1)
    def units(i):return [[i,e,bit] for e in range(rows[i]['a']) for bit in (0,1)]
    assignments=[]
    for i,r in enumerate(rows):
        doubles=[e for e,v in enumerate(r['B_events']) if v[0]!='ZIG']
        own=min(r['q'],2*r['a'])
        for u,e in zip(units(i)[:own],doubles[:own]):
            assignments.append(dict(A_unit=u,B_double=[i,e],kind='own'))
    demand=[p,[e for e,v in enumerate(rows[p]['B_events']) if v[0]!='ZIG'][2]]
    last=units(donor)[-1]
    assert rows[donor]['q']<=2*rows[donor]['a']-1
    assignments.append(dict(A_unit=last,B_double=demand,kind='source-certified-later-donor'))
    aa=[tuple(v['A_unit']) for v in assignments];bb=[tuple(v['B_double']) for v in assignments]
    assert len(set(aa))==len(aa) and len(set(bb))==len(bb)==sum(r['q'] for r in rows)
    assert set(bb)=={(i,e) for i,r in enumerate(rows) for e,v in enumerate(r['B_events']) if v[0]!='ZIG'}
    rotated=b.execute(rows[p]['source_A'],rows[p]['source_B'],[(rows[i]['mode'],rows[i]['key']) for i in order])
    assert rotated[-1]['destination_A']==rows[p]['source_A'] and rotated[-1]['destination_B']==rows[p]['source_B']
    return dict(positive_block=p,cut_order=order,donor_block=donor,donor_unit=last,
        pending_demand=demand,assignments=assignments,paid_doubles=len(bb),used_units=len(aa),
        available_units=2*sum(r['a'] for r in rows),startup_credit_used=0,
        future_period_credit_used=0,reservations_selected_from_future_demand=False,
        FI_PF_FE_acceptance_claimed=False,positive_cut_source_closed=True,
        identity_convention='original cyclic block/occurrence, actual source event index, capacity bit0/1')


def main():
    source=b.read(HERE/'source_discharge_certificate.json')
    overlaps=b.read(HERE/'overlap_discharge_certificate.json')['cases']
    connector=b.read(HERE/'fixed_connector_certificate.json')['connector']
    connector2=b.read(HERE/'overlap_connector_certificate.json')['connector']
    cases={}
    for name,extra,sync,tail in [('base',None,None,connector),('overlap4',4,4,connector),('overlap2',2,2,connector2)]:
        ds=[8,7]+([] if extra is None else [extra])+[1,13]
        word=[('DELETE',x) for x in ds]+[('KEEP',8),('KEEP',7)]
        if sync is not None:word.append(('KEEP',sync))
        word.extend(('KEEP',x) for x in tail)
        B0=source['B0'];rows=b.execute(B0,B0,word)
        assert rows[-1]['destination_A']==rows[-1]['destination_B']==B0
        injection=inject(rows)
        symbolic=b.execute(b.inflate(B0),b.inflate(B0),word)
        assert symbolic[-1]['destination_A']==symbolic[-1]['destination_B']==b.inflate(B0)
        reflected=b.execute(mirror(B0),mirror(B0),[(m,14-x) for m,x in word])
        assert reflected[-1]['destination_A']==reflected[-1]['destination_B']==mirror(B0)
        assert [(r['a'],r['q']) for r in rows]==[(r['a'],r['q']) for r in reflected]
        cases[name]=dict(word=word,rows=rows,symbolic_rows=symbolic,reflected_rows=reflected,
            full_pair_closed=True,cyclic_blocks_equal_occurrences=True,
            positive_blocks=[i for i,r in enumerate(rows) if r['delta']>0],
            A=sum(r['a'] for r in rows),Q=sum(r['q'] for r in rows),
            Q_minus_2A=sum(r['delta'] for r in rows),direct_injection=injection)
    b.save('closed_discharge_certificate.json',dict(cases=cases,
        source_discharge_sha256=b.sha(HERE/'source_discharge_certificate.json'),
        overlap_discharge_sha256=b.sha(HERE/'overlap_discharge_certificate.json'),
        fixed_connector_sha256=b.sha(HERE/'fixed_connector_certificate.json'),
        overlap_connector_sha256=b.sha(HERE/'overlap_connector_certificate.json'),
        all_fourteen_common_ordered_gap_variables=True,larger_finite_fits=0,
        no_strict_FI_PF_FE_coverage_claim=True,FE02_CD='OPEN',
        supersedes_only_historical_closed_embedding_status_in_first_phase=True))
    print({k:dict(blocks=len(v['rows']),A=v['A'],Q=v['Q'],donor=v['direct_injection']['donor_block']) for k,v in cases.items()})


if __name__=='__main__':main()
