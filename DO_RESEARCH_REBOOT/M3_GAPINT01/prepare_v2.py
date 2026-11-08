from pathlib import Path
p=Path('DO_RESEARCH_REBOOT/M3_GAPINT01/framework.py');q=p.with_name('framework_v2.py');assert not q.exists();s=p.read_text()
needle="    cache=tr.cache_info();tr.cache_clear();wid.clear()"
assert needle in s
s=s.replace(needle,needle+"\n    with (folder/'A_profiles_v2.json').open('x',encoding='utf-8') as f:json.dump({'gap':g,'models':models,'queries':queries,'shadows':sh,'low_options':opts,'witnesses':witnesses},f)\n    print(json.dumps({'gap':g,'models':models,'source_queries':queries,'shadow_classes':len(sh)}),flush=True)")
s=s.replace("cnt=Counter();safe=0","cnt=Counter();safe=0;debt_safe=Counter()")
needle="            if w>=2:safe+=1;continue"
assert needle in s
s=s.replace(needle,needle+"\n            if (w==1 and psi[bj]>=1) or (w==0 and psi[bj]==2):debt_safe[w]+=1;continue")
s=s.replace("'range_safe':safe,'cpu_seconds'","'range_safe':safe,'debt_safe':dict(debt_safe),'cpu_seconds'")
with q.open('x',encoding='utf-8') as f:f.write(s)
q=p.with_name('build_v2.py');assert not q.exists();s=p.with_name('build.py').read_text().replace('from framework import','from framework_v2 import')
with q.open('x',encoding='utf-8') as f:f.write(s)
print({'version2_prepared':True})
