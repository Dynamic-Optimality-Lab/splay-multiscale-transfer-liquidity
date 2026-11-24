"""Exact original-signature audit on sealed controls; no old artifact writes."""
from base2 import *
from residual0 import gap_costs
from auditc import known_star
import ast,gc

def star_for(e,i):
    if i<36:return known_star(e)
    if e['origin']=='C1_NEW':
        j=e['index']
        if j<8:return load(C1/f'NEW_PRIMARY_{j:02}.json')['original_R_star']
        return next(z['original_R_star'] for z in load(C1/'NATIVE_SELECTOR_RESULTS.json') if z.get('index')==j)
    return load(C1/'GUARDED_RESULTS.json')[e['index']]['original_R_star']

if __name__=='__main__':
    meter=Meter('inherited_exact_signature');out=[];catalog=[]
    for i,e in enumerate(controls()):
        s=e['source'];p=load(e['physical']);b=load(e['birth']);f=load(e['forest']);w=load(e['weights'])
        U={ast.literal_eval(k):v for k,v in b['U'].items()};V={tuple(z['parent']):z for z in f['vertices']}
        ds={tuple(z['parent']):z for z in p['doubles']};gs=gap_costs(s,p['boundaries'])
        dep={tuple(z['vertex']):z['distance'] for z in load(e['M1_audit'])['C_fringe_depths']}
        star=star_for(e,i);sig=[];counts=defaultdict(set);geom=[]
        for v,ud in U.items():
            if V[v]['type']!='C' or dep[v]<=2:continue
            creator=tuple(ud['creator'])
            silent=creator in U and not U[creator]['exposed']
            if not silent:continue
            counts[v[0]].add(v)
            geom.append({'parent':v,'creator':creator,'birth':ud,'distance':dep[v],
                'incoming_A':gs[v[0]],'original_j':v[1],'beyond_original_prefix':v[1]>2*gs[v[0]]})
        byp={tuple(z['parent']):z for z in geom}
        rstarcounts=defaultdict(set)
        for rho in star or []:
            v=tuple(rho['original_parent'])
            if v not in byp:continue
            sig.append({**byp[v],'rho':rho['rho'],'old_g':ds[v]['g'],'pre_A_path':p['boundaries'][v[0]-1]['A_path'],
                'whole_frame':ds[v]['F'],'chosen_output':ds[v]['J'],'original_R_star':rho,
                'literal_current_S_UU_member':False,'current_exclusion_reason':'Frozen positive periodic case or unchanged cheap-parent quota.'})
            rstarcounts[v[0]].add(v)
        for z in w['vertices']:assert z['w']==0
        xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(p['original_S'])}
        raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs)) if rank else 0
        assert raw<=10*b['A']
        rows=[{'h':h,'A_gap':gs[h],'physical_deep_silent_UU_parents':sorted(vs),
               'original_R_star_deep_silent_parents':sorted(rstarcounts[h]) if star is not None else None,
               'physical_count':len(vs),'bound_2A':2*gs[h],
               'physical_2A_packing_holds_here':len(vs)<=2*gs[h]} for h,vs in sorted(counts.items())]
        out.append({'index':i,'source':s['name'],'source_sha256':digest(s),'A':b['A'],
            'original_R_star_scope':'Earlier sealed native original selector' if star is not None else 'NOT_CLASSIFIED',
            'deep_silent_R_star_signatures':sig,'physical_deep_silent_UU':geom,'packet_packing_rows':rows,
            'actual_S_UU':[],'actual_zero_reason':'Original raw periodic certificate plus original cheap-parent quota.',
            'raw_periodic_cost':raw,'all_original_R6':len(b['original_R6'])})
        catalog.append({**e,'source_sha256':digest(s),'sealed_input_hashes':{k:hfile(e[k]) for k in ('physical','forest','weights','M1_audit','birth')}})
        del p,b,f,w;gc.collect()
    write('INHERITED_SOURCE_CATALOG.json',catalog);write('INHERITED_SIGNATURE_RESULTS.json',out)
    violations=[{'source':r['source'],**z} for r in out for z in r['packet_packing_rows'] if not z['physical_2A_packing_holds_here']]
    write('LOCAL_PACKING_SCREEN.json',{'candidate':'Number of all physical deep silent-UU C parents at h <=2A(G_h)',
        'scope':'Finite exact check of a stronger geometric superset; no universal proof or original residual reclassification.',
        'physical_violations':violations,'positive_actual_S_UU_witness':False})
    meter.info.update(complete_sealed_controls=len(out));meter.ok=True
    print('PASS inherited exact signatures52; physical local-packing violations',len(violations),flush=True)
