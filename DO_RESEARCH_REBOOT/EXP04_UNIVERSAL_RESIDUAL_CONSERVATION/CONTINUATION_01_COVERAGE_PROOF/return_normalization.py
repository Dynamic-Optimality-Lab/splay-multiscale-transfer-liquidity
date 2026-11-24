from core import *


def guarded_skeleton(r,ts,guard_kind='internal_neutral'):
    protected={t for (t,j),d in r.doubles.items() if d['signs']==[0,0] and (guard_kind=='all_neutral' or not(d['F']&r.extremes))}
    assert all(e['consumer'] in protected for e in getattr(r,'original_R_star',[]))
    stack=[];initial=r.boundaries[ts[0]-1]['pre_B'];locations={digest(initial):(0,initial)};omitted=[]
    for t in ts:
        row=r.boundaries[t-1]
        if row['tag']!='K':continue
        state=row['post_B'];key=digest(state)
        if t in protected:
            stack.append(t);locations={key:(len(stack),state)}
        elif key in locations:
            index,oldstate=locations[key];assert state==oldstate
            discarded=stack[index:]+[t];assert not set(discarded).intersection(protected)
            omitted.append({'discarded_original_KEEP':discarded,'equal_complete_B_hash':key})
            stack=stack[:index];locations={k:v for k,v in locations.items() if v[0]<=index}
        else:
            stack.append(t);locations[key]=(len(stack),state)
    B=Tree(initial);ind=r.as_tuple(B);targets=[];Q=0
    J=closure(B,[r.ops[t-1][1] for t in stack])
    for t in stack:
        row=r.boundaries[t-1];assert B.state()==row['pre_B'] and set(B.path(row['x']))<=J
        ind,ev=r.ind.trace(ind,row['x']);Replay.plain_splay(B,row['x']);assert ind==r.as_tuple(B)==r.as_tuple(Tree(row['post_B']))
        Q+=sum(e[0]!='ZIG' for e in ev)
        if not targets or targets[-1]!=row['x']:targets.append(row['x'])
    assert B.state()==r.boundaries[ts[-1]-1]['post_B']
    rank={x:i for i,x in enumerate(sorted(J))};L=sum(abs(rank[y]-rank[x]).bit_length() for x,y in zip(targets,targets[1:]))
    A=sum(r.boundaries[t-1]['a'] for t in ts)
    return {'operations':ts,'retained_KEEP':stack,'protected_operations_in_span':sorted(set(ts)&protected),'erased_returns':omitted,
        'J':sorted(J),'targets':targets,'L':L,'D':len(J)+len(targets)+L,'A':A,'retained_actual_Q':Q,
        'initial_B':initial,'ending_B':B.state(),'guard':guard_kind,'independent_shadow_accesses':len(stack)}


def irredundant_subcover(arcs,n):
    coverage=[0]*n
    for arc in arcs:
        for t in arc['operations']:coverage[t-1]+=1
    original_union={i+1 for i,c in enumerate(coverage) if c};selected=[]
    for arc in reversed(arcs):
        ts=arc['operations']
        if all(coverage[t-1]>=2 for t in ts):
            for t in ts:coverage[t-1]-=1
        else:selected.append(arc)
    assert {i+1 for i,c in enumerate(coverage) if c}==original_union
    assert max(coverage,default=0)<=2
    assert all(any(coverage[t-1]==1 for t in arc['operations']) for arc in selected)
    return list(reversed(selected)),coverage


if __name__=='__main__':
    meter=Meter('CONT01_guarded_return_payment');out=[]
    sets=[('OWNERSHIP_SOURCES.json','OWNERSHIP_RESULTS.json','escape'),('COLUMN_SOURCES.json','COLUMN_RESULTS.json','frozen_escape')]
    for sf,rf,field in sets:
        if not (ROOT/sf).exists():continue
        sources={s['name']:s for s in json.loads((ROOT/sf).read_text())}
        for z in json.loads((ROOT/rf).read_text()):
            if not z[field]:continue
            r=Replay(sources[z['source']]);r.original_R_star=z['R_star'];ts=list(range(1,len(r.ops)+1))
            normalized=guarded_skeleton(r,ts)
            result={'source':z['source'],'original_escape':z[field],'normalized_full_period':normalized,
                'eligible_D_le_5A':normalized['D']<=5*r.A,
                'protected_all_escaping_consumers':all(e['consumer'] in normalized['retained_KEEP'] for e in z[field])}
            out.append(result);print(z['source'],'guards',len(normalized['protected_operations_in_span']),
                'retained',len(normalized['retained_KEEP']),'D',normalized['D'],'A',r.A,'eligible',result['eligible_D_le_5A'],flush=True)
    write('GUARDED_RETURN_RESULTS.json',out);meter.success=True
