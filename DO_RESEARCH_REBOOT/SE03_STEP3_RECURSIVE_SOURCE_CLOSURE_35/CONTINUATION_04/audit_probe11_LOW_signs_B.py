"""Independent complete LOW sign check: sorted sparse reductions, not DAG apply.

All literal H1/H2 rows have the prior independent completeness receipt.
Only fixed candidate values are checked here; this never advances them.
"""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();BATCH=int(sys.argv[3]);PHASE=sys.argv[4]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    cp=F/'global_probe11_H3B_DAG_01.pkl';mp=F/'global_probe11_LOW_model.pkl'
    accepted=json.loads((F/'independent_global_probe11_LOW_model.json').read_text())
    assert accepted['input_sha256'][mp.name]==sha(mp)
    with mp.open('rb') as f:m=pickle.load(f)
    with cp.open('rb') as f:z=pickle.load(f)
    assert not z['pending'] and z['status']=='LOW_AND_ADDED_H3_SUBGRAPH_COMPLETE'
    nodes=z['nodes'];columns=z['columns'];roots=m['roots'];classes=m['classes']
    for i,(l,r) in nodes.items():
        assert (l<0 or l<i and l in nodes) and (r<0 or r<i and r in nodes) and not(l==r and l<0)
    assert len(set(nodes.values()))==len(nodes)
    pairs=collections.defaultdict(list)
    for b,(g,p) in enumerate(zip(roots,columns)):pairs[int(g),int(p)].append(b)
    work=sorted(pairs);sizes=[len(c) for c in classes];bounds={}
    def range_of(i,n,w):
        if i<0:return -i-1,-i-1
        if n==w:return bounds[i]
        l,r=nodes[i];h=w//2
        a=range_of(l,min(n,h),h)
        if n<=h:return a
        b=range_of(r,n-h,h);return min(a[0],b[0]),max(a[1],b[1])
    for i in sorted(nodes):
        l,r=nodes[i];a=(-l-1,-l-1) if l<0 else bounds[l];b=(-r-1,-r-1) if r<0 else bounds[r]
        bounds[i]=(min(a[0],b[0]),max(a[1],b[1]))
    rb={k:range_of(k[1],sizes[k[0]-1],1<<(sizes[k[0]-1]-1).bit_length()) for k in work}
    assert max(v[1] for v in rb.values())==z['max_D']==4
    bounds.clear()
    oldgroups=m.pop('groups');sortedrows={};tuples=0;targets=0
    for g in range(1,12):
        for x in range(1,12):
            if x==g:continue
            a=oldgroups.pop((1,g,x));b=oldgroups.pop((2,g,x))
            ss=np.concatenate((a[:,0],b[:,0]));tt=np.concatenate((a[:,1],b[:,1]))
            cc=np.concatenate((np.full(len(a),2,dtype=np.int8),np.full(len(b),4,dtype=np.int8)))
            order=np.argsort(tt,kind='stable');ss=ss[order];tt=tt[order];cc=cc[order]
            offsets=np.r_[0,np.flatnonzero(tt[1:]!=tt[:-1])+1];target=tt[offsets]
            sortedrows[g,x]=(ss,cc,offsets,target);tuples+=len(ss);targets+=len(target)
    assert not oldgroups and tuples==772616;del oldgroups,a,b,ss,tt,cc,order,offsets,target
    base_records=tuples+targets+len(nodes)+m['A_count']+m['B_count']+len(pairs)+len(work)
    assert base_records<1950000
    byte_limit=min(180000,1950000-base_records)
    cache=collections.OrderedDict();cells=0
    def dense(i,w):
        nonlocal cells
        if i<0:return bytes([-i-1])*w
        key=(i,w)
        if key in cache:
            v=cache.pop(key);cache[key]=v;return v
        l,r=nodes[i];h=w//2;v=dense(l,h)+dense(r,h)
        if w<=128:
            cache[key]=v;cells+=w
            while cells>byte_limit:
                _,old=cache.popitem(last=False);cells-=len(old)
        return v
    def values(g,p):
        n=sizes[g-1];return np.frombuffer(dense(p,1<<(n-1).bit_length()),dtype=np.uint8,count=n)
    position=0;checked_edges=checked_rows=envelope=0
    if BATCH>1:
        prior=json.loads((F/f'independent_probe11_LOW_B_{BATCH-1:02d}.json').read_text())
        assert prior['status']=='CHECKPOINT' and prior['candidate_sha256']==sha(cp)
        position=prior['next_group'];checked_edges=prior['checked_B_edges'];checked_rows=prior['checked_literal_inequalities'];envelope=prior['coarse_envelope_edges']
    failure=None
    while position<len(work) and time.process_time()-START<CAP-4:
        g,p=work[position];srcmax=rb[g,p][1];src=None
        for x in range(1,12):
            if x==g:continue
            need=[]
            for b in pairs[g,p]:
                bt=int(m['B_destination'][b,x-1]);q=int(m['B_Q'][b,x-1]);pt=int(columns[bt])
                if 2-q+rb[x,pt][0]-srcmax>=0:
                    checked_edges+=1;envelope+=1;continue
                need.append((b,bt,q,pt))
            if not need:continue
            if src is None:src=values(g,p).astype(np.int16)
            ss,price,off,tar=sortedrows[g,x]
            image=np.maximum.reduceat(src[ss]-price,off)
            for b,bt,q,pt in need:
                dest=values(x,pt);margin=dest[tar].astype(np.int16)-image-q
                j=int(margin.argmin());checked_rows+=len(ss);checked_edges+=1
                if int(margin[j])<0:
                    failure={'B_source':b,'B_target':bt,'KEEP':x,'signed_margin':int(margin[j]),'A_target_local':int(tar[j])}
                    break
            if failure:break
        if failure:break
        position+=1
    complete=position==len(work) and not failure
    if complete:assert checked_edges==587860
    r={'status':'PASS_ALL_COMPLETE_NATIVE11_LOW_INEQUALITIES' if complete else ('FAILED' if failure else 'CHECKPOINT'),
      'next_group':position,'total_groups':len(work),'checked_B_edges':checked_edges,
      'checked_literal_inequalities':checked_rows,'coarse_envelope_edges':envelope,'failure':failure,
      'source_rows':tuples,'target_groups':targets,'DAG_nodes':len(nodes),'base_live_records':base_records,
      'dense_cache_cells_cap':byte_limit,'candidate_sha256':sha(cp),'source_queries':0,'source_engine_calls':0,
      'comparison_formula':'D_new >= D_old+Q-2H on every independently complete H1/H2 row',
      'JR35':'OPEN','scope':'fixed eleven ordered anchors; no arbitrary-support promotion',
      'input_sha256':{p.name:sha(p) for p in (cp,mp,F/'independent_global_probe11_LOW_model.json')}}
    with (F/f'independent_probe11_LOW_B_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(r,f,indent=2)
    print(json.dumps(r),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
