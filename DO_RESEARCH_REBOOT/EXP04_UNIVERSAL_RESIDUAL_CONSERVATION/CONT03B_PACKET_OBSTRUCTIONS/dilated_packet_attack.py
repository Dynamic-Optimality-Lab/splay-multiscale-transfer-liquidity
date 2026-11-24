from campaign3b import *
from private_scaling import construct as base_source
from fast_physics import physical_replay,decode
from cohort_repeat_attack import run
from new_payments import intern_original_states
import gc


def nodes(tree,g):
    out=[];todo=[g]
    while todo:
        k=todo.pop();out.append(k);todo.extend(x for x in tree.ch[k] if x is not None)
    return out


if __name__=='__main__':
    meter=Meter('dilated_packet_attack');pool=intern_original_states();sources=[];results=[]
    base=base_source(4,stride=9);f=physical_replay(base,collect_A=True);first=646;g=154
    ast=Tree(decode(f['rows'][first-1]['A_code'],577));bst=Tree(decode(f['rows'][first-1]['B_code'],577))
    ag=nodes(ast,g);bg=nodes(bst,g);candidates=[]
    for x in bg:
        if min(ag)<=x<=max(ag):continue
        path=bst.path(x);d=len(path)-1-path.index(g)
        if d>=6 and d%2==0:candidates.append((d,x))
    candidates.sort(reverse=True)
    write('DILATED_PACKET_SETUP.json',{'g':g,'A_subtree_range':[min(ag),max(ag)],
        'B_subtree_range':[min(bg),max(bg)],'exact_even_distance_outside_A_candidates':candidates,
        'scope':'Full physical original support577, after first target; no Pi inferred from candidates.'})
    print('dilated g',g,'A',min(ag),max(ag),'B',min(bg),max(bg),'candidates',candidates,flush=True)
    # Choose a spread of exact physical candidates, with helpers strictly
    # outside the permanent A component. Stop at a genuine prehybrid escape.
    xs=[]
    for d,x in candidates:
        if x not in xs:xs.append(x)
        if len(xs)==4:break
    for x in xs:
        for helper in (None,118):
            previous=36;piece=[];indices=[646]
            for k,target in enumerate((72,x)):
                if k and helper is not None:piece.append(['D',helper])
                piece += [['D',target],['K',previous],['K',target]];previous=target;indices.append(646+len(piece))
            assert all(target<min(ag) for tag,target in piece)
            s={k:v for k,v in base.items() if k not in ('A','Q_B','trace_hash','closing_A','closing_B')}
            s.update(name=f'C3B_d9_x{x}_A{helper}',family='fenced_A_component_deep_private_repeat',
                operations=base['operations'][:646]+piece+base['operations'][646:],
                packet_target_operations=indices,second_private_target=x,auxiliary_A_helper=helper,
                fixed_component_key=g,fixed_component_range=[min(ag),max(ag)])
            r,z=run(s);z['target_g']=g
            z['packet_g_parents']=[{'parent':[h,j],'signs':d['signs'],'in_original_U':(h,j) in r.U}
                 for (h,j),d in r.doubles.items() if h in indices and d['g']==g]
            sources.append(s);results.append(z);write('DILATED_PACKET_SOURCES.json',sources);write('DILATED_PACKET_RESULTS.json',results)
            unpaid=z['ordered_accounting']['first_use_E_C']['repeat_original_gaps']
            print(s['name'],'Rstar',len(z['original_R_star']),'C',len(z['ordered_accounting']['C_after_frozen_and_prefix']),
                  'repeatC',len(unpaid),flush=True)
            del r;pool.clear();gc.collect()
            if z.get('unpaid_C_demands'):
                meter.success=True;meter.details['new_original_sources']=len(sources);sys.exit(0)
    meter.success=True;meter.details['new_original_sources']=len(sources)
