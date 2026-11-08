"""Metadata-only bounded source phase declarations; inherited caps unchanged."""
import json
from pathlib import Path
B=Path(__file__).resolve().parent;e=json.loads((B/'entry_authorized.json').read_text())
e['phase_query_caps'].update(core=50000,verify=50000);e['phase_caps'].update(core=20,verify=90)
with (B/'entry_research.json').open('x') as f:json.dump(e,f,indent=2)
with (B/'run_phase_research.py').open('x') as f:f.write((B/'run_phase.py').read_text().replace("entry.json","entry_research.json"))
print('Source phases declared within unchanged50k batches and cumulative3M limit.')
