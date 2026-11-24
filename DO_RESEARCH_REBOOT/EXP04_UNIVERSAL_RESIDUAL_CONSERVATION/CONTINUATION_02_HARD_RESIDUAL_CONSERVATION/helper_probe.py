from fast_physics import *


if __name__=='__main__':
    meter=Meter('hard_consumer_helper_probe');out=[];sources=[]
    base=json.loads((C1/'OWNERSHIP_SOURCES.json').read_text())[0]
    # The old consumer is645, after the explicitly inserted KEEP2 at644.
    for helper in (3,4,5,6,7,10,18,34):
        s={k:v for k,v in base.items() if k not in ('A','Q_B','trace_hash','closing_A','closing_B')}
        s['name']=f'C02_helper{helper}_before_K2';s['operations']=base['operations'][:643]+[['D',helper]]+base['operations'][643:]
        f=physical_replay(s);h=646;row=f['rows'][h-1]
        z={'source':s['name'],'A':f['A'],'Q_B':f['Q_B'],'target_consumer':h,
            'local_A':row['a'],'A_gap':row['A_gap'],'q':row['q'],'guard_H':row['guard_H']}
        if row['guard_H']:
            r=Replay(s);ev,_,_=original_residual(r);z['original_R_star']=ev
            z['original_R6_at_target']=[p for p in r.pairs if p['class']=='R6' and p['rho'][0]==h]
            z['independent_original_operations']=r.independent_checks
            s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state())
            r.original_R_star=ev;norm=guarded_skeleton(r,list(range(1,len(r.ops)+1)))
            z['G_normalization']=norm
            write(f'HELPER_TRACE_{helper}.json',{'source':s,'events':r.events,'boundaries':r.boundaries,
                                               'original_R_star':ev,'original_R6':r.pairs})
        else:z['original_Pi_status']='not run: targeted hard guard failed before Pi'
        sources.append(s);out.append(z)
        print(helper,'q',row['q'],'A_gap',row['A_gap'],'H',row['guard_H'],
              'R* target',sum(e['consumer']==h for e in z.get('original_R_star',[])),flush=True)
        write('HELPER_SOURCES.json',sources);write('HELPER_RESULTS.json',out)
    meter.success=True;meter.details.update(complete_original_sources=len(sources),
        Pi_classified=sum('original_R_star' in z for z in out))
