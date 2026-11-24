from base2 import *
from native2 import adapter
from residual0 import gap_costs,E_stream
import ast,gc

def ordered(s,p,b,star):
    import exp04_core,exp04_monotone
    r=adapter(s,p,b);eps,_=exp04_core.psi_episodes(r)
    carrier=exp04_core.comparisons(r,star,eps);f1={digest(e['rho']) for e in carrier['paid']}
    left=[e for e in star if digest(e['rho']) not in f1]
    mono=exp04_monotone.monotone_analysis(r,left,eps);f2={digest(e['rho']) for e in mono['paid']}
    F=f1|f2;gs=gap_costs(s,p['boundaries'])
    C=[e for e in star if digest(e['rho']) not in F and e['original_parent'][1]>2*gs[e['consumer']]]
    E=E_stream(p,C);ei={digest(e['rho']) for e in E}
    xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(p['original_S'])}
    raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
    assert raw<=10*b['A']
    H=[e for e in star if p['boundaries'][e['consumer']-1]['q']>2*gs[e['consumer']]]
    hi={digest(e['rho']) for e in H}
    D=[e for e in star if digest(e['rho']) not in F|ei|hi]
    def quota(pool):
        packs=defaultdict(lambda:defaultdict(list))
        for e in pool:packs[e['consumer']][tuple(e['original_parent'])].append(e)
        rows=[];selected=set()
        for h,ps in sorted(packs.items()):
            keys=sorted(ps);picked=keys[:2*gs[h]]
            for key in picked:selected.update(digest(e['rho']) for e in ps[key])
            rows.append({'h':h,'A_gap':gs[h],'distinct_original_parents':keys,'b_h':len(keys),'selected':picked})
        return rows,selected
    qr,qs=quota(D);overflow=[e for e in D if digest(e['rho']) not in qs];assert not overflow
    diagnostic=[e for e in star if digest(e['rho']) not in F|ei]
    dh,dqs=quota(diagnostic)
    assignments={'carrier':[],'skipped_rank':[],'E_old':[],'H_all':[],'Q_D':[],'overflow':[]}
    for e in star:
        key=digest(e['rho']);kind=('carrier' if key in f1 else 'skipped_rank' if key in f2 else
            'E_old' if key in ei else 'H_all' if key in hi else 'Q_D' if key in qs else 'overflow')
        assignments[kind].append(e)
    assert sum(map(len,assignments.values()))==len(star)
    return {'source':s['name'],'source_sha256':digest(s),'A':b['A'],'raw_periodic_certificate':raw,
        'native_original_R_star':star,'frozen_carrier_eligible':carrier['paid'],'frozen_skipped_after_carrier_eligible':mono['paid'],
        'C_old':C,'E_old':E,'periodic_H_eligible_noncheap':H,'exact_D':D,'quota_rows':qr,
        'disjoint_original_assignments':assignments,'actual_S_UU':0,
        'no_H_diagnostic':{'scope':'Counterfactual pool only; NOT original D or a redefined residual.',
            'pool':diagnostic,'quota_rows':dh,'all_selected':all(digest(e['rho']) in dqs for e in diagnostic)}}

if __name__=='__main__':
    meter=Meter('literal_ordered_selectors');out=[]
    ss=load(ROOT/'RUN_B_SOURCE_CATALOG.json');rows=load(ROOT/'RUN_B_RESULTS.json')
    for i in (0,1,2):
        s=ss[i];p=load(ROOT/f'RUN_B_PHYS_{i:02}.json');b=load(ROOT/f'RUN_B_BIRTH_{i:02}.json')
        star=rows[i]['original_R_star'];assert star is not None
        z=ordered(s,p,b,star);write(f'ORDERED_{i:02}.json',z)
        out.append({'index':i,'source':s['name'],'counts':{k:len(v) for k,v in z['disjoint_original_assignments'].items()},
            'C_old':len(z['C_old']),'no_H_diagnostic_all_quota_selected':z['no_H_diagnostic']['all_selected'],
            'actual_S_UU':0})
        print('PASS literal selectors',i,out[-1]['counts'],flush=True)
        del p,b,z;gc.collect()
    write('ORDERED_RESULTS.json',out);meter.ok=True
