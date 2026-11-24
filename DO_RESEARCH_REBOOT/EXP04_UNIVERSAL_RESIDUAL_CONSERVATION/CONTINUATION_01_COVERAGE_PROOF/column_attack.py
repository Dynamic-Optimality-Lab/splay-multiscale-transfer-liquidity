from core import *
from all_intervals import all_intervals_through,materialize


if __name__=='__main__':
    meter=Meter('CONT01_marked_column_attack');sources=[];out=[]
    plans=[(2,7,256,256),(2,15,256,256),(3,7,256,256),(4,7,512,512)]
    for p,q,left,right in plans:
        s=both_oscillations(p,left,right,'bitreverse',right_low=2,q=q);r=Replay(s)
        ev,_,_=original_residual(r);row=metrics(r,ev);m=enriched(r,row);eps,_=psi_episodes(r);den=density_analysis(r,ev,eps)
        remain={digest(e['rho']) for e in den['remaining']};escape=[e for e in m['remaining'] if digest(e['rho']) in remain]
        s.update(A=r.A,Q_B=r.Q,trace_hash=digest(r.events),closing_A=r.a.state(),closing_B=r.b.state());sources.append(s)
        z={'source':s['name'],'A':r.A,'Q_B':r.Q,'R_star':ev,'frozen_escape':escape,'monotone_and_cycle':m,
            'carrier':row['new_comparison'],'density':den,'lifecycles':physical_lifecycles(r,ev),'independent_operations':r.independent_checks}
        if escape:
            h=escape[0]['consumer'];audit=all_intervals_through(r,h,stop_at=5)
            # If c5 is impossible the scan is complete, proving intrinsic escape.
            z['all_interval_audit']=audit
            if audit['feasible'][5]:z['c5_witness']=materialize(r,audit['feasible'][5])
            trace=f'TRACE_{digest(s["name"])[:12]}.json';write(trace,{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':ev,'escape':escape});z['trace_file']=trace
        out.append(z);write('COLUMN_SOURCES.json',sources);write('COLUMN_RESULTS.json',out)
        print(s['name'],'A',r.A,'Q',r.Q,'R*',len(ev),'frozen escape',len(escape),'raw c5',
            'not_tested' if not escape else bool(z['all_interval_audit']['feasible'][5]),flush=True)
        if escape and z['all_interval_audit']['feasible'][5] is None:break
    meter.success=True;meter.details.update(sources=len(sources))
