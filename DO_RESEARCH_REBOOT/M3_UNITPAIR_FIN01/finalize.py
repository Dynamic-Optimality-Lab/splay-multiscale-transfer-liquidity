"""Combine preserved prior success evidence with ONLY the newly finished controls."""
from pathlib import Path
import json,subprocess
from entry import BASE,sha
OLD=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
def main():
    out=BASE/'final_manifest.json';assert not out.exists();new=json.loads((BASE/'source_completion.json').read_text());assert new['status']=='THREE_REMAINING_SOURCE_CONTROLS_PASS'
    old=json.loads((OLD/'source_audit_cap.json').read_text());finished=set(map(tuple,old['completed_supports']))
    for filename in new['checkpoint_files']:
        p=json.loads((BASE/filename).read_text());assert p['status']=='PASS' and tuple(p['pair']) not in finished and len(p['rows'])==3
        finished.add(tuple(p['pair']));assert p['cycle']['full147_O_closure'] and p['cycle']['same127_M']
    assert finished=={(g,h) for g in range(10) for h in range(g+1,10)}
    finite=json.loads((OLD/'finite_summary.json').read_text());assert finite['status']=='ALL24_NEW_CANONICAL_FINITE_CERTIFICATES_PASS'
    for pair in json.loads((OLD/'run_result.json').read_text())['completed_pairs']:
        folder=OLD/f'p{pair[0]}_{pair[1]}';audit=json.loads((folder/'audit.json').read_text());assert audit['status']=='INDEPENDENT_FINITE_EXACT_PASS' and sha(folder/'potential.json')==audit['potential_sha256']
    assert json.loads((OLD/'outer_helper_controls.json').read_text())['status']=='ORIGINAL_BOTH_OUTER_HELPERS_PASS'
    provenance=old['reproducible_progress_provenance'];assert sha(OLD/'source_audit.py')==provenance['prototype_program_sha256'] and sha(OLD/'source_audit_v3.py')==provenance['version3_program_sha256']
    baseline=json.loads((BASE/'entry_baseline.json').read_text());existing={x['path'] for x in baseline['files']}
    assert all(Path(x['path']).is_file() and sha(Path(x['path']))==x['sha256'] for x in baseline['files'])
    assert not [p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in existing]
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True) and subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['head']
    integrity={'status':'PASS','old_files_unchanged':len(existing),'head':baseline['head'],'tracked_tree_clean':True,'writes_confined_here':True}
    with (BASE/'integrity.json').open('x',encoding='utf-8') as f:json.dump(integrity,f,indent=2)
    result={'status':'PROVED_RESTRICTED_DOMAIN_ALL45_DISTINCT_TWO_UNIT_SUPPORTS','signature_family':'sigma=e_g+e_h,0<=g<h<=9',
      'legal_masks':126,'signatures':45,'mask_signature_sectors':5670,'new_sectors_since_first_two_gap_signature':5544,
      'both_regions_where_realizable':True,'J_range':[-2,0],'uniform_finite_walk_bound':-7,'closed_walk_lower_bound':0,
      'combined_single_gap_and_two_unit_bank':{'signatures':2706,'mask_signature_sectors':340956},'all_total_population_le2_covered':True,
      'new_original_root_queries':9,'previously_completed_checks_repeated':0,'completed_support_cases':45,'unique_original_family_roots':139,
      'full_O_coordinates':147,'actual_M_coordinates':127,'source_phase_CPU_seconds':new['CPU_seconds'],'old_cap_status_preserved':old['status'],
      'old_lost_environments_claimed_saved':False,'old_controls_reused_with_provenance':True,'R1_R4_preserved':True,'h0_correction_retained':True,
      'remaining':'multiple support,total>=3,hard deficit D_L>2N_H+P_L','full_M3_proved':False,'negative_original_cycle_certified':False,'integrity':integrity}
    with (BASE/'certificate.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    text='''# All distinct two-unit gap supports — completed certificate

**PROVED—RESTRICTED DOMAIN:** every sigma=e_g+e_h,0<=g<h<=9,
all126 masks. Both chi8 regions are included wherever realizable; positive
gap9 makes chi8 impossible. Every original leg obeys the shared-state
potential W(O)=J(O)-5chi8(O.b),W(M)=-5chi8(M.b),J in[-2,0]. Arbitrary
finite walks have weight>=-7 and full original closed mixed walks have
weight>=0 (outside-only bound-2).

Only the three missing support controls(7,8),(7,9),(8,9) were executed:
9 original roots and3 full147-coordinate O/127-coordinate M cycles.
Each support was checkpointed immediately. Completion CPU12.547 seconds,
below the unchanged300-second completion-phase cap. None of the42 finished
support cases,4 outer-helper controls or541463592 finite residual checks
was repeated. The user's new explicit completion instruction authorizes
this strictly smaller audit; the earlier cap failure/costs remain intact.

The preserved42 observed successful cases are reused with pinned deterministic
program/progress provenance; their lost raw environments are NOT invented.
New raw environments and exact extracted interfaces are in p7_8.json,
p7_9.json,p8_9.json. In total the family has139 unique original root
controls and45 full closed mixed controls. All25 canonical finite tables
were independently checked before this phase; their hashes remain pinned.
The source-complete lift/reflection and high absorption are those reviewed
in M3_UNITPAIR01/SOURCE_PROOF.md and M3_TWOGAP_AUD01/AUDIT_REPORT.md.
No M3 sign assumption enters those dependencies.

The complete45-signature family now enters the audited sign bank:5670
mask/signature sectors,5544 beyond the first independently certified
two-gap signature. Combined with the old arbitrary-population single-gap
bank,2706 signatures/340956 mask sectors are covered. Every signature
with total population<=2 is included. This is not full M3.

BEFORE: complete finite candidates; three source controls outstanding.
RESULT: exactly those controls PASS, no repeated completed checks.
AFTER/NET ADVANCEMENT: all45 distinct two-unit supports certified.
No new assumption, source/graph/observable/backend change, cap increase,
or Stage04 promotion. R1–R4, original q/weights/sorts/shared midpoint,
h=0 correction, depth2,T266 and Bank25=25 remain frozen. integrity.json
verifies old files and Git are unchanged.

**Full M3 remains OPEN:** multiple-support populations with total>=3 and
D_L>2*N_H+P_L require new complete source-profile arguments and exact
certificates. Larger populations/supports are a separate gated campaign.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(text)
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.iterdir()) if p.is_file()]
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
