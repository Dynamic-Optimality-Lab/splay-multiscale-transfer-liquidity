"""Exact cyclic interval feasibility, retaining every original physical key."""
from core import *
from collections import Counter


def all_intervals_through(r,h,stop_at=None):
    n=len(r.ops);keys=r.keys;bit={x:1<<i for i,x in enumerate(keys)}
    best=None;per_start=[];feasible={4:None,5:None};candidate_intervals=[]
    doubled=r.boundaries+r.boundaries
    for start in range(n):
        tree=Tree(r.boundaries[start]['pre_B']);M={row['x'] for row in r.boundaries if row['tag']=='K'}
        paths={x:sum(bit[y] for y in tree.path(x)) for x in M}
        J=0;A=0;blocks=0;last=None;L=0;counts=Counter();minimum=None;distance=(h-1-start)%n
        for delta in range(n):
            row=doubled[start+delta];A+=row['a']
            if row['tag']=='K' and row['x']!=last:
                x=row['x'];blocks+=1
                if last is not None:counts[(last,x)]+=1
                newJ=J|paths[x]
                if newJ!=J:
                    J=newJ;rank={y:i for i,y in enumerate(k for k in keys if J&bit[k])}
                    L=sum(count*abs(rank[v]-rank[u]).bit_length() for (u,v),count in counts.items())
                elif last is not None:L+=abs(rank[x]-rank[last]).bit_length()
                last=x
            if delta<distance:continue
            D=J.bit_count()+blocks+L
            if A and (best is None or D*best['A']<best['D']*A):
                best={'start':start+1,'end':row['t'],'length':delta+1,'D':D,'A':A,'J_size':J.bit_count(),'blocks':blocks,'L':L}
            deficit=D-4*A
            if minimum is None or deficit<minimum:minimum=deficit
            for c in feasible:
                if feasible[c] is None and blocks and D<=c*A:
                    feasible[c]={'start':start+1,'end':row['t'],'length':delta+1,'D':D,'A':A,'J_size':J.bit_count(),'blocks':blocks,'L':L}
            if stop_at and feasible[stop_at]:return {'best':best,'feasible':feasible,'exhaustive':False}
        per_start.append({'start':start+1,'minimum_D_minus_4A_through_consumer':minimum})
    return {'best':best,'feasible':feasible,'per_start':per_start,'exhaustive':True,'cyclic_intervals_checked':n*(n+1)//2,
        'note':'Exactly n(n+1)/2 start/length pairs contain one fixed occurrence, including n distinct full-period cuts.'}


def materialize(r,w):
    n=len(r.ops);start=w['start']-1;ts=[(start+i)%n+1 for i in range(w['length'])]
    rows=[r.boundaries[t-1] for t in ts];initial=rows[0]['pre_B'];tree=Tree(initial);J=closure(tree,[row['x'] for row in rows if row['tag']=='K'])
    rank={x:i for i,x in enumerate(sorted(J))};xs=[]
    for row in rows:
        if row['tag']=='K' and (not xs or xs[-1]!=row['x']):xs.append(row['x'])
    L=sum(abs(rank[y]-rank[x]).bit_length() for x,y in zip(xs,xs[1:]));steps=[e['id'] for e in r.events if e['actor']=='A' and e['id'][3]==0 and e['id'][1] in set(ts)]
    assert len(J)+len(xs)+L==w['D'] and len(steps)==w['A']
    B=Tree(initial);ind=r.as_tuple(B);Q=0
    for t in ts:
        row=r.boundaries[t-1]
        if row['tag']!='K':continue
        assert B.state()==row['pre_B'] and set(B.path(row['x']))<=J
        ind,ev=r.ind.trace(ind,row['x']);Replay.plain_splay(B,row['x'])
        assert ind==r.as_tuple(B)==r.as_tuple(Tree(row['post_B']))
        Q+=sum(e[0]!='ZIG' for e in ev)
    return {**w,'operations':ts,'J':sorted(J),'targets':xs,'original_A_StepEv':steps,'actual_Q_B':Q,
        'initial_B':initial,'ending_B':B.state(),'independently_checked_B_accesses':sum(row['tag']=='K' for row in rows)}


if __name__=='__main__':
    meter=Meter('CONT01_exact_all_intervals')
    row=next(z for z in json.loads((ROOT/'OWNERSHIP_RESULTS.json').read_text()) if z['escape'])
    s=next(s for s in json.loads((ROOT/'OWNERSHIP_SOURCES.json').read_text()) if s['name']==row['source'])
    r=Replay(s);h=row['escape'][0]['consumer'];z=all_intervals_through(r,h)
    assert z['exhaustive'];z.update(source=s['name'],consumer=h,source_A=r.A,source_Q=r.Q)
    for c,w in z['feasible'].items():
        if w is not None:z['feasible'][c]=materialize(r,w)
    write('ALL_INTERVALS_ESCAPE_AUDIT.json',z)
    print(s['name'],'minimum ratio',str(Fraction(z['best']['D'],z['best']['A'])),
        'c4',z['feasible'][4],'c5',z['feasible'][5],flush=True)
    meter.success=True;meter.details.update(intervals=z['cyclic_intervals_checked'])
