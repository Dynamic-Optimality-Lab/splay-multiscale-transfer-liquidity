"""Targeted recurrent-source Hall search. No finite-state CD enumeration."""
from fractions import Fraction
from collections import Counter
import random,time
from sharp02_common import *
from sharp02_fast import FastTree,evaluate,recurrent
from sharp02_graph import solve
from sharp01_oracle import vine

SEED=20261111

def zero_run(r):
    n=2*r-1
    seq=[['K',x] for x in list(range(3,n+1,2))+list(range(n-2,2,-2))]
    gamma=seq+[['D',n],['D',1],['K',1],['K',n],['K',1],['D',n],['D',2],['D',n],['D',1]]+seq+[['K',1]]
    C=[['K',3],['K',n]]+[['D',x] for x in range(n-2,2,-2)]+seq+[['K',1]]+[['D',x] for x in range(n,0,-1)]
    return {'name':f'C15_zero_param_r{r}','family':'C15_parametric_zero_run','initial_A':vine(range(1,n+1)),
            'initial_B':vine(range(1,n+1)),'reaching_prefix':[],'operations':gamma+C,'parameter_r':r}

def random_diagonal(n,rng):
    order=list(range(1,n+1));rng.shuffle(order);ch={str(k):[None,None] for k in order};root=order[0]
    for x in order[1:]:
        p=root
        while ch[str(p)][int(x>p)] is not None:p=ch[str(p)][int(x>p)]
        ch[str(p)][int(x>p)]=x
    st={'root':root,'children':ch}
    return {'name':f'random_diagonal_{n}','initial_A':st,'initial_B':st,'reaching_prefix':[]}

def summary(d,res):
    D=res['tight_subset'];demand=sum(d['weights'][i] for i in D)
    return {k:d[k] for k in ('name','n','operations','A','Q','U','C','Delta')}|{
        'Q_over_A':str(Fraction(d['Q'],d['A'])) if d['A'] else None,'U_over_C':str(Fraction(d['U'],d['C'])) if d['C'] else None,
        'matched':res['flow'],'unmatched':res['unmatched'],'tight_nonempty_margin':res['tight_nonempty_margin'],
        'tight_subset':D,'tight_demand':demand,'tight_neighbor_capacity':demand+res['tight_nonempty_margin'] if D else None}

