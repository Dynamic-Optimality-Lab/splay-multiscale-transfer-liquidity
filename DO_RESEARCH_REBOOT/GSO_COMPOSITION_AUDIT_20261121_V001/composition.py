"""Proof-interface composition audit on complete original paired sources."""
import json
import sys
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;PREVIOUS=HERE.parent/'GSO_CONTEXT_LIFECYCLE_20261121_V001'
sys.path.insert(0,str(PREVIOUS));import context as C;sys.path.pop(0)
K=C.K


def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists(),'sealed output'
    path=HERE/name;assert not path.exists(),'retain existing artifacts; use a new run name'
    K.dump(path,value)


def raw_state(t):
    if t is None:return None
    ch={};stack=[t]
    while stack:
        k,l,r=stack.pop();ch[str(k)]=[l[0] if l else None,r[0] if r else None];stack.extend(x for x in (l,r) if x)
    return {'root':t[0],'children':ch}


def state_raw(s):
    def rec(k):return (k,rec(s['children'][str(k)][0]),rec(s['children'][str(k)][1])) if k is not None else None
    return rec(s['root'])


def project(s,low,high):
    ch=s['children']
    def rec(k):
        if k is None:return None
        left,right=ch[str(k)]
        if k<low:return rec(right)
        if k>high:return rec(left)
        return (k,rec(left),rec(right))
    return rec(s['root'])


def local_splay(t,x):
    s=raw_state(t);keys=sorted(map(int,s['children']));rank={k:i+1 for i,k in enumerate(keys)};rank[None]=0
    e=tuple([rank[s['root']]]+[rank[v] for k in keys for v in s['children'][str(k)]])
    out,d=K.original_splay(e,rank[x])
    inv={i+1:k for i,k in enumerate(keys)};inv[0]=None
    ch={str(inv[i]):[inv[out[2*i-1]],inv[out[2*i]]] for i in range(1,len(keys)+1)}
    return state_raw({'root':inv[out[0]],'children':ch}),d


def embed(source,n=10,active=(4,6,7,8,9)):
    mapping={i+1:x for i,x in enumerate(active)}
    def balanced(lo,hi):
        if lo>hi:return None
        k=(lo+hi)//2;return (k,balanced(lo,k-1),balanced(k+1,hi))
    def tree(s):
        def rec(k,lo,hi):
            if k is None:
                assert not any(lo<=x<=hi for x in active)
                return balanced(lo,hi)
            x=mapping[k];left,right=s['children'][str(k)]
            return (x,rec(left,lo,x-1),rec(right,x+1,hi))
        return raw_state(rec(s['root'],1,n))
    out={'name':'embedded_optimum5_two_rank_blocks','initial_A':tree(source['initial_A']),'initial_B':tree(source['initial_B']),'diagonal':tree(source['diagonal']),'prefix':[[m,mapping[x]] for m,x in source['prefix']],'operations':[[m,mapping[x]] for m,x in source['operations']],'expected_A':source['expected_A'],'expected_Q':source['expected_Q'],'embedding':{'active_keys':list(active),'physical_keys':list(range(1,n+1))}}
    return out


