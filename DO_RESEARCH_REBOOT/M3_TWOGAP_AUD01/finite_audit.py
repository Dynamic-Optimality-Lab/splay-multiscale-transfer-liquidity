"""Independent exact regeneration; no TWOGAP01 Python imports."""
import json,time,hashlib
from pathlib import Path
from collections import deque,Counter
from itertools import product
import reference as R
BASE=Path('DO_RESEARCH_REBOOT/M3_TWOGAP_AUD01');OLD=Path('DO_RESEARCH_REBOOT/M3_TWOGAP01')
def main():
    out=BASE/'finite_audit.json';assert not out.exists();start=time.process_time();queries=0
    c=json.loads((OLD/'relation.json').read_text());N=c['classes'];sid={R.frozen(a):i for i,a in enumerate(c['shadows'])}
    assert len(sid)==N==29397
    expected={};count=0
    for a,options in enumerate(c['options']):
        for o in options:
            key=(a,o['H'],o['target'],o['destination']);assert key not in expected;expected[key]=count;count+=1
            w=c['witnesses'][o['witness']];t=R.tree(w['tree']);owner=t[0];assert R.observations(t,owner)==R.frozen(c['shadows'][a])
            targets=[]
            for p in w['paths']:
                x=R.at(t,p)[0];targets.append(x);t=R.splay(t,x)
            assert targets==w['targets'] and targets[-1]//16==o['target'] and len(targets)==o['H']
            assert R.observations(t,owner)==R.frozen(c['shadows'][o['destination']]);queries+=1
            if queries%8192==0:assert time.process_time()-start<120,'UNKNOWN finite CPU cap'
    del c['witnesses'];seen=bytearray(count);family=[]
    words=[(p,) for p in R.PATHS]+[(p,q) for p,q in product(R.PATHS,repeat=2)]
    for word in words:
        n=0
        for t in R.prefixes(word):
            owner=t[0];sa=R.observations(t,owner);targets=[]
            for p in word:
                x=R.at(t,p)[0];targets.append(x);t=R.splay(t,x)
            ta=R.observations(t,owner);key=(sid[sa],len(word),targets[-1]//16,sid[ta]);seen[expected[key]]=1;n+=1;queries+=1
            if queries%8192==0:assert queries<=1000000 and time.process_time()-start<120,'UNKNOWN finite cap'
        if n:family.append({'word':word,'assignments':n})
    assert sum(seen)==count==430806 and sum(r['assignments'] for r in family)==462916
    print(json.dumps({'stage':'A_complete','queries':queries,'options':count,'CPU':round(time.process_time()-start,3)}),flush=True)
    del expected,seen
    oldb=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    bt=[R.frozen(r['tree']) for r in oldb['nodes']];bid={t:i for i,t in enumerate(bt)};assert set(R.bsts(tuple(range(9))))==set(bt) and len(bt)==4862
    dest=[];depths=[];neg=[[] for _ in bt];ind=[0]*len(bt);negative=0
    for b,t in enumerate(bt):
        dr=[];hr=[]
        for x in range(9):
            h=R.depth(t,x);v=bid[R.splay(t,x)];dr.append(v);hr.append(h);queries+=1;w=2-h//2
            if w<0:neg[b].append((v,-w));ind[v]+=1;negative+=1
        dest.append(dr);depths.append(hr)
    psi=[0]*len(bt);queue=deque(i for i,n in enumerate(ind) if not n);order=[]
    while queue:
        b=queue.popleft();order.append(b)
        for v,debt in neg[b]:
            psi[v]=max(psi[v],psi[b]+debt);ind[v]-=1
            if not ind[v]:queue.append(v)
    assert len(order)==4862 and negative==4224 and max(psi)==2 and psi==[r['psi'] for r in oldb['nodes']]
    oldcc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text());assert dest==oldcc['B_destination'] and depths==oldcc['B_depth']
    oldk=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/fringe_kernel_certificate.json').read_text())
    oldrows={(r['entry_core'],r['target']):r for r in oldk['rows']};kernel={};kept=0
    for b,t in enumerate(bt):
        pre=R.splay(R.insert(t,-1),-1)
        for x in range(9):
            h=R.depth(pre,x);result=R.splay(pre,x);f=R.find(result,-1);leaf=f[1] is None and f[2] is None;queries+=1
            old=oldrows[(b,x)];assert old['terminal_depth']==h and old['q']==h//2 and old['w']==4-h//2 and old['gap0_childless_at_exit']==leaf
            if leaf:
                bb=bid[R.without_fringe(result)];assert bb==old['exit_core'];kernel[(b,x)]=(bb,4-h//2);kept+=1
    assert kept==16842 and queries==981238
    print(json.dumps({'stage':'B_complete','queries':queries,'CPU':round(time.process_time()-start,3)}),flush=True)
    m=json.loads((OLD/'decoder_metadata.json').read_text());assert m['classes']==N and m['shadows']==c['shadows'] and list(map(R.frozen,m['B_trees']))==bt and m['psi']==psi
    p=json.loads((OLD/'potential_sparse.json').read_text());assert p['N']==N and p['default']=='-psi(B)';lab={int(k):v for k,v in p['labels'].items()}
    byroot={r:[] for r in range(9)}
    for a,s in enumerate(c['shadows']):byroot[s[0][2]].append(a)
    for key,value in lab.items():
        b,a=divmod(key,N);assert 0<=b<4862 and 0<=a<N and c['shadows'][a][0][2]==bt[b][0] and -2<=value<=-psi[b]
    checked=0;hist=Counter();automatic=Counter();states=0
    for b,t in enumerate(bt):
        for a in byroot[t[0]]:
            states+=1;value=lab.get(b*N+a,-psi[b])
            if value==0:automatic['zero_source_states']+=1;continue
            for o in c['options'][a]:
                x=o['target']
                if o['H']==1:
                    h=depths[b][x]
                    if not h:automatic['nongenuine']+=1;continue
                    bb=dest[b][x];w=2-h//2
                else:
                    pair=kernel.get((b,x))
                    if pair is None:automatic['nonchildless_exit']+=1;continue
                    bb,w=pair
                if w>=2:automatic['range']+=1;continue
                v=lab.get(bb*N+o['destination'],-psi[bb]);res=w-v+value;assert res>=0,(b,a,o,value,v,w);hist[res]+=1;checked+=1
        assert time.process_time()-start<120,'UNKNOWN finite CPU cap'
    for b in range(4862):
        for x in range(9):
            w=2-depths[b][x]//2
            if w<0:assert -psi[dest[b][x]]<=w
    assert all(w>=0 for bb,w in kernel.values())
    report={'status':'INDEPENDENT_FINITE_EXACT_PASS','queries':queries,'A_assignments':462916,'stored_witnesses_replayed':count,
      'alpha_classes':N,'all_A_options_regenerated':True,'core_trees':4862,'negative_core_edges':negative,
      'psi_histogram':dict(Counter(psi)),'fringe_cases':43758,'retained_fringe_rows':kept,
      'potential_changed_states':len(lab),'J_range':[-2,0],'product_states_streamed':states,'explicit_residuals':checked,
      'minimum_residual':min(hist),'residual_histogram':dict(hist),'analytic':dict(automatic),'families':family,
      'materialized_B_product_edges':0,'potential_sha256':hashlib.sha256((OLD/'potential_sparse.json').read_bytes()).hexdigest(),
      'cpu_seconds':round(time.process_time()-start,3),'source_lift_audit_pending':True,'full_M3_proved':False}
    with out.open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='families'},indent=2),flush=True)
if __name__=='__main__':main()
