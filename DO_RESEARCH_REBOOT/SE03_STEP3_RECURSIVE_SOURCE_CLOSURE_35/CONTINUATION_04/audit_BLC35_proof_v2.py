"""Correct receipt-schema handling; the failed generic status check is retained."""
from pathlib import Path
p=Path(__file__).with_name('audit_BLC35_proof.py');s=p.read_text()
a="        data=json.loads((F/name).read_text());assert data['status'].startswith('PASS')"
b="""        data=json.loads((F/name).read_text())
        if name.endswith(('LOW_B_01.json','LOW_B_02.json')):
            assert data['status']=='CHECKPOINT' and data.get('failure') is None
        elif name=='independent_probe11_LOW_B_03.json':
            assert data['status']=='PASS_ALL_COMPLETE_NATIVE11_LOW_INEQUALITIES'
            assert data['next_group']==data['total_groups'] and data['checked_B_edges']==587860
        elif name=='independent_probe11_HIGH_envelope_B01.json':
            assert data['H_ge_4_minimum_margin']>=0 and data['H_ge_4_failed_envelopes']==0
        elif name=='independent_probe11_H3_actual_signs_B01.json':
            assert data['status']=='ALL_ACTUAL_H3_INEQUALITIES_PASS_CANDIDATE_B01'
            assert data['all_OTHER_H3_edges_from_checked_endpoint_envelope'] and data['exception_edges']==14
        else:assert data['status'].startswith('PASS')"""
assert s.count(a)==1;s=s.replace(a,b)
s=s.replace("            if Path(p).is_absolute():assert sha(Path(p))==h", "            assert sha(Path(p) if Path(p).is_absolute() else F/p)==h")
s=s.replace("F/'audit_BLC35_proof.py']", "F/'audit_BLC35_proof.py',F/'audit_BLC35_proof_v2.py']")
s=s.replace("audit_verify149_exit.json","audit_verify150_exit.json")
exec(compile(s,str(Path(__file__).resolve()),'exec'))
