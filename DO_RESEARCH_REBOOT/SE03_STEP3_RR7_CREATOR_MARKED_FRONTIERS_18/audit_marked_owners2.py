"""Fix the local decoder reference, preserving the failed implementation.
The prior failed source/CPU charges remain in the ledger. Save each new
owner input before further analysis so subsequent work can reuse it.
"""
from pathlib import Path
p=Path(__file__).with_name('audit_marked_owners.py')
source=p.read_text(encoding='utf-8').replace('V.unpack(', 'W.unpack(')
source=source.replace('r=V.one(c,z,True);M=',"r=V.one(c,z,True);W.out('marked_owner_input_'+str(z)+'.json',r);M=")
source=source.replace("'audit_marked_owners_exit.json'","'audit_marked_owners2_exit.json'")
exec(compile(source,str(p),'exec'))
