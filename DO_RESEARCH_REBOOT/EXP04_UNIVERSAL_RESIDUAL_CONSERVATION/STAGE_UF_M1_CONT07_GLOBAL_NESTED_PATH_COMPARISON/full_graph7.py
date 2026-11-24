from base7 import *
from catalog7 import complete_controls
from global7 import fresh_sources
from catalog5 import data
from bisect import bisect_right

def last(items,hi,T):
    if not items:return None
    i=bisect_right([e['time'] for e in items],hi)-1
    if i>=0:return items[i],items[i]['time']
    return items[-1],items[-1]['time']-T

def contained(a,b):return b[0]<=a[0]<=a[1]<=b[1]

def audit(e):
    p,rows,events,ds,vs,gs,A=data(e);T=rows[-1]['end_time'] if rows else 0
    resets=defaultdict(list);promos=defaultdict(list);Aup=defaultdict(list);countA=0;countB=0
    for ev in events():
        if ev['actor']=='A':resets[ev['pivot']].append(ev);Aup[ev['promoted']].append(ev);countA+=1
        else:promos[ev['promoted']].append(ev);countB+=1
    assert countA<=2*A
    def classify(pool,forest=False):
        cols=defaultdict(list)
        for v in sorted(pool):cols[ds[v]['g']].append(v)
        out=[];rootdonors=set()
        for g,vertices in cols.items():
            for i,v in enumerate(vertices):
                u=vertices[i-1];hi=rows[v[0]-1]['post_A_time'];lo=rows[u[0]-1]['end_time']-(T if u[0]>=v[0] else 0)
                ar=last(resets[g],hi,T);bp=last(promos[g],hi,T)
                row={'parent':v,'previous_same_g_in_this_inventory':u,'old_g':g,'interval_lift':[lo,hi],
                    'same_original_ID_preceding_lap':u==v,'A_resetless_column':not resets[g],
                    'full_F':ds[v]['physical_frame_interval'],'original_all_double_type':vs[v]['type']}
                if ar and ar[1]>lo:
                    row.update(classification='R' if forest else 'epoch_first',original_A_donor=ar[0]['id'])
                    if forest:
                        donor=tuple(ar[0]['id']);assert donor not in rootdonors;rootdonors.add(donor)
                elif bp and bp[1]>lo:
                    beta=bp[0];assert beta['case'] in ('LL','RR') and beta['id'][3]==0 and beta['target']!=g
                    r=tuple(beta['id'][1:3]);assert ds[r]['p']==g
                    assert contained(ds[v]['physical_frame_interval'],ds[r]['physical_P_interval'])
                    assert ds[r]['physical_P_interval']!=ds[r]['physical_frame_interval']
                    row.update(classification='P' if forest else 'promotion_mediated',original_B_mediator=beta['id'],
                        predecessor=r,completed_full_P=ds[r]['physical_P_interval'])
                else:
                    assert contained(ds[v]['physical_frame_interval'],ds[u]['physical_J_interval'])
                    assert ds[u]['physical_J_interval']!=ds[u]['physical_frame_interval']
                    row.update(classification='C' if forest else 'promotion_free',predecessor=u,completed_full_J=ds[u]['physical_J_interval'])
                if row['classification']!=('R' if forest else 'epoch_first'):
                    au=last(Aup[g],hi,T);assert au is None or au[1]<=lo
                if forest:assert row['classification']==vs[v]['type']
                out.append(row)
        return out,rootdonors
    forest,donors=classify(ds,True);physical,_=classify([v for v in ds if v[1]>2*gs[v[0]]])
    children=Counter(tuple(v['predecessor']) for v in forest if v['classification']!='R');assert max(children.values(),default=0)<=2
    assert len(donors)<=countA<=2*A
    return {'source':e['source']['name'],'source_sha256':digest(e['source']),'origin':e['origin'],'A':A,'Q_B':len(ds),
        'all_original_B_double_forest':forest,'all_physical_index_noncheap_epoch_renewals':physical,
        'full_root_injection_checked':True,'binary_outdegree_checked':True,'real_A_bits':countA,'real_B_bits':countB,
        'epochless_old_g_columns':sorted({d['g'] for d in ds.values() if not resets[d['g']]}),
        'scope':'Complete physical/all-double and index-noncheap graphs; NOT a C_old graph or positive residual count. Expansion sources retain pinned native limitations.'}

if __name__=='__main__':
    unsealed();m=Meter('all_complete_physical_renewal_graphs');refs=complete_controls()
    for i,s in enumerate(fresh_sources()):refs.append({'source':s,'source_sha256':digest(s),'physical':str(ROOT/f'FRESH_PHYS_{i:02}.json'),'origin':'C7_fresh'})
    assert len(refs)==120;out=[]
    for i,e in enumerate(refs):
        z=audit(e);file=f'COMPLETE_PHYSICAL_GRAPH_{i:03}.json';write(file,z)
        out.append({'source':z['source'],'source_sha256':z['source_sha256'],'origin':e['origin'],'file':file,'sha256':hfile(ROOT/file),
            'A':z['A'],'Q_B':z['Q_B'],'epochless_old_g_columns':z['epochless_old_g_columns'],
            'physical':e.get('physical'),'expansion':e.get('expansion',False),'new_expansion':e.get('new_expansion',False)})
        write('COMPLETE_PHYSICAL_GRAPH_INDEX.json',out);gc.collect()
    write('ALL_COMPLETE_CONTROL_REFERENCES.json',refs);m.info['complete_original_sources']=len(out);m.ok=True
    print('PASS complete original all-double/noncheap graphs on',len(out),'sources; original expansions preserved',flush=True)
