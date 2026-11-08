"""Exact closed-source obstruction to extending extremal three-macro rule.
Bounded construction; actual original A/full-B period, not graph lifting.
"""
import collections,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=float(sys.argv[1])
sp=importlib.util.spec_from_file_location('C29_nonextreme2_engine',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)

def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)

def fr(t):return tuple(fr(v) for v in t) if isinstance(t,list) else t

def main():
    old=json.loads((B/'comb_source_fixtures.json').read_text());T=fr(old['reports'][0]['original_diagonal_tree']);a=T
    for k in range(13,0,-1):a=C.tr(a,k)[0]
    todo=collections.deque([(a,[])]);seen={a};found=None
    while todo and C.queries<450:
        a,word=todo.popleft()
        if a[0]==13:
            z=a;hh=[]
            for k in (7,11,5):z,_,ev=C.tr(z,k);hh.append(len(ev))
            if hh==[1,1,1]:found=word;break
        if len(word)>=6:continue
        for k in (5,7,11,13):
            z=C.tr(a,k)[0]
            if z not in seen:seen.add(z);todo.append((z,word+[k]))
    assert found is not None,('no bounded preparation',C.queries)
    word=[];tags={};b=T;kept=[]
    def keep(k,label=None,record=True):
        nonlocal b
        if label:tags[label]=len(word)+1
        path=C.path(b,k);assert len(path)%2==0 and all(path[i:i+2] in ('LL','RR') for i in range(0,len(path),2))
        ancestors=[C.p.at(b,path[:i])[0] for i in range(0,len(path),2)]
        b,_,ev=C.tr(b,k);assert all(e['G'] in C.M and e['P'] not in C.M for e in ev)
        word.append(('K',k))
        if record:kept.append(ancestors)
    for k in (7,11,7):keep(k)
    word.extend(('D',k) for k in list(range(13,0,-1))+found)
    keep(13,'preparation_end');keep(7,'j');keep(11,'helper');keep(5,'comb')
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):keep(k,record=False)
    assert b==T
    # Closed SS support loops cover the previously untouched marked1 and9.
    kept=[]
    for k in (1,):keep(k)
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):keep(k,record=False)
    assert b==T;kept=[]
    for k in (7,13,9):keep(k)
    for anc in reversed(kept[:]):
        for k in C.inverse(anc):keep(k,record=False)
    assert b==T
    word.extend(('D',k) for k in range(13,0,-1));word.append(('D',3))
    # The final reset makes the A endpoint independent of its input. One
    # original body is a genuine reaching prefix; BF returns T exactly.
    _,start=C.replay(T,T,T,word);rows,end=C.replay(*start,word)
    assert start[:2]==end[:2]
    base=len(word)
    for r in rows:r['occurrence']+=base
    tags={k:v+base for k,v in tags.items()};mm=C.L.macros(rows);by={m['occurrences'][-1]:m for m in mm};triple=[]
    for key in ('j','helper','comb'):
        m=by[tags[key]];beta=len(m['branch']);rho=2*min(m['H'],3)-beta-m['z'];_,ch=C.L.marked_tree(m['rows'][0]['before'][1],C.M);_,nc=C.L.marked_tree(m['rows'][-1]['after'][1],C.M)
        E=lambda cc:sum(max(len(v)-2,0) for v in cc.values())
        triple.append({'label':key,'occurrences':m['occurrences'],'target':m['rows'][-1]['target'],'H':m['H'],'Q':m['Q'],'beta':beta,'z':m['z'],
            'rho':rho,'E_before':E(ch),'E_after':E(nc),'sigma_E':2*min(m['H'],3)-m['Q']+E(nc)-E(ch)})
    assert [(z['H'],z['Q'],z['beta'],z['z']) for z in triple]==[(1,1,1,0),(1,2,1,1),(1,3,3,1)],triple
    assert sum(z['sigma_E'] for z in triple)==-1 and sum(z['rho'] for z in triple)==-3
    assert {r['target'] for r in rows if r['mode']=='K'}==C.M
    assert C.queries<1100,C.queries
    out('nonextreme_closed_countercertificate.json',{'status':'ORIGINAL_REACHABLE_A_FULL_B_PAIRED_CLOSED_SOURCE','original_diagonal_tree':T,
        'reaching_prefix':word,'period':word,'initial':start,'end':end,'rows':rows,'actual_interval':[base+1,2*base],'tags':tags,'triple':triple,
        'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),
        'erased_key':11,'BE_also_closed':start[2]==end[2],'owner_map_claimed':False,
        'refuted':'Unconditional extension of MC29-X predecessor/triple E rule to nonextremal combs; universal source assertion Hj>=2 for weak P',
        'not_refuted':['MC29-X with its extremal hypothesis','all possible marked-comb mechanisms','Coarse-Double','Universal CD','Dynamic Optimality']})
    print(json.dumps({'status':'NONEXTREME_CLOSED_COUNTERCERTIFICATE','operations':len(word),'queries':C.queries,'triple':triple,'BE_closed':start[2]==end[2]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_nonextreme2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
