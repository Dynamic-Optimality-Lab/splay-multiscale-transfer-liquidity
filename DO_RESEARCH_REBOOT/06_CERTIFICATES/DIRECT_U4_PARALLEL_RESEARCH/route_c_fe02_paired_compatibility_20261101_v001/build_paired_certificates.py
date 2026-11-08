"""One FE02 paired-return campaign: fixed source data and explicit controls."""
import hashlib
import importlib.util
import json
import sys
from collections import deque
from itertools import combinations
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PG=HERE.parent/'route_c_pf_positive_gap_closure_20261101_v001'
FE=HERE.parent/'route_c_fe01_first_entry_20261101_v001'


def load(name,p):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
tu=load('paired_original_tuple',ROOT/'python/independent/splay.py')
fe=load('frozen_FE01_exact_H',FE/'source_first_entry.py')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return [t[1],jt(t[2]),jt(t[3])]
def splay(t,x):
    a,ev=tu.trace(tt(t),x);return jt(a),[list(e) for e in ev]
def depth(t,y):return len(fe.path(t,y)[0])-1
def ancestors(t,parents=()):
    if t is None:return {}
    if isinstance(t,str):return {t:set(parents)}
    return {t[0]:set(parents),**ancestors(t[1],parents+(t[0],)),**ancestors(t[2],parents+(t[0],))}
def discord(A,B):
    aa,bb=ancestors(A),ancestors(B);ks=sorted(k for k in aa if isinstance(k,int));out=[]
    def rel(m,u,v):return 1 if u in m[v] else -1 if v in m[u] else 0
    for u,v in combinations(ks,2):
        if rel(aa,u,v)!=rel(bb,u,v):out.append([u,v])
    return out
def mirror(t):
    if t is None:return None
    if isinstance(t,str):return 'F_lower'
    return [14-t[0],mirror(t[2]),mirror(t[1])]


def paired_step(row,y):
    r=row['source_A'][0];assert r==row['source_B'][0]
    x=row['key'];hA=depth(row['source_A'],y);hB=depth(row['source_B'],y)
    pA=fe.profile(row['source_A'],x,y);pB=fe.profile(row['source_B'],x,y)
    eA=fe.profile(row['source_A'],x,r)['H'];eB=fe.profile(row['source_B'],x,r)['H']
    deltaA=pA['H']-hA;deltaB=pB['H']-hB
    far=(y-r)*(x-r)<0
    sep=None
    if (eA,eB)==(1,2):
        separator=fe.path(row['source_B'],x)[0][1][0]
        aa,bb=ancestors(row['destination_A']),ancestors(row['destination_B'])
        assert r in aa[separator] and separator in bb[r]
        sep=[r,separator]
    return dict(key=y,old_root=r,target=x,old_root_or_far_side=(y==r or far),far_side=far,
        epsilon_A=eA,epsilon_B=eB,before_A_depth=hA,before_B_depth=hB,
        after_A_depth=pA['H'],after_B_depth=pB['H'],A_shift=deltaA,B_shift=deltaB,
        paired_gap_before=hB-2*hA,paired_gap_after=pB['H']-2*pA['H'],
        paired_gap_shift=deltaB-2*deltaA,source_A_profile=pA,source_B_profile=pB,
        equality_separator_pair=sep)


def returns(rows):
    out=[];N=len(rows)
    for j,row in enumerate(rows):
        y=row['key'];L=next(k for k in range(1,N+1) if rows[(j-k)%N]['key']==y)
        prev=(j-L)%N;indices=[(prev+t)%N for t in range(1,L)]
        steps=[dict(block=t,**paired_step(rows[t],y)) for t in indices]
        retreat=all(s['old_root_or_far_side'] for s in steps)
        if retreat:
            assert depth(row['source_A'],y)==sum(s['epsilon_A'] for s in steps)
            assert depth(row['source_B'],y)==sum(s['epsilon_B'] for s in steps)
            assert row['delta']<=0
        out.append(dict(return_block=j,key=y,previous_same_block=prev,gap=L,
            retreat_only=retreat,steps=steps,actual_a=row['a'],actual_q=row['q'],delta=row['delta'],
            strict_pair_steps=[s['block'] for s in steps if s['epsilon_B']-2*s['epsilon_A']<0],
            all_pair_equality=all((s['epsilon_A'],s['epsilon_B'])==(1,2) for s in steps),
            A_return_depth=depth(row['source_A'],y),B_return_depth=depth(row['source_B'],y)))
    return out


def execute_pair(A,B,word):
    rows=[]
    for j,(mode,x) in enumerate(word):
        da=depth(A,x);na,ae=splay(A,x)
        if mode=='KEEP':db=depth(B,x);nb,be=splay(B,x)
        else:db=None;nb=B;be=[]
        a=len(ae);q=sum(e[0]!='ZIG' for e in be)
        rows.append(dict(occurrence=j,mode=mode,key=x,source_A=A,source_B=B,destination_A=na,destination_B=nb,
            d_A=da,d_B=db,a=a,q=q,z=sum(e[0]=='ZIG' for e in be),delta=q-2*a,A_events=ae,B_events=be))
        A,B=na,nb
    return rows


