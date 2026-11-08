"""Independent profile regeneration and row audit for one registered signature."""
import sys,json,time,hashlib
from pathlib import Path
from itertools import product
from collections import Counter
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01')
import reference as R
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01');CORE=set(16*i for i in range(9))
def independent_prefixes(g,h,helper,word):
    original=R.universe();t=original;required={()};types={():None}
    for j,p in enumerate(word):
        for i in range(len(p)+1):required.add(R.at(t,p[:i])[0])
        k=R.at(t,p)[0];types[k]=16*helper-8 if j<len(word)-1 else None;t=R.splay(t,k)
    observed=set(R.SHADOW)|{R.at(t,p)[0] for p in R.SHADOW};oldroot=R.find(t,());observed.update(n[0] for n in oldroot[1:] if R.real(n));observed|=required
    for p in tuple(observed):observed.update(p[:i] for i in range(len(p)))
    universe=tuple(sorted(CORE|{16*g-8,16*h-8}))
    def fill(p,values):
        if p not in observed:
            yield None;return
        if p not in required:
            yield None
            if not CORE.intersection(values):yield R.GHOST
        for i,x in enumerate(values):
            if p in types:
                if types[p] is None and x not in CORE:continue
                if types[p] is not None and x!=types[p]:continue
            for left in fill(p+(0,),values[:i]):
                for right in fill(p+(1,),values[i+1:]):yield (x,left,right)
    return fill((),universe)
def reflect_alpha(a):
    return tuple((kind,iss,8-k if iss and kind==0 else k) for p in (0,2,1,6,5,4,3) for kind,iss,k in [a[p]])
def main():
    g,h=map(int,sys.argv[1:3]);folder=BASE/f'p{g}_{h}';out=folder/'audit.json';assert not out.exists();start=time.process_time()
    c=json.loads((folder/'relation.json').read_text());p=json.loads((folder/'potential.json').read_text());B=json.loads((BASE/'B_bank.json').read_text());assert B['status']=='INDEPENDENT_B_BANK_PASS'
    N=c['classes'];sid={R.frozen(a):i for i,a in enumerate(c['shadows'])};assert len(sid)==N
    expected={};num=0
    for a,options in enumerate(c['options']):
        for H,x,aa,helper,family,code in options:
            key=(a,H,x,aa,helper);assert key not in expected;expected[key]=num;num+=1
            assert c['families'][family]['helper']==helper and len(c['families'][family]['word'])==H
    assert num==c['option_count'];matched=bytearray(num);queries=0;families=[]
    words=[(None,(p,)) for p in R.PATHS]
    for helper in (g,h):
        if helper in (0,9):words.extend((helper,(p,q)) for p,q in product(R.PATHS,repeat=2))
    for helper,word in words:
        number=0
        for t in independent_prefixes(g,h,helper,word):
            owner=t[0];sa=R.observations(t,owner)
            for path in word:t=R.splay(t,R.at(t,path)[0])
            ta=R.observations(t,owner);key=(sid[sa],len(word),t[0]//16,sid[ta],helper);matched[expected[key]]=1;number+=1;queries+=1
            if queries%8192==0:assert queries<=1000000 and time.process_time()-start<120,'UNKNOWN independent profile cap'
        if number:families.append({'helper':helper,'word':[list(p) for p in word],'count':number})
    assert queries==c['queries'] and sum(matched)==num
    assert families==c['families'];del matched,expected
    psi=B['psi'];values={int(k):v for k,v in p['values'].items()};byroot={r:[] for r in range(9)}
    for a,s in enumerate(c['shadows']):byroot[s[0][2]].append(a)
    for k,v in values.items():
        b,a=divmod(k,N);assert c['shadows'][a][0][2]==B['trees'][b][0] and -2<=v<=-psi[b]
    checked=states=zero=0;residual=Counter();automatic=Counter()
    for b,t in enumerate(B['trees']):
        for a in byroot[t[0]]:
            states+=1;du=values.get(b*N+a,-psi[b])
            if du==0:zero+=1;continue
            for H,x,aa,helper,fi,code in c['options'][a]:
                if H==1:
                    dep=B['depths'][b][x]
                    if dep==0:automatic['nongenuine']+=1;continue
                    bb=B['destinations'][b][x];w=2-dep//2
                else:
                    pair=B['kernels'][str(helper)][b][x]
                    if pair is None:automatic['nonchildless_exit']+=1;continue
                    bb,w=pair
                if w>=2:automatic['range']+=1;continue
                v=values.get(bb*N+aa,-psi[bb]);r=w-v+du;assert r>=0,(g,h,b,a,H,x,helper,du,v,w);residual[r]+=1;checked+=1
        assert time.process_time()-start<120,'UNKNOWN independent residual CPU cap'
    for b in range(4862):
        for x in range(9):
            w=2-B['depths'][b][x]//2
            if w<0:assert -psi[B['destinations'][b][x]]<=w
    assert all(pair is None or pair[1]>=0 for kernel in B['kernels'].values() for row in kernel for pair in row)
    symmetry=0
    if g+h==9:
        reflected=[]
        for a in c['shadows']:
            ra=reflect_alpha(a);assert reflect_alpha(ra)==R.frozen(a);reflected.append(sid[ra])
        for k,v in values.items():
            b,a=divmod(k,N);bb=B['mirror'][b];v2=values.get(bb*N+reflected[a],-psi[bb]);assert v2==v;symmetry+=1
    report={'status':'INDEPENDENT_FINITE_EXACT_PASS','g':g,'h':h,'profile_queries':queries,'classes':N,'access_options':num,
      'all_profiles_regenerated':True,'changed_states':len(values),'J_range':[-2,0],'explicit_residuals':checked,'minimum_residual':min(residual),
      'residual_histogram':dict(residual),'product_states_streamed':states,'zero_source_states_discharged':zero,
      'analytic':dict(automatic),'self_reflection_entries_checked':symmetry,'cpu_seconds':round(time.process_time()-start,3),
      'potential_sha256':hashlib.sha256((folder/'potential.json').read_bytes()).hexdigest(),'source_family_audit_pending':True,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
