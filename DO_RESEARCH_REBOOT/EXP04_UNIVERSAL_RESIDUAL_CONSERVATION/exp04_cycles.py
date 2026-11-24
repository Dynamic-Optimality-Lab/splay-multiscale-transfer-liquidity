from exp04_core import *
from exp04_sources import first_corpus
from exp04_boundary import edge_audit


def physical_lifecycles(r,events):
    parents=parent_sets(events);records=[];loads=Counter()
    for kind,ids in parents['sets'].items():
        for t,j in ids:
            d=r.U[(t,j)];g=d['g'];row=r.boundaries[t-1];x=row['x']
            h=ancestry_history(r,g,x);loss=last_A_loss(r,h,row['post_A_time'])
            if loss:loads[tuple(loss['id'])]+=1
            present=ancestor(Tree(row['post_A']),g,x)
            bchanges=[e for e in h['changes'] if e['id'][0]=='B']
            bcont=None
            if loss:
                bcont=h['initial_relation']['B']
                for change in bchanges:
                    if change['time']<=loss['time']:bcont=change['present_after']
                lo=loss['unrolled_time'];hi=row['post_A_time']
                for e in bchanges:
                    lifted=e['time'] if e['time']<=hi else e['time']-r.T
                    if lo<lifted<=hi and not e['present_after']:bcont=False
            records.append({'original_parent':[t,j],'type':kind,'g':g,'target':x,'history':h,'last_A_loss':loss,
                'g_is_A_ancestor_post_A':present,'B_continuous_from_last_A_loss':bcont,
                'A_path':row['A_path'],'B_path':row['B_path'],'original_parent_certificate':d,
                'gaps':[e for e in events if e['original_parent']==[t,j]]})
    return {'source':r.source['name'],'parents':records,'last_loss_loads':{str(list(k)):v for k,v in loads.items()},
        'maximum_load':max(loads.values(),default=0),'undefined':sum(p['last_A_loss'] is None for p in records)}


if __name__=='__main__':
    resume='--resume' in sys.argv
    meter=Meter('EXP04_cycles_2_3_resume' if resume else 'EXP04_cycles_2_3')
    sources=first_corpus();results=[];life=[];edges=[];start=0
    if resume:
        checkpoint=json.loads((ROOT/'EXP04_NEW_SOURCE_CHECKPOINT.json').read_text());start=checkpoint['completed']
        sources[:start]=checkpoint['sources'];results=json.loads((ROOT/'EXP04_NEW_RESULTS.json').read_text())
        life=json.loads((ROOT/'EXP04_NEW_LIFECYCLES.json').read_text());edges=json.loads((ROOT/'EXP04_NEW_EDGE_AUDIT.json').read_text())
    for i in range(start,len(sources)):
        s=sources[i]
        r=Replay(s);events,c,old=original_residual(r);m=metrics(r,events)
        m['old_R6_other']=len(c['other']);m['old_unhandled']=len(c['unhandled'])
        m['old_restart_paid']=old['paid_gap_count'];m['original_rows']=c['original_rows']
        results.append(m);lf=physical_lifecycles(r,events);life.append(lf);edges.append(edge_audit(r,events))
        s.update(trace_hash=digest(r.events),A=r.A,Q_B=r.Q,closing_A=r.a.state(),closing_B=r.b.state())
        if s['family']=='protected_fringe' and any(e['type']=='G' for e in events):
            file=f"EXP04_TRACE_{digest(s['name'])[:12]}.json"
            write(file,{'source':s,'events':r.events,'boundaries':r.boundaries,'R_star':events,'new_comparison':m['new_comparison']})
            m['full_trace_file']=file
        print(i+1,s['name'],'R*',dict(Counter(e['type'] for e in events)),
            'paid',len(m['new_comparison']['paid']),'remaining',len(m['remaining']),'eq',len(m['equality_boundaries']),
            'lossload',lf['maximum_load'],'undefined',lf['undefined'],flush=True)
        write('EXP04_NEW_SOURCE_CHECKPOINT.json',{'planned':len(sources),'completed':i+1,'sources':sources[:i+1]})
        write('EXP04_NEW_RESULTS.json',results);write('EXP04_NEW_LIFECYCLES.json',life);write('EXP04_NEW_EDGE_AUDIT.json',edges)
        del r
    meter.details.update(new_sources=len(sources),new_R_star=sum(r['R_star'] for r in results),
        remaining=sum(len(r['remaining']) for r in results));meter.success=True
