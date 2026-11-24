"""Brute-subset and augmenting-path checks of the grouped flow implementation."""
from random import Random
from itertools import combinations
from collections import Counter
from sharp02_common import *
from sharp02_graph import solve

with Run('network_exact_tests_v001',limit=30) as run:
    rng=Random(20261110);cases=0
    for _ in range(240):
        m=rng.randrange(1,6);n=rng.randrange(0,10);w={str(i):rng.randrange(1,4) for i in range(m)}
        units={j:{'gap_index':rng.randrange(1,4)} for j in range(n)}
        adj={str(i):{j for j in units if rng.randrange(3)} for i in range(m)}
        caps={j:rng.randrange(4) for j in range(1,4)}
        for group in (None,caps):
            margins=[]
            for size in range(1,m+1):
                for D in combinations(w,size):
                    near=set().union(*(adj[i] for i in D))
                    if group is None:c=len(near)
                    else:
                        counts=Counter(units[j]['gap_index'] for j in near);c=sum(min(caps[g],counts[g]) for g in caps)
                    margins.append(c-sum(w[i] for i in D))
            res=solve(w,adj,units,group)
            assert res['tight_nonempty_margin']==min(margins)
            assert res['flow']==sum(w.values())+min(0,min(margins))
            cases+=1
    write(BASE/'SHARP02_NETWORK_TESTS.json',{'status':'PASS','exact_random_graph_cases':cases,'all_nonempty_demand_subsets_exhausted_per_case':True})
    run.check(cases=cases);print('PASS',cases,'exact fixed/optimized-reservation graph tests')
