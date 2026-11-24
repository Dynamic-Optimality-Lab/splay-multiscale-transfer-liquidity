from exp04_adversarial import *
from exp04_sources import third_corpus


if __name__=='__main__':
    meter=Meter('EXP04_sparse_lifecycle');sources=third_corpus();out=[];life=[]
    for i,s in enumerate(sources):
        r=Replay(s);events,c,old=original_residual(r);row=metrics(r,events);lf=physical_lifecycles(r,events)
        z=enriched(r,row);row['following_classes']=z;out.append(row);life.append(lf)
        s.update(trace_hash=digest(r.events),A=r.A,Q_B=r.Q,closing_A=r.a.state(),closing_B=r.b.state())
        print(i+1,s['name'],'S',len(r.S),'M',len(r.M),'R*',dict(Counter(e['type'] for e in events)),
            'undefinedloss',lf['undefined'],'maxlossload',lf['maximum_load'],'remaining',len(z['remaining']),flush=True)
        write('EXP04_SPARSE_SOURCES.json',sources[:i+1]);write('EXP04_SPARSE_RESULTS.json',out);write('EXP04_SPARSE_LIFECYCLES.json',life)
    meter.success=True;meter.details.update(sources=len(sources),undefined_loss=sum(z['undefined'] for z in life))
