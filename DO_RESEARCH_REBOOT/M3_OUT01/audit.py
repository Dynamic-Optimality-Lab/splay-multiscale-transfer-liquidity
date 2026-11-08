"""Read-only provenance, explicit-glue and preservation audit; fresh outputs only."""
import sys,json,hashlib,subprocess,time
from collections import Counter
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M2_DSK01']
from global_potential import GlobalSingleGapPotential,chi
from certify_dirty import cases
BASE=Path('DO_RESEARCH_REBOOT/M3_OUT01');ROOT=Path.cwd()

def raw(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes()
def digest(p):return hashlib.sha256(raw(p)).hexdigest()
def read(p):return json.loads(raw(p))
def write(p,j):
    with p.open('x',encoding='utf-8') as f:json.dump(j,f,indent=2)
def git(*args):return subprocess.check_output(['git',*args]).decode().strip()

def main():
    start=time.process_time();baseline=read(BASE/'entry_baseline.json')
    assert len(baseline)==414
    for r in baseline:assert digest(ROOT/r['path'])==r['sha256'],r['path']
    assert not git('status','--porcelain','--untracked-files=no')
    assert git('branch','--show-current')=='coarse-double-branch'
    assert git('rev-parse','HEAD')=='fea2a25b05e97f726b6e1891cebb12c4cfca821a'
    cert=read(BASE/'proof_certificate.json');diag=read(BASE/'diagnostic.json')
    assert cert['status']=='PASS_PRODUCTION_DAG' and diag['status']=='PASS_NORMAL_FORM_ROOT_CLAIMS'
    assert cert['cases']==diag['cases']==5040 and not cert['failures'] and not diag['failures']
    expected=[]
    for meta,source,period,word in cases():
        if meta['d']!=14:continue
        for depth in range(10,14):
            pins={**source,'T_bT0':meta['target'],'T_bd0':depth}
            for k in range(depth+1):pins[f'T_bp0_{k}']=period[k%len(period)]
            for k in range(depth):pins[f'T_bdir0_{k}']=word[k%len(word)]
            expected.append({**meta,'d':depth,'forced_final_root_claim_verified':True,
                             'pins_sha256':hashlib.sha256(json.dumps(pins,sort_keys=True).encode()).hexdigest()})
    assert expected==cert['rows'];assert cert['production_DAG_nodes']==14600
    assert cert['right_cases']==2044 and cert['left_cases']==2996
    assert cert['cpu_seconds']<300 and diag['cpu_seconds']<120
    transfer=read(BASE/'original_transfer_audit.json');outer=read(BASE/'gap9_original_audit_v2.json')
    high=read(BASE/'high_controls.json');reflection=read(BASE/'reflection_audit.json')
    assert all(j['status']=='PASS' for j in [transfer,outer,high])
    assert reflection['status']=='PASS_COMPLETE_LOW_REFLECTION_IDENTITIES'
    assert reflection['models']==48450 and reflection['A_word_queries']==151717 and reflection['B_kernel_queries']==43758
    assert reflection['cpu_seconds']<120 and not reflection['raw_high_states_reflected']
    assert transfer['original_roots']==62 and outer['original_roots']==14
    assert high['queries']==100 and high['accepted']==28 and high['rejected_cheap_dirty_candidates']==72
    assert all(j['cpu_seconds']<300 for j in [transfer,outer,high])
    assert len(transfer['closed_mixed_cycles'])==5 and outer['closed_mixed_cycle']['weight']==8
    P=GlobalSingleGapPotential();residuals=Counter();checks=0;negative_ingress=0
    records=[]
    for n in ['M3_GAP01']+[f'M3_GAPINT0{g}' for g in range(1,5)]:
        records+=read(Path('DO_RESEARCH_REBOOT')/n/'original_audit.json')['records']
    records+=transfer['records']+outer['records']
    for r in records:
        ws=P.ordinary(r['source']);wt=P.ordinary(r['destination'])
        assert -7<=ws<=0 and -7<=wt<=0
        if r['kind']=='LOW':
            assert chi(r['source']['b'])==chi(r['destination']['b'])
            residual=r['w']+ws-wt;assert residual>=0;residuals[residual]+=1
        else:
            wm=P.midpoint(r['shared_midpoint']);a=r['w']+ws-wm;b=wm-wt
            assert a>=0 and b>=0;residuals[a]+=1;residuals[b]+=1
        checks+=1
    for r in high['records']:
        if not r['high_root']:continue
        alpha=[[2,0,0] for _ in range(7)];alpha[0]=[2,1,r['alpha_root']]
        s={'mu':r['mu'],'sigma':r['sigma'],'b':r['source'],'alpha':alpha}
        t={'mu':r['mu'],'sigma':r['sigma'],'b':r['destination'],'alpha':alpha}
        wm=P.midpoint({'b':t['b']});ws=P.ordinary(s);wt=P.ordinary(t)
        a=r['w']+ws-wm;b=wm-wt;assert a>=0 and b>=0
        residuals[a]+=1;residuals[b]+=1;checks+=1
        if r['w']<0:
            assert not chi(s['b']) and chi(t['b']) and s['b']['root']==t['b']['root']==8
            negative_ingress+=1
    assert checks==166 and negative_ingress==2
    # Algebraic ingress audit includes the worst J(source)=-2 case, not only samples.
    for j in (-2,-1,0):
        for w in range(-3,7):assert w-(-5-j)>=0
    glue={'status':'PASS_EXPLICIT_GLOBAL_GLUE','accepted_original_records_checked':checks,
          'same_midpoint_OM_MO_inequalities':True,'residual_histogram':dict(residuals),
          'h0_negative_root_preserving_ingresses':negative_ingress,
          'ordinary_formula':'J-5*chi8','midpoint_formula':'-5*chi8','range':[-7,0],
          'new_fit_or_graph_coordinate':False,'cpu_seconds':round(time.process_time()-start,3)}
    write(BASE/'global_glue_audit.json',glue)
    files=[]
    for p in sorted(BASE.rglob('*')):
        if p.is_file():files.append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(raw(p)),'sha256':digest(p)})
    deps=[]
    for row in baseline:
        if row['path'].startswith(('DO_RESEARCH_REBOOT/M2_DSK01/','DO_RESEARCH_REBOOT/M2_SEP01/',
                                  'DO_RESEARCH_REBOOT/M3_PHI01/','DO_RESEARCH_REBOOT/M3_GAP',
                                  'DO_RESEARCH_REBOOT/M3_H2R01/')):
            deps.append(row)
    prefix='DO_RESEARCH_REBOOT/06_CERTIFICATES/'
    for folder in ['DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER','DIRECT_CDK5N_11F_STRICT_CLOSURE',
                   'DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE']:
        for p in sorted((ROOT/prefix/folder).glob('*.py')):
            deps.append({'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p)})
    # Verify the old research again after the read-only proof-value audit.
    for r in baseline:assert digest(ROOT/r['path'])==r['sha256'],r['path']
    baseline_names={r['path'] for r in baseline}
    for p in subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0'):
        if p and p not in baseline_names:assert p.startswith(BASE.as_posix()+'/'),p
    assert not git('status','--porcelain','--untracked-files=no')
    manifest={'status':'PASS_RESTRICTED_MIXED_THEOREM_AND_UNIVERSAL_HIGH_TOLL',
       'date_local':'2026-10-29 Asia/Karachi','branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),
       'old_research_files_unchanged':len(baseline),'tracked_source_unchanged':True,
       'outside_high_OM_weight_lower_bound':2,'high_OM_lower_bound_on_any_closed_mixed_walk':2,
       'all_signature_signed_subclass':'D_L <= 2*N_H+P_L',
       'single_support_gaps':list(range(10)),'max_population':266,'all_legal_masks':126,
       'proved_signature_vectors':2661,'proved_mask_signature_sectors':335286,
       'outside_walk_bound':-2,'global_single_support_walk_bound':-7,
       'fresh_original_root_evaluations_and_replays':176,'fresh_accepted_original_roots':104,
       'fresh_closed_mixed_cycles':6,'production_DAG_identities':5040,
       'multiple_positive_gap_compensation':'OPEN','original_negative_mixed_cycle_certified':False,
       'R1_R4_preserved':True,'h0_correction_preserved':True,'Bank25':25,'Stage04_run':False,
       'prototype_fixture_failure_preserved':'gap9_original_audit.py stopped before output on kind2-only assertion; version2 permits zero-inventory port',
       'completed_control_program_cpu_seconds':{'transfer':transfer['cpu_seconds'],'high':high['cpu_seconds'],'gap9_v2':outer['cpu_seconds']},
       'global_glue':glue,'source_and_inherited_dependencies':deps,'files_excluding_this_manifest':files}
    write(BASE/'final_manifest.json',manifest)
    print(json.dumps({k:v for k,v in manifest.items() if k not in ['source_and_inherited_dependencies','files_excluding_this_manifest','global_glue']},indent=2))

if __name__=='__main__':main()
