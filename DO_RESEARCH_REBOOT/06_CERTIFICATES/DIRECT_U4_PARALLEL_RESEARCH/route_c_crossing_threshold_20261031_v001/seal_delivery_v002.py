"""Append-only correction of two source links, followed by final sealing."""
from pathlib import Path
import hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def save(name,v):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def prose(name,value):
    with (OUT/name).open('x',encoding='utf-8') as f:f.write(value)
def main():
    oldproof='CT01_STRUCTURAL_DEFINITION_AND_DELETE.md';newproof='CT01_STRUCTURAL_DEFINITION_AND_DELETE_v002.md'
    oldreport='CT04_FINAL_REPORT.md';newreport='CT04_FINAL_REPORT_v002.md'
    text=(OUT/oldproof).read_text(encoding='utf-8')
    assert text.count('../../../../../python/')==2
    prose(newproof,text.replace('../../../../../python/','../../../../python/'))
    text=(OUT/oldreport).read_text(encoding='utf-8').replace('('+oldproof+')','('+newproof+')').replace('(proof_status_ledger.json)','(proof_status_ledger_v002.json)')
    prose(newreport,text)
    prose('CT06_DELIVERY_LINK_ERRATUM.md',
      '# Source link correction and preserved first seal\n\n'
      'The first delivery seal stopped on two relative source links in CT01: each climbed one directory too far. '
      'It had already written proof_status_ledger.json; it wrote no final integrity or delivery manifest. '
      'The source and mathematical checks passed before that link assertion. No mathematical statement, source datum or certificate changed.\n\n'
      'Append-only handling preserves the original report, proof, ledger and failed seal script. '
      'The active [proof](CT01_STRUCTURAL_DEFINITION_AND_DELETE_v002.md) corrects both links; the active '
      '[final report](CT04_FINAL_REPORT_v002.md) points to it and to [the versioned ledger](proof_status_ledger_v002.json). '
      'The corrected [seal](seal_delivery_v002.py) records the two archived broken links explicitly and verifies all active links. '
      'The independent source certificate and its PASS audit are unchanged.\n')
    ledger=read('proof_status_ledger.json')
    for row in ledger['results']:
        if row.get('proof')==oldproof:row['proof']=newproof
    ledger['delivery_link_erratum']='CT06_DELIVERY_LINK_ERRATUM.md'
    save('proof_status_ledger_v002.json',ledger)
    e=read('entry_source_pins.json');a=read('independent_audit.json');c=read('crossing_certificate.json')
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'crossing_certificate.json')
    assert sha(OUT/'CT00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert now==sorted(e['stage11g_all_files']) and not changed
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    links=0;archived=[]
    for p in OUT.glob('CT*.md'):
        text=p.read_text(encoding='utf-8');assert '\ufffd' not in text and text.endswith('\n')
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if target.startswith(('http://','https://')):continue
            if target=='final_integrity.json':continue
            if p.name==oldproof and target.startswith('../../../../../python/'):
                assert (OUT/target.replace('../../../../../python/','../../../../python/')).resolve().is_file()
                archived.append({'file':p.name,'old_link':target,'corrected_in':newproof});continue
            assert (OUT/target).resolve().is_file(),(p.name,target)
            links+=1
    assert len(archived)==2
    result={'status':'PASS','date':'2026-10-31','source_pins_checked':len(e['files']),'changed_pins':changed,
      'stage11g_files_checked':len(now),'stage11g_file_inventory_unchanged':True,'stage11g_all_pinned_bytes_unchanged':True,
      'head':head,'branch':branch,'tracked_modifications':tracked,'head_and_branch_preserved':True,
      'old_reports_and_certificates_overwritten':False,'write_scope':OUT.relative_to(ROOT).as_posix(),
      'independent_source_and_chord_audit':'PASS','written_gate_preserved':True,'report_links_checked':links,
      'archived_link_errors_corrected_by_versioning':archived,'active_final_report':newreport,'active_proof_status_ledger':'proof_status_ledger_v002.json',
      'finite_potential_fits':0,'larger_fits':0,'new_pair_state_graphs':0,'single_tree_connector':c['connector'],
      'new_threshold_candidates_after_failure':0,'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,'exclusion':'self hash excluded','final_report':newreport})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'active_report_links_verified':links,'archived_link_errors_versioned':len(archived),
      'delivery_files_hashed':len(files),'final_report':newreport},indent=2))
if __name__=='__main__':main()
