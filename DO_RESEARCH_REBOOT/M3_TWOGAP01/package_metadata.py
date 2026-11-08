import json
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_TWOGAP01')
c=json.loads((BASE/'relation.json').read_text());b=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
obj={'status':'CONSTRUCTED_PENDING_INDEPENDENT_CERTIFICATION','classes':c['classes'],'shadows':c['shadows'],
  'B_trees':[r['tree'] for r in b['nodes']],'psi':[r['psi'] for r in b['nodes']],
  'signature':[1,1]+[0]*8,'mask_scope':'all126 legal five-bit masks','regions':'both chi8 regions',
  'default':'-psi(B)','shared_normalization':'raw alpha7 with unused fields and coarse kinds normalized; no S filling',
  'high_correction':'W(O)=J(O)-5*chi8(O.b); W(M)=-5*chi8(M.b)',
  'independent_certification_complete':False,'full_M3_proved':False}
with (BASE/'decoder_metadata.json').open('x',encoding='utf-8') as f:json.dump(obj,f,separators=(',',':'))
print(json.dumps({'status':obj['status'],'classes':c['classes']}),flush=True)
