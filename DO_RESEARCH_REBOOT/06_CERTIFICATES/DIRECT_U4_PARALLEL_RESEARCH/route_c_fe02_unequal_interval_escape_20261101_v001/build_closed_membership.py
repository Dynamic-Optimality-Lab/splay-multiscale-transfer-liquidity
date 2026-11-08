"""One declared composition, original13-core source, no connector search."""
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('corrected_interval_producer',HERE/'build_interval_certificates_v002.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)


def add_gaps(t):
    gap=0
    def go(u):
        nonlocal gap
        if u is None:
            i=gap;gap+=1
            return 'L' if i==0 else 'F' if i==4 else None
        return b.N(u[0],go(u[1]),go(u[2]))
    v=go(t);assert gap==14;return v


def main():
    five=b.read(HERE/'odd_boundary_obstruction_certificate.json')
    old=b.read(b.BASE/'route_c_pf_positive_gap_closure_20261101_v001/closed_source_certificate.json')
    fiveword=[tuple(z) for z in five['source_word']]
    startup=[(r['mode'],r['key']) for r in old['startup_rows']]
    period=[(r['mode'],r['key']) for r in old['ordinary_rows']]
    assert period==[('KEEP',x) for x in [7,5,3,1,5,6,4,1,2,1,5,1,6,7,1,2,1,3,1]]
    word=fiveword+startup+period+[('KEEP',x) for x in range(2,14)]+[('KEEP',x) for x in range(12,0,-1)]
    V=old['startup_rows'][0]['source_B'];rows=b.execute(V,V,word)
    assert rows[-1]['destination_A']==rows[-1]['destination_B']==V
    positives=[i for i,r in enumerate(rows) if r['delta']>0]
    p=len(fiveword)+len(startup)
    assert positives==[p] and (rows[p]['a'],rows[p]['q'])==(1,3)
    assert all(rows[j]['key']!=rows[(j+1)%len(rows)]['key'] for j in range(len(rows)))
    S=add_gaps(V);symbolic=b.execute(S,S,word)
    assert symbolic[-1]['destination_A']==symbolic[-1]['destination_B']==S
    bad=symbolic[4]
    before=b.count_expr(bad['source_A'],bad['source_B']);after=b.count_expr(bad['destination_A'],bad['destination_B'])
    assert before==dict(constant=1,opaque_size_coefficients={'L':1})
    assert after==dict(constant=9,opaque_size_coefficients={})
    scan_at=len(fiveword)+len(startup)+len(period)
    assert all(r['q']==0 for r in rows[scan_at:])
    donor=next((p+j)%len(rows) for j in range(1,len(rows)) if rows[(p+j)%len(rows)]['delta']<0)
    assignments=[]
    for j,r in enumerate(rows):
        ds=[e for e,z in enumerate(r['B_events']) if z[0]!='ZIG']
        units=[[j,e,bit] for e in range(r['a']) for bit in (0,1)]
        for d,u in zip(ds[:2*r['a']],units):assignments.append(dict(B_double=[j,d],A_unit=u,kind='own'))
    assignments.append(dict(B_double=[p,2],A_unit=[donor,rows[donor]['a']-1,1],kind='later-source-negative-block'))
    assert len({tuple(v['A_unit']) for v in assignments})==len(assignments)
    assert len({tuple(v['B_double']) for v in assignments})==sum(r['q'] for r in rows)==len(assignments)
    result=dict(scope_sha256=b.sha(HERE/'UI00A_CLOSED_FE02_MEMBERSHIP_SCOPE.md'),
        source_word=word,rows=rows,symbolic_rows=symbolic,
        positive_block=p,positive_type=[1,3],saturated_obstruction_block=4,
        before_common_core=before,after_common_core=after,delta_common_core='8-|L|',
        L_order='all keys below1',F_order='all keys strictly between4 and5',
        no_internal_fringe_key_accessed=True,full_pair_closed=True,
        A=sum(r['a'] for r in rows),Q=sum(r['q'] for r in rows),
        positive_blocks=positives,block_count=len(rows),
        direct_injection=dict(assignments=assignments,positive_block=p,donor_block=donor,
            donor_unit=[donor,rows[donor]['a']-1,1],startup_credit_used=0,future_period_credit_used=0),
        scan_B_double_demand=0,all_same_source_key_count=13,
        mathematical_claim='unbounded saturated common-core loss inside actual FE02 closed source histories',
        not_a_single_positive_saturated_return=True,FE02_CD='OPEN',Coarse_Double_counterexample=False)
    b.save('closed_FE02_boundary_certificate.json',result)
    print({k:result[k] for k in ['block_count','A','Q','positive_block','delta_common_core','FE02_CD']})


if __name__=='__main__':main()
