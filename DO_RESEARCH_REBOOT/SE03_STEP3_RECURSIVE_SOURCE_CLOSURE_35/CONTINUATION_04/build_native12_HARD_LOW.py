"""Reuse complete unchanged root/target groups; construct only the new ones."""
from pathlib import Path
p=Path(__file__).with_name('build_native12_fixed_LOW.py');s=p.read_text()
s=s.replace('native12_fixed_B_word.json','native12_hard_B_word.json')
s=s.replace('native12_LOW_build_','native12_HARD_LOW_build_')
old="if BATCH==1:z={'g':1,'next_s':0,'groups':{},'partial':{},'source_substitutions':0,'source_queries':0}"
new="""if BATCH==1:
        with (F/'native12_LOW_build_01.pkl').open('rb') as f:prior=pickle.load(f)
        previous=json.loads((F/'native12_fixed_B_word.json').read_text())
        reused={g:a for g,a in prior['groups'].items() if previous['next_key_by_root'][str(g)]==nextkey[g]}
        z={'g':1,'next_s':0,'groups':reused,'partial':{},'source_substitutions':0,'source_queries':0}
        del prior
"""
assert s.count(old)==1;s=s.replace(old,new)
old="        x=nextkey[g];s=max(s,offset[g-1]);stop=offset[g]"
new="""        if g in groups:
            g+=1;s=offset[g-1] if g<=12 else N
            continue
        x=nextkey[g];s=max(s,offset[g-1]);stop=offset[g]"""
assert s.count(old)==1;s=s.replace(old,new)
exec(compile(s,str(Path(__file__).resolve()),'exec'))
