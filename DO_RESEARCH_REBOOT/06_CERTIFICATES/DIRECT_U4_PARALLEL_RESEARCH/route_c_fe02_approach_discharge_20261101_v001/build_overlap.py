"""Two fixed overlapping setups; all fringe targets classified symbolically."""
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('same_discharge_source',HERE/'build_discharge.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
N,execute,inflate,save=base.N,base.execute,base.inflate,base.save


def gap_depths(t,depth=0):
    if isinstance(t,str):return {t:depth}
    if t is None:return {}
    return {**gap_depths(t[1],depth+1),**gap_depths(t[2],depth+1)}


def main():
    original=base.read(HERE/'source_discharge_certificate.json')
    connector=base.read(HERE/'fixed_connector_certificate.json')['connector']
    assert connector is not None
    B0,C=original['B0'],original['C'];out={}
    for u,synchronizing_key in [(4,4),(2,2)]:
        startup=execute(B0,B0,[('DELETE',x) for x in [8,7,u,1,13]])
        A0=startup[-1]['destination_A']
        span=execute(A0,B0,[('KEEP',8),('KEEP',7)])
        assert [(r['a'],r['q']) for r in span]==[(1,2),(1,3)]
        A,B=span[-1]['destination_A'],span[-1]['destination_B'];assert B==C and A!=B
        table=[]
        for key in range(1,14):
            if key==7:continue
            row=execute(A,B,[('KEEP',key)])[0]
            table.append(dict(key=key,d_A=row['d_A'],d_B=row['d_B'],a=row['a'],q=row['q'],
                delta=row['delta'],synchronizes=row['destination_A']==row['destination_B']))
        if u==4:
            assert all(r['delta']<0 for r in table)
            # Right rotation of A's left child4 over its child1.
            g=A[1];p=g[1]
            rotated=N(A[0],N(p[0],p[1],N(g[0],p[2],g[2])),A[2])
            assert rotated==B
        else:
            assert [r['key'] for r in table if r['delta']>=0]==[2]
            assert next(r for r in table if r['key']==2)['delta']==0
        one=execute(A,B,[('KEEP',synchronizing_key)])[0]
        assert one['destination_A']==one['destination_B']
        D=one['destination_A']
        da,db=gap_depths(inflate(A)),gap_depths(inflate(B));fringes=[]
        for gap in sorted(da,key=lambda s:int(s[1:])):
            pars=[]
            for parity in [0,1]:
                a_const=(da[gap]+parity+1)//2;q_const=(db[gap]+parity)//2
                delta_const=q_const-2*a_const;assert delta_const<=-1
                pars.append(dict(parity=parity,A_StepEv_constant=a_const,A_StepEv_v_coefficient=1,
                    B_double_constant=q_const,B_double_v_coefficient=1,
                    delta_constant=delta_const,delta_v_coefficient=-1))
            fringes.append(dict(gap=gap,A_root_depth=da[gap],B_root_depth=db[gap],internal_depth='2v+parity',
                                v='any nonnegative integer',parity_cases=pars))
        symbolic_start=execute(inflate(B0),inflate(B0),[('DELETE',x) for x in [8,7,u,1,13]])
        assert symbolic_start[-1]['destination_A']==inflate(A0)
        symbolic_span=execute(inflate(A0),inflate(B0),[('KEEP',8),('KEEP',7),('KEEP',synchronizing_key)])
        assert symbolic_span[-1]['destination_A']==symbolic_span[-1]['destination_B']==inflate(D)
        tail=execute(D,D,[('KEEP',x) for x in connector]);success=tail[-1]['destination_A']==B0
        out[str(u)]=dict(extra_DELETE=u,A0=A0,B0=B0,startup_rows=startup,exposure_rows=span,
            postpositive_A=A,postpositive_B=B,core_successors=table,fringe_successors=fringes,
            synchronizing_key=synchronizing_key,synchronizing_successor=one,synchronized_state=D,
            symbolic_startup_rows=symbolic_start,symbolic_span_rows=symbolic_span,
            same_connector=connector,same_connector_rows=tail,same_connector_success=success)
    save('overlap_discharge_certificate.json',dict(scope_sha256=base.sha(HERE/'AD00B_OVERLAP_SCOPE_GATE.md'),
        base_source_sha256=base.sha(HERE/'source_discharge_certificate.json'),cases=out,
        fixed_overlaps=[4,2],larger_finite_fits=0,no_other_overlaps_tested=True,FE02_CD='OPEN'))
    print(json.dumps(dict(status='OVERLAP_SOURCE_LAWS_VERIFIED',cases={u:dict(
        nonnegative_successors=[r['key'] for r in v['core_successors'] if r['delta']>=0],
        all_arbitrary_gap_targets_negative=True,same_connector_success=v['same_connector_success']) for u,v in out.items()}),indent=2))


if __name__=='__main__':main()
