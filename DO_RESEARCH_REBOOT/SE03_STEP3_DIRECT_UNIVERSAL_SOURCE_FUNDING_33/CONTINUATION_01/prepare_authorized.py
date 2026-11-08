"""Metadata-only cap amendment; all prior phase charges remain cumulative."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent
e=json.loads((B/'entry.json').read_text());e['group_caps']['symbolic']=480;e['resource_amendment']='resource_amendment.json'
with (B/'entry_authorized.json').open('x') as f:json.dump(e,f,indent=2)
with (B/'run_phase_authorized.py').open('x') as f:f.write((B/'run_phase.py').read_text().replace("entry.json","entry_authorized.json"))
print('Authorized symbolic cap480; cumulative usage and all other caps preserved.')
