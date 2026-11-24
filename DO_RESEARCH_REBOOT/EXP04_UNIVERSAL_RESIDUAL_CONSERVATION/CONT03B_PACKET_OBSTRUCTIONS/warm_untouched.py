from campaign3b import *
from fast_physics import FullTree
from epoch_payment import from_replay
from accounting import audit
from new_payments import compact_trace
from exp04_monotone import monotone_analysis
from periodic_payment import periodic_cost
import random,gc


def shape(n,seed):
    t=Tree(vine(range(1,n+1)));xs=list(range(1,n+1));random.Random(seed).shuffle(xs)
    for x in xs:Replay.plain_splay(t,x)
    return t.state()


def make(n,seed,length,mode='shallow'):
    rng=random.Random(seed);assert (n-1)%3==0
    M=list(range(1,n+1,3));diag=shape(n,seed)
    # A real full scan reaches the complete physical left vine; the odd
    # spacing active sweep then produces the gap-refined marked right vine.
    a=FullTree(diag);b=FullTree(diag);prep=ops('D',list(range(1,n+1))+M[-2::-1])
    for tag,x in prep:a.splay(x,b,'A')
    aa=a.state();assert closure(Tree(aa),M)==set(M)
    body=[]
    for k in range(length):
        if mode=='pairs':
            v=M[k] if k<len(M) else rng.choice(M)
            x=rng.choice([x for x in M if x!=v])
            for tag,y in [('D',x),('K',v),('K',x)]:
                ac,_,_,_=a.splay(y,b,'A');body.append([tag,y])
            assert ac==1
            continue
        candidates=[];todo=[(a.root,0)]
        while todo:
            x,d=todo.pop()
            if x in M and x!=a.root:candidates.append(x)
            if d<2:
                if a.l[x]:todo.append((a.l[x],d+1))
                if a.r[x]:todo.append((a.r[x],d+1))
        assert candidates;x=rng.choice(candidates);aa_cost,_,_,_=a.splay(x,b,'A');assert aa_cost==1
        body.append(['K',x])
    reset=ops('D',M+M[-2::-1])
    for tag,x in reset:a.splay(x,b,'A')
    assert a.state()==aa
    V=body+reset;states={};saved=[]
    for j in range(65):
        if b.code in states:
            start=states[b.code];bb=saved[start];period=V*(j-start)
            stem='warm' if mode=='shallow' else mode
            return {'name':f'C3B_{stem}_n{n}_s{seed}_l{length}','family':'A_untouched_fringe_warmed_'+mode+'_word',
                'initial_A':aa,'initial_B':bb,'diagonal_initial':diag,'reaching_prefix':prep+V*start,
                'operations':period,'marked_targets':M,'body':body,'reset':reset,
                'warmup_periods':start,'cycle_periods':j-start,
                'reachability':'explicit original A-only marked preparation, then exact physical warm periods from a common diagonal'},None
        states[b.code]=j;saved.append(b.state())
        for tag,x in body:
            if tag=='K':b.splay(x,a,'A')
    return None,{'n':n,'seed':seed,'length':length,'status':'no exact B cycle detected in64 warm periods'}


def physical_screen(s):
    a=Tree(s['initial_A']);b=Tree(s['initial_B']);M={x for tag,x in s['operations'] if tag=='K'}
    S=closure(b,M);A_allowed=set(s['marked_targets'])
    # Record actual B grandparents; signs and Pi remain the original oracle's job.
    hits=[];cost=0;A=0;unmarked_g=set()
    for h,(tag,x) in enumerate(s['operations'],1):
        ap=a.path(x);A+=len(ap)//2;Replay.plain_splay(a,x)
        if tag=='K':
            path=b.path(x);q=(len(path)-1)//2;cost+=q
            for j in range(1,q+1):
                g=path[-1-2*j]
                if g not in A_allowed:
                    unmarked_g.add(g)
                    if j>=3 and h>1 and s['operations'][h-2][0]=='K':hits.append([h,j,g])
            Replay.plain_splay(b,x)
    assert a.state()==s['initial_A'] and b.state()==s['initial_B']
    ss=sorted(S);gaps=[]
    marks=sorted(M)
    for x,y in zip(marks,marks[1:]):gaps.append([x,y,len([g for g in ss if x<g<y])])
    return {'A':A,'Q_B':cost,'S':ss,'B_core_unmarked_keys':sorted(S-M),
        'unmarked_B_grandparents':sorted(unmarked_g),'targeted_upper_candidates':hits,
        'marked_rank_gap_unmarked_counts':gaps}


