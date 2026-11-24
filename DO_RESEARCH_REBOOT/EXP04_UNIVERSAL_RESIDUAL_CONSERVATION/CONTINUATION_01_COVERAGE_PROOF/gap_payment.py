from core import *
from return_normalization import guarded_skeleton
from types import SimpleNamespace


def keep_gaps(r):
    ks=[t for t,row in enumerate(r.boundaries,1) if row['tag']=='K']
    result={};load=Counter();T=len(r.ops);by_operation=defaultdict(list)
    for e in r.events:
        if e['actor']=='A' and e['id'][3]==0:by_operation[e['id'][1]].append(e['id'])
    for i,h in enumerate(ks):
        previous=ks[i-1];length=(h-previous)%T or T
        ts=[(previous+j-1)%T+1 for j in range(1,length+1)]
        ids=[eid for t in ts for eid in by_operation[t]]
        A=sum(r.boundaries[t-1]['a'] for t in ts);assert len(ids)==A
        load.update(map(tuple,ids));q=r.boundaries[h-1]['q']
        result[h]={'previous_KEEP':previous,'operations':ts,'A':A,'Q_at_KEEP':q,
                   'cheap_q_le_2A_gap':q<=2*A,'A_StepEv':ids}
    assert sum(g['A'] for g in result.values())==(r.A if ks else 0)
    assert max(load.values(),default=0)<=1
    return result


def hard_guarded(r,ts,gaps=None):
    gaps=gaps or keep_gaps(r)
    view=SimpleNamespace(**r.__dict__)
    view.doubles={k:d for k,d in r.doubles.items() if not gaps[k[0]]['cheap_q_le_2A_gap']}
    view.original_R_star=[e for e in getattr(r,'original_R_star',[]) if not gaps[e['consumer']]['cheap_q_le_2A_gap']]
    view.as_tuple=r.as_tuple
    result=guarded_skeleton(view,ts)
    result['guard']='original internal neutral double AND original q(h)>2 A(previous_KEEP,h]'
    return result


if __name__=='__main__':
    meter=Meter('CONT01_KEEP_gap_payment');out=[]
    for sf,rf,field in [('OWNERSHIP_SOURCES.json','OWNERSHIP_RESULTS.json','escape'),
                         ('COLUMN_SOURCES.json','COLUMN_RESULTS.json','frozen_escape')]:
        sources={s['name']:s for s in json.loads((ROOT/sf).read_text())}
        for z in json.loads((ROOT/rf).read_text()):
            if not z[field]:continue
            r=Replay(sources[z['source']]);r.original_R_star=z['R_star'];gaps=keep_gaps(r)
            cheap=[e for e in z['R_star'] if gaps[e['consumer']]['cheap_q_le_2A_gap']]
            hard=[e for e in z['R_star'] if not gaps[e['consumer']]['cheap_q_le_2A_gap']]
            norm=hard_guarded(r,list(range(1,len(r.ops)+1)),gaps)
            out.append({'source':z['source'],'A':r.A,'Q_B':r.Q,'original_R_star':z['R_star'],
                        'cheap_paid':cheap,'hard_residual':hard,'KEEP_gaps':gaps,'hard_guarded_full_period':norm})
            print(z['source'],'cheap',len(cheap),'hard',len(hard),'D_H',norm['D'],'A',r.A,flush=True)
    write('KEEP_GAP_PAYMENT_RESULTS.json',out);meter.success=True
