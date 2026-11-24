from core import *
from backward import tail_test


if __name__=='__main__':
    meter=Meter('CONT01_greedy_ownership_attack');sources=[];out=[]
    for left in (256,512,1024):
        s=both_oscillations(4,left,256,'bitreverse',right_low=2);r=Replay(s)
        ev,_,_=original_residual(r);row=metrics(r,ev);m=enriched(r,row);eps,_=psi_episodes(r);den=density_analysis(r,ev,eps)
        remaining={digest(e['rho']) for e in den['remaining']};escape=[e for e in m['remaining'] if digest(e['rho']) in remaining]
        ss={**s,'A':r.A,'Q_B':r.Q,'trace_hash':digest(r.events),'closing_A':r.a.state(),'closing_B':r.b.state()};sources.append(ss)
        rec={'source':s['name'],'A':r.A,'Q_B':r.Q,'R_star':ev,'carrier_comparison':row['new_comparison'],
            'monotone_and_cycle':m,'frozen_density':den,'escape':escape,'tail':tail_test(r,ev),
            'lifecycles':physical_lifecycles(r,ev),'independent_operations':r.independent_checks}
        if escape:
            h=escape[0]['consumer'];witness=[]
            for start in range(max(0,h-8),h):
                for end in range(h-1,min(len(r.ops),h+10)):
                    q=interval_cost(r.boundaries,r.boundaries[start]['pre_B'],start,end)
                    if q['D']<=4*q['A']:witness.append({'start':start+1,'end':end+1,**q})
            rec['other_eligible_intervals']=witness
            file=f'TRACE_{digest(s["name"])[:12]}.json';write(file,{'source':ss,'events':r.events,'boundaries':r.boundaries,'R_star':ev,'escape':escape});rec['trace_file']=file
        out.append(rec);print(s['name'],'A',r.A,'Q',r.Q,'original R*',len(ev),'combined escape',len(escape),
            'alternative funded intervals',len(rec.get('other_eligible_intervals',[])),flush=True)
        write('OWNERSHIP_SOURCES.json',sources);write('OWNERSHIP_RESULTS.json',out)
        if escape:break
    meter.success=True;meter.details.update(sources=len(sources),escaping_gaps=sum(len(r['escape']) for r in out))
