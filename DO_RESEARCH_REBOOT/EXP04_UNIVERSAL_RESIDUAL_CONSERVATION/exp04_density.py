from exp04_monotone import *


def density_windows(r,eps,c=4):
    windows=[];usedA=set()
    for ep in eps:
        ts=ep['operations'];start=0
        while start<len(ts):
            initial=r.boundaries[ts[start]-1]['pre_B'];tree=Tree(initial);J=set();targets=[];a=0;travel=0;best=None
            for end in range(start,len(ts)):
                row=r.boundaries[ts[end]-1];a+=row['a']
                if row['tag']=='K' and (not targets or targets[-1]!=row['x']):
                    targets.append(row['x']);oldlen=len(J);J.update(tree.path(row['x']))
                    if len(J)!=oldlen:
                        ranks={x:i for i,x in enumerate(sorted(J))}
                        travel=sum(abs(ranks[y]-ranks[x]).bit_length() for x,y in zip(targets,targets[1:]))
                    elif len(targets)>1:travel+=abs(ranks[targets[-1]]-ranks[targets[-2]]).bit_length()
                D=len(J)+len(targets)+travel
                if targets and D<=c*a:best=(end,sorted(J),list(targets),travel,a,D)
            if best is None:start+=1;continue
            end,J,targets,L,a,D=best;owned=ts[start:end+1];ownedset=set(owned)
            steps=[e['id'] for e in r.events if e['actor']=='A' and e['id'][3]==0 and e['id'][1] in ownedset]
            assert len(steps)==a and not usedA.intersection(map(tuple,steps));usedA.update(map(tuple,steps))
            Q=sum(r.boundaries[t-1]['q'] for t in owned)
            # All actual KEEP operations are retained. Check exact isolation
            # and independent tuple evolution on the fixed initial domain.
            B=Tree(initial);ind=r.as_tuple(B)
            for t in owned:
                row=r.boundaries[t-1]
                if row['tag']!='K':continue
                assert B.state()==row['pre_B'] and set(B.path(row['x']))<=set(J)
                Replay.plain_splay(B,row['x']);ind,_=r.ind.trace(ind,row['x']);assert ind==r.as_tuple(B)
                assert B.state()==row['post_B']
            windows.append({'episode':ep['id'],'operations':owned,'J':J,'targets':targets,'integer_rank_travel':L,
                'density_D':D,'original_A':a,'original_A_StepEv':steps,'actual_Q_B':Q,'initial_B':initial,'ending_B':B.state()})
            start=end+1
    assert sum(w['original_A'] for w in windows)<=r.A
    return windows


def density_analysis(r,events,eps):
    windows=density_windows(r,eps);owned={t for w in windows for t in w['operations']}
    paid=[e for e in events if e['consumer'] in owned]
    assert len(paid)<=3*sum(w['actual_Q_B'] for w in windows)
    return {'windows':windows,'paid':paid,'remaining':[e for e in events if e['consumer'] not in owned],
        'bound':'R_density <= 3 C_DF sum D <=12 C_DF A','maximum_original_A_load':1}


if __name__=='__main__':
    meter=Meter('EXP04_density')
    a=json.loads((ROOT/'EXP04_SOURCE_WITNESSES.json').read_text())
    a['new_sources']=json.loads((ROOT/'EXP04_NEW_SOURCE_CHECKPOINT.json').read_text())['sources']+json.loads((ROOT/'EXP04_ADVERSARIAL_SOURCES.json').read_text())
    rows=json.loads((ROOT/'EXP04_RESIDUAL_INVENTORY.json').read_text())['inherited_sources']+json.loads((ROOT/'EXP04_NEW_RESULTS.json').read_text())+json.loads((ROOT/'EXP04_ADVERSARIAL_RESULTS.json').read_text())
    by={r['source']:r for r in rows};out=[]
    # Test the new density mechanism on ALL R_* sources, not just whichever
    # few happened to survive the previous comparison strategies.
    for s in a['inherited_sources']+a['new_sources']:
        row=by[s['name']]
        if not row['R_star']:continue
        r=Replay(s);eps,_=psi_episodes(r);z=density_analysis(r,row['events'],eps);z['source']=s['name'];out.append(z)
        print(s['name'],'windows',len(z['windows']),'paid',len(z['paid']),'remaining',len(z['remaining']),flush=True)
        write('EXP04_DENSITY_RESULTS.json',out);del r
    meter.success=True;meter.details.update(sources=len(out),remaining=sum(len(z['remaining']) for z in out))