def root_child_connector(start,target):
    encode=lambda t:json.dumps(t,separators=(',',':'))
    first,goal=encode(start),encode(target);parent={first:None};trees={first:start};queue=deque([first])
    while queue and goal not in parent:
        key=queue.popleft();t=trees[key];neighbors=[]
        if t[1] is not None:
            x=t[1];neighbors.append((x[0],[x[0],x[1],[t[0],x[2],t[2]]]))
        if t[2] is not None:
            x=t[2];neighbors.append((x[0],[x[0],[t[0],t[1],x[1]],x[2]]))
        for access,dest in sorted(neighbors):
            k=encode(dest)
            if k not in parent:parent[k]=(key,access);trees[k]=dest;queue.append(k)
        assert len(parent)<=42
    assert goal in parent,'fixed five-core connector absent'
    accesses=[];at=goal
    while parent[at] is not None:
        at,access=parent[at];accesses.append(access)
    return accesses[::-1],len(parent)


def main():
    pg=read(PG/'closed_source_certificate.json');deep={}
    for orientation,rows in [('ordinary',pg['ordinary_rows']),('reflected',pg['reflected_rows'])]:
        D=[]
        for j,row in enumerate(rows):
            before=discord(row['source_A'],row['source_B']);after=discord(row['destination_A'],row['destination_B'])
            x=row['key'];target=[p for p in before if x in p]
            transfer=len([p for p in after if x not in p])-len([p for p in before if x not in p])
            assert all(x not in p for p in after)
            D.append(dict(block=j,key=x,delta=row['delta'],D_before=len(before),D_after=len(after),
                target_removed=len(target),other_transfer=transfer,change=len(after)-len(before)))
        tracked=[3,4,5,6] if orientation=='ordinary' else [11,10,9,8]
        source_steps={str(y):[dict(block=t,**paired_step(rows[t],y)) for t in range(5)] for y in tracked}
        ret=returns(rows)
        assert ret[4]['retreat_only'] and ret[4]['A_return_depth']==2 and ret[4]['B_return_depth']==3
        assert not ret[0]['retreat_only']
        deep[orientation]=dict(tracked_source_steps=source_steps,returns=ret,discordance_steps=D,
            inherited_FE_donor=dict(demand=[0,0,2],unit=[0,2,0,1]),
            inherited_FE02_donor=dict(demand=[0,0,2],unit=[0,4,0,1]))
    save('walk_deep_certificate.json',dict(source_PG_sha256=sha(PG/'closed_source_certificate.json'),data=deep))

    def adversary(F):
        return ([1,None,[5,[2,None,[3,None,[4,None,F]]],None]],
                [1,None,[2,None,[3,None,[4,None,[5,F,None]]]]])
    A,B=adversary(None);connector,visited=root_child_connector(B,A)
    word=[('DELETE',x) for x in connector]+[('KEEP',5)]+[('KEEP',x) for x in [1,2,3,4,5,4,3,2,1]]
    cycle=execute_pair(B,B,word);edge=cycle[len(connector)]
    assert (edge['source_A'],edge['source_B'])==(A,B) and (edge['a'],edge['q'])==(1,2)
    assert cycle[-1]['destination_A']==cycle[-1]['destination_B']==B
    before=discord(A,B);after=discord(edge['destination_A'],edge['destination_B'])
    assert len(before)==3 and len(after)==4
    As,Bs=adversary('F');symbolic=execute_pair(As,Bs,[('KEEP',5)])[0]
    aa,bb=ancestors(As),ancestors(Bs)
    before_coeff=len(aa['F']^bb['F'])
    aa,bb=ancestors(symbolic['destination_A']),ancestors(symbolic['destination_B'])
    after_coeff=len(aa['F']^bb['F'])
    assert (before_coeff,after_coeff)==(0,2)
    save('discordance_obstruction_certificate.json',dict(status='SATURATED_D_MONOTONICITY_REFUTED_EXACT',
        core_source_A=A,core_source_B=B,target=5,core_D_before=3,core_D_after=4,
        symbolic_edge=symbolic,symbolic_D_before=dict(constant=3,coefficient_of_fringe_size=0),
        symbolic_D_after=dict(constant=4,coefficient_of_fringe_size=2),
        symbolic_change='1+2|F|',fringe_order='4<F<target, realized by relabeling target to |F|+5',
        root_child_DELETE_connector=connector,connector_visited_shapes=visited,connector_shape_bound=42,
        actual_closed_rows=cycle,saturated_edge_index=len(connector),
        actual_Coarse_Double_margin=sum(r['q']-2*r['a'] for r in cycle),
        no_Coarse_Double_counterexample_claimed=True,no_single_positive_saturated_return_claimed=True))

    R4=[1,None,[2,None,[3,None,[4,None,None]]]]
    startup=execute_pair(R4,R4,[('KEEP',x) for x in [1,2,3,4]])
    L4=startup[-1]['destination_A'];qual=execute_pair(L4,L4,[('KEEP',x) for x in [1,3,2,4]])
    assert qual[-1]['destination_A']==qual[-1]['destination_B']==L4
    rr=returns(qual);assert not any(r['retreat_only'] for r in rr)
    save('qualitative_return_control.json',dict(status='CLOSED_RETURN_DOES_NOT_FORCE_A_RETREAT_ONLY_INTERVAL',
        startup_rows=startup,closed_rows=qual,returns=rr,
        FE02_counterexample=False,scope='unqualified closure claim only; all costs remain source-valid'))
    print(json.dumps(dict(status='CERTIFICATES_WRITTEN',W_retreat_returns=[r['return_block'] for r in deep['ordinary']['returns'] if r['retreat_only']],
        W_D_nonnegative_blocks=[r for r in deep['ordinary']['discordance_steps'] if r['delta']>=0],
        discordance_counter_edge_a=1,discordance_counter_edge_q=2,D_change='1+2|F|',
        connector=connector,connector_visited=visited,qualitative_retreat_intervals=0),indent=2))


if __name__=='__main__':main()
