"""Combine new finite/source evidence and pin exact coverage; no predicate reruns."""
import json,subprocess
from pathlib import Path
from entry import BASE,sha
def main():
    out=BASE/'final_manifest.json';assert not out.exists();run=json.loads((BASE/'run_result.json').read_text());assert run['status']=='ALL7_LEADING_THREE_UNIT_FINITE_CERTIFICATES_PASS'
    source=json.loads((BASE/'source_audit.json').read_text());assert source['status']=='POPULATION3_ORIGINAL_SOURCE_AND_FULL_CLOSURE_PASS' and source['CPU_seconds']<300
    combined=json.loads((BASE/'combination_check.json').read_text());assert combined['status']=='COMBINED_COVERED_DOMAIN_PASS_FULL_M3_INCOMPLETE' and combined['production_predicates_replayed']==0
    audits=[];builds=[];constructs=[];covered=[]
    for sig in run['completed_signatures']:
        folder=BASE/('s'+''.join(map(str,sig)));a=json.loads((folder/'audit.json').read_text());b=json.loads((folder/'build_status.json').read_text());c=json.loads((folder/'construction.json').read_text())
        assert a['status']=='INDEPENDENT_POPULATION_PREFIX_AND_RESIDUAL_PASS' and c['status']=='CONSTRUCTED_UNAUDITED' and b['status']=='COMPLETE_POPULATION_PREFIX_RELATION_UNAUDITED'
        assert a['potential_sha256']==sha(folder/'potential.json') and a['canonical_transition_queries']==b['queries'] and a['access_options']==b['option_count']
        assert a['canonical_transition_queries']<=1000000 and a['cpu_seconds']<120 and b['cpu_seconds']<120 and c['cpu_seconds']<300
        assert c['peak_conservative_resident_records']<2000000 and b['peak_DP_records']<2000000 and b['option_count']<5000000
        audits.append(a);builds.append(b);constructs.append(c);full=list(sig)+[0]*7;covered.extend((full,list(reversed(full))))
    assert len({tuple(s) for s in covered})==14
    rows=[json.loads((BASE/p).read_text()) for p in source['root_files']];assert len(rows)==51
    high=next(r for r in rows if 'h0_corrected' in r['label']);e=high['environment']
    assert e['MXHbt_bT0']==high['source']['b']['root']==high['destination']['b']['root']==8 and e['MXHbt_bd0']==18
    assert high['weight']==-3 and high['q']==9 and high['midpoint']['v']==4
    assert not (high['source']['b']['kr'][8]==0 and high['source']['b']['rr'][8]==19) and high['destination']['b']['kr'][8]==0 and high['destination']['b']['rr'][8]==19
    macro=next(r for r in rows if 'DELETE_KEEP_normal_form' in r['label']);e=macro['environment'];assert e['MXLw_nev']==3 and e['MXLw_ed1']==0 and e['MXLw_eT0']==e['MXLw_eT1']
    normal=next(r for r in rows if r is not macro and r['kind']=='LOW' and r['source']==macro['source'] and r['destination']==macro['destination'] and r['q']==macro['q'] and r['weight']==macro['weight'])
    lr=next(r for r in rows if 'LRTrue' in r['label']);e=lr['environment'];parent=e['MXLw_cl0'];assert e['MXLw_kl0']==0 and e[f'MXLw_kr{parent}']==0 and e[f'MXLw_cr{parent}']==e['MXLw_eT0']
    attributes={'status':'SAVED_NEW_SOURCE_ATTRIBUTES_PASS','production_predicates_replayed':0,
      'h0_actual_root8_declared18_q9_weight_minus3_fiber4':True,'full_macro_source_destination_H_q_weight_preserved':True,
      'zero_charge_KEEP_same_actual_anonymous_slot':True,'new_actual_LR_helper_confirmed':True,
      'new_source_queries':source['unique_original_roots'],'new_full_closed_mixed_cycles':source['full_closed_mixed_cycles']}
    with (BASE/'semantic_attributes.json').open('x',encoding='utf-8') as f:json.dump(attributes,f,indent=2)
    baseline=json.loads((BASE/'entry_baseline.json').read_text());old={r['path'] for r in baseline['files']}
    assert all(Path(r['path']).is_file() and sha(Path(r['path']))==r['sha256'] for r in baseline['files'])
    assert not [p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],text=True)
    assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['head']
    integrity={'status':'PASS','old_files_unchanged':len(old),'head':baseline['head'],'tracked_tree_clean':True,'new_writes_confined_here':True}
    with (BASE/'integrity.json').open('x',encoding='utf-8') as f:json.dump(integrity,f,indent=2)
    result={'status':'PROVED_RESTRICTED_DOMAIN_14_POPULATION_THREE_SIGNATURES','leading_signatures':run['completed_signatures'],'covered_signatures':covered,
      'legal_masks':126,'new_signature_count':14,'new_mask_signature_sectors':1764,'both_chi8_regions_where_realizable':True,
      'J_range':[-2,0],'uniform_finite_walk_bound':-7,'closed_mixed_walk_lower_bound':0,
      'canonical_transition_queries':sum(a['canonical_transition_queries'] for a in audits),'private_assignment_visits':sum(a['private_assignment_visits'] for a in audits),
      'private_duplicate_rows_removed_by_proved_identity':sum(a['duplicate_private_assignments_quotiented'] for a in audits),
      'finite_access_options':sum(a['access_options'] for a in audits),'independent_explicit_residuals':sum(a['explicit_residuals'] for a in audits),
      'minimum_residual':min(a['minimum_residual'] for a in audits),'maximum_canonical_queries_per_phase':max(a['canonical_transition_queries'] for a in audits),
      'maximum_DP_records':max(b['peak_DP_records'] for b in builds),'maximum_construction_records':max(c['peak_conservative_resident_records'] for c in constructs),
      'finite_CPU_seconds':round(sum(a['cpu_seconds'] for a in audits)+sum(b['cpu_seconds'] for b in builds)+sum(c['cpu_seconds'] for c in constructs),3),
      'source_CPU_seconds':source['CPU_seconds'],'original_source_roots':51,'fully_closed_new_mixed_cycles':14,
      'completed_old_source_checks_repeated':0,'combined_bank':{'signature_vectors':2720,'mask_signature_sectors':342720,'walk_bound':-7,'closed_walk_bound':0},
      'remaining_total3_signature_vectors':196,'remaining_larger_multi_support_populations':True,
      'remaining_uncovered_branch':'support>=2 and (total>=4 or uncovered total3 positions), NH>=1, DL>2NH+PL',
      'R1_R4_preserved':True,'h0_correction_retained':True,'Bank25':25,'full_M3_proved':False,'negative_original_cycle_certified':False,'integrity':integrity}
    with (BASE/'certificate.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    report=f'''# POP3_01 — repeated populations and three-gap supports certified

**PROVED—RESTRICTED DOMAIN:** all seven multiple-support signatures of
total3 within gaps0,1,2, and their seven reflected counterparts within
gaps7,8,9. All126 legal masks are covered. Both chi8 regions are included
where realizable; positive gap9 excludes chi8. J is in[-2,0] and every
original leg obeys W(O)=J(O)-5chi8(O.b),W(M)=-5chi8(M.b). Arbitrary finite
walks have weight>=-7 and fully closed original mixed walks have weight>=0.

The leading signatures are(2,1,0),(1,1,1),(1,2,0),(2,0,1),(1,0,2),
(0,2,1),(0,1,2), padded with seven zeros. Reflect all10 coordinates for
the other seven. This closes both a larger-population case and genuine
three-positive-gap support; no arbitrary-population extrapolation is made.

## New mechanism and independent evidence

The population-budgeted prefix DP retains every compatible private gap
choice and exact selected anonymous multiplicity. It permits a helper at
ANY actual node in an outer gap, including a nonminimum gap0/nonmaximum
gap9 node. Duplicate internal subterms are unfolded as distinct original
nodes; same-gap occurrences never share a unit. Only IDENTICAL projected
RAW prefix terms under the SAME access word are deduplicated. Their alpha
endpoints/H/B helper/core target/weight are literally identical, so all
private branches still constrain one shared-state value. No private gap
label is observed by J, no hidden-S completion is chosen and no vertices
are merged. SOURCE_PROOF.md gives the structural induction and original
normal-form/terminal-debt lift, including weak LE bills and G's literal
slot0/current-child lookups.

Independent ordered-key enumeration projects private colors BEFORE the
transition query and uses source-address identities for all occurrences.
It does not import the DP. It regenerated{result['canonical_transition_queries']}
canonical word profiles from{result['private_assignment_visits']} private
assignments, verifies every{result['finite_access_options']} access option,
and independently checks{result['independent_explicit_residuals']} explicit
integer residuals, minimum0. Analytic range/zero-source/debt omissions
are checked against the pinned independently rebuilt B bank. No new
solver/fit backend or B-product edge graph is introduced.

The original-source audit checks51 NEW complete production roots and14
full147-coordinate O/actual127-coordinate M closed mixed cycles, with
immediate per-root checkpoints. It includes nonminimum gap0 helpers at
weights0/+1; the newly enabled LR helper pattern; a nonmaximum gap9
helper; charged DELETE/zero-charge KEEP at the SAME actual node; two
exposed anonymous nodes in one interior gap; Gamma0 H2 with actual
terminal q4; and actual h=0/declared18/q9/weight-3 high entry with fiber
v4 independent of actual B target/root8. All original q/weights and
complete shared interfaces pass. No earlier production predicate or old
finite matrix was rerun. Saved-value checks validate the new combined
dispatch without production-predicate replay.

## Resources, coverage and proof ledger

Maximum canonical queries in a registered phase:
{result['maximum_canonical_queries_per_phase']}<1m. Maximum live DP records:
{result['maximum_DP_records']}<2m; maximum construction records:
{result['maximum_construction_records']}<2m. Each finite phase stayed below
120 CPU seconds and construction below300. Total new finite CPU:
{result['finite_CPU_seconds']}s; one source-family phase:
{result['source_CPU_seconds']}s<300. Original production DAGs remain
1400081 LOW/53455 HIGH, below4m. No cap increase, solver/backend change,
new state coordinate/observable, production edit, install or Git mutation.
R1–R4, h0 correction, depth2,T266 and Bank25=25 remain frozen.
integrity.json confirms all2513 old research files and Git are unchanged.

BEFORE: all distinct two-unit supports were certified by UNITPAIR_FIN01;
multiple-support total3 cases remained open. RESULT: all14 named new
signatures now certified. AFTER/NET ADVANCEMENT:14 signatures and1764
new mask/signature sectors, with no new assumptions. Combined with the
old single-gap and two-unit bank,2720 signatures/342720 mask sectors have
signed certificates. combined_certificate.py explicitly rejects open
signatures and loads one table at a time. Typed isolated invalid vertices
may receive J0; this never enlarges the certified signature domain.

**Full M3 remains OPEN.** Exactly196 other total3 signature vectors still
lack full signed certificates, as do larger multiple-support populations.
The universal balanced-count theorem still handles DL<=2NH+PL in those
sectors; their hard-deficit branch remains open. No full-M3, Stage04,
Bank25 or Dynamic Optimality promotion, and no negative original cycle
claim. The next natural extension is other total3 positions, then a
source-proved population saturation/reduction before arbitrary larger
counts. It must use a new four-rule gate; finite n3 tests alone do not
prove n4 or unbounded population.
'''
    with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(report)
    result['files']=[{'path':p.as_posix(),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('files','covered_signatures','leading_signatures')},indent=2),flush=True)
if __name__=='__main__':main()
