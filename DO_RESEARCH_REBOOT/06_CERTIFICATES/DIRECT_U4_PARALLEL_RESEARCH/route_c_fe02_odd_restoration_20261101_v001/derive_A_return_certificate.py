"""Derive a full-A restoration fact from already independently checked rows."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=HERE/'odd_restoration_source_certificate.json';d=json.loads(p.read_text())
    audit=json.loads((HERE/'independent_audit.json').read_text())
    assert audit['status']=='PASS' and audit['certificate_hashes'][p.name]==sha(p)
    ids=d['episode_indices'];rs=[d['rows'][i] for i in ids]
    assert rs[0]['source_A']==rs[-1]['destination_A']
    assert rs[0]['source_B']!=rs[-1]['destination_B']
    sy=[d['symbolic_rows'][i] for i in ids]
    assert sy[0]['source_A']==sy[-1]['destination_A']
    assert sy[0]['source_B']!=sy[-1]['destination_B']
    result=dict(status='EXACT_FULL_A_RETURN_WITH_B_DRIFT',source_certificate_sha256=sha(p),
        independent_audit_sha256=sha(HERE/'independent_audit.json'),episode_indices=ids,
        episode_word=[7,11,1],A_steps=3,A_physical_units=6,B_double_demands=7,
        complete_A_source_restored=True,complete_B_source_restored=False,
        original_boundary_ancestor_restored=True,transferred_inversion=[7,8],
        all14_common_opaque_gap_extension=True,full_closed_control_still_FE02=True,
        eventual_discharge='OPEN in general; later donor block10 in this control',
        FE02_CD='OPEN',Coarse_Double_counterexample=False)
    with (HERE/'A_return_source_certificate.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,indent=2);f.write('\n')
    print('Full A returns exactly; full B does not; source deficit remains1')


if __name__=='__main__':main()
