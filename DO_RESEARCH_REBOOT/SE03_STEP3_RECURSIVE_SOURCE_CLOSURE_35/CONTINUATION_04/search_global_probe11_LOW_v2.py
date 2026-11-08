"""Derive exact numerical image/result memoization; retain original code."""
from pathlib import Path
source=Path(__file__).with_name('search_global_probe11_LOW.py').read_text()
old='''    cycle=None;limit=None
'''
new='''    cycle=None;limit=None
    images=collections.OrderedDict();imagecells=0;memo=collections.OrderedDict();image_hits=result_hits=0
    def assign_profile(b,pid):
        nonlocal cells
        old=columns[b]
        if old==pid:return
        refs[pid]+=1;columns[b]=pid;refs[old]-=1
        if refs[old]==0:
            keyold=profiles.pop(old);del intern[keyold];del refs[old];cells-=len(keyold[1])
'''
assert source.count(old)==1;source=source.replace(old,new)
start=source.index('''        for x in range(1,12):
''',source.index('''    while todo'''))
end=source.index('''        processed+=1
''',start)
source=source[:start]+'''        sourcepid=columns[b]
        for x in range(1,12):
            if x==g:continue
            bt=int(m['B_destination'][b,x-1]);q=int(m['B_Q'][b,x-1]);targetpid=columns[bt];mk=(sourcepid,targetpid,x,q)
            if not tracking and mk in memo:
                pid=memo.pop(mk);memo[mk]=pid
                if pid in profiles:assign_profile(bt,pid);result_hits+=1;continue
            ik=(sourcepid,x);nt=len(classes[x-1])
            if ik in images:
                base=images.pop(ik);images[ik]=base;image_hits+=1
            else:
                base=np.full(nt,-1000000,dtype=np.int32)
                for h in (1,2):
                    data=groups[h,g,x];np.maximum.at(base,data[:,1],values[data[:,0]]-2*h)
                images[ik]=base;imagecells+=nt
                while imagecells>300000:
                    _,v=images.popitem(last=False);imagecells-=len(v)
            vv=base+q;target=dict(profiles[targetpid][1]);changed=False
            for t in np.flatnonzero(vv>0):
                t=int(t);v=int(vv[t])
                if v<=target.get(t,0):continue
                target[t]=v;changed=True;updates+=1
                if v>maxd:maxd=v
                if maxd>8:tracking=True
                if tracking:
                    choices=[]
                    for h in (1,2):
                        data=groups[h,g,x];mask=(data[:,1]==t)&(values[data[:,0]]+q-2*h==v)
                        if np.any(mask):
                            row=data[np.flatnonzero(mask)[0]];choices.append((int(row[0]),h,int(row[2])))
                    assert choices;s,h,y=choices[0];code=bt*n+int(classes[x-1][t])
                    if code not in parents:parentcells+=1
                    parents[code]=(b,s,h,x,y);trigger=code
            if changed:
                replace(bt,target)
                if not inq[bt]:inq[bt]=1;todo.append(bt)
            if not tracking:
                memo[mk]=columns[bt]
                if len(memo)>20000:memo.popitem(last=False)
            if cells+len(profiles)+n+nb+imagecells+len(memo)>1850000 or parentcells>3900000:limit='RECORD_CAP_CHECKPOINT';break
''' + source[end:]
old="'proof_from_passing_finite_population_search':False,'parents_omitted_before_trigger_does_not_bound_potential':True}"
new="'proof_from_passing_finite_population_search':False,'parents_omitted_before_trigger_does_not_bound_potential':True,'image_cache_hits':image_hits,'result_cache_hits':result_hits,'derived_image_cells':imagecells}"
assert source.count(old)==1;source=source.replace(old,new)
exec(compile(source,str(Path(__file__).resolve()),'exec'))
