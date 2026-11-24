"""Independent streaming construction, distinct from forest5's reverse searches."""
from base0 import *
from collections import deque

KINDS={'actual_A_reset':'R','last_non_target_promotion':'P','no_promotion_same_column':'C'}

def scan_forest(r,cut=0):
    N=len(r.ops);order=list(range(cut,N))+list(range(cut))
    old_col={};last_A={};last_B={};answer={}
    byop={i+1:[] for i in range(N)}
    for p in sorted(r.doubles):byop[p[0]].append(p)
    for lap in range(2):
        for i in order:
            row=r.boundaries[i];h=i+1
            for e in r.events[row['start_time']:row['post_A_time']]:
                assert e['actor']=='A';last_A[e['pivot']]=tuple(e['id'])
            # Every parent is classified at PRE-B, before this splay's promotions.
            for v in byop[h]:
                g=r.doubles[v]['g']
                if lap:
                    assert g in old_col
                    if g in last_A:
                        z={'type':'R','predecessor':None,'A_donor':last_A[g]}
                    elif g in last_B:
                        e=last_B[g]
                        assert e['target']!=g and e['case'] in ('LL','RR') and e['id'][3]==0
                        z={'type':'P','predecessor':tuple(e['id'][1:3])}
                    else:z={'type':'C','predecessor':old_col[g]}
                    answer[v]=z
            for e in r.events[row['post_A_time']:row['end_time']]:
                assert e['actor']=='B';last_B[e['promoted']]=e
            for v in byop[h]:
                g=r.doubles[v]['g'];old_col[g]=v;last_A.pop(g,None);last_B.pop(g,None)
    assert set(answer)==set(r.doubles)
    return answer

def audit_forest(r,answer):
    roots=[];donors=set();children=defaultdict(list);roles=Counter()
    byid={tuple(e['id']):e for e in r.events}
    for v,z in answer.items():
        typ=z['type'];roles[typ]+=1
        if typ=='R':
            donor=tuple(z['A_donor']);assert donor not in donors;donors.add(donor)
            e=byid[donor]
            assert e['actor']=='A' and e['pivot']==r.doubles[v]['g'];roots.append(v)
        else:
            p=z['predecessor'];assert p in answer and p!=v;children[p].append(v)
            d=r.doubles[p];cap=d['J'] if typ=='C' else d['P_output']
            F=r.doubles[v]['F'];parent=d['F'];x=d['target']
            assert F&~cap==0 and cap&~parent==0 and not cap&r.bits[x] and parent&r.bits[x]
            ph=d['physical_J_interval'] if typ=='C' else d['physical_P_interval']
            lo,hi=r.doubles[v]['physical_frame_interval'];pl,pr=d['physical_frame_interval']
            assert pl<=ph[0]<=lo<=hi<=ph[1]<=pr and not(ph[0]<=x<=ph[1])
    assert max(map(len,children.values()),default=0)<=2
    for p,cs in children.items():
        assert sum(answer[v]['type']=='C' for v in cs)<=1
        assert sum(answer[v]['type']=='P' for v in cs)<=1
    queue=deque(roots);done=[]
    while queue:
        p=queue.popleft();done.append(p);queue.extend(children[p])
    assert len(done)==len(answer) # independent cycle check, no frame topological sort
    real=sum(e['actor']=='A' for e in r.events)
    steps={tuple(e['id'][:3]) for e in r.events if e['actor']=='A'}
    assert len(steps)==r.A
    assert len(roots)<=real<=2*r.A
    return {'root_count':len(roots),'real_A_bits':real,'actual_A_StepEv':r.A,'vertex_count':len(answer),
        'types':dict(roles),'root_donors_injective':True,'topological_vertices_removed':len(done),
        'maximum_immediate_children':max(map(len,children.values()),default=0)}
