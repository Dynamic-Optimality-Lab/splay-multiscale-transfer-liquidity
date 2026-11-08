"""Seal the independently audited restricted certificate; fail closed for full M3."""
import json,hashlib,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[1];R=ROOT/'DO_RESEARCH_REBOOT'
def raw(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes()
def sha(p):return hashlib.sha256(raw(p)).hexdigest()
def read(p):return json.loads(raw(p))
def write(p,j):
    with p.open('x',encoding='utf-8') as f:json.dump(j,f,indent=2)
def git(*args):return subprocess.check_output(['git',*args]).decode().strip()

def pins(j):
    if isinstance(j,dict):
        if isinstance(j.get('path'),str) and isinstance(j.get('sha256'),str):yield j['path'],j['sha256']
        for k,v in j.items():
            if isinstance(v,str) and len(v)==64 and (k.startswith('DO_RESEARCH_REBOOT/') or k.startswith('python/')):yield k,v
            yield from pins(v)
    elif isinstance(j,list):
        for x in j:yield from pins(x)

def main():
    baseline=read(BASE/'entry_baseline.json');assert len(baseline)==444
    for row in baseline:assert sha(ROOT/row['path'])==row['sha256'],row['path']
    combined=read(BASE/'combined_audit.json');projected=read(BASE/'actual_projected_product_audit_v2.json')
    assert combined['full_M3_certificate_pass'] is False and combined['restricted_single_gap_certificate_pass']
    assert projected['status']=='PASS_ACTUAL_FROZEN_PRODUCT_AND_PROJECTIONS'
    assert len(projected['projected_sort_weight_cases'])==22 and projected['Product_DAG_nodes']<4000000 and projected['cpu_seconds']<120
    historical={};manifest_paths=[]
    for name in ['M2_DSK01','M2_SEP01','M3_PHI01','M3_LDR01','M3_H2R01','M3_AER01','M3_GAP01','M3_OUT01']:
        for filename in ['manifest.json','final_manifest.json']:
            p=R/name/filename
            if not p.exists():continue
            manifest_paths.append(p.relative_to(ROOT).as_posix())
            for name,digest in pins(read(p)):
                assert name not in historical or historical[name]==digest,('conflicting old pin',name)
                historical[name]=digest
    for name,digest in historical.items():assert sha(ROOT/name)==digest,('historical dependency hash mismatch',name)
    assert len(historical)==333
    finite=[read(BASE/f'finite_gap{g}.json') for g in range(5)]
    assert sum(r['all_stored_edges_checked'] for r in finite)==19174005
    tables=[]
    for g,j in enumerate(finite):
        name='M3_GAP01' if g==0 else f'M3_GAPINT0{g}';folder=R/name
        tables.append({'canonical_gap':g,'covers_gaps':[g,9-g],
                       'catalog':{'path':(folder/'catalog.json').relative_to(ROOT).as_posix(),'sha256':sha(folder/'catalog.json')},
                       'values':{'path':(folder/'potential.bin').relative_to(ROOT).as_posix(),'sha256':sha(folder/'potential.bin')},
                       'states':j['states'],'verified_edges':j['all_stored_edges_checked'],
                       'audit':(BASE/f'finite_gap{g}.json').relative_to(ROOT).as_posix()})
    bundle={'name':'Combined independently audited RESTRICTED M3 certificate',
      'status':'PASS_RESTRICTED_DOMAIN_FULL_M3_INCOMPLETE','full_M3_complete':False,
      'domain':{'mu':'9-bit masks with exactly five marked cores','sigma':'ten integers0..266; at most one positive component',
                'signature_vectors':2661,'mask_signature_sectors':335286,'chi8':'both regions and entering paths'},
      'source_state':'(mu,b,alpha,sigma)','ordinary_raw_coordinate_count':147,'midpoint_raw_coordinate_count':127,
      'potential':{'O':'J-5*chi8','M':'-5*chi8','range':[-7,0],'low_table_range':[-2,0],
                   'decoder':(BASE/'candidate.py').relative_to(ROOT).as_posix(),'zero_support_table':'canonical gap0'},
      'weights':{'OO':'2H-q at actual terminal source','OM':'6-q','MO':0,'MM':'no edge'},
      'tables':tables,'dependencies':(BASE/'dependency_ledger.json').relative_to(ROOT).as_posix(),
      'universal_all_signature_consequence':'closed weight >= 2*N_H+P_L-D_L',
      'uncovered_obligation':'multiple positive gaps, N_H>=1, D_L>2*N_H+P_L, in both chi8 regions',
      'original_negative_cycle_certified':False,'source_and_interface_audit':(BASE/'actual_projected_product_audit_v2.json').relative_to(ROOT).as_posix(),
      'original_semantics_and_full_closure_audit':(BASE/'original_semantics_audit.json').relative_to(ROOT).as_posix(),
      'verdict':(BASE/'coverage_audit.json').relative_to(ROOT).as_posix(),'Bank25':25,'Stage04_run':False}
    write(BASE/'COMBINED_CERTIFICATE.json',bundle)
    integrity={'status':'PASS','prior_research_files_unchanged':len(baseline),'historical_pinned_files_checked':len(historical),
               'historical_manifests_checked':manifest_paths,'conflicting_pins':[],'hash_mismatches':[],
               'tracked_source_unchanged':not git('status','--porcelain','--untracked-files=no'),
               'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD')}
    assert integrity['tracked_source_unchanged'] and integrity['branch']=='coarse-double-branch' and integrity['HEAD']=='fea2a25b05e97f726b6e1891cebb12c4cfca821a'
    write(BASE/'integrity_audit.json',integrity)
    for row in baseline:assert sha(ROOT/row['path'])==row['sha256']
    old_names={r['path'] for r in baseline};prefix=BASE.relative_to(ROOT).as_posix()+'/'
    for p in subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).decode().split('\0'):
        if p and p not in old_names:assert p.startswith(prefix),p
    files=[{'path':p.relative_to(ROOT).as_posix(),'bytes':len(raw(p)),'sha256':sha(p)} for p in sorted(BASE.rglob('*')) if p.is_file()]
    manifest={'status':'AUDIT_COMPLETE_FULL_M3_OPEN_INCOMPLETE_COVERAGE','date_local':'2026-10-29 Asia/Karachi',
              'full_M3_pass':False,'restricted_certificate_pass':True,'integrity':integrity,
              'combined_audit':combined,'actual_Product_audit':projected,
              'dependency_graph':'acyclic; explicit OPEN multi-gap leaf',
              'source_proof_scope':'finite/original executable checks plus reviewed written structural reduction; not proof-assistant formalization',
              'no_new_sign_case_deleted_by_the_audit':True,'R1_R4_preserved':True,'h0_correction_preserved':True,
              'Bank25':25,'Stage04_run':False,'files_excluding_this_manifest':files}
    write(BASE/'final_manifest.json',manifest)
    print(json.dumps({'status':manifest['status'],'full_M3_pass':False,'restricted_certificate_pass':True,
                      'pinned_files_checked':333,'prior_research_unchanged':444,'actual_Product_nodes':projected['Product_DAG_nodes'],
                      'actual_projection_scopes_checked':22,'original_roots_replayed':240,'full_state_cycles':11,
                      'new_artifacts':len(files),'Bank25':25},indent=2))

if __name__=='__main__':main()
