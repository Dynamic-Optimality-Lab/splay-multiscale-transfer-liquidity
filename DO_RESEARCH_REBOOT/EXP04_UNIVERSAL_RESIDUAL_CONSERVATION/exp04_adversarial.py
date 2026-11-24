from exp04_cycles import physical_lifecycles
from exp04_sources import second_corpus
from exp04_monotone import *
from exp04_boundary import edge_audit


if __name__=='__main__':
    meter=Meter('EXP04_cycles_4_5_adversarial');sources=second_corpus();results=[];life=[];edges=[];mono=[]
    for i,s in enumerate(sources):
        r=Replay(s);events,c,old=original_residual(r);row=metrics(r,events);m=enriched(r,row)
        results.append(row);mono.append(m);life.append(physical_lifecycles(r,events));edges.append(edge_audit(r,events))
        s.update(trace_hash=digest(r.events),A=r.A,Q_B=r.Q,closing_A=r.a.state(),closing_B=r.b.state())
        if m['remaining']:
            file=f"EXP04_TRACE_{digest(s['name'])[:12]}.json"
            write(file,{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':events,'after_all_new_classes':m['remaining']})
            row['full_trace_file']=file
        print(i+1,s['name'],'A',r.A,'Q',r.Q,'R*',dict(Counter(e['type'] for e in events)),
            'aftermono',len(m['after_monotone']),'L/A',m['rank_travel']['ratio'],'remaining',len(m['remaining']),flush=True)
        write('EXP04_ADVERSARIAL_SOURCES.json',sources[:i+1]);write('EXP04_ADVERSARIAL_RESULTS.json',results)
        write('EXP04_ADVERSARIAL_MONOTONE.json',mono);write('EXP04_ADVERSARIAL_LIFECYCLES.json',life)
        write('EXP04_ADVERSARIAL_EDGES.json',edges);del r
    meter.details.update(new_sources=len(sources),R_star=sum(s['R_star'] for s in results),
        remaining=sum(len(s['remaining']) for s in mono));meter.success=True
