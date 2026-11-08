from pathlib import Path
import sys
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/analyze_saved_hybrid_source_relations.py'
s=p.read_text();a=s.index('    sources=[];pins=[]');b=s.index('    reports=[]',a)
s=s[:a]+"""    p=F/'C20_hybrid_source_control.json'
    data=json.loads(p.read_text())
    pins=[p]
    sources=[('C20_SATURATED',data['period_rows'],'new full A/B source replay; independent check pending')]
"""+s[b:]
s=s.replace("F/'saved_hybrid_source_relations.json'","F/'C20_hybrid_source_relations.json'")
sys.argv.append('proof273');globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
