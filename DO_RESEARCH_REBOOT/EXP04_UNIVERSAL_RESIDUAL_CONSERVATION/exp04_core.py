"""Thin experiment orchestration of the unchanged physical and Pi engines."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
PREV=ROOT.parent/'EXP03_FINAL_R6_ESCAPE_CONSERVATION'
sys.path.insert(0,str(PREV))
import exp03_core as prior
from exp03_core import *
ROOT=Path(__file__).resolve().parent
prior.ROOT=ROOT
inherited_distortion.ROOT=ROOT;inherited_frame.ROOT=ROOT
import exp03_restart as restart_module
from exp03_episodes import actual_mismatch_episodes
from exp03_sources import omitted_family,outside_probe,mixed_closed,closed_private,warmed_private,many_interruptions
from exp03_inheritance import file_hash


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')


class Meter:
    """Never overwrite an earlier run's resource measurement."""
    def __init__(self,stage):
        self.stage=stage;self.cpu=timing.process_time();self.wall=timing.perf_counter();self.success=False;self.details={}
        base='EXP04_RESOURCE_'+stage;name=base+'.json';version=2
        while (ROOT/name).exists():name=base+f'_v{version:03d}.json';version+=1
        self.name=name;atexit.register(self.finish)
    def finish(self):
        write(self.name,{'stage':self.stage,'status':'completed' if self.success else 'failed_or_interrupted',
            'process_CPU_seconds':timing.process_time()-self.cpu,'wall_seconds':timing.perf_counter()-self.wall,
            'memory':memory(),**self.details})


def psi_state(a,b,bits):
    aa=set(Tree(a).labels(bits).values())-{0};bb=set(Tree(b).labels(bits).values())-{0}
    return len(bb-aa)


def psi_episodes(r):
    """Cut on actual SET carrier containment, without changing physical trees."""
    ps=[psi_state(b['post_A'],b['post_B'],r.bits) for b in r.boundaries]
    initial=psi_state(r.source['initial_A'],r.source['initial_B'],r.bits)
    for row,p in zip(r.boundaries,ps):
        if p==0:assert all(e['sign']==-1 for e in r.events[row['post_A_time']:row['end_time']])
    n=len(r.ops)
    if not n:return [],ps
    if not any(p==0 for p in ps):
        return [{'id':0,'kind':'persistent_positive_Psi','operations':list(range(1,n+1)),
            'A_StepEv':[e['id'] for e in r.events if e['actor']=='A' and e['id'][3]==0],'A':r.A}],ps
    start=0 if initial==0 else next(i+1 for i,p in enumerate(ps) if p==0)%n
    eps=[];current=None;used=set()
    for di in range(n):
        i=(start+di)%n
        if current is None:
            if ps[i]==0:continue
            current={'id':len(eps),'kind':'between_actual_Psi_zero_boundaries','operations':[]}
        current['operations'].append(i+1)
        if ps[i]==0:eps.append(current);current=None
    assert current is None
    for ep in eps:
        ts=set(ep['operations']);steps=[e['id'] for e in r.events if e['actor']=='A' and e['id'][3]==0 and e['id'][1] in ts]
        assert not used.intersection(map(tuple,steps));used.update(map(tuple,steps))
        ep.update(A_StepEv=steps,A=len(steps))
    assert len(used)<=r.A
    return eps,ps


def directional_windows(r,eps,d):
    ws=[];used=set();slots=set()
    for ep in eps:
        bs=[]
        for t in ep['operations']:
            tag,x=r.ops[t-1]
            if tag!='K':continue
            if not bs or bs[-1]['x']!=x:bs.append({'x':x,'ts':[]})
            bs[-1]['ts'].append(t)
        i=0
        while i<len(bs):
            w=inherited_distortion.shadow_candidate(r,bs,i,d,len(bs)-i)
            if w is None:i+=1;continue
            assert not used.intersection(w['operations']);used.update(w['operations'])
            rb=[]
            for t in w['retained']:
                x=r.ops[t-1][1]
                if not rb or rb[-1]['x']!=x:rb.append({'x':x,'ts':[]})
                rb[-1]['ts'].append(t)
            witnesses=[]
            for a,b in zip(rb,rb[1:]):
                event=A_gap(r,a['ts'][-1],b['ts'][0]);slot=tuple(event[1:3])
                assert slot not in slots and event in ep['A_StepEv'];slots.add(slot);witnesses.append(event)
            w.update(episode=ep['id'],original_A_transition_witnesses=witnesses);ws.append(w);i+=w['block_span']
    assert sum(w['domain_size'] for w in ws)<=2*len(slots)<=2*r.A
    return ws


def comparisons(r,events,eps,directions=(1,-1)):
    saved=restart_module.restart_windows;results=[]
    try:
        for d in directions:
            restart_module.restart_windows=lambda rr,ee:directional_windows(rr,ee,d)
            z=restart_module.restart_analysis(r,events,eps)
            z['comparison_orientation']=d;results.append(z)
    finally:restart_module.restart_windows=saved
    paid={};destloads=Counter();slots=Counter()
    for z in results:
        for w in z['windows']:
            for e in w['original_A_transition_witnesses']:slots[tuple(e)]+=1
        for e in z['paid_original_gaps']:paid.setdefault(digest(e['rho']),{**e,'comparison_orientation':z['comparison_orientation']})
    assert max(slots.values(),default=0)<=len(directions)
    return {'systems':results,'paid':list(paid.values()),'maximum_A_witness_load':max(slots.values(),default=0),
        'sum_J':sum(z['sum_J'] for z in results),'bound_coefficient_Cseq':6*len(directions)}


def original_residual(r):
    c=current_classification(r)
    old=restart_module.restart_analysis(r,c['unhandled'],actual_mismatch_episodes(r))
    paid={digest(e['rho']) for e in old['paid_original_gaps']}
    return [e for e in c['unhandled'] if digest(e['rho']) not in paid],c,old


def metrics(r,events):
    parents=parent_sets(events);eq=[b['post_A']==b['post_B'] for b in r.boundaries]
    eps,ps=psi_episodes(r);new=comparisons(r,events,eps);paid={digest(e['rho']) for e in new['paid']}
    remain=[e for e in events if digest(e['rho']) not in paid]
    largest=0;run=0
    for v in eq+eq:
        run=0 if v else run+1;largest=max(largest,min(len(eq),run))
    return {'source':r.source['name'],'family':r.source.get('family','inherited'),'population':len(r.keys),
        'operations':len(r.ops),'A':r.A,'Q_B':r.Q,'R_star':len(events),'parents':parents,'events':events,
        'new_comparison':new,'remaining':remain,'Psi_after_operations':ps,'Psi_episodes':eps,
        'equality_boundaries':[i+1 for i,e in enumerate(eq) if e],'longest_no_equality_operations':largest,
        'genuine_KEEP_support':sorted(r.M),'S':sorted(r.S),'I':sorted(r.I),
        'ratios':{'R_star_over_A':str(Fraction(len(events),r.A)) if r.A else None,'Q_over_A':str(Fraction(r.Q,r.A)) if r.A else None},
        'A_StepEv':[e['id'] for e in r.events if e['actor']=='A' and e['id'][3]==0],
        'B_doubles':[[t,j,d['g']] for (t,j),d in r.doubles.items()],
        'trace_hash':digest(r.events),'independent_original_operations':r.independent_checks,'complete_paired_closure':r.closed}
