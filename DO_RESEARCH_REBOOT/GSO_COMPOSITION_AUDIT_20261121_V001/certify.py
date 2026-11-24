"""Exact semantic and budget certificates for the composition audit."""
import json
from collections import deque
from fractions import Fraction
import composition as M
K=M.K;C=M.C


def encode_raw(t):
    s=M.raw_state(t);keys=sorted(map(int,s['children']));rank={k:i+1 for i,k in enumerate(keys)};rank[None]=0
    return tuple([rank[s['root']]]+[rank[v] for k in keys for v in s['children'][str(k)]])


def local_B_reachable(before):
    keys=sorted(map(int,M.raw_state(before)['children']));queue=deque([before]);seen={before};trans=[]
    while queue:
        t=queue.popleft()
        for x in keys:
            out,d=M.local_splay(t,x);trans.append({'before':t,'target':x,'after':out,'depth':d})
            if out not in seen:seen.add(out);queue.append(out)
    return seen,trans


def main():
    non=K.load(M.HERE/'NONCOMMUTATION_DISCOVERY.json');before=tupleize(non['projected_before']);after=tupleize(non['actual_projection_after']);seen,trans=local_B_reachable(before)
    assert len(seen)==3 and after not in seen
    M.write('COMPONENT_UNREACHABILITY_CERTIFICATE.json',{'status':'REFUTED_EXACT_PROJECTED_COMPONENT_HISTORY','complete_original_source':'source_02.json.gz','original_operation':1,'physical_interval':non['interval'],'component_before':before,'component_after':after,'closed_reachable_B_states':sorted(seen,key=str),'all_ordinary_splay_transitions_from_closed_set':trans,'proof':'The displayed finite set contains the start and is closed under every possible local KEEP. DELETE freezes B. The actual projected destination is outside the set. No legal local Pair Access history realizes this transition, regardless of local A cost or the number of extra operations.','scope':'Refutes direct interval restriction and every ordinary local-word legalization with this retained key set and these endpoints. Not arbitrary adaptive/overlapping composition or Universal CD.'})
    embedded=K.load(M.HERE/'source_01.json.gz');hits=[{'op':r['op'],'target':r['target'],'mode':r['mode'],'component':c} for r in embedded['rows'] for c in r['components'] if c['zero_A_legal_source_obstruction']];assert len(hits)==1
    assert hits[0]['op']==2 and hits[0]['target']==4 and hits[0]['component']['physical_keys']==[6,7,8,9,10]
    M.write('ZERO_ORIGINAL_A_INTERFACE_CERTIFICATE.json',{'status':'REFUTED_EXACT_ZERO_COST_COMPONENT_REALIZATION','complete_original_source':'source_01.json.gz','period_A':embedded['A'],'period_Q_B':embedded['Q_B'],'witness':hits[0],'reason':'At original KEEP4 the component A projection has no attributed original work and stays rooted at7. Its B projection changes from root7 to root6. Every local history of A cost zero can only target7; B is then frozen or splays its existing root7, so it cannot change. Any ordinary legalization needs extra A credit or an explicitly costed non-splay interface.'})
    # The same complete source also obstructs a naive block-contraction BST.
    initial=embedded['source']['initial_A'];assert initial['root']==7 and initial['children']['7'][0]==4 and initial['children']['4'][1]==6
    M.write('QUOTIENT_TREE_OBSTRUCTION.json',{'status':'REFUTED_EXACT_UNQUALIFIED_BLOCK_CONTRACTION','complete_original_source':'source_01.json.gz','physical_A_path':[7,4,6],'blocks':[[1,2,3,4,5],[6,7,8,9,10]],'block_path':[1,0,1],'contracted_edges':[[1,0],[0,1]],'reason':'Identifying every key of a rank block produces a directed two-cycle. The quotient is not a BST; applying CD recursively to it is not licensed. Multiple ports/copies would require new semantics and work-sharing accounting.'})
    graph=K.load(M.PREVIOUS/'core5_001/CONTEXT_GRAPH.json.gz');certificate=K.load(M.PREVIOUS/'core5_001/CONTEXT_CERTIFICATE.json');values=certificate['upper_certificate']['potential_numerators'];index={C.core_key(p):i for i,p in enumerate(graph['pairs'])}
    def potential(A,B):return values[index[C.core_key(C.reduce_pair(encode_raw(M.state_raw(A)),encode_raw(M.state_raw(B))))]]
    temporal=K.load(M.HERE/'source_00.json.gz');records=[]
    for row in temporal['rows']:
        before,after=row['full_before'],row['full_after'];a=sum(s['actor']=='A' for s in row['steps']);q=row['q'];p=potential(before['A'],before['B']);r=potential(after['A'],after['B']);assert 2*q+r-p<=3*a
        records.append({'original_op':row['op'],'a':a,'q':q,'P_before':p,'P_after':r,'scaled_slack':3*a-2*q-r+p})
    critical=records[1];assert critical['a']==0 and critical['q']==1 and critical['P_after']<critical['P_before']
    assert sum(x['q'] for x in records)==6 and sum(x['a'] for x in records)==4 and sum(x['P_after']-x['P_before'] for x in records)==0
    M.write('TEMPORAL_COMPOSITION_CERTIFICATE.json',{'status':'PROVED_TEMPORAL_COMPOSITION_WITH_EXPLICIT_POTENTIAL_ENDPOINTS','complete_original_source':'source_00.json.gz','singleton_pieces':records,'open_piece_counterexample':critical,'scope':'An open piece has q+DeltaPhi<=3a/2, not necessarily q<=3a/2. Any temporal partition telescopes when the same physical state descriptor is used at adjacent interfaces. This does not spatially split a large irreducible core.'})
    bursts=[]
    for i in (9,10,11,12):
        z=K.load(M.HERE/f'source_{i:02d}.json.gz');s=z['source'];n=len(s['initial_A']['children']);r=next(r for r in z['rows'] if r['op']==n+7);a=sum(t['actor']=='A' for t in r['steps']);e=sum(t.get('classification')=='boundary_double' for t in r['steps']);assert a==1 and e==s['q']+1
        bursts.append({'source_file':f'source_{i:02d}.json.gz','q':s['q'],'N':n,'original_op':n+7,'A':a,'interaction':e,'full_period_A':z['A'],'full_period_Q_B':z['Q_B']})
    M.write('INTERACTION_EQUIVALENCE_CERTIFICATE.json',{'status':'PROVED_SOURCE_UNIFORM_IDENTITIES_AND_LOCAL_ALL_PARAMETER_OBSTRUCTION','fixed_partition':'Any fixed disjoint physical-key blocks of size<=5, constant within a source; contiguous blocks for the projection witness and exact critical formula.','definitions':'I counts literal original B doubles with all three pivots in one block. E is their literal complement. Each original A StepEv is attributed internally to at most one block.','identities':['sum attributed original A units <= A (L=1 for physical attribution)','Q_B=I+E','I<=2K_B<=2A','E<=Q_B<=E+2A'],'global_equivalence':'A universal bound on E/A for these fixed small blocks is equivalent up to additive2 in the constant to Universal Coarse Double itself. The local decomposition has not independently proved it.','critical_H3q':'For every q>=1 and every consecutive rank-block partition of size<=5, the q critical RR steps have old parent/grandparent keys differing by8. The final LR connects target N-7 to parent2. All q+1 steps cross blocks; E_t=q+1, a_t=1.','local_law_refuted':'E_t<=D a_t for every finite D. The aggregate law E(W)<=D A(W) is NOT refuted.','finite_complete_examples':bursts,'root_status':'OPEN'})
    M.write('COMPOSITION_RESULT.json',{'root_status':'OPEN','user_composition_implication':'VALID when the local certificates, coverage, bounded physical A reuse and all boundary debt are actually proved.','proved_interfaces':['Temporal open-potential composition','Fixed disjoint-block physical A attribution with L=1','Closed physical projection endpoints','Exact internal/interaction count and E equivalence'],'first_missing':'A legally applicable, physically funded cutting-and-rejoining interface for noncommon spatial pieces. Direct interval restriction can create a component B state unreachable by ANY local splay word.','narrow_candidate_status':'REFUTED_EXACT_FIXED_INTERVAL_RESTRICTION_AND_UNQUALIFIED_BLOCK_QUOTIENT','general_adaptive_overlapping_composition':'OPEN','new_global_original_obligations_deleted':0,'no_new_donor_policy':True})
    print(json.dumps({'component_reachable_states':len(seen),'component_transitions':len(trans),'zero_A_interface_failures':len(hits),'temporal_pieces':len(records),'critical_bursts_checked':len(bursts),'root_status':'OPEN'}))


def tupleize(t):return None if t is None else (t[0],tupleize(t[1]),tupleize(t[2]))


if __name__=='__main__':main()
