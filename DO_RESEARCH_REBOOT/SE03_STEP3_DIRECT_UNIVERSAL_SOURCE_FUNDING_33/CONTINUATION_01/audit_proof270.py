from pathlib import Path
import sys
p=Path(__file__).resolve().parents[2]/'SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/search_FP_access_countercut.py'
s=p.read_text()
s=s.replace("if a in seen:lo=seen[a];break\n            seen[a]=len(keys)",
 """if a in seen and 16<=len(keys)-seen[a]<=160 and len(set(keys[seen[a]:]))>=7:
                lo=seen[a];break
            if a not in seen or len(keys)-seen[a]>160:seen[a]=len(keys)""")
sys.argv.extend(['proof270','2'])
globals()['__file__']=str(p)
exec(compile(s,str(p),'exec'))
