from base0 import *
from fast_physics import decode
from model0 import FullTree
import ast,gc

def gap_costs(s,rows):
    N=len(rows);ks=[i for i,r in enumerate(rows) if r['tag']=='K'];out={}
    for k,i in enumerate(ks):
        prev=ks[k-1];length=(i-prev)%N or N
        out[i+1]=sum(rows[(prev+j)%N]['a'] for j in range(1,length+1))
    if ks:assert sum(out.values())==sum(r['a'] for r in rows)
    return out

def E_stream(phys,C):
    ops=phys['boundaries'];events=phys['events'];ds={tuple(z['parent']):z for z in phys['doubles']}
    byh=defaultdict(list);selected=set();epoch={};used={}
    for e in C:byh[e['consumer']].append(e)
    for lap in range(2):
        for row in ops:
            for e in events[row['start_time']:row['post_A_time']]:
                g=e['pivot'];epoch[g]=tuple(e['id']);used[g]=False
            for e in byh[row['t']]:
                p=tuple(e['original_parent']);g=ds[p]['g']
                if g in epoch and not used[g]:
                    if lap:selected.add(p)
                    used[g]=True
    return [e for e in C if tuple(e['original_parent']) in selected]

def weight_map(phys,forest,gaps,check_beta=False):
    verts={tuple(z['parent']):z for z in forest['vertices']}
    doubles={tuple(z['parent']):z for z in phys['doubles']};counts=Counter();rhoids=set();classified={c:[] for c in 'RCP'}
    bcache={};beta_checked=0
    for e in gaps:
        rho=e['rho'];key=digest(rho);assert key not in rhoids;rhoids.add(key)
        p=tuple(e['original_parent']);assert p in verts and p[0]==e['consumer']==rho[0]
        if check_beta:
            h=rho[0];inner=doubles[tuple(rho[1])]['g'];outer=doubles[tuple(rho[2])]['g']
            row=phys['boundaries'][h-1]
            if h not in bcache:
                st=decode(int(phys['state_pool']['states'][row['pre_B_state']],16),phys['state_pool']['n'])
                bcache[h]=FullTree(st)
            tree=bcache[h];path=[inner]
            while path[-1]!=outer:
                v=tree.p[path[-1]];assert v;path.append(v)
            path.reverse();edges={(u,v,int(v>u)) for u,v in zip(path,path[1:])}
            beta=next(ev for ev in phys['events'][row['post_A_time']:row['end_time']]
                      if edges.intersection(map(tuple,ev['deleted'])))
            assert beta['case']!='ZIG' and tuple(beta['id'][1:3])==p;beta_checked+=1
        counts[p]+=1;classified[verts[p]['type']].append(rho)
    assert max(counts.values(),default=0)<=3
    out=[{'parent':p,'type':v['type'],'w':counts[p]} for p,v in sorted(verts.items())]
    RR,RC,RP=(len(classified[c]) for c in 'RCP')
    assert RR+RC+RP==len(gaps)
    return {'vertices':out,'R_overflow':len(gaps),'R_R':RR,'R_C':RC,'R_P':RP,
            'literal_gap_lists_by_vertex_type':classified,'fresh_first_edge_beta_checks':beta_checked}

def saved_accounting(index,name):
    # Only immutable historical source-defined records are imported here.
    if index==7:
        v=load(BASE/'CONTINUATION_04_PACKET_OVERFLOW/WIDTH_VERIFICATION.json')[0]
        a=v['ordered_inherited_audit']
        return a['original_R_star'],a,'C04 full original Pi/R6 and primary selectors, independently archived.'
    if index==6:
        z=load(BASE/'CONT03B_PACKET_OBSTRUCTIONS/DILATED_PACKET_RESULTS.json')[-1]
        return z['original_R_star'],z['ordered_accounting'],'C03B full original Pi/R6 and primary selectors, independently archived.'
    if index==9:
        a=load(BASE/'CONTINUATION_03_UPPER_PARENT/PRIVATE_ORDERED_ACCOUNTING.json')
        return a['original_R_star'],a,'C03 original193 source accounting and independent Pi pins.'
    if index==8:
        z=load(BASE/'CONTINUATION_01_COVERAGE_PROOF/OWNERSHIP_RESULTS.json')[0]
        F1=z['carrier_comparison']['paid'];F2=z['monotone_and_cycle']['monotone_comparison']['paid']
        a={'ordered_original_assignments':{'1_frozen_carrier':F1,'2_frozen_skipped_rank':F2}}
        return z['R_star'],a,'C01 original critical Pi/U and cohort records, with frozen comparisons.'
    # C05 small full-classification source records.
    if index<6:
        v=load(C5/'INDEPENDENT_RESULTS.json')[index]
        if v['full_original_Pi']:
            assert v['original_R_star']==[]
            return [],None,'C05 full original Pi/cohorts and R_star selector rerun; empty R_star.'
        return None,None,'C05 large physical screen; full original Pi is unrun, not zero.'
    if index>=16:return [],None,'Fresh A=B KEEP or B-identity degenerate control; no neutral original R6 parent.'
    return None,None,'Historical original full Pi/R6 record preserved; higher R_star not re-enumerated in M0.'

