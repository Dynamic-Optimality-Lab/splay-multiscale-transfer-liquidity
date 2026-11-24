from core import *
from return_normalization import guarded_skeleton


def candidate(p,pattern_index,repeats=64):
    n=2**(p+2)+1;base=both_oscillations(p,0,0,'bitreverse',right_low=2);word=base['operations']
    patterns=[[2,n-2,n//2],[2,n-2,n-4],[2,n-2,n-4,n-6,2*n//3],
        [2,n-2,3*n//4,n-4,n//2,n-6,5*n//8],
        [2,n-2,n//2,n-4,n//3,n-6,n//4],
        [2,n-2,3*n//4,n//2,5*n//8,7*n//8],
        [2,n-2,4,n-4,6,n-6,n//2],
        [2,n-2,n-4,n-6,n-8,n-10,n-12,n-14]]
    pattern=patterns[pattern_index];loop=ops('K',pattern)*repeats
    cut=2*n+1
    newword=word[:cut]+loop+[['K',2]]+[word[cut+1]]+loop+word[cut+2:]
    # word has an identity KEEP2 before its original hit because the base
    # used return_to_two=True with a zero-length left oscillation.
    assert word[cut]==['K',2] and word[cut+1]==['K',5]
    return source(f'interiorloop_p{p}_pat{pattern_index}_r{repeats}',n,newword,
        family='interior_guarded_loops',p=p,pattern=pattern,repeats=repeats)


if __name__=='__main__':
    meter=Meter('CONT01_interior_guard_falsification');sources=[];out=[]
    for p in (4,5):
        for pat in range(8):
            s=candidate(p,pat);r=Replay(s);ev,_,_=original_residual(r);r.original_R_star=ev
            normalized=guarded_skeleton(r,list(range(1,len(r.ops)+1)))
            row={'source':s['name'],'A':r.A,'Q_B':r.Q,'R_star':ev,'normalized':normalized,
                'full_period_eligible':normalized['D']<=5*r.A,'independent_operations':r.independent_checks}
            s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state());sources.append(s);out.append(row)
            print(s['name'],'R*',len(ev),'A',r.A,'D',normalized['D'],'guards',len(normalized['protected_operations_in_span']),
                'full funded',row['full_period_eligible'],flush=True)
            write('INTERIOR_SOURCES.json',sources);write('INTERIOR_RESULTS.json',out)
            if ev and not row['full_period_eligible']:
                row['trace_file']=f'TRACE_{digest(s["name"])[:12]}.json';write(row['trace_file'],{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':ev})
                write('INTERIOR_RESULTS.json',out);meter.success=True;exit()
    meter.success=True;meter.details.update(sources=len(sources))
