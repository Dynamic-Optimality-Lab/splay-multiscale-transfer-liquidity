"""One declared factorization from the frozen A-closed OR source episode."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('same_boundary_lift',HERE/'build_boundary_lift.py')
b=importlib.util.module_from_spec(s);s.loader.exec_module(b)


def main():
    p=b.BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json'
    d=b.read(p);rs=[d['rows'][i] for i in d['episode_indices']]
    assert rs[0]['source_A']==rs[-1]['destination_A']
    assert [r['A_events'][0][0] for r in rs]==['ZIG','ZIG','LL']
    source=rs[-1]['source_A'];x=rs[-1]['key']
    assert source[0]==11 and source[1][0]==7 and source[1][1][0]==1
    local,_=b.splay(source[1],x)
    result,step=b.lift(source,local,x,1)
    assert result==rs[-1]['destination_A']==rs[0]['source_A']
    assert step['base_lift']!=result and step['comparison_correction']
    out=dict(status='INDEPENDENT_CORRECTION_CANCELLATION_REFUTED_EXACT',
        gate_sha256=b.sha(HERE/'BL00A_COMPOSITION_GATE_REVIEW.md'),
        old_source_certificate_sha256=b.sha(p),source_episode_word=[7,11,1],
        source_episode_indices=d['episode_indices'],complete_A_returns=True,
        comparison_corrections_in_A_episode=[dict(block=9,source_event=0,case='LL',
            old_external_key=11,old_child_key=7,comparison_rotation='right at11 promoting7')],
        number_of_A_comparison_corrections=1,opposite_A_comparison_corrections=0,
        source_before_final_A=source,local_splay=local,base_lift=step['base_lift'],
        corrected_result=result,original_A_source=rs[0]['source_A'],
        base_part_alone_is_not_closed=True,correction_restores_actual_A_source=True,
        refuted_scope='per-tree pairwise cancellation of the root-lift comparison corrections on a complete source return',
        arbitrary_coupled_cancellation_refuted=False,FE02_CD='OPEN',Coarse_Double_counterexample=False)
    b.save('composition_shortcut_obstruction_certificate.json',out)
    print('Exact composition shortcut obstruction: A closes with one unpaired correction; global FE02 stays OPEN')


if __name__=='__main__':main()
