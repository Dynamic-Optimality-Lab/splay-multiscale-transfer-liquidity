"""Frozen 3/4/6-key chord audit; no fits, pair graphs or new candidates."""
from pathlib import Path
from collections import deque
import hashlib, json, subprocess, sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as S
from liquidity import legacy_embedding as P

def ck(ok,msg):
    if not ok: raise AssertionError(msg)
def save(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f: json.dump(obj,f,indent=2)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def raw(t): return None if t==S.LEAF else [t[1],raw(t[2]),raw(t[3])]
def ptr(t):
    if t==S.LEAF: return None
    p=P.mknode(t[1],ptr(t[2]),ptr(t[3]))
    for side in ('l','r'):
        if p[side] is not None: p[side]['p']=p
    return p
def rp(t): return None if t is None else [t['k'],rp(t['l']),rp(t['r'])]
def sets(t):
    if t==S.LEAF: return set()
    keys=S.inorder(t)
    return {(keys[0],keys[-1])}|sets(t[2])|sets(t[3])
def proper(t):
    c=sets(t);keys=S.inorder(t)
    if keys: c.remove((keys[0],keys[-1]))
    return sorted(c)
def crosses(I,J):
    a,b=I[0]-1,I[1]+1;c,d=J[0]-1,J[1]+1
    return a<c<b<d or c<a<d<b
def val(a,b):
    ai=proper(a);bi=proper(b)
    adj=[[j for j,J in enumerate(bi) if crosses(I,J)] for I in ai]
    deg=list(map(len,adj))
    return {'A_intervals':[list(i) for i in ai], 'B_intervals':[list(i) for i in bi],
      'crossing_adjacency':adj,'crossing_degrees':deg,'H1':sum(k>=1 for k in deg),
      'H2':sum(k>=2 for k in deg),'H3':sum(k>=3 for k in deg)}
def mirror(t,n):
    return S.LEAF if t==S.LEAF else S.node(n+1-t[1],mirror(t[3],n),mirror(t[2],n))
def edge(label,a,b,mode,x):
    ap,ea=S.trace(a,x)
    if mode=='K': bp,eb=S.trace(b,x)
    else: bp,eb=b,[]
    pa,pea=P.splay_trace(ptr(a),x)
    if mode=='K': pb,peb=P.splay_trace(ptr(b),x)
    else: pb,peb=ptr(b),[]
    ev=lambda es:[[e['case'],e['lo'],e['hi'],e['orient']] for e in es]
    ck(raw(ap)==rp(pa) and raw(bp)==rp(pb),'physical source engines agree')
    ck([list(e) for e in ea]==ev(pea) and [list(e) for e in eb]==ev(peb),'all oriented source events agree')
    da=S.lookup(a,x)[1];db=S.lookup(b,x)[1] if mode=='K' else None
    ac=len(ea);q=sum(e[0]!='ZIG' for e in eb);z=sum(e[0]=='ZIG' for e in eb)
    ck(ac==(da+1)//2 and q==(db//2 if db is not None else 0) and z==(db%2 if db is not None else 0),'source units')
    v0,vm,v1=val(a,b),val(ap,b),val(ap,bp)
    ck(abs(vm['H2']-v0['H2'])<=da,'A bound corroboration')
    return ap,bp,{'label':label,'source_A':raw(a),'source_B':raw(b),'mode':mode,'key':x,
      'destination_A':raw(ap),'destination_B':raw(bp),'dA':da,'dB':db,'a':ac,'q':q,'z':z,
      'events_A':ev(pea),'events_B':ev(peb),'source_values':v0,'after_A_values':vm,'destination_values':v1,
      'delta_H2':v1['H2']-v0['H2'],'budget':2*ac-q,'H2_law_holds':v1['H2']-v0['H2']<=2*ac-q}

def main():
    ck((OUT/'CT00_FOUR_RULE_GATE.md').is_file(),'written gate precedes source audit')
    git=lambda *args: subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    old=OUT.parent/'route_c_capped_residual_20261031_v001'
    inherited=json.loads((old/'entry_source_pins.json').read_text(encoding='utf-8'))
    paths=set(inherited['files'])
    paths.update('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_capped_residual_20261031_v001/'+p for p in ['CR02_MONOTONE_AGGREGATION_OBSTRUCTION.md','CR04_STRATEGY_REVIEW.md','CR05_FINAL_REPORT.md','capped_residual_certificate.json','independent_audit.json'])
    paths.update(['audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md','DO_RESEARCH_REBOOT/ORIGINAL_PIPELINE.md','DO_RESEARCH_REBOOT/01_MAIN_PIPELINE/stage_04_coarse_double.md'])
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_paths=[p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file()]
    paths.update(stage_paths)
    pins={p:sha(ROOT/p) for p in sorted(paths)}
    ck(all(pins[p]==h for p,h in inherited['files'].items()),'inherited pins unchanged at entry')
    ck(not git('status','--porcelain=v1','--untracked-files=no'),'tracked entry clean')
    save('entry_source_pins.json',{'date':'2026-10-31','head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),
      'files':pins,'stage11g_all_files':stage_paths,'gate_sha256':sha(OUT/'CT00_FOUR_RULE_GATE.md')})

    leaf=lambda k:S.node(k,S.LEAF,S.LEAF)
    a=S.node(4,S.node(2,leaf(1),leaf(3)),S.LEAF);b=S.vine(4)
    controls=[]
    _,_,r=edge('principal_four_key_starved_KEEP',a,b,'K',4);controls.append(r)
    ck((r['a'],r['q'],r['z'],r['source_values']['H2'],r['destination_values']['H2'])==(0,1,1,1,1),'principal registered source failure')
    for n in (3,6):
        _,_,r=edge('registered_opposite_vines_'+str(n),S.vine_left(n),S.vine(n),'K',n);controls.append(r)
    mirrored=[]
    for r in controls:
        def dec(t):return S.LEAF if t is None else S.node(t[0],dec(t[1]),dec(t[2]))
        n=len(S.inorder(dec(r['source_A'])))
        _,_,m=edge('reflection_of_'+r['label'],mirror(dec(r['source_A']),n),mirror(dec(r['source_B']),n),'K',n+1-r['key'])
        ck(m['source_values']['H2']==r['source_values']['H2'] and m['destination_values']['H2']==r['destination_values']['H2'],'reflection values')
        mirrored.append(m)

    # Only one four-key, single-tree connector BFS. No pair-state graph.
    queue=deque([b]);previous={b:None};expanded=requests=0
    while queue:
        t=queue.popleft()
        if t==a:break
        expanded+=1
        for x in range(1,5):
            u,_=S.trace(t,x);requests+=1
            if u not in previous: previous[u]=(t,x);queue.append(u)
    ck(a in previous,'fixed four-key connector found')
    word=[];cur=a
    while previous[cur] is not None:
        parent,x=previous[cur];word.append(['D',x]);cur=parent
    word.reverse();failed=len(word)
    word+=[['K',4]]+[['K',x] for x in [1,2,3,4,3,2,1]]
    ca=cb=b;replay=[]
    for i,(mode,x) in enumerate(word):
        ca,cb,r=edge('closed_word_'+str(i),ca,cb,mode,x);replay.append(r)
    ck(ca==cb==b,'exact diagonal paired closure')
    ck(replay[failed]['source_A']==raw(a) and replay[failed]['source_B']==raw(b),'principal counteredge reached')
    A=sum(r['a'] for r in replay);Q=sum(r['q'] for r in replay);Z=sum(r['z'] for r in replay)
    ck(Q<=2*A,'witness is not a CD counterexample')
    save('crossing_certificate.json',{'date':'2026-10-31','definition':'Hk=sum over C0(A) of indicator(number of B chords crossing (min(I)-1,max(I)+1)>=k)',
      'controls':controls,'reflections':mirrored,
      'threshold_partition':{'k=1_control':2,'k=2_control':0,'k>=3_control':1},
      'closed_witness':{'initial_A':raw(b),'initial_B':raw(b),'word':word,'failed_edge_index':failed,'full_replay':replay,'A':A,'Q_B':Q,'Z_B':Z},
      'connector':{'single_tree_BFS_calls':1,'n':4,'states_visited':len(previous),'states_expanded':expanded,'requests':requests},
      'no_larger_finite_fits':True,'new_pair_graphs':0})
    print(json.dumps({'principal':{'source':controls[0]['source_values'],'destination':controls[0]['destination_values'],'a':0,'q':1,'z':1},
      'opposite3':{'source':controls[1]['source_values']['crossing_degrees'],'destination':controls[1]['destination_values']['crossing_degrees']},
      'opposite6':{'source':controls[2]['source_values']['crossing_degrees'],'destination':controls[2]['destination_values']['crossing_degrees']},
      'closed_word':word,'totals':[A,Q,Z],'pins':len(pins),'stage11g_files':len(stage_paths),'BFS_states':len(previous)},indent=2))

if __name__=='__main__': main()
