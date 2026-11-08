"""Targeted exact nonextremal weak-P construction; no broad variant search.
The six-key or old-owner theorem is not assumed from this source witness.
"""
import importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time()
sp=importlib.util.spec_from_file_location('C30_source_engine',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)

def path(t,x):
    if C.queries>=QCAP:raise TimeoutError('C30 exact remaining query cap')
    C.queries+=1;return C.original_path(t,x)
C.path=path;C.p.path=path

def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t

def main():
    old=json.loads((P/'SE03_STEP3_MARKED_COMB_SIGNED_REPAYMENT_29/comb_source_fixtures.json').read_text());T=fr(old['reports'][0]['original_diagonal_tree'])
    reset=list(range(13,0,-1));attempts=[];chosen=None
    # Source algebra suggests the two reflected positions within the SAME
    # comb. They are explicit candidate words, not a population cutoff.
    for prep,Z,Y,route in [([11,7,12,13,7,6,7,5,7,13],13,7,[7,11,7]),([11,7,12,13,7,6,7,5,7],7,13,[7,11,13])]:
        a=T
        for k in reset+prep:a=C.tr(a,k)[0]
        before=a;hh=[];paths=[]
        for k in (Y,11,5):a,pa,ev=C.tr(a,k);hh.append(len(ev));paths.append(pa)
        attempts.append({'prep':reset+prep,'Z':Z,'Y':Y,'A_before':before,'H':hh,'paths':paths})
        if before[0]==Z and hh==[1,1,1]:chosen=(prep,Z,Y,route);break
    out('targeted_A_preparations2.json',{'status':'EXACT_A_ONLY_SOURCE_PREPARATIONS','attempts':attempts,'matched':chosen is not None})
    if chosen is None:
        print(json.dumps({'status':'EXACT_PREPARATION_NOT_MATCHED','queries':C.queries}),flush=True);return
    prep,Z,Y,route=chosen;word=[];tags={};b=T;kept=[]
    def keep(k,label=None,record=True):
        nonlocal b
        if label:tags[label]=len(word)+1
        pa=C.path(b,k);assert len(pa)%2==0 and all(pa[i:i+2] in ('LL','RR') for i in range(0,len(pa),2))
        anc=[C.p.at(b,pa[:i])[0] for i in range(0,len(pa),2)]
        b,_,ev=C.tr(b,k);assert all(ev0['G'] in C.M and ev0['P'] not in C.M for ev0 in ev)
        word.append(('K',k))
        if record:kept.append(anc)
    for k in route:keep(k)
    word.extend(('D',k) for k in reset+prep)
    keep(Z,'preparation_end');keep(Y,'j');keep(11,'helper');keep(5,'comb')
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):keep(k,record=False)
    assert b==T;kept=[]
    keep(1)
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):keep(k,record=False)
    assert b==T;kept=[]
    for k in (7,13,9):keep(k)
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):keep(k,record=False)
    assert b==T
    word.extend(('D',k) for k in reset);word.append(('D',3))
    _,S=C.replay(T,T,T,word);rows,end=C.replay(*S,word);assert S[:2]==end[:2]
    base=len(word)
    for r in rows:r['occurrence']+=base
    tags={k:v+base for k,v in tags.items()};mm=C.L.macros(rows);profile=[]
    for label in ('j','helper','comb'):
        m=next(m for m in mm if tags[label] in m['occurrences']);x=m['rows'][-1]['target'];pa,ch=C.L.marked_tree(m['rows'][0]['before'][1],C.M);_,nc=C.L.marked_tree(m['rows'][-1]['after'][1],C.M)
        anc=[];v=pa[x]
        while v is not None:anc.append(v);v=pa[v]
        E=lambda cc:sum(max(len(v)-2,0) for v in cc.values());beta=sum(len(ch[v])>=2 for v in anc);k3=sum(len(ch[v])>=3 for v in anc);z=int(not ch[x]);c=min(m['H'],3)
        profile.append({'label':label,'occurrences':m['occurrences'],'target':x,'H':m['H'],'Q':m['Q'],'beta':beta,'z':z,'k3':k3,
            'rho':2*c-beta-z,'E_before':E(ch),'E_after':E(nc),'sigma_E':2*c-m['Q']+E(nc)-E(ch),'marked_before':ch,'marked_after':nc})
    assert [(z['H'],z['Q'],z['beta'],z['z']) for z in profile]==[(1,1,1,0),(1,2,1,1),(1,3,3,1)],profile
    assert sum(z['sigma_E'] for z in profile)==-1 and sum(z['rho'] for z in profile)==-3
    assert {r['target'] for r in rows if r['mode']=='K'}==C.M
    out('nonextremal_source_countercertificate.json',{'status':'PRODUCER_ORIGINAL_A_FULL_B_CLOSED_SOURCE_PENDING_DISTINCT_AUDIT',
        'original_diagonal_tree':T,'reaching_prefix':word,'period':word,'initial':S,'end':end,'rows':rows,'actual_interval':[base+1,2*base],
        'tags':tags,'triple':profile,'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),
        'erased_key':11,'BE_also_closed':S[2]==end[2],'owner_map_claimed':False,'A_preparation':reset+prep,
        'refuted_candidates':['Every weak P before a marked comb forces Hj>=2 without an extremal order guard','The immediate predecessor/triple E packet always repays a shallow helper'],
        'not_refuted':['MC29-X with its stated extremal guard','NH30 existential source repayment','all possible packet rules','Coarse-Double','Universal CD','Dynamic Optimality']})
    print(json.dumps({'status':'NONEXTREMAL_SOURCE_COUNTERCERTIFICATE','length':len(word),'queries':C.queries,'profile':profile,'BE_closed':S[2]==end[2]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
