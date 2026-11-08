"""Record the source child barrier in the already checked restoration word."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=HERE/'odd_restoration_source_certificate.json';d=json.loads(p.read_text())
    audit=json.loads((HERE/'independent_audit.json').read_text())
    assert audit['status']=='PASS' and audit['certificate_hashes'][p.name]==sha(p)
    rs=d['rows'];pos,helper,ret=[rs[i] for i in d['episode_indices']]
    original=pos['source_B'][2][0];after=ret['destination_B'][2][0]
    assert original==pos['source_path_B'][1]==2
    assert after==helper['source_path_B'][1]==8
    assert original<pos['key']<after
    assert rs[-1]['destination_B'][2][0]==original
    result=dict(status='EXACT_SOURCE_CHILD_BARRIER',source_certificate_sha256=sha(p),
        independent_audit_sha256=sha(HERE/'independent_audit.json'),common_boundary=1,
        initial_B_child=original,first_positive_target=7,first_restored_B_child=after,
        child_order='2<7<8',initial_B_source_not_restored_at_first_boundary_return=True,
        final_closed_B_child=2,first_later_real_donor=10,
        general_ordered_zero_reserve_barrier='p0<r0<p_k, or reflected reverse order',
        arbitrary_first_reset_payment='OPEN',FE02_CD='OPEN',Coarse_Double_counterexample=False)
    with (HERE/'B_child_barrier_certificate.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print('Exact B child barrier: 2<7<8; eventual original child restored in safe full control')


if __name__=='__main__':main()
