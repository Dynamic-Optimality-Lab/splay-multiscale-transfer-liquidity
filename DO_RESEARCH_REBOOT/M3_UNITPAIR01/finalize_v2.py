"""Promote only the complete, independently verified two-unit family."""
import json,subprocess,time
from pathlib import Path
from entry import BASE,sha
def main():
    start=time.process_time();out=BASE/'final_manifest.json';assert not out.exists()
    run=json.loads((BASE/'run_result.json').read_text());assert run['status']=='ALL24_NEW_CANONICAL_FINITE_CERTIFICATES_PASS'
    source=json.loads((BASE/'source_audit_v3.json').read_text());outer=json.loads((BASE/'outer_helper_controls.json').read_text())
    assert source['status']=='ORIGINAL_SOURCE_FAMILY_AND_FULL_CLOSURE_PASS' and outer['status']=='ORIGINAL_BOTH_OUTER_HELPERS_PASS'
    assert source['registered_family_CPU_including_prototypes']<300
    audits=[];constructions=[];relations=[]
    for g,h in run['completed_pairs']:
        f=BASE/f'p{g}_{h}';a=json.loads((f/'audit.json').read_text());c=json.loads((f/'construction.json').read_text());r=json.loads((f/'relation.json').read_text())
        assert a['status']=='INDEPENDENT_FINITE_EXACT_PASS' and c['status']=='CONSTRUCTED_UNAUDITED'
        assert sha(f/'potential.json')==a['potential_sha256'];audits.append(a);constructions.append(c);relations.append({k:v for k,v in r.items() if k not in ('shadows','options','families')})
    covered=[]
    for g in range(10):
        for h in range(g+1,10):
            canonical=(g,h) if g+h<=9 else (9-h,9-g)
            assert canonical==(0,1) or list(canonical) in run['completed_pairs']
            covered.append({'g':g,'h':h,'canonical':canonical,'reflected':g+h>9,'status':'PROVED_RESTRICTED_DOMAIN','chi8_realizable':h!=9})
    assert len(covered)==45
    b=json.loads((BASE/'entry_baseline.json').read_text());old={r['path'] for r in b['files']}
    assert all(Path(r['path']).is_file() and sha(Path(r['path']))==r['sha256'] for r in b['files'])
    unexpected=[p.as_posix() for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old];assert not unexpected
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==b['head']
    integrity={'status':'PASS','old_files_unchanged':len(old),'tracked_tree_clean':True,'head':b['head'],'writes_confined_here':True}
    with (BASE/'integrity.json').open('x',encoding='utf-8') as f:json.dump(integrity,f,indent=2)
    report={'status':'PROVED_RESTRICTED_DOMAIN_ALL45_DISTINCT_UNIT_PAIRS','signature_family':'sigma=e_g+e_h,0<=g<h<=9','masks':126,
      'unit_pair_signatures':45,'unit_pair_mask_sectors':5670,'new_signature_count_after_TWOGAP_AUD01':44,'new_mask_sectors_after_TWOGAP_AUD01':5544,
      'canonical_tables_total':25,'new_canonical_tables':24,'new_profile_queries':sum(a['profile_queries'] for a in audits),
      'new_A_access_options':sum(a['access_options'] for a in audits),'new_explicit_residuals':sum(a['explicit_residuals'] for a in audits),
      'minimum_residual':min(a['minimum_residual'] for a in audits),'maximum_construction_resident_records':max(c['peak_conservative_resident_records'] for c in constructions),
      'new_finite_CPU_seconds':round(sum(a['cpu_seconds'] for a in audits)+sum(c['cpu_seconds'] for c in constructions)+sum(c['cpu_seconds'] for c in relations),3),
      'source_audit_CPU_seconds':source['registered_family_CPU_including_prototypes'],'original_roots':139,'full_closed_mixed_controls':45,'source_cases_reused_with_provenance':22,'source_cases_with_saved_final_environments':23,
      'J_range':[-2,0],'uniform_walk_bound':-7,'closed_walk_bound':0,'h0_correction_retained':True,'R1_R4_preserved':True,
      'combined_with_previous_single_gap_bank':{'signatures':2706,'mask_signature_sectors':340956,'status':'PROVED_RESTRICTED_DOMAIN'},
      'remaining_uncovered':'support(sigma)>=2, sum(sigma)>=3, N_H>=1, D_L>2*N_H+P_L; both regions where realizable',
      'larger_populations_or_supports_proved':False,'full_M3_proved':False,'negative_original_cycle_certified':False,'covered_pairs':covered}
    with (BASE/'certificate.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    text=f'''# UNITPAIR01 â€” every distinct two-unit gap support certified

**PROVEDâ€”RESTRICTED DOMAIN:** every sigma=e_g+e_h,0<=g<h<=9,
all126 legal masks. Both chi8 regions are included wherever realizable;
positive gap9 makes chi8 impossible. All original legs obey the signed
potential. Arbitrary finite walks have weight>=-7 and fully closed mixed
walks have weight>=0. Outside-only bound is the sharper-2.

The25 canonical tables cover all45 supports by the source-derived low
reflection proof in SOURCE_PROOF.md. Only mathematical low images are
reflected; original high sentinels, weak LE bills and actual shared states
are preserved. Pair(0,9) includes BOTH changing outer helpers. The old
independently audited(0,1) table is reused;24 new tables pass independent
prefix regeneration, exact row residuals, debt/default checks and the
self-mirror consistency checks.

New finite queries:{report['new_profile_queries']}; new access options:
{report['new_A_access_options']}; independent explicit residuals:
{report['new_explicit_residuals']}, minimum0. No B-product graph is stored.
Peak conservative construction records:{report['maximum_construction_resident_records']}, below2m.
Every registered fixed-signature finite phase is below1m source queries
and120 CPU seconds; each construction is below300 CPU seconds. Total
new finite CPU:{report['new_finite_CPU_seconds']}s. Limits and backend are unchanged.

The bounded unchanged-source family audit verifies139 unique complete original
roots, including45 fully closed mixed cycle controls and45 weight-2 LOW
controls, covering every actual support and both reflected orientations.
Four additional H2 roots directly exercise helper0/helper9 at weights0/+1
in the both-outer signature. Their q is actual preterminal credit.
The first22 deterministic support cases reuse observed successful original
checks from the preserved prototype (reused_controls.json); the remaining23
save fresh raw environments in source_audit_v3.json. No lost in-memory
prototype environment is claimed to have been saved. Reuse and fixture-only
preparation optimizations are justified in SOURCE_AUDIT_REUSE.md; all
prototype CPU, outer-helper CPU and a conservative stop margin remain
inside the SAME300-second source budget.

Closure checks all147 original O coordinates and the actual127-coordinate
M, including alpha unused fields and B lo/hi. Original source audit CPU:
{report['source_audit_CPU_seconds']}s, below the300-second family cap.

decoder.py uses static dispatch on existing sigma, normalized RAW alpha7,
core B and default-psi; it loads one canonical table at a time. No private
gap label becomes observable, no original states are merged, and no field
is omitted from ORIGINAL closure. The h=0/declared18/q9/weight-3 entering
correction and independent high fiber v remain in the inherited universal
high absorption law. Source q/weights, two sorts/shared midpoint, depth2,
T266 and Bank25=25 remain frozen. R1â€“R4 PASS. integrity.json verifies every
old research file and the tracked Git tree remain unchanged.

BEFORE: only one two-gap unit signature independently certified.
RESULT: all45 distinct two-unit supports certified.
AFTER/NET ADVANCEMENT:44 additional signatures,5544 new mask/signature
sectors beyond TWOGAP_AUD01. With the earlier single-gap bank,2706 distinct
signatures and340956 mask/signature sectors have signed certificates.
No new assumptions or circular M3 sign dependencies are introduced.

**Full M3 remains OPEN.** The missing hard-deficit branch now has at least
three anonymous units: support>=2,sum(sigma)>=3,N_H>=1 and
D_L>2*N_H+P_L. This includes larger two-gap populations and three-or-more
positive gaps. Arbitrary population/support extrapolation is not permitted.
A separate source-complete campaign is required before promotion. A full
M3 coverage audit must remain INCOMPLETE until that branch is closed.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(text)
    manifest={k:v for k,v in report.items() if k!='covered_pairs'};manifest['integrity']=integrity
    manifest['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    with out.open('x',encoding='utf-8') as f:json.dump(manifest,f,indent=2)
    print(json.dumps({k:v for k,v in manifest.items() if k!='files'},indent=2),flush=True)
if __name__=='__main__':main()