def audit_general(r,star):
    eps,_=psi_episodes(r);car=comparisons(r,star,eps);ids={digest(e['rho']) for e in car['paid']}
    after=[e for e in star if digest(e['rho']) not in ids];mono=monotone_analysis(r,after,eps)
    mids={digest(e['rho']) for e in mono['paid']};after=[e for e in after if digest(e['rho']) not in mids]
    gaps=keep_gaps(r);prefix=[e for e in after if e['original_parent'][1]<=2*gaps[e['consumer']]['A']]
    pids={digest(e['rho']) for e in prefix};C=[e for e in after if digest(e['rho']) not in pids]
    own=[e for e in C if r.U[tuple(e['original_parent'])]['g'] in r.boundaries[e['consumer']-1]['A_path'][:-1]]
    E=from_replay(r,C);unpaid=E['repeat_original_gaps']+E['A_demotion_free_key_original_gaps']
    raw=periodic_cost([x for tag,x in r.ops if tag=='K'],r.S)
    assert raw['B_cyclic']<=10*r.A
    return {'source':r.source['name'],'A':r.A,'Q_B':r.Q,'original_R_star':star,
        'C_after_frozen_and_prefix':C,'first_use_E_C':E,'epoch_unpaid_original_C':unpaid,
        'ordered_assignments':{'carrier':car['paid'],'skipped_rank':mono['paid'],'prefix':prefix,
            'own_path':own,'old_hybrid':[e for e in C if e not in own]},
        'old_raw_periodic_certificate':raw,'literal_R_upper':[],
        'all_original_S':sorted(r.S),'full_physical_keys':r.keys}


if __name__=='__main__':
    meter=Meter('warm_untouched_search');screen=[];sources=[];results=[];failed=[];full=0
    for n in (25,49,61):
        for seed in range(1,65):
            s,fail=make(n,seed,128 if n<61 else 256)
            if fail:failed.append(fail);continue
            z=physical_screen(s);s.update(A=z['A'],Q_B=z['Q_B']);sources.append(s)
            row={'source':s['name'],'population':n,**z,'full_original_Pi_classification':False}
            if z['targeted_upper_candidates'] and full<24:
                r=Replay(s);star,_,_=original_residual(r);a=audit_general(r,star)
                full+=1;row.update(full_original_Pi_classification=True,original_R_star=star,ordered_accounting=a,
                    original_R6_count=r.counts['R6'],independent_original_operations=r.independent_checks)
                s.update(trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
                unpaid=a['first_use_E_C']['A_demotion_free_key_original_gaps']+a['first_use_E_C']['repeat_original_gaps']
                if unpaid:compact_trace(r,star,'UNTOUCHED_COUNTEREXAMPLE_TRACE.json');row['trace_file']='UNTOUCHED_COUNTEREXAMPLE_TRACE.json'
                print(s['name'],'S',len(r.S),'R6',r.counts['R6'],'Rstar',len(star),'C',len(a['C_after_frozen_and_prefix']),
                      'epoch-unpaid',len(unpaid),flush=True)
                del r;gc.collect()
            screen.append(row);write('WARM_SOURCES.json',sources);write('WARM_RESULTS.json',screen)
            write('INCOMPLETE_WARM_PROTOTYPES.json',failed)
            if row.get('ordered_accounting',{}).get('epoch_unpaid_original_C'):
                meter.success=True;meter.details.update(complete_sources=len(sources),full_original_oracles=full);sys.exit(0)
            if full>=24:break
        if full>=24:break
    meter.success=True;meter.details.update(complete_sources=len(sources),full_original_oracles=full)
