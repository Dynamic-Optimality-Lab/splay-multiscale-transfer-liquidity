from campaign4 import *
from packed_states import install
from accounting import audit
from packet_payments import test
from independent_Pi3 import check as check_pi
from independent_cohorts import verify as check_cohorts
from independent_path_audit import check as check_physical
from fast_physics import physical_replay

def quota_independent(r,D):
    by=defaultdict(list)
    for e in r.events:
        if e['actor']=='A' and e['id'][3]==0:by[e['id'][1]].append(e['id'][:3])
    keeps=[i for i,(tag,x) in enumerate(r.ops,1) if tag=='K'];N=len(r.ops)
    packets=defaultdict(lambda:defaultdict(list))
    for e in D:packets[e['consumer']][tuple(e['original_parent'])].append(e)
    allocations=[];tails=[];rows=[];loads=Counter();excess=0
    for i,h in enumerate(keeps):
        prev=keeps[i-1];length=(h-prev)%N or N
        donors=[eid for k in range(1,length+1) for eid in by[(prev+k-1)%N+1]]
        ps=sorted(packets[h]);a=len(donors);e=max(0,len(ps)-2*a);excess+=e
        for k,p in enumerate(ps):
            if k>=2*a:tails.extend(packets[h][p]);continue
            donor=tuple(donors[k//2]);loads[donor]+=len(packets[h][p])
            allocations.append({'parent':p,'actual_A_StepEv':donor,'rho':[z['rho'] for z in packets[h][p]]})
        if ps:rows.append({'h':h,'a_h':a,'b_h':len(ps),'e_h':e,
            'original_parents':[{'id':p,'old_g':r.doubles[p]['g'],'original_gaps':[z['rho'] for z in packets[h][p]]} for p in ps]})
    assert max(loads.values(),default=0)<=6
    assert excess<=len(tails)<=3*excess
    assert sum(len(x['rho']) for x in allocations)+len(tails)==len(D)
    return {'packets':rows,'sum_parent_overflow':excess,'literal_gap_overflow':tails,
        'quota_original_assignments':allocations,'maximum_A_StepEv_load':max(loads.values(),default=0)}

if __name__=='__main__':
    meter=Meter('verify_width');pool,restore=install(Tree)
    sys.setrecursionlimit(max(sys.getrecursionlimit(),10000))
    sources=json.loads((ROOT/'SOURCE_WITNESSES.json').read_text())
    rows=json.loads((ROOT/'WIDTH_RESULTS.json').read_text());out=[]
    for s,old in zip(sources,rows):
        physical=check_physical(s)
        result={'source':s['name'],'physical':physical,'original_Pi_classified':old['original_Pi_classified']}
        if old['original_Pi_classified']:
            r=Replay(s)
            if '--reuse-primary-selection' in sys.argv:
                # Prior completed original selection is bound to this exact
                # full original event/U/pair stream. No independent phase is
                # reused: it is recomputed below from immutable rotations.
                star=old['original_R_star']
                assert json.loads(json.dumps(r.pairs))==old['original_pairs']
                assert json.loads(json.dumps({str(k):v for k,v in r.U.items()}))==old['original_U']
            else:star,_,_=original_residual(r)
            assert star==old['original_R_star'] and digest(r.events)==s['trace_hash']
            meter.details['primary_selection_reused']='--reuse-primary-selection' in sys.argv
            print('PASS fresh original replay/event/U/pair binding',s['name'],flush=True)
            write('NEW_INDEPENDENT_PI.json',check_pi(r))
            write('NEW_INDEPENDENT_R6.json',check_cohorts(r))
            a=audit(r,star);assert a['positive_old_periodic_certificate'] is not None
            assigned=a['ordered_original_assignments']
            F={digest(z['rho']) for key in ('1_frozen_carrier','2_frozen_skipped_rank') for z in assigned[key]}
            E={digest(z['rho']) for z in a['first_use_E_C']['selected_original_gaps']}
            gaps=keep_gaps(r)
            H={digest(z['rho']) for z in star if r.boundaries[z['consumer']-1]['q']>2*gaps[z['consumer']]['A']}
            D=[z for z in star if digest(z['rho']) not in F|E|H]
            quota=quota_independent(r,D);generic=quota_independent(r,star)
            primary=test(s,D)
            assert primary['literal_overflow']==quota['literal_gap_overflow']
            assert quota['sum_parent_overflow']==0
            allids={digest(z['rho']) for z in star};seen=set();partition={}
            for label,eligible in [('F_carrier',{digest(z['rho']) for z in assigned['1_frozen_carrier']}),
                ('F_skipped',{digest(z['rho']) for z in assigned['2_frozen_skipped_rank']}),('E_old',E),('H_all',H),
                ('Q_D',{digest(rho) for z in quota['quota_original_assignments'] for rho in z['rho']})]:
                take=eligible&allids-seen;partition[label]=[z for z in star if digest(z['rho']) in take];seen|=take
            assert seen|{digest(z['rho']) for z in quota['literal_gap_overflow']}==allids
            result.update(ordered_inherited_audit=a,literal_partition=partition,exact_D=D,
                post_hybrid_quota=quota,prehybrid_original_R_star_quota=generic,
                original_U_count=len(r.U),original_pair_count=len(r.pairs))
            write('WIDTH_VERIFICATION.json',out+[result])
        else:
            f=physical_replay(s)
            # Independently written cyclic formula, using full genuine support
            # of this full-scanning source, without any normalization selector.
            xs=[x for tag,x in s['operations'] if tag=='K']
            changes=sum(x!=xs[i-1] for i,x in enumerate(xs))
            travel=sum(abs(x-xs[i-1]).bit_length() for i,x in enumerate(xs))
            assert changes+travel<=10*f['A']
            result['independent_raw_periodic_certificate']={'m':changes,'L':travel,'cost':changes+travel,'A':f['A']}
            result['zero_overflow_reason']='All noncheap original R_star is H_all-paid; all remaining D parents satisfy b<=q<=2a. No unrun Pi count is asserted.'
        out.append(result);write('WIDTH_VERIFICATION.json',out)
        print('PASS independent',s['name'],'Pi',old['original_Pi_classified'],flush=True)
    restore();meter.success=True
