"""Exact pointwise DAG apply; historical scalar engine remains intact."""
from pathlib import Path
source=Path(__file__).with_name('search_global_probe11_DAG.py').read_text()
source=source.replace('from probe11_decision_dag import DAG','from probe11_decision_dag import DAG\nfrom probe11_dag_apply import Apply')
old="processed,updates,maxd,tracking=(z[k] for k in ('processed','updates','max_D','tracking'));del z"
new="processed,updates,maxd,tracking=(z[k] for k in ('processed','updates','max_D','tracking'));functionupdates=z.get('function_updates',0);del z"
assert source.count(old)==1;source=source.replace(old,new)
old="densecells=imagecells=hits=0;cycle=None;limit=None"
new="densecells=imagecells=hits=0;cycle=None;limit=None;ap=Apply(dag);candidate_roots=collections.OrderedDict()"
assert source.count(old)==1;source=source.replace(old,new)
start=source.index('''        for x in range(1,12):
''',source.index('''    while todo'''))
end=source.index('''        processed+=1
''',start)
source=source[:start]+'''        for x in range(1,12):
            if x==g:continue
            bt=int(m['B_destination'][b,x-1]);q=int(m['B_Q'][b,x-1]);target=columns[bt];ck=(g,source,x,q);nt=len(classes[x-1])
            candidate_root=None
            if ck in candidate_roots:
                r=candidate_roots.pop(ck);candidate_roots[ck]=r
                if r<0 or r in dag.nodes:candidate_root=r
            if candidate_root is None:
                ik=(g,source,x)
                if ik in images:base=images.pop(ik);images[ik]=base
                else:
                    base=np.full(nt,-1000000,dtype=np.int32)
                    for h in (1,2):
                        data=groups[h,g,x];np.maximum.at(base,data[:,1],values[data[:,0]]-2*h)
                    images[ik]=base;imagecells+=nt
                    while imagecells>180000:
                        _,v=images.popitem(last=False);imagecells-=len(v)
                candidate=base+q;positive=np.flatnonzero(candidate>0)
                candidate_root=dag.changes(-1,1<<(nt-1).bit_length(),positive,candidate[positive])
                candidate_roots[ck]=candidate_root
                if len(candidate_roots)>20000:candidate_roots.popitem(last=False)
            result=ap.combine(target,candidate_root)
            if result==target:continue
            functionupdates+=1;maxd=max(maxd,ap.maximum(result))
            if maxd>8:tracking=True
            if tracking:
                before=get_values(x,target);after=get_values(x,result);changed=np.flatnonzero(after>before)
                for t in changed.tolist():
                    v=int(after[t]);options=[]
                    for h in (1,2):
                        data=groups[h,g,x];ok=(data[:,1]==t)&(values[data[:,0]]+q-2*h==v)
                        if np.any(ok):r=data[np.flatnonzero(ok)[0]];options.append((int(r[0]),h,int(r[2])))
                    assert options;s,h,y=options[0];code=bt*n+int(classes[x-1][t]);parents[code]=(b,s,h,x,y);trigger=code
            schedule(bt,result)
''' +source[end:]
source=source.replace("if len(dag.nodes)>500000:dag.collect(columns)","if len(dag.nodes)>400000:ap.collect(columns);candidate_roots.clear()")
source=source.replace("len(memo)+n+nb+m['stored_source_rows']","len(memo)+len(ap.cache)+len(ap.maxcache)+len(candidate_roots)+n+nb+m['stored_source_rows']")
source=source.replace("            dag.collect(columns)\n","            ap.collect(columns);candidate_roots.clear()\n")
source=source.replace("'processed':processed,'updates':updates,'max_D':maxd", "'processed':processed,'updates':updates,'function_updates':functionupdates,'update_counter_note':'updates retains earlier scalar coefficient count; function_updates counts later exact function merges','max_D':maxd")
source=source.replace("'numeric_merge_cache_hits':hits,","'numeric_merge_cache_hits':hits,'pointwise_apply_cache_hits':ap.hits,")
exec(compile(source,str(Path(__file__).resolve()),'exec'))
