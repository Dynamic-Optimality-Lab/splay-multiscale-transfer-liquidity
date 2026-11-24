"""Independent composition/projection/reference check plus sealed full Pi audit.

Imports no new producer, interval projector, composition teacher or transporter.
All physical splays use the previous sealed immutable implementation. Interval
projection uses two BST splits, different from the producer's unary filter.
"""
import gzip
import importlib.util
import json
import sys
import time
from collections import Counter,defaultdict,deque
from pathlib import Path
from fractions import Fraction
sys.dont_write_bytecode=True
sys.setrecursionlimit(20000)
HERE=Path(__file__).resolve().parent;PREV=HERE.parent/'GSO_CONTEXT_LIFECYCLE_20261121_V001'
spec=importlib.util.spec_from_file_location('composition_pinned_independent_checker',PREV/'verify.py');P=importlib.util.module_from_spec(spec);sys.modules[spec.name]=P;spec.loader.exec_module(P)
V=P.V


def load(p):
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8')) as f:return json.load(f)


def canonical(x):return json.loads(json.dumps(x))


def split(t,key):
    if t is None:return None,None
    if t.k<key:
        low,high=split(t.r,key);return V.node(t.k,t.l,low),high
    low,high=split(t.l,key);return low,V.node(t.k,high,t.r)


def restrict(t,lo,hi):
    _,ge=split(t,lo);middle,_=split(ge,hi+1);return middle


def lookup(t,x):
    while t.k!=x:t=t.l if x<t.k else t.r
    return t


def rotated(t,parent,promoted):
    if t.k==parent:
        child=t.l if promoted<parent else t.r;assert child and child.k==promoted
        return V.right(t) if promoted<parent else V.left(t)
    return V.node(t.k,rotated(t.l,parent,promoted),t.r) if parent<t.k else V.node(t.k,t.l,rotated(t.r,parent,promoted))


def verify_record(path):
    z=load(path);s=z['source'];event_source=load(HERE/'original_event_companions'/path.name)
    assert s==event_source['source'] and z['A']==event_source['A'] and z['Q_B']==event_source['Q_B'] and z['original_U']==event_source['original_U']
    original=P.verify_source(HERE/'original_event_companions'/path.name)
    blocks=z['blocks'];owner={k:i for i,part in enumerate(blocks) for k in part};assert len(owner)==len(s['initial_A']['children'])
    assert all(len(part)<=5 and part==list(range(part[0],part[-1]+1)) for part in blocks)
    trees={a:P.from_state(s['initial_'+a]) for a in ('A','B')};A=Q=insideA=insideB=outsideB=0;all_A_bits={};illegal=0
    for op,((mode,x),saved) in enumerate(zip(s['operations'],z['rows']),1):
        assert mode==saved['mode'] and x==saved['target']
        assert {a:P.raw(t) for a,t in trees.items()}=={a:P.raw(P.from_state(saved['full_before'][a])) for a in trees}
        before={a:trees[a] for a in trees};step_data={};steps=[];q=0;original_A_units=defaultdict(set);bits_by_actor={a:Counter() for a in trees}
        for actor in ('A','B') if mode=='K' else ('A',):
            def emit(step,bit,typ,promoted,pivot,demoted):
                idx=owner[promoted.k] if owner[promoted.k]==owner[pivot.k] else None
                key=(actor,step)
                if key not in step_data:
                    row={'actor':actor,'op':op,'step':step,'type':typ,'bit_ids':[],'internal_block_per_bit':[]};step_data[key]=row;steps.append(row)
                step_data[key]['bit_ids'].append([actor,op,step,bit]);step_data[key]['internal_block_per_bit'].append(idx)
                if actor=='A':all_A_bits[('A',op,step,bit)]={'promoted':promoted.k,'demoted':pivot.k}
                if idx is not None:
                    bits_by_actor[actor][idx]+=1
                    if actor=='A':original_A_units[idx].add(step)
                return 0
            trees[actor],depth=P.splay(trees[actor],x,emit)
            if actor=='A':A+=(depth+1)//2
            else:Q+=depth//2;q=depth//2
        for row in steps:
            inside=row['internal_block_per_bit'];parts={i for i in inside if i is not None};assert len(parts)<=1
            if row['actor']=='B' and len(inside)==2:
                if inside[0] is not None and inside[0]==inside[1]:row['classification']='internal_double';insideB+=1
                else:row['classification']='boundary_double';outsideB+=1
        assert steps==saved['steps'] and q==saved['q']
        assert {a:P.raw(t) for a,t in trees.items()}=={a:P.raw(P.from_state(saved['full_after'][a])) for a in trees}
        insideA+=sum(len(v) for v in original_A_units.values())
        for i,(part,c) in enumerate(zip(blocks,saved['components'])):
            ab=restrict(before['A'],part[0],part[-1]);bb=restrict(before['B'],part[0],part[-1]);aa=restrict(trees['A'],part[0],part[-1]);ba=restrict(trees['B'],part[0],part[-1]);target=x in part
            assert [canonical(P.raw(v)) for v in (ab,bb,aa,ba)]==[c[k] for k in ('before_A','before_B','after_A','after_B')]
            ea=P.splay(ab,x)[0] if target else ab;eb=P.splay(bb,x)[0] if target and mode=='K' else bb
            legal=P.raw(ea)==P.raw(aa) and P.raw(eb)==P.raw(ba)
            zero=not original_A_units[i] and P.raw(ab)==P.raw(aa) and ab.k==bb.k and P.raw(bb)!=P.raw(ba)
            assert legal==c['deleting_outside_operations_is_legal_here'] and zero==c['zero_A_legal_source_obstruction']
            assert len(original_A_units[i])==c['attributed_original_A_units'] and bits_by_actor['A'][i]==c['internal_real_A_bits'] and bits_by_actor['B'][i]==c['internal_real_B_bits'];illegal+=zero
        access_internal=sum(row.get('classification')=='internal_double' for row in steps);assert access_internal<=(len(blocks[owner[x]])-1)//2
    assert (A,Q,insideA,insideB,outsideB)==(z['A'],z['Q_B'],z['internal_A_units'],z['internal_B_doubles'],z['interaction_B_doubles'])
    assert insideA<=A and insideB+outsideB==Q and insideB<=2*z['K_B'] and z['K_B']<=A
    # Replay the exact reference compiler output without trusting its bits.
    ref=load(HERE/'reference'/path.name)
    if ref.get('reference_required',True):
        ra=P.from_state(ref['reference_initial_A']);rb=P.from_state(ref['B_initial']);startA=P.raw(ra);startB=P.raw(rb);seen=set();b_rot=0
        for bundle in ref['bundles']:
            for bit in bundle['actual_original_A_rotations']:
                identifier=tuple(bit['original_id']);assert identifier not in seen and all_A_bits[identifier]=={'promoted':bit['promoted'],'demoted':bit['demoted']};seen.add(identifier)
                ra=rotated(ra,bit['demoted'],bit['promoted'])
            target=bundle['target'];assert ra.k==target
            rb,depth=P.splay(rb,target);b_rot+=depth;assert depth==bundle['B_real_rotations']
            assert bundle['reference_request_cost']==len(bundle['actual_original_A_rotations'])+1
        assert seen==set(all_A_bits) and P.raw(ra)==startA and P.raw(rb)==startB
        assert len(seen)==ref['R_A'] and b_rot==ref['R_B'] and len(ref['bundles'])==z['K_B']
        assert ref['reference_cost']==len(seen)+z['K_B']<=3*A and 2*Q<=ref['B_root_BST_cost']==b_rot+z['K_B']
    return {'file':path.name,'name':s['name'],'physical_keys':len(owner),'operations':len(s['operations']),'A':A,'Q_B':Q,'literal_U':len(z['original_U']),'original_real_rotations':original['real_rotations'],'A_internal_units':insideA,'B_internal_doubles':insideB,'B_interaction_doubles':outsideB,'zero_A_local_obstructions':illegal,'all_original_Pi_and_costs_checked':True,'reference_exact_original_A_bits_checked':True}


