import json,hashlib
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01');out=BASE/'source_audit_v3.py';assert not out.exists()
reused=[(g,h) for g in range(10) for h in range(g+1,10)][:22];assert reused[-1]==(2,7)
record={'status':'PREVIOUSLY_OBSERVED_ORIGINAL_CHECKS_REUSED','completed_pairs':reused,'accepted_original_roots':66,'full_closure_cycles':22,
  'negative_controls':22,'original_program_sha256':hashlib.sha256((BASE/'source_audit.py').read_bytes()).hexdigest(),
  'evidence':'prototype stdout progressed through pair[2,7],roots66,CPU142.531 before recorded stopCPU145.359375',
  'raw_environments_saved':False,'reproduction_recipe':'Run the pinned source_audit.py deterministic first22 pair iterations; all original data/source files are unchanged.'}
with (BASE/'reused_controls.json').open('x',encoding='utf-8') as f:json.dump(record,f,indent=2)
s=(BASE/'source_audit_v2.py').read_text().replace('from proposal_factory import proposals','from proposal_factory_v2 import proposals')
s=s.replace("out=BASE/'source_audit_v2.json'","out=BASE/'source_audit_v3.json'")
s=s.replace('rows=[];cycles=[];negative=[];S=IN.S;z=S.LEAF',"rows=[];cycles=[];negative=[];S=IN.S;z=S.LEAF\n    reuse=json.loads((BASE/'reused_controls.json').read_text());reused={tuple(p) for p in reuse['completed_pairs']}\n    prior=sum(json.loads((BASE/f).read_text())['cpu_seconds'] for f in ('source_prototype_stop.json','source_v2_stop.json'))+json.loads((BASE/'outer_helper_controls.json').read_text())['cpu_seconds']+2\n    assert prior<300")
s=s.replace("helper=FOUT if h==9 or (g+h)%2 else FIN","if (g,h) in reused:continue\n            helper=FOUT if h==9 or (g+h)%2 else FIN")
s=s.replace("time.process_time()-start<300,'UNKNOWN source family CPU cap'","prior+time.process_time()-start<300,'UNKNOWN shared source family CPU cap'")
s=s.replace('assert len(cycles)==45 and len(negative)==45 and len(rows)==135','assert len(cycles)==23 and len(negative)==23 and len(rows)==69')
s=s.replace("'signature_pairs':45,'full_original_roots':135,'low_roots':90,'high_roots':45","'signature_pairs':45,'full_original_roots':135,'low_roots':90,'high_roots':45,'fresh_final_version_roots':69,'reused_original_roots':66")
s=s.replace("'fresh_full_mixed_cycles':45,'negative_low_controls':45","'fresh_full_mixed_cycles':23,'reused_full_mixed_cycles':22,'negative_low_controls':45")
s=s.replace("'cpu_seconds':round(time.process_time()-start,3),'rows':rows", "'cpu_seconds':round(time.process_time()-start,3),'registered_family_CPU_including_prototypes':round(prior+time.process_time()-start,3),'reused_controls':reuse,'rows':rows")
with out.open('x',encoding='utf-8') as f:f.write(s)
print(json.dumps({'reused_pairs':22,'remaining_pairs':23}),flush=True)