if __name__=='__main__':
    meter=Meter('residual_partition');catalog=load(ROOT/'SOURCE_CATALOG.json')
    rows=[];actual_weights=[];diagnostics=[]
    c5v={v['source']:v for v in load(C5/'INDEPENDENT_RESULTS.json')}
    for i,entry in enumerate(catalog):
        s=entry['source'];phys=load(ROOT/f'PHYS_{i:02}.json');f=load(ROOT/f'FOREST_{i:02}.json')
        gs=gap_costs(s,phys['boundaries']);star,a,scope=saved_accounting(i,s['name'])
        if s['name'] in c5v and c5v[s['name']]['full_original_Pi']:
            assert phys['state_pool']['original_event_sha256']==c5v[s['name']]['original_event_sha256']
        S=phys['original_S'];xs=[x for tag,x in s['operations'] if tag=='K']
        if S:
            rank={x:k for k,x in enumerate(S)}
            raw=sum((x!=xs[k-1])+abs(rank[x]-rank[xs[k-1]]).bit_length() for k,x in enumerate(xs))
        else:raw=0
        assert raw<=10*sum(z['a'] for z in phys['boundaries'])
        detail={'source':s['name'],'original_R_star':star,'membership_scope':scope,
            'old_raw_periodic_certificate':raw,'A':sum(z['a'] for z in phys['boundaries']),
            'zero_overflow_reason':'Positive frozen raw periodic source case pays every noncheap original R_star; any cheap remaining D has b<=q<=2a and is entirely quota-selected.',
            'fallback_local_case':'Inactive because a periodic certificate exists.'}
        if star is not None:
            diag=weight_map(phys,f,star,check_beta=True)
            diagnostics.append({'source':s['name'],'scope':'Original R_star BEFORE F/E/hybrid/quota, not post-hybrid overflow.',
                                **{k:v for k,v in diag.items() if k!='vertices'}})
        if a is not None:
            ass=a['ordered_original_assignments']
            F={digest(e['rho']) for key in ('1_frozen_carrier','2_frozen_skipped_rank') for e in ass[key]}
            C=[e for e in star if digest(e['rho']) not in F and e['original_parent'][1]>2*gs[e['consumer']]]
            E=E_stream(phys,C)
            if 'C_after_frozen_and_prefix' in a:assert C==a['C_after_frozen_and_prefix']
            if 'first_use_E_C' in a:
                assert {digest(e['rho']) for e in E}=={digest(e['rho']) for e in a['first_use_E_C']['selected_original_gaps']}
            Eids={digest(e['rho']) for e in E}
            V={tuple(v['parent']):v for v in f['vertices']}
            assert all(digest(e['rho']) in Eids for e in C if V[tuple(e['original_parent'])]['type']=='R')
            H={digest(e['rho']) for e in star
               if phys['boundaries'][e['consumer']-1]['q']>2*gs[e['consumer']]}
            D=[e for e in star if digest(e['rho']) not in F|Eids|H]
            packets=defaultdict(lambda:defaultdict(list))
            for e in D:packets[e['consumer']][tuple(e['original_parent'])].append(e)
            Q=set();quota_rows=[];excess=0
            for h,pack in sorted(packets.items()):
                parents=sorted(pack);a_h=gs[h];excess+=max(0,len(parents)-2*a_h)
                for p in parents[:2*a_h]:Q.update(digest(e['rho']) for e in pack[p])
                quota_rows.append({'h':h,'a_h':a_h,'b_h':len(parents),
                                   'parents':parents,'selected':parents[:2*a_h]})
            overflow=[e for e in D if digest(e['rho']) not in Q]
            assert excess<=len(overflow)<=3*excess and overflow==[]
            detail.update(C_old=C,E_old=E,H_all_noncheap_rho_ids=[e['rho'] for e in star if digest(e['rho']) in H],
                          exact_D=D,quota_rows=quota_rows,original_root_C_old_contained_in_E_old=True)
        else:overflow=[] # The independently proved positive periodic/cheap-quota implication above.
        w=weight_map(phys,f,overflow,check_beta=True)
        assert w['R_R']==0 and w['R_overflow']<=6*detail['A']+w['R_C']+w['R_P']
        write(f'WEIGHTS_{i:02}.json',w);actual_weights.append({'source':s['name'],'weights_file':f'WEIGHTS_{i:02}.json',
               **{k:v for k,v in w.items() if k!='vertices'}})
        rows.append(detail)
        write('RESIDUAL_AUDIT.json',rows)
        del phys,f;gc.collect()
    write('WEIGHT_INVENTORY.json',actual_weights)
    write('DIAGNOSTIC_PREHYBRID_WEIGHTS.json',diagnostics)
    meter.ok=True;print('PASS exact prescribed residual weights; distinct prehybrid diagnostic scopes; root exclusion',flush=True)