def verify_unreachable():
    z=load(HERE/'COMPONENT_UNREACHABILITY_CERTIFICATE.json');start=P.imm(z['component_before']);destination=P.imm(z['component_after']);closed=set();queue=deque([start]);transitions=[]
    while queue:
        t=queue.popleft();signature=P.raw(t)
        if signature in closed:continue
        closed.add(signature)
        for x in (1,2,3):
            out,_=P.splay(t,x);transitions.append((signature,x,P.raw(out)));queue.append(out)
    assert len(P.universe(3))==5 and len(closed)==3 and P.raw(destination) not in closed
    assert {json.dumps(x) for x in closed}=={json.dumps(x) for x in z['closed_reachable_B_states']}
    assert len(transitions)==9
    for row in z['all_ordinary_splay_transitions_from_closed_set']:
        assert (P.raw(P.imm(row['before'])),row['target'],P.raw(P.imm(row['after']))) in transitions
    source=load(HERE/z['complete_original_source']);first=source['rows'][0]
    assert canonical(P.raw(restrict(P.from_state(first['full_before']['B']),1,3)))==z['component_before']
    assert canonical(P.raw(restrict(P.from_state(first['full_after']['B']),1,3)))==z['component_after']
    return {'independent_tree_universe':5,'closed_reachable_states':3,'all_transitions_checked':9,'projected_destination_unreachable':True,'unlimited_A_credit_cannot_repair_B_reachability':True}


def verify_temporal():
    cert=load(HERE/'TEMPORAL_COMPOSITION_CERTIFICATE.json');source=load(HERE/cert['complete_original_source']);graph=load(PREV/'core5_001/CONTEXT_GRAPH.json.gz');p=load(PREV/'core5_001/CONTEXT_CERTIFICATE.json')['upper_certificate']['potential_numerators'];index={P.ck(tuple(map(tuple,q))):i for i,q in enumerate(graph['pairs'])}
    values=[]
    for saved,row in zip(cert['singleton_pieces'],source['rows']):
        def val(which):
            d=row[which];pair=P.prune(P.from_state(d['A']),P.from_state(d['B']))[0];return p[index[P.ck(pair)]]
        before,after=val('full_before'),val('full_after');assert (saved['P_before'],saved['P_after'])==(before,after)
        assert 2*saved['q']+after-before<=3*saved['a'];values.append(after-before)
    assert sum(values)==0 and cert['open_piece_counterexample']['a']==0 and cert['open_piece_counterexample']['q']==1
    return {'all_local_potential_inequalities':len(values),'signed_boundary_sum':sum(values),'open_piece_needs_boundary_credit':True}


def main():
    start=time.process_time();sources=[verify_record(path) for path in sorted(HERE.glob('source_*.json.gz'))]
    result={'passed':True,'sources':sources,'complete_sources':len(sources),'original_operations':sum(x['operations'] for x in sources),'real_rotations':sum(x['original_real_rotations'] for x in sources),'literal_U':sum(x['literal_U'] for x in sources),'component_unreachability':verify_unreachable(),'temporal_composition':verify_temporal(),'cpu_seconds':time.process_time()-start,'trust':'No current producer/projector/reference-compiler imports. Pinned immutable original-event/Pi checker, independent two-split projection, full real-event allocation and reference-bit replay. Same-agent implementation independence, not external peer review or full Lean source verification.','root_status':'OPEN'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
