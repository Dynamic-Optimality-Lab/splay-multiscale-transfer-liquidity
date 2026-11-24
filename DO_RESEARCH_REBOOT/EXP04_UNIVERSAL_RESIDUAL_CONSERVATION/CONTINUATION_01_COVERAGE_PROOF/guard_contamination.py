from core import *
from return_normalization import guarded_skeleton


def candidate(p,pat,repeats=256):
    n=2**(p+2)+1
    patterns=[[2,n-2,n//3,2*n//3],
              [2,n-2,n//4,3*n//4,n//2],
              [2,n-2,n//2,n-4],
              [2,n-2,n//3,n-4,2*n//3,n-6],
              [2,n//4,n//2,3*n//4,n-2],
              [2,n-2,n//4,3*n//4,3,n-3,n//2],
              [2,n-2,n//2,n-4,n//3,n-6,n//4],
              [2,n-2,n-4,n-6,n-8,n-10,n-12,n-14]]
    pattern=patterns[pat];base=both_oscillations(p,0,0,'bitreverse',right_low=2)
    cut=2*n+1;word=base['operations'];loop=ops('K',pattern)*repeats
    assert word[cut:cut+2]==[['K',2],['K',5]]
    word=word[:cut]+loop+[['K',2],['K',5]]+loop+word[cut+2:]
    return source(f'guardcontam_p{p}_pat{pat}_r{repeats}',n,word,
        family='guard_contamination',p=p,pattern=pattern,repeats=repeats)


if __name__=='__main__':
    meter=Meter('CONT01_guard_contamination');sources=[];out=[]
    for p,pat,repeats in [(6,i,256) for i in range(6)]+[(7,i,192) for i in (0,1)]:
        s=candidate(p,pat,repeats);r=Replay(s,certify=False)
        normalized=guarded_skeleton(r,list(range(1,len(r.ops)+1)))
        row={'source':s['name'],'A':r.A,'Q_B':r.Q,'normalized':normalized,
            'full_period_eligible':normalized['D']<=5*r.A,'independent_operations':r.independent_checks,
            'original_Pi_certification':'not run at screening; guard does not require Pi'}
        s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
        sources.append(s);out.append(row)
        print(s['name'],'A',r.A,'D',normalized['D'],'guards',len(normalized['protected_operations_in_span']),
            'full funded',row['full_period_eligible'],flush=True)
        write('GUARD_CONTAMINATION_SOURCES.json',sources);write('GUARD_CONTAMINATION_RESULTS.json',out)
        if not row['full_period_eligible']:
            ev,_,_=original_residual(r);row['R_star']=ev
            row['original_Pi_certification']='fresh original classification completed'
            row['trace_file']=f'TRACE_{digest(s["name"])[:12]}.json'
            write(row['trace_file'],{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':ev})
            write('GUARD_CONTAMINATION_RESULTS.json',out);break
        del r
    meter.success=True;meter.details['sources']=len(sources)