def inspect(source,block_size=5,explicit_blocks=None):
    original=K.OLD.replay(source);keys=sorted(original['keys'])
    blocks=explicit_blocks or [keys[i:i+block_size] for i in range(0,len(keys),block_size)]
    owner={k:i for i,block in enumerate(blocks) for k in block};assert set(owner)==set(keys)
    assert all(block==list(range(block[0],block[-1]+1)) for block in blocks)
    trees={a:K.OLD.Tree(source['initial_'+a],original['S']) for a in ('A','B')}
    rows=[];a_internal=0;internal=boundary=0;step_records=[]
    for op,(mode,target) in enumerate(source['operations'],1):
        before={a:trees[a].state() for a in trees};aproj=[project(before['A'],b[0],b[-1]) for b in blocks];bproj=[project(before['B'],b[0],b[-1]) for b in blocks]
        actor_units=Counter();actor_bits={a:Counter() for a in trees};q=0;steps=[]
        for actor in ('A','B') if mode=='K' else ('A',):
            t=trees[actor];step=0
            while t.parent[target] is not None:
                step+=1;p=t.parent[target];g=t.parent[p]
                typ='ZIG' if g is None else ('L' if p<g else 'R')+('L' if target<p else 'R')
                pivots=[target] if g is None else [p,target] if typ in ('LL','RR') else [target,target]
                ids=[];inside=[]
                for bit,y in enumerate(pivots):
                    parent=t.parent[y];idx=owner[y] if owner[y]==owner[parent] else None
                    event=t.rotate(y);ids.append([actor,op,step,bit]);inside.append(idx)
                    if idx is not None:actor_bits[actor][idx]+=1
                parts={i for i in inside if i is not None};assert len(parts)<=1
                rec={'actor':actor,'op':op,'step':step,'type':typ,'bit_ids':ids,'internal_block_per_bit':inside};steps.append(rec)
                if actor=='A':
                    for i in parts:actor_units[i]+=1;a_internal+=1
                elif len(pivots)==2:
                    q+=1
                    if inside[0] is not None and inside[0]==inside[1]:internal+=1;rec['classification']='internal_double'
                    else:boundary+=1;rec['classification']='boundary_double'
        after={a:trees[a].state() for a in trees};component=[]
        for i,b in enumerate(blocks):
            aa=project(after['A'],b[0],b[-1]);bb=project(after['B'],b[0],b[-1]);in_block=target in b
            expected_a=local_splay(aproj[i],target)[0] if in_block else aproj[i]
            expected_b=local_splay(bproj[i],target)[0] if in_block and mode=='K' else bproj[i]
            illegal_zero_A=actor_units[i]==0 and aproj[i]==aa and aproj[i][0]==bproj[i][0] and bb!=bproj[i]
            component.append({'block':i,'physical_keys':b,'before_A':aproj[i],'before_B':bproj[i],'after_A':aa,'after_B':bb,'original_target_in_block':in_block,'attributed_original_A_units':actor_units[i],'internal_real_A_bits':actor_bits['A'][i],'internal_real_B_bits':actor_bits['B'][i],'deleting_outside_operations_is_legal_here':aa==expected_a and bb==expected_b,'zero_A_legal_source_obstruction':illegal_zero_A})
        rows.append({'op':op,'mode':mode,'target':target,'full_before':before,'full_after':after,'q':q,'components':component,'steps':steps});step_records.extend(steps)
    assert all(trees[a].state()==source['initial_'+a] for a in trees)
    assert internal+boundary==original['Q_B'] and a_internal<=original['A']
    K_B=sum(row['mode']=='K' and row['full_before']['B']['root']!=row['target'] for row in rows)
    assert K_B<=original['A']
    assert internal<=max((len(b)-1)//2 for b in blocks)*K_B
    return {'source':source,'S':original['S'],'blocks':blocks,'A':original['A'],'Q_B':original['Q_B'],'K_B':K_B,'internal_A_units':a_internal,'internal_B_doubles':internal,'interaction_B_doubles':boundary,'original_U':original['demands'],'rows':rows,'prefix_checked':True,'full_pair_closure':True}


def find_noncommuting_source():
    evaluated=0
    for n in (3,4,5):
        g=K.load(C.PREVIOUS/'run_001'/f'graph_{n}.json.gz');trees=g['trees'];cache={}
        for eid in g['recurrent_edges']:
            u,v,a,q,mode,x=g['edges'][eid]
            if mode!='K':continue
            tb=g['pairs'][u][1];nb=g['pairs'][v][1];s=K.json_state(trees[tb]);out=K.json_state(trees[nb])
            for lo in range(1,n+1):
                for hi in range(lo+1,n+1):
                    if not lo<=x<=hi:continue
                    signature=(tb,nb,x,lo,hi)
                    if signature in cache:continue
                    projected=project(s,lo,hi);observed=project(out,lo,hi);expected,_=local_splay(projected,x);evaluated+=1;cache[signature]=True
                    if observed!=expected:
                        ids=C.T.close_edge(g,eid);source=K.source_from_cycle(g,ids,f'recurrent_noncommuting_n{n}_I{lo}_{hi}')
                        blocks=([list(range(1,lo))] if lo>1 else [])+[list(range(lo,hi+1))]+([list(range(hi+1,n+1))] if hi<n else [])
                        return source,blocks,{'support':n,'original_graph_edge':eid,'original_selected_op':1,'interval':[lo,hi],'physical_before_B':s,'physical_after_B':out,'projected_before':projected,'actual_projection_after':observed,'ordinary_splay_after':expected,'queries_until_first':evaluated,'minimality_scope':'No global minimality claim; bounded recurrent search order only.'}
    raise AssertionError('No recurrent noncommutation found in admitted bounded search')


def main():
    base=K.load(C.PREVIOUS/'run_001/optimum_cycle_n5.json')['source'];population=[(base,None),(embed(base),None)]
    source,blocks,noncommute=find_noncommuting_source();population.append((source,blocks));write('NONCOMMUTATION_DISCOVERY.json',noncommute)
    # This already sealed family distinguishes genuine KEEP support from
    # common-leaf paired-core size. Its zero Q is explicitly not an escape.
    sys.path.insert(0,str(C.PREVIOUS));import parametric;sys.path.pop(0)
    for n in (8,32,128):population.append((parametric.make(n,'reverse_guard3'),None))
    wanted={'W_2_1','G_4_1_L31_r4_z1','H3_rho2_Y1_copies2'}
    for i in range(3):
        old=K.load(C.PREVIOUS/'run_001'/f'flow_case_{i}.json');assert old['name'] in wanted;population.append((K.SOURCES.canonical(old['ref']),None))
    for q in (1,3,7,17):population.append((K.PARAM.H(3,q),None))
    summary=[]
    for i,(s,parts) in enumerate(population):
        z=inspect(s,explicit_blocks=parts);name=f'source_{i:02d}.json.gz';write(name,z)
        row={'file':name,'name':s['name'],'physical_keys':len(z['source']['initial_A']['children']),'operations':len(s['operations']),'A':z['A'],'Q_B':z['Q_B'],'internal_A_units':z['internal_A_units'],'internal_B_doubles':z['internal_B_doubles'],'interaction_B_doubles':z['interaction_B_doubles'],'zero_A_local_legality_failures':sum(c['zero_A_legal_source_obstruction'] for r in z['rows'] for c in r['components'])}
        summary.append(row);print(json.dumps(row),flush=True)
    write('SUMMARY.json',{'cases':summary,'root_status':'OPEN','scope':'Original complete sources and deterministic physical interval composition, not a universal composition disproof or finite coverage proof.'})


if __name__=='__main__':main()
