"""Metadata-only publication. No source operation or old audit rerun."""
import json,time,hashlib,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;START=time.process_time()
def rd(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    entry=rd(B/'entry.json');pins=rd(B/'dependency_pins.json')
    for p in pins['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==entry['head']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()==entry['branch']
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
    expected={'endpoint_obstruction_independent_audit.json':'PASS_GAMMA55_SOURCE_AND_ALL_MATCHING_ENDPOINT_OBSTRUCTION',
              'static_owner_independent_audit.json':'PASS_GAMMA55_STATIC_OWNER_EXTENSION',
              'burst_sharp_independent_audit.json':'PASS_ALL_MATCHING_B_REPLAY_LOWER_BOUND'}
    for n,status in expected.items():
        d=rd(B/n);assert d['status']==status
        for f,h in d['input_sha256'].items():assert sha(B/f)==h
    assert not (B/'FULL_PROOF.md').exists() and not (B/'SOURCE_FORCED_UNIVERSAL_FUNDING_LEMMA.md').exists()
    phases=[];total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=entry['inherited_conservative_queries']
    for p in sorted(B.glob('run_*_result.json')):
        r=rd(p);c=rd(B/('controller_'+r['phase']+'_exit.json'));charge=r['child_CPU']+c['whole_process_CPU_seconds']
        total+=charge;groups[r['group']]+=charge;queries+=r['source_queries']
        assert r['source_queries']<=r['allocated_query_cap']<=50000
        phases.append(dict(r,controller_CPU=c['whole_process_CPU_seconds'],total_charge=charge))
    assert total<7200 and groups['symbolic']<240 and groups['independent']<600 and queries<=3000000
    out('resources_checkpoint.json',{'status':'CUMULATIVE_NO_RESET','cumulative_CPU':total,'global_cap':7200,'global_remaining':7200-total,
        'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],'group_remaining':{k:entry['group_caps'][k]-v for k,v in groups.items()},
        'conservative_all_queries':queries,'query_limit':3000000,'conservative_remaining_queries':3000000-queries,
        'new_source_queries':queries-entry['inherited_conservative_queries'],'per_batch_query_limit':50000,'phases':phases,
        'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,'memory_limit_bytes':32*1024**3,
        'wall_limit_hours':12,'global_reserve':5,'controller_reserve':1,'all_child_controller_charges_preserved':True,
        'metadata_CPU_excluded_under_inherited_convention':{'entry':entry['metadata_CPU_excluded'],'publication_before_manifest':time.process_time()-START},
        'resource_limit_hit':False,'principal_U33':'OPEN','U33_EP':'REFUTED','Gate_U':'OPEN'})
    out('U33_RESULT_CERTIFICATE.json',{'principal_U33':'UNRESOLVED','terminal_outcome_for_principal':'UNRESOLVED_UNIVERSAL_SOURCE_BRIDGE_OPEN',
        'completed_submechanism_outcome':'E_U33_EP_REFUTED','failed_assertion':'uniform full matching with all-original-event endpoint bank<=25',
        'new_universal_negative_theorem':'every B replay with q demands forces all-matching endpoint peak>=ceil(q/2)',
        'exact_source':'Gamma55_original_source.json','r':55,'period':[223,444],'q_at_333':54,'minimum_full_and_common_endpoint_peak':27,
        'scalar_margin':332,'static_owner_extension_complete':True,'old_values_preserved':322,'new_payments':2,'full_demands':324,
        'original_GateU14_working_architecture_refuted':False,'new_universal_source_funding_proved':False,
        'normalized_I54_receipt_fabricated':False,'independent_implementation_checks':'PASS_SAME_AGENT','external_or_formal_verification':False,
        'branch':entry['branch'],'head':entry['head'],'tracked_clean':True,'inherited_pins_preserved':len(pins['pins']),
        'Gate_U':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
    files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    out('campaign_manifest.json',{'files':files,'principal_status':'OPEN','completed_negative_theorem':'U33-EP','branch':entry['branch'],'head':entry['head']})
    out('publication_seal.json',{'manifest_sha256':sha(B/'campaign_manifest.json'),'files':len(files),'inherited_pins':len(pins['pins']),
        'principal_U33_closed':False,'U33_EP_countercertificate_complete':True,'checks':'separate same-agent implementations PASS','external_or_formal_audit':False})
    print(json.dumps({'status':'U33_NEGATIVE_RESULT_PUBLISHED_PRINCIPAL_OPEN','files':len(files),'CPU':total,'groups':groups,'queries':queries,'remaining_queries':3000000-queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('publication_exit.json',{'metadata_CPU_excluded':time.process_time()-START,'error':error})
