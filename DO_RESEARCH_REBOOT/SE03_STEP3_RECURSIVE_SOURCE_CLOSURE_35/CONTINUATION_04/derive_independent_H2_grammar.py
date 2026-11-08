"""Create a separate support-parameterized copy of the accepted C14 grammar.
Only metadata/code editing here; source derivations run in audit phases.
"""
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
source=(P/'SE03_STEP2_UNARY_A_LIFT_14/branch_frames2.py').read_text()
start=source.index("s=importlib.util.spec_from_file_location")
end=source.index('@functools.lru_cache',start)
header='''from cached_low_frames import Frames
M=set(range(1000,8000,1000));calls=0;A_START=0;A_END=5947
class CachedSource:
    def __init__(self):
        root=B.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
        self.frames=Frames(root/'native10_source_actions.json')
    def path(self,t,x):return ''.join('L' if c==1 else 'R' for c in self.frames.path(t,x))
    def core(self,t,marks):
        if not isinstance(t,tuple):return None
        l=self.core(t[1],marks);r=self.core(t[2],marks)
        return (t[0],l,r) if t[0] in marks or l is not None or r is not None else None
    def trace(self,t,x):
        # Cached WHOLE-action term substitution. These operand dictionaries
        # are grammar metadata, not fabricated physical source event rows.
        path=self.frames.path(t,x);after,h=self.frames.apply(t,x)
        if h==1:
            event={'G':t[0] if len(path)==2 else None,
                   'P':t[path[0]][0] if len(path)==2 else t[0],'target':x}
            return after,None,[event]
        return after,None,[{} for _ in range(h)]
p=CachedSource()
'''
source=source[:start]+header+source[end:]
assert source.count('family(1,6)')==1;source=source.replace('family(1,6)','family(1,7)')
assert source.count('lo,hi=0,7000')==1;source=source.replace('lo,hi=0,7000','lo,hi=0,8000')
assert source.count('assert len(aa)==974')==1;source=source.replace('assert len(aa)==974','assert len(aa)==5947')
assert source.count('for a,raw in enumerate(aa):')==1
source=source.replace('for a,raw in enumerate(aa):','for a in range(A_START,A_END):\n        raw=aa[a]')
source=source.replace("'source_engine_calls':calls", "'cached_source_identity_substitutions':calls")
with (F/'independent_H2_grammar.py').open('x',encoding='utf-8') as f:f.write(source)
print('SEPARATE_C14_GRAMMAR_CREATED_WITH_CACHE_BINDING_AND_SEVEN_MARKS')
