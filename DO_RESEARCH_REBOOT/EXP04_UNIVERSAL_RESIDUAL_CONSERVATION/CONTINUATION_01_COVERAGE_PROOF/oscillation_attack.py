from core import *
from backward import tail_test


if __name__=='__main__':
    meter=Meter('CONT01_two_sided_oscillation');sources=[];rows=[]
    for left,right in ((0,0),(16,16),(64,64),(256,256)):
        s=both_oscillations(4,left,right);r=Replay(s);ev,c,old=original_residual(r);row=metrics(r,ev);other=enriched(r,row)
        eps,_=psi_episodes(r);den=density_analysis(r,ev,eps)
        remhash={digest(e['rho']) for e in den['remaining']};escape=[e for e in other['remaining'] if digest(e['rho']) in remhash]
        life=physical_lifecycles(r,ev);tails=tail_test(r,ev)
        result={'source':s['name'],'A':r.A,'Q_B':r.Q,'R_star':ev,'carrier_and_monotone':other,
            'frozen_density':den,'frozen_combined_escape':escape,'tail_alternative':tails,'lifecycles':life,
            'trace_hash':digest(r.events),'independent_operations':r.independent_checks}
        sources.append({**s,'A':r.A,'Q_B':r.Q,'trace_hash':digest(r.events),'closing_A':r.a.state(),'closing_B':r.b.state()});rows.append(result)
        if escape or any(not t['funded_prefix_exists'] for t in tails):
            file=f'TRACE_{digest(s["name"])[:12]}.json';write(file,{'source':sources[-1],'events':r.events,'boundaries':r.boundaries,
                'R_star':ev,'frozen_combined_escape':escape});result['trace_file']=file
        print(s['name'],'A',r.A,'Q',r.Q,'R*',len(ev),'combined escape',len(escape),
            'failed tails',[t['consumer'] for t in tails if not t['funded_prefix_exists']],flush=True)
        write('SOURCE_WITNESSES.json',sources);write('OSCILLATION_RESULTS.json',rows)
        if escape:break
    meter.success=True;meter.details.update(sources=len(rows),escaping_gaps=sum(len(r['frozen_combined_escape']) for r in rows))
