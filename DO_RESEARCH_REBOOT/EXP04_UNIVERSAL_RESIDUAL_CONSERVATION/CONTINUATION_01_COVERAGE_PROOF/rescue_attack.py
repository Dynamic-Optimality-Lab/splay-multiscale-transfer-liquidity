from core import *
from backward import tail_test


if __name__=='__main__':
    meter=Meter('CONT01_rescue_attack');sources=json.loads((ROOT/'SOURCE_WITNESSES.json').read_text());results=[]
    plans=[(4,64,256,'bitreverse',2),(5,32,256,'alternating',2),(5,32,256,'bitreverse',2),
        (6,32,512,'alternating',2),(6,64,512,'bitreverse',2),(6,64,512,'bitreverse',1)]
    for p,left,right,style,low in plans:
        s=both_oscillations(p,left,right,style,right_low=low);r=Replay(s);ev,c,old=original_residual(r)
        row=metrics(r,ev);m=enriched(r,row);eps,_=psi_episodes(r);den=density_analysis(r,ev,eps)
        still={digest(e['rho']) for e in den['remaining']};escape=[e for e in m['remaining'] if digest(e['rho']) in still]
        tails=tail_test(r,ev);s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state());sources.append(s)
        z={'source':s['name'],'A':r.A,'Q_B':r.Q,'R_star':ev,'comparison':m,'density':den,'escape':escape,
            'tail_alternative':tails,'lifecycles':physical_lifecycles(r,ev),'independent_operations':r.independent_checks}
        results.append(z)
        if escape or any(not t['funded_prefix_exists'] for t in tails):
            file=f'TRACE_{digest(s["name"])[:12]}.json';write(file,{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':ev,'escape':escape});z['trace_file']=file
        print(s['name'],'A',r.A,'Q',r.Q,'R*',len(ev),'escape',len(escape),
            'failedtails',[t['consumer'] for t in tails if not t['funded_prefix_exists']],flush=True)
        write('SOURCE_WITNESSES.json',sources);write('RESCUE_ATTACK_RESULTS.json',results)
        if escape:break
    meter.success=True;meter.details.update(completed=len(results),escaping_gaps=sum(len(z['escape']) for z in results))
