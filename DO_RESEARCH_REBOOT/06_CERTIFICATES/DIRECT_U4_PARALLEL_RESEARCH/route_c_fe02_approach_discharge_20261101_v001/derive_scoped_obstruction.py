"""Extract an exact boundary obstruction from already independently checked rows."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    p=HERE/'closed_discharge_certificate.json'
    d=json.loads(p.read_text())['cases']['overlap2']
    positive=d['rows'][6];following=d['rows'][7]
    assert (positive['mode'],positive['key'],positive['a'],positive['q'])==('KEEP',7,1,3)
    assert (following['mode'],following['key'],following['a'],following['q'])==('KEEP',2,1,2)
    assert following['source_A']==positive['destination_A'] and following['source_B']==positive['destination_B']
    assert (following['d_A'],following['d_B'])==(1,4)
    assert following['destination_A']==following['destination_B']
    audit=json.loads((HERE/'independent_audit.json').read_text())
    assert audit['status']=='PASS'
    result=dict(status='REFUTED—EXACT for the two scoped immediate-discharge claims',
        source_certificate_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        independent_audit_sha256=hashlib.sha256((HERE/'independent_audit.json').read_bytes()).hexdigest(),
        actual_reachable_closed_case='overlap2',positive_block=6,positive_type=[1,3],
        post_positive_tracked_key=2,post_positive_depths_A_B=[1,4],
        full_pair_rotation_distance_lower_bound=3,
        following_block=7,following_type=[1,2],following_delta=0,
        following_has_unused_A_unit_after_own_payment=False,
        following_synchronizes_full_pair=True,eventual_donor_block=8,
        refuted_claims=['every positive(1,3) exit is equal or one rotation apart',
            'every unique positive(1,3) has a negative immediate next nontrivial block'],
        eventual_discharge_refuted=False,FE02_CD='OPEN',Coarse_Double_counterexample=False)
    with (HERE/'scoped_obstruction_certificate.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2);f.write('\n')
    ledger=json.loads((HERE/'proof_status_ledger.json').read_text())
    ledger['universal_immediate_equal_or_one_rotation_exit']='REFUTED—EXACT: reachable exactly-closed overlap2 control, post-positive key2 depth difference3'
    ledger['universal_immediate_negative_successor']='REFUTED—EXACT: same control, saturated following KEEP2'
    ledger['supersedes_status_ambiguity_only']='AD04 unused extension is more precisely REFUTED, as AD06 explains'
    with (HERE/'proof_status_ledger_v002.json').open('x',encoding='utf-8') as f:
        json.dump(ledger,f,indent=2);f.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
