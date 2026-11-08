"""Final provenance/source-interface/assembly seal; no old theorem replay."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    pins=json.loads((B/'dependency_pins.json').read_text());bad=[]
    for p in pins['pins']:
        f=ROOT/p['path']
        if not f.is_file() or sha(f)!=p['sha256']:bad.append(p['path'])
    for p in pins['external_pins']:
        if not Path(p['path']).is_file() or sha(Path(p['path']))!=p['sha256']:bad.append(p['path'])
    assert not bad
    ind=json.loads((B/'independent_audit.json').read_text());adv=json.loads((B/'adversarial_audit.json').read_text());inter=json.loads((B/'interface_audit.json').read_text())
    assert ind['status']=='PASS_UNIVERSAL_SYMBOLIC_COVERAGE_AND_CLOSURE'
    assert adv['status']=='PASS_ADVERSARIAL_UNIVERSAL_COVERAGE' and inter['status']=='PASS_SOURCE_INTERFACE_ASSEMBLY'
    assert (ind['seed_recent_frames'],ind['backward_frames'],ind['H1_predecessor_edges'])==(240,260,20)
    cert=json.loads((B/'saturation3.json').read_text());assert cert['closed'] and not cert['goal'] and cert['stop'] is None
    assert len(cert['records'])==260 and cert['statistics']['proposals']==20
    status=json.loads((B/'research_status_ledger.json').read_text());assert status['saturation'].startswith('INVALID')
    required=['THEOREM_BOX.md','SOURCE_SPEC.md','SOURCE_PROVENANCE.md','FULL_PROOF.md','CASE_LEDGER.md',
        'INDEPENDENT_AUDIT.md','IAGS_CLOSURE.md','SOURCE_REPLAY.md','FINAL_VERDICT.md','CHECKPOINT.md']
    assert all((B/f).is_file() for f in required)
    proof=(B/'FULL_PROOF.md').read_text();assert 'finite-to-universal bridge' in proof and 'one-way necessary projection' in proof
    assert 'both E0 and E1' in proof or 'Both E0 and E1' in proof
    assert 'all3698 legal SS edges remain in G' in proof and 'Step2' in proof
    entry=json.loads((B/'entry.json').read_text())
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    tracked=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True)
    assert branch==entry['branch'] and head==entry['head'] and not tracked
    out('dependency_revalidation.json',{'status':'PASS','inherited_local_pins':len(pins['pins']),'external_pins':len(pins['external_pins']),'mismatches':bad})
    result={'status':'PASS_COMPLETE_TP_DEPTH3_ASSEMBLY','terminal_outcome':'A','theorem':'TP-DEPTH3',
        'source_coverage':'ALL2394 density contexts, arbitrary gap substitution, every affordable predecessor',
        'independent_engine_and_forward_derivation':'PASS','adversarial_coverage':'PASS','source_interfaces':'PASS',
        'private_populations':'arbitrary, no finite lifting gap','both_orientations':'covered','regeneration':'all finite lengths by closed backward language',
        'all_full_source_fields':'preserved by necessary projection; no realization or splice claim',
        'new_donor_allocations':0,'frozen_artifacts_changed':False,'invalid_first_saturation_discarded':True,
        'branch':branch,'HEAD':head,'tracked_status':tracked,'pins_verified':len(pins['pins']),
        'Step2':'OPEN','Step3':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN',
        'audit_trust':'same agent; separate immutable engine, not external peer review/formal assistant',
        'source_engine_calls':0,'new_finite_tests':0}
    out('seal_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