def main(label='adversarial_search_v001'):
    suffix='' if label=='adversarial_search_v001' else '_'+label.rsplit('_',1)[-1]
    def out(name):
        p=Path(name);return BASE/(p.stem+suffix+p.suffix)
    with Run(label,limit=500,seed=SEED,max_candidates=50000,max_orbit=32,record_all_complete_sources=True) as run:
        rng=random.Random(SEED);old=read(OLD/'SHARP01_SOURCE_WITNESSES.json')['sources']
        initial=[s for s in old if s['name'] in ('H_2_1','H_3_1','W_3_1','W_3_1_hit_3','W_5','C15_owner_r7_mirrorFalse','C15_zero_r7_mirrorFalse','C15_zero_r8_mirrorFalse','warmed_random_13','warmed_random_21','warmed_random_33')]
        initial += [zero_run(r) for r in (7,8,10,12,16,24,32)]
        for r in (7,8):assert zero_run(r)['operations']==next(s for s in old if s['name']==f'C15_zero_r{r}_mirrorFalse')['operations']
        # Carefully remove full resets or isolate source phases, then select an
        # ACTUAL recurrent pair. These are new complete sources, not open fragments.
        proposals=[(s,s['operations'],'control') for s in initial]
        for s in initial:
            if 'C15' in s['name']:
                n=len(s['initial_A']['children'])
                for cut in (n,2*n,3*n):
                    if len(s['operations'])>cut+3:proposals.append((s,s['operations'][:-cut],f'remove_suffix_{cut}'))
        elite=[];seen=set();counts=Counter();best=None;parametric=[];found=None;all_hard=[]
        log=out('SHARP02_SEARCH_LOG.jsonl').open('w',encoding='utf-8')
        try:
            for candidate in range(50000):
                if time.process_time()-run.t>480:counts['CPU_bounded_stop']+=1;break
                attack=None
                if candidate<len(proposals):seed,word,method=proposals[candidate]
                elif elite and rng.randrange(100)<72:
                    rec=elite[min(int(rng.expovariate(0.28)),len(elite)-1)];ss=rec['source']
                    diag=ss.get('diagonal_initial',ss['initial_A']);seed={'name':ss['name'],'initial_A':diag,'initial_B':diag,'reaching_prefix':[]}
                    word=[list(z) for z in ss.get('generating_word',ss['operations'])];method='elite_mutation'
                    if rng.randrange(3)==0 and rec['eligible_operations']:
                        at=rng.choice(rec['eligible_operations'])%len(word);kind=rng.randrange(3)
                        if kind==0 and len(word)>3:word.pop(at)
                        elif kind==1:word[at][0]='K' if word[at][0]=='D' else 'D'
                        else:word[at][1]=rng.choice(list(map(int,seed['initial_A']['children'])))
                        attack='eligible_rotation_operation'
                    else:
                        for _ in range(1+rng.randrange(3)):
                            at=rng.randrange(len(word));choice=rng.randrange(7);keys=list(map(int,seed['initial_A']['children']))
                            if choice==0:word[at][0]='D' if word[at][0]=='K' else 'K'
                            elif choice==1 and len(word)>3:word.pop(at)
                            elif choice==2:word.insert(at,[rng.choice(('K','D')),rng.choice(keys)])
                            elif choice==3:word[at][1]=rng.choice(keys)
                            elif choice==4:
                                other=rng.randrange(len(word));word[at],word[other]=word[other],word[at]
                            elif choice==5:
                                end=min(len(word),at+rng.randrange(2,8));word[at:end]=reversed(word[at:end])
                            elif len(word)>8:
                                end=min(len(word),at+rng.randrange(1,5));del word[at:end]
                else:
                    n=rng.choice((7,9,11,13,15,17,21,25,33));seed=random_diagonal(n,rng) if rng.randrange(3)==0 else {'name':f'vine{n}','initial_A':vine(range(1,n+1)),'initial_B':vine(range(1,n+1)),'reaching_prefix':[]}
                    support=rng.sample(range(1,n+1),rng.randrange(3,min(n,9)+1));length=rng.randrange(8,4*n+1)
                    word=[['D' if rng.randrange(100)<rng.choice((20,35,50,65)) else 'K',rng.choice(support) if rng.randrange(5) else rng.randrange(1,n+1)] for _ in range(length)]
                    method='independent_periodic'
                if not word or len(word)>1200:counts['word_bound_reject']+=1;continue
                ss=recurrent(seed,word,f'S02_candidate_{candidate:05d}')
                counts['proposals']+=1
                if ss is None:counts['orbit_bound_reject']+=1;continue
                key=sha_word=hashlib.sha256(repr((ss['initial_A'],ss['initial_B'],ss['operations'])).encode()).hexdigest()
                if key in seen:counts['duplicate_complete_source']+=1;continue
                seen.add(key);counts['complete_sources']+=1
                d=evaluate(ss)
                if d['Delta']>0:
                    write(out('SHARP02_POSSIBLE_SHARP_COUNTEREXAMPLE.json'),{'source':ss,'costs':{k:d[k] for k in ('A','Q','Delta')}})
                    found={'type':'POSSIBLE_III','source':ss};break
                if not d['U']:
                    counts['zero_demand_sources']+=1
                    log.write(json.dumps({**{k:d[k] for k in ('name','n','operations','A','Q','U','C','Delta')},
                        'Q_over_A':str(Fraction(d['Q'],d['A'])) if d['A'] else None,'U_over_C':str(Fraction(d['U'],d['C'])) if d['C'] else None,
                        'matched':0,'unmatched':0,'tight_nonempty_margin':None,'tight_subset':[],
                        'search_candidate':candidate,'method':method,'word_sha256':sha_word,'vacuous':True})+'\n');log.flush()
                    if candidate%50==0:run.check(counts=dict(counts),best=best)
                    continue
                res=solve(d['weights'],d['adj'],d['free']);counts['positive_demand_sources']+=1
                sm=summary(d,res);ss['search_metadata']={'seed':SEED,'candidate':candidate,'method':method,'attack':attack,'word_sha256':sha_word}
                incident=set().union(*d['adj'].values()) if d['adj'] else set()
                log.write(json.dumps(sm|{'search_candidate':candidate,'method':method,'word_sha256':sha_word,'vacuous':False,
                    'broad':res,'weights':d['weights'],'edges':{i:sorted(js) for i,js in d['adj'].items()},
                    'incident_actual_units':{j:d['free'][j] for j in incident},'physical_sorted_keys':sorted(map(int,ss['initial_A']['children']))})+'\n');log.flush()
                margin=res['tight_nonempty_margin'];D=res['tight_subset'];need=sum(d['weights'][i] for i in D)
                eligible_ops=[d['free'][j]['id'][1]-1 for i in D for j in d['adj'][i]]
                score=(margin,-Fraction(need,need+margin) if need+margin>0 else Fraction(-10**6),-Fraction(d['Q'],d['A']),len(ss['operations']),d['n'])
                rec={'score':score,'source':ss,'summary':sm,'eligible_operations':eligible_ops}
                elite.append(rec);elite.sort(key=lambda x:x['score']);elite=elite[:32]
                if best is None or margin<best['tight_nonempty_margin']:
                    best=sm;print(json.dumps({'new_best':sm,'candidate':candidate}),flush=True)
                    write(out('SHARP02_BEST_SOURCE.checkpoint.json'),{'source':ss,'summary':sm,'flow':res})
                if method=='control' and seed['name'].startswith('C15_zero_param'):
                    parametric.append({'source':ss,'summary':sm,'broad':res})
                if res['unmatched']:
                    optimized=solve(d['weights'],d['all_adj'],d['units'],d['capacities'])
                    found={'type':'II' if not optimized['unmatched'] else 'I','source':ss,'summary':sm,'broad':res,'optimized_reservation':optimized}
                    write(out('SHARP02_PRINCIPAL_COUNTEREXAMPLE_RAW.json'),found)
                    print(json.dumps({'HALL_FAILURE':sm,'classification':found['type'],'optimized_unmatched':optimized['unmatched']}),flush=True)
                    break
                if candidate%25==0:
                    run.check(counts=dict(counts),best=best)
                    write(out('SHARP02_SEARCH.checkpoint.json'),{'counts':dict(counts),'best':best,'elite':[{'source':x['source'],'summary':x['summary']} for x in elite]})
        finally:log.close()
        write(out('SHARP02_SEARCH_RESULTS.json'),{'counts':dict(counts),'seed':SEED,'best':best,'counterexample':found,
            'elite':[{'source':x['source'],'summary':x['summary']} for x in elite],'parametric_C15_controls':parametric,
            'completeness':'bounded deterministic parameter cases plus seeded targeted mutations and independent recurrent words; no exhaustive universal coverage'})
        run.check(counts=dict(counts),best=best)
        print(json.dumps({'counts':dict(counts),'counterexample_type':None if found is None else found['type']}))

if __name__=='__main__':
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else 'adversarial_search_v001')
