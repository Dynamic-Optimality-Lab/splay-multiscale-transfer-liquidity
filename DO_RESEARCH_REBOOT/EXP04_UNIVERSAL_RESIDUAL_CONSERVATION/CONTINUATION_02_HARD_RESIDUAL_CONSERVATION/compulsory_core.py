from fast_physics import *


def compulsory(replay):
    rows=replay['rows'];T=len(rows);guards=[i for i,r in enumerate(rows) if r.get('guard_H',False)]
    if not guards:return {'mandatory_original_KEEP':[],'guard_count':0,'cyclic_cost_lower_bound':0,'target_core':[]}
    cut=(guards[0]+1)%T;order=[(cut+i)%T for i in range(T)]
    difference=[0]*(T+1);states={rows[(cut-1)%T]['B_code']:[0,0]}
    def finish():
        for first,last in states.values():
            if first<last:difference[first]+=1;difference[last]-=1
    for pos,i in enumerate(order):
        row=rows[i];state=row['B_code']
        if row.get('guard_H',False):
            finish();states={state:[pos+1,pos+1]}
        elif state in states:states[state][1]=pos+1
        else:states[state]=[pos+1,pos+1]
    finish();load=0;mandatory=[]
    for pos,i in enumerate(order):
        load+=difference[pos]
        if rows[i]['tag']=='K' and load==0:mandatory.append(i+1)
    mandatory_set=set(mandatory);assert all(i+1 in mandatory_set for i in guards)
    mandatory.sort();targets=[rows[t-1]['x'] for t in mandatory];P=set(targets)
    bound=periodic_cost(targets,P)
    return {'mandatory_original_KEEP':mandatory,'guard_count':len(guards),'target_core':sorted(P),
        'cyclic_cost_lower_bound':bound['B_cyclic'],'cyclic_blocks_lower_bound':bound['cyclic_blocks'],
        'cyclic_integer_rank_lower_bound':bound['cyclic_integer_rank_travel']}


if __name__=='__main__':
    meter=Meter('compulsory_return_core_certificate')
    source=json.loads((ROOT/'ADAPTIVE_LIFT_SOURCE.json').read_text());f=physical_replay(source)
    certificate=compulsory(f);certificate.update(source=source['name'],A=f['A'],
        periodic_all_cut_failure_certified=certificate['cyclic_cost_lower_bound']>10*f['A'],
        qualification='Universal lower-bound lemma applied exactly; failure of this sufficient negative test is not a positive coverage proof.')
    body=source['body_length'];P=certificate['target_core'];rank={x:i for i,x in enumerate(P)}
    ms=[t for t in certificate['mandatory_original_KEEP'] if t<=body];xs=[f['rows'][t-1]['x'] for t in ms]
    localL=sum(abs(rank[y]-rank[x]).bit_length() for x,y in zip(xs,xs[1:]))
    certificate['mandatory_body_cost_lower_bound']=len(xs)+localL
    certificate['actual_body_A']=sum(r['a'] for r in f['rows'][:body])
    write('COMPULSORY_RETURN_CORE_CERTIFICATE.json',certificate)
    print('mandatory keys',len(P),'periodic cost lower bound',certificate['cyclic_cost_lower_bound'],'A',f['A'],
          'body lower bound',len(xs)+localL,'body A',certificate['actual_body_A'],flush=True)
    meter.success=True
