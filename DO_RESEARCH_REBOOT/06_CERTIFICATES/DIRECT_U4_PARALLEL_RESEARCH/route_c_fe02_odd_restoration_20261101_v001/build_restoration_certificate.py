"""One declared original-source restoration/transfer episode; no fit/search."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
s=importlib.util.spec_from_file_location('restoration_original_tuple',ROOT/'python/independent/splay.py')
tu=importlib.util.module_from_spec(s);s.loader.exec_module(tu)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,d):
    with (HERE/name).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def N(k,l=None,r=None):return [k,l,r]
def tt(t):
    if t is None:return tu.LEAF
    if isinstance(t,str):return ('opaque',t)
    return tu.node(t[0],tt(t[1]),tt(t[2]))
def jt(t):
    if t[0]=='leaf':return None
    if t[0]=='opaque':return t[1]
    return N(t[1],jt(t[2]),jt(t[3]))
def path(t,x):
    out=[]
    while isinstance(t,list):
        out.append(t[0])
        if t[0]==x:return out
        t=t[1 if x<t[0] else 2]
    raise AssertionError('explicit core key')
def dep(t,x):return len(path(t,x))-1
def epsilon(t,x):
    p=path(t,x);d=len(p)-1
    if d==0:return 0
    if d%2:return 1
    return 2 if (p[1]<p[0])==(p[2]<p[1]) else 1
def splay(t,x):
    v,e=tu.trace(tt(t),x);return jt(v),[list(z) for z in e]
def ancestor(t,u,v):
    while isinstance(t,list) and t[0]!=u:t=t[1 if u<t[0] else 2]
    return isinstance(t,list) and v in path(t,v)
def is_ancestor(t,u,v):
    while isinstance(t,list) and t[0]!=u:t=t[1 if u<t[0] else 2]
    while isinstance(t,list):
        if t[0]==v:return True
        t=t[1 if v<t[0] else 2]
    return False
def prefix_contains(a,b,x):
    while isinstance(a,list) and isinstance(b,list) and a[0]==b[0]:
        if a[0]==x:return True
        side=1 if x<a[0] else 2;a,b=a[side],b[side]
    return False
def inflate(t):
    gap=0
    def go(t):
        nonlocal gap
        if t is None:
            z='F'+str(gap);gap+=1;return z
        return N(t[0],go(t[1]),go(t[2]))
    v=go(t);assert gap==14;return v
def mirror(t):
    if t is None:return None
    return N(14-t[0],mirror(t[2]),mirror(t[1]))


def execute(A,B,word):
    out=[]
    for j,(mode,x) in enumerate(word):
        da=dep(A,x);aa,ae=splay(A,x);ea=epsilon(A,x)
        if mode=='KEEP':db=dep(B,x);bb,be=splay(B,x);eb=epsilon(B,x)
        else:db=None;bb=B;be=[];eb=None
        q=sum(e[0]!='ZIG' for e in be)
        out.append(dict(occurrence=j,mode=mode,key=x,source_A=A,source_B=B,destination_A=aa,destination_B=bb,
            d_A=da,d_B=db,a=len(ae),q=q,z=sum(e[0]=='ZIG' for e in be),delta=q-2*len(ae),
            A_events=ae,B_events=be,source_path_A=path(A,x),source_path_B=path(B,x) if mode=='KEEP' else None,
            source_epsilon_A=ea,source_epsilon_B=eb))
        A,B=aa,bb
    return out


def injection(rows,p):
    donor=next((p+j)%len(rows) for j in range(1,len(rows)) if rows[(p+j)%len(rows)]['delta']<0)
    out=[]
    for i,r in enumerate(rows):
        units=[[i,e,bit] for e in range(r['a']) for bit in (0,1)]
        demands=[[i,e] for e,z in enumerate(r['B_events']) if z[0]!='ZIG']
        for u,d in zip(units,demands):out.append(dict(A_unit=u,B_double=d,kind='own'))
    out.append(dict(A_unit=[donor,rows[donor]['a']-1,1],B_double=[p,2],kind='later-real-negative-block'))
    assert len({tuple(v['A_unit']) for v in out})==len(out)
    assert len({tuple(v['B_double']) for v in out})==len(out)==sum(r['q'] for r in rows)
    return dict(positive_cut=p,donor_block=donor,donor_unit=[donor,rows[donor]['a']-1,1],
        assignments=out,used_units=len(out),available_units=2*sum(r['a'] for r in rows),
        startup_credit_used=0,future_period_credit_used=0,FI_PF_FE_acceptance_claimed=False)


def main():
    V=None
    for x in range(13,0,-1):V=N(x,None,V)
    startup=[('DELETE',x) for x in [11,9,11,7,3,7,1]]
    episode=[('KEEP',7),('KEEP',11),('KEEP',1)]
    word=startup+episode+[('KEEP',x) for x in range(2,14)]+[('KEEP',x) for x in range(12,0,-1)]
    rows=execute(V,V,word);p=len(startup);episode_rows=rows[p:p+3]
    assert [(r['a'],r['q']) for r in episode_rows]==[(1,3),(1,2),(1,2)]
    assert [i for i,r in enumerate(rows) if r['delta']>0]==[p]
    assert rows[-1]['destination_A']==rows[-1]['destination_B']==V
    assert all(rows[i]['key']!=rows[(i+1)%len(rows)]['key'] for i in range(len(rows)))
    states=[(episode_rows[0]['source_A'],episode_rows[0]['source_B'])]+[(r['destination_A'],r['destination_B']) for r in episode_rows]
    common=[prefix_contains(A,B,1) for A,B in states]
    assert common==[True,False,False,True]
    last=episode_rows[-1]
    assert last['destination_A'][2][0]==7 and last['destination_B'][2][0]==8
    assert is_ancestor(last['destination_A'],7,8) and is_ancestor(last['destination_B'],8,7)
    assert all(is_ancestor(t,7,8) for t in states[0])
    assert all(is_ancestor(t,1,2) for t in states[-1])
    assert (episode_rows[0]['source_epsilon_A'],episode_rows[0]['source_epsilon_B'])==(1,2)
    assert (episode_rows[1]['source_epsilon_A'],episode_rows[1]['source_epsilon_B'])==(1,2)
    symbolic=execute(inflate(V),inflate(V),word)
    assert symbolic[-1]['destination_A']==symbolic[-1]['destination_B']==inflate(V)
    reflected=execute(mirror(V),mirror(V),[(mode,14-x) for mode,x in word])
    assert reflected[-1]['destination_A']==reflected[-1]['destination_B']==mirror(V)
    assert [(r['a'],r['q']) for r in reflected]==[(r['a'],r['q']) for r in rows]
    assignment=injection(rows,p)
    local_units=[[i,e,bit] for i in range(p,p+3) for e in range(rows[i]['a']) for bit in (0,1)]
    local_demands=[[i,e] for i in range(p,p+3) for e,z in enumerate(rows[i]['B_events']) if z[0]!='ZIG']
    assert (len(local_units),len(local_demands))==(6,7)
    result=dict(gate_sha256=sha(HERE/'OR00_FOUR_RULE_GATE.md'),source_word=word,rows=rows,
        symbolic_rows=symbolic,reflected_rows=reflected,all14_ordered_gap_variables=True,
        startup_word=startup,episode_word=episode,episode_indices=list(range(p,p+3)),
        positive_block=p,positive_type=[1,3],old_boundary=1,old_B_parent=2,
        common_boundary_by_episode_cut=common,first_restoration_block=p+2,
        restored_block_type=[1,2],restoration_is_saturated=True,
        exported_boundary_pair=[7,8],restored_old_pair=[1,2],
        source_before_episode_A=states[0][0],source_before_episode_B=states[0][1],
        local_capacity_certificate=dict(A_units=local_units,B_double_demands=local_demands,
            capacity=6,demand=7,deficit=1,all_A_units_are_real=True,all_B_demands_are_real=True,
            no_negative_block_from_positive_through_first_restoration=True),
        full_pair_closed=True,reachable_from_diagonal=True,exactly_one_positive_block=True,
        block_count=len(rows),A=sum(r['a'] for r in rows),Q=sum(r['q'] for r in rows),
        direct_injection=assignment,larger_finite_fits=0,larger_key_count_replays=0,
        first_restoration_implies_local_repayment='REFUTED—EXACT within actual FE02 closed histories',
        unrestricted_eventual_repayment='OPEN',FE02_CD='OPEN',Coarse_Double_counterexample=False)
    save('odd_restoration_source_certificate.json',result)
    print(json.dumps({k:result[k] for k in ['block_count','A','Q','positive_block','first_restoration_block','exported_boundary_pair','FE02_CD']},indent=2))


if __name__=='__main__':main()
