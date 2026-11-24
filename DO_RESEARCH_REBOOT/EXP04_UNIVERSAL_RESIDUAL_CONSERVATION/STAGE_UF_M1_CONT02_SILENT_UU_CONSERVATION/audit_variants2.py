from base2 import *
from sources2 import padded
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze
from birthc import reconstruct
from native2 import adapter,original_star
from residual0 import gap_costs
import gc,ast

if __name__=='__main__':
    run=sys.argv[1];assert run in ('A','B');meter=Meter('padded_version_'+run)
    if run=='A':ss=load(ROOT/'NEW_SOURCE_CATALOG.json')
    else:ss=[padded(k,L) for k,L in ((4,3),(4,5),(16,3),(32,5),(64,5),(64,1))]
    stem='RUN_'+run;write(stem+'_SOURCE_CATALOG.json',ss);out=[]
    for i,s in enumerate(ss):
        pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
        p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
            'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],
            'boundaries':r.boundaries,'state_pool':pool}
        f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
        assert len(r.S)==len(s['initial_B']['children'])==s['expected_population']
        mb=1<<(s['critical_g']-1);guards=(1<<(s['low_guard']-1))|(1<<(s['high_guard']-1))
        for e in r.events:
            if e['actor']=='A':
                for lab in e['created']:assert not(lab&mb and not lab&guards)
        xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
        raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
        assert raw<=10*r.A
        w={'vertices':[{'parent':v,'type':z['type'],'w':0} for v,z in sorted(ff.items())],
           'R_overflow':0,'zero_reason':'Positive original raw periodic certificate; noncheap paid and all cheap D quota-selected.'}
        an=analyze(s,p,f,w);birth=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,birth)
        star=original_star(native) if len(r.S)<=200 else None
        U={ast.literal_eval(k):v for k,v in birth['U'].items()}
        gs=gap_costs(s,r.boundaries);depth={tuple(z['vertex']):z['distance'] for z in an['C_fringe_depths']}
        pairby=defaultdict(list);starby=defaultdict(list)
        for z in birth['original_pairs']:pairby[tuple(z['parent'])].append(z)
        for z in star or []:starby[tuple(z['original_parent'])].append(z)
        ids=[];cr=[]
        for a,h in enumerate(s['critical_operations']):
            vs=[v for v,d in r.doubles.items() if v[0]==h and d['g']==s['critical_g']];assert len(vs)==1
            v=vs[0];assert v in U and v[1]==s['L']+1;ids.append(v)
            if not a:continue
            assert ff[v]['type']=='C' and tuple(ff[v]['predecessor'])==ids[a-1]
            assert U[v]['creator']==ids[a-1] and U[v]['output_kind']=='grandparent'
            assert not U[ids[a-1]]['exposed'] and gs[h]==1 and depth[v]==3*(s['k']-a)
            r6=[z for z in pairby[v] if z['class']=='R6']
            if run=='B':assert r6
            cr.append({'parent':v,'creator':ids[a-1],'A_gap':gs[h],'distance':depth[v],
                'j':v[1],'quota_early':v[1]<=2*gs[h],'R6':r6,'all_consumed_original_pairs':pairby[v],
                'original_R_star':starby[v] if star is not None else None,
                'S_UU':False,'zero_reason':'Positive original periodic certificate remains active.'})
        for label,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',birth)):
            write(f'{stem}_{label}_{i:02}.json',z)
        row={'index':i,'source':s['name'],'source_sha256':digest(s),'k':s['k'],'L':s['L'],
            'population':len(s['initial_B']['children']),'operations':len(s['operations']),'A':r.A,'Q_B':r.Q,
            'primitives':r.T,'prefix':pref,'raw_periodic_cost':raw,'original_U':len(U),
            'original_R6':len(birth['original_R6']),'original_R_star':star,
            'native_R_star_scope':'EXECUTED' if star is not None else 'NOT_CLASSIFIED',
            'critical_consumers':cr,'actual_S_UU':0,'actual_R_C_deep':0}
        out.append(row);write(stem+'_RESULTS.json',out)
        print('PASS',run,s['k'],s['L'],'R6',len(birth['original_R6']),'late',sum(not z['quota_early'] for z in cr),
            'Rstar',len(star) if star is not None else 'unrun',flush=True)
        del r,pool,p,f,w,an,birth,native,ff;gc.collect()
    meter.info.update(fresh_complete_sources=len(out));meter.ok=True
