from core import *
from return_normalization import guarded_skeleton
from gap_payment import keep_gaps,hard_guarded


def candidate(p=7,pat=0,repeats=192):
    n=2**(p+2)+1;k=(n-1)//8
    patterns=[[2]+[n-2-i*k for i in range(8)],
              [2]+[n-2-i*((n-1)//6) for i in range(6)],
              [2]+[n-2-i*((n-1)//4) for i in range(4)],
              [2,n-2,7*k+1,6*k+1,5*k+1,4*k+1,3*k+1,2*k+1,k+1]]
    pattern=patterns[pat];base=both_oscillations(p,0,0,'bitreverse',right_low=2)
    cut=2*n+1;word=base['operations'];loop=ops('K',pattern)*repeats
    assert word[cut:cut+2]==[['K',2],['K',5]]
    word=word[:cut]+loop+[['K',2],['K',5]]+loop+word[cut+2:]
    return source(f'wideguard_p{p}_pat{pat}_r{repeats}',n,word,
        family='wide_rank_guard_contamination',p=p,pattern=pattern,repeats=repeats)


if __name__=='__main__':
    meter=Meter('CONT01_wide_rank_guard_attack');sources=[];out=[]
    for pat in range(4):
        s=candidate(pat=pat);r=Replay(s,certify=False)
        normalized=guarded_skeleton(r,list(range(1,len(r.ops)+1)))
        gaps=keep_gaps(r);hnorm=hard_guarded(r,list(range(1,len(r.ops)+1)),gaps)
        row={'source':s['name'],'A':r.A,'Q_B':r.Q,'normalized':normalized,
            'hard_normalized':hnorm,'full_period_eligible':normalized['D']<=5*r.A,
            'hard_full_period_eligible':hnorm['D']<=5*r.A,'independent_operations':r.independent_checks,
            'original_Pi_certification':'not run at screening; physical guards do not require Pi'}
        s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
        sources.append(s);out.append(row)
        print(s['name'],'A',r.A,'D_G',normalized['D'],'D_H',hnorm['D'],
              'guards',len(normalized['protected_operations_in_span']),
              'full funded',row['full_period_eligible'],flush=True)
        write('WIDE_GUARD_SOURCES.json',sources);write('WIDE_GUARD_RESULTS.json',out)
        if not row['full_period_eligible']:
            ev,_,_=original_residual(r);row['R_star']=ev
            row['original_Pi_certification']='fresh original classification completed'
            row['trace_file']=f'TRACE_{digest(s["name"])[:12]}.json'
            write(row['trace_file'],{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':ev})
            write('WIDE_GUARD_RESULTS.json',out);break
        del r
    meter.success=True;meter.details['sources']=len(sources)
