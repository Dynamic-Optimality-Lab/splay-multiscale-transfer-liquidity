from core import *
from types import SimpleNamespace


def prefix_profile(rows,c=4):
    initial=Tree(rows[0]['pre_B']);J=set();xs=[];A=0;L=0;out=[]
    for row in rows:
        A+=row['a']
        if row['tag']=='K' and (not xs or xs[-1]!=row['x']):
            xs.append(row['x']);old=len(J);J.update(initial.path(row['x']))
            if len(J)!=old:
                rank={x:i for i,x in enumerate(sorted(J))}
                L=sum(abs(rank[y]-rank[x]).bit_length() for x,y in zip(xs,xs[1:]))
            elif len(xs)>1:L+=abs(rank[xs[-1]]-rank[xs[-2]]).bit_length()
        D=len(J)+len(xs)+L
        out.append({'end':row['t'],'A':A,'J_size':len(J),'blocks':len(xs),'L':L,'D':D,
            'deficit':D-c*A,'eligible':bool(xs) and D<=c*A})
    return out


def trace_view(trace):
    s=trace['source'];rows=trace['boundaries'];keys=sorted(map(int,s['initial_B']['children']))
    M={r['x'] for r in rows if r['tag']=='K' and len(r['B_path'])>1};S=closure(Tree(s['initial_B']),M)
    bits={k:1<<i for i,k in enumerate(keys) if k in S}
    return SimpleNamespace(source=s,boundaries=rows,events=trace['events'],ops=s['operations'],keys=keys,S=S,bits=bits,
        A=sum(r['a'] for r in rows),T=len(trace['events']))


def tail_test(r,events):
    eps,_=psi_episodes(r);results=[]
    for h in sorted({e['consumer'] for e in events}):
        ep=next(ep for ep in eps if h in ep['operations']);idx=ep['operations'].index(h)
        ts=ep['operations'][idx:];rows=[r.boundaries[t-1] for t in ts];profile=prefix_profile(rows)
        results.append({'consumer':h,'original_events':[e for e in events if e['consumer']==h],
            'episode':ep['id'],'episode_end':ts[-1],'funded_prefix_exists':any(p['eligible'] for p in profile),
            'minimum_deficit':min(p['deficit'] for p in profile),'profile':profile})
    return results


if __name__=='__main__':
    meter=Meter('CONT01_backward_tail_alternative');out=[]
    for path in sorted(PARENT.glob('EXP04_VERIFIED_TRACE_*.json')):
        tr=json.loads(path.read_text());r=trace_view(tr);events=tr['original_R_star'];res=tail_test(r,events)
        out.append({'source':r.source['name'],'tests':res})
        print(r.source['name'],'tail failures',[p['consumer'] for p in res if not p['funded_prefix_exists']],flush=True)
    write('TAIL_ALTERNATIVE_RESULTS.json',out);meter.success=True
