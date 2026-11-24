from exp04_adversarial import *
from exp04_sources import last_corpus
from exp04_density import density_analysis


if __name__=='__main__':
    meter=Meter('EXP04_cycles_6_7');sources=last_corpus();results=[];life=[];density=[]
    for i,s in enumerate(sources):
        r=Replay(s);events,c,old=original_residual(r);row=metrics(r,events);m=enriched(r,row);lf=physical_lifecycles(r,events)
        eps,_=psi_episodes(r);den=density_analysis(r,events,eps) if events else {'windows':[],'paid':[],'remaining':[]}
        remaining_hash={digest(e['rho']) for e in den['remaining']}
        m['after_density']=[e for e in m['remaining'] if digest(e['rho']) in remaining_hash]
        row['following_classes']=m;results.append(row);life.append(lf);density.append({'source':s['name'],**den})
        s.update(trace_hash=digest(r.events),A=r.A,Q_B=r.Q,closing_A=r.a.state(),closing_B=r.b.state())
        if m['remaining'] or lf['undefined']:
            file=f"EXP04_TRACE_{digest(s['name'])[:12]}.json"
            write(file,{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':events,
                'before_density':m['remaining'],'after_density':m['after_density'],'lifecycles':lf,'density':den})
            row['full_trace_file']=file
        print(i+1,s['name'],'A',r.A,'Q',r.Q,'M/S',len(r.M),len(r.S),'R*',dict(Counter(e['type'] for e in events)),
            'aftermono',len(m['after_monotone']),'L/A',m['rank_travel']['ratio'],'beforedensity',len(m['remaining']),
            'remaining',len(m['after_density']),'undefinedloss',lf['undefined'],flush=True)
        write('EXP04_FINAL_CYCLE_SOURCES.json',sources[:i+1]);write('EXP04_FINAL_CYCLE_RESULTS.json',results)
        write('EXP04_FINAL_CYCLE_LIFECYCLES.json',life);write('EXP04_FINAL_CYCLE_DENSITY.json',density)
        del r
    meter.success=True;meter.details.update(new_sources=len(sources),remaining=sum(len(s['following_classes']['after_density']) for s in results))
