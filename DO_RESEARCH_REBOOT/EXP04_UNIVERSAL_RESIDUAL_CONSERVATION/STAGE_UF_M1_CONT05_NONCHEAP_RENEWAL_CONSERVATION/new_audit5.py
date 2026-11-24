from base5 import *
from model0 import replay,prefix_check
from independent0 import scan_forest,audit_forest
from physical1 import analyze,Edges
from birthc import reconstruct
from native5 import adapter,original_star
from account2 import ordered
from gate1 import signature,packets
from residual0 import gap_costs
from rn1_audit5 import audit as reduction

def audit(s,i,stem='NEW'):
    pref=prefix_check(s);r,pool=replay(s);ff=scan_forest(r);fc=audit_forest(r,ff)
    p={'source':s['name'],'source_sha256':digest(s),'original_S':sorted(r.S),'original_genuine_M':sorted(r.M),
        'events':r.events,'doubles':[{'parent':v,**d} for v,d in sorted(r.doubles.items())],'boundaries':r.boundaries,'state_pool':pool}
    f={'source':s['name'],'vertices':[{'parent':v,**d} for v,d in sorted(ff.items())],**fc}
    a=Edges(s['initial_A']);bad=set(s.get('protected_labels',[]));assert not bad.intersection(a.m[1:])
    for e in r.events:
        if e['actor']=='A':a.step(e);assert not bad.intersection(a.m[1:])
    xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(sorted(r.S))}
    raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs));assert raw<=10*r.A
    w={'vertices':[{'parent':v,'type':d['type'],'w':0} for v,d in sorted(ff.items())],'R_overflow':0,
        'zero_reason':'Positive original raw periodic certificate; cheap original D quota. No new universal residual claim.'}
    an=analyze(s,p,f,w);b=reconstruct(s,p,f,an,weights=w);native=adapter(s,p,b);star=original_star(native)
    acc=ordered(s,p,b,star);red=packets(s,p,b,f,an,acc['exact_D'],star);rn=reduction(s,p,f,b,an,acc)
    sig=signature(p,b,f,an);gs=gap_costs(s,p['boundaries']);h=s['critical_operation'];c=s['creator_operation']
    C={digest(e['rho']) for e in acc['C_old']};E={digest(e['rho']) for e in acc['E_old']}
    Fs={digest(e['rho']) for k in ('carrier','skipped_rank') for e in acc['disjoint_original_assignments'][k]}
    current=[e for e in star if e['consumer']==h]
    candidates=[e for e in current if digest(e['rho']) not in Fs|E and tuple(e['original_parent']) in sig]
    row={'source':s['name'],'source_sha256':digest(s),'index':i,'population':len(r.S),'operations':len(s['operations']),
        'A':r.A,'Q_B':r.Q,'primitives':r.T,'prefix':pref,'raw_periodic_cost':raw,
        'original_R6':len(b['original_R6']),'original_R_star':star,
        'creator':{'h':c,'A_gap':gs[c],'q_B':p['boundaries'][c-1]['q'],'original_R_star':[e for e in star if e['consumer']==c],
            'original_C_old':[e for e in acc['C_old'] if e['consumer']==c]},
        'critical':{'h':h,'A_gap':gs[h],'N_h':sum(v[0]==h for v in sig),
            'R6_parents':sorted({tuple(e['parent']) for e in b['original_R6'] if e['parent'][0]==h}),
            'R_star_parents':sorted({tuple(e['original_parent']) for e in current}),
            'sigma_F_E_negative_gaps':candidates,'canonical_repeated_sigma_edges':[e for e in rn['canonical_renewals'] if e['later_parent'][0]==h and e['later_sigma']]},
        'assigned_counts':{k:len(v) for k,v in acc['disjoint_original_assignments'].items()},
        'actual_S_UU':red['literal_S_UU'],'sum_z_h':red['sum_z_h'],
        'no_H_diagnostic':acc['no_H_diagnostic'],'scope':'Full native original predicates and actual residual; no-H pool remains counterfactual.'}
    for lab,z in (('PHYS',p),('FOREST',f),('WEIGHTS',w),('M1_AUDIT',an),('BIRTH',b),('ORDERED',acc),('REDUCTION',red),('RENEWAL',rn)):
        write(f'{stem}_{lab}_{i:02}.json',z)
    return row

if __name__=='__main__':
    m=Meter('cheap_entry_original_audits');ss=load(ROOT/'NEW_SOURCE_CATALOG.json');out=[]
    for i,s in enumerate(ss):
        row=audit(s,i);out.append(row);write('NEW_RESULTS.json',out)
        print('PASS cheap-entry',i,'creator a',row['creator']['A_gap'],'creator star',len(row['creator']['original_R_star']),
            'creator C_old',len(row['creator']['original_C_old']),'critical N',row['critical']['N_h'],
            'F_E_negative',len(row['critical']['sigma_F_E_negative_gaps']),'renewals',len(row['critical']['canonical_repeated_sigma_edges']),flush=True);gc.collect()
    m.info['fresh_complete_sources']=len(out);m.ok=True
