"""Physical common-subtree context compiler; old GSO code is read-only.

The reduced pair is an accounting descriptor, never a replacement source.
All concrete source records retain every original physical vertex.
"""
import importlib.util
import json
import sys
from pathlib import Path
from fractions import Fraction
from collections import Counter
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
PREVIOUS=HERE.parent/'GSO_ENGINE_20261121_V001'
sys.path.insert(0,str(PREVIOUS))
import kernel as K
import teacher as T
sys.path.pop(0)


def write(path,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists(),'sealed output'
    K.dump(path,value)


def children(t):
    return {k:[t[2*k-1],t[2*k]] for k in range(1,(len(t)+1)//2)}


def reduce_pair(a,b,record=False):
    """Delete common physical leaves in deterministic rounds, then rank relabel."""
    ca,cb=children(a),children(b);ra,rb=a[0],b[0];removed=[]
    while ca:
        leaves=sorted(k for k in ca if ca[k]==[0,0] and cb[k]==[0,0])
        if not leaves:break
        selected=set(leaves)
        for ch in (ca,cb):
            for k in leaves:del ch[k]
            for k in ch:
                ch[k]=[0 if v in selected else v for v in ch[k]]
        if ra in selected:ra=0
        if rb in selected:rb=0
        removed.append(leaves)
    keys=sorted(ca);rank={k:i+1 for i,k in enumerate(keys)};rank[0]=0
    def enc(ch,r):return tuple([rank[r]]+[rank[v] for k in keys for v in ch[k]])
    result=(enc(ca,ra),enc(cb,rb))
    return (result,keys,removed) if record else result


def core_key(pair):
    return json.dumps(pair,separators=(',',':'))


def size(pair):return (len(pair[0])-1)//2


def compile_graph(limit=3):
    """Every pair and operation on <=2k keys, including unreachable pairs.

    In particular no transient/reaching edge is passed off as a closed original
    witness. The finite rows are stronger sufficient symbolic obligations.
    """
    assert limit==3,'the admission covers boundary core3 / retained support6'
    states=[];state_index={};edges=[];provenance=[];seen={};hist=[]
    def sid(core):
        key=core_key(core)
        if key not in state_index:
            state_index[key]=len(states);states.append(core)
        return state_index[key]
    for n in range(1,2*limit+1):
        old=K.load(PREVIOUS/'run_001'/f'graph_{n}.json.gz')
        trees=list(map(tuple,old['trees']));trans=old['tree_transitions'];count=len(trees)
        cores=[[reduce_pair(a,b) for b in trees] for a in trees]
        kept=0;all_edges=0
        for ia,a in enumerate(trees):
            for ib,b in enumerate(trees):
                before=cores[ia][ib]
                for target in range(1,n+1):
                    na,da=trans[ia][target-1];nb,db=trans[ib][target-1]
                    for mode,jb,q in [('D',ib,0),('K',nb,db//2)]:
                        all_edges+=1;after=cores[na][jb]
                        if size(before)>limit or size(after)>limit:continue
                        kept+=1;row=(sid(before),sid(after),(da+1)//2,q)
                        if row in seen:continue
                        seen[row]=len(edges)
                        edges.append([*row,mode,target])
                        provenance.append({'support':n,'A_tree':ia,'B_tree':ib,'mode':mode,'target':target,'after_A_tree':na,'after_B_tree':jb,'a':row[2],'q':q})
        hist.append({'support':n,'all_complete_tree_pairs':count*count,'all_original_operation_rows':all_edges,'rows_with_both_boundary_cores_within_limit':kept})
    graph={'support':2*limit,'boundary_core_limit':limit,'pairs':states,'edges':edges,'row_provenance':provenance,'enumeration':hist,'scope':'All full pair shapes and legal original operations on <=6 retained vertices, then exact common-leaf aliases. The quotient cycle is not necessarily a physical closed source.'}
    return graph


def solve(graph):
    result=T.optimum(graph)
    assert result['status']=='FINITE_EXACT_OPTIMUM',result
    if Fraction(result['C'])<1:
        cert=T.exact_trial(graph,1);assert cert['status']=='FINITE_EXACT_POTENTIAL'
        result={'status':'FINITE_EXACT_UPPER_CERTIFICATE','C':'1','upper_certificate':cert,'abstract_optimum':result}
    p=result['upper_certificate'];den=p['potential_denominator'];values=p['potential_numerators']
    # Additive normalization has no mathematical effect, including the seam.
    low=min(values);values=[x-low for x in values];p['potential_numerators']=values
    assert all(den*q+values[v]-values[u]<=Fraction(result['C'])*den*a for u,v,a,q,_,_ in graph['edges'])
    result['potential_range']=str(Fraction(max(values)-min(values),den))
    result['floating_LP_role']='Discovery only; all-edge integer upper inequalities and a tight abstract cycle certify the finite quotient optimum, not the optimum original source constant.'
    result['abstract_cycle_scope']='Only an optimum certificate for the finite quotient. Not claimed to be an admissible physical cycle.'
    return result


def run(out):
    out.mkdir(parents=True,exist_ok=False)
    graph=compile_graph();write(out/'CONTEXT_GRAPH.json.gz',graph)
    cert=solve(graph);write(out/'CONTEXT_CERTIFICATE.json',cert)
    return {'abstract_states':len(graph['pairs']),'distinct_transition_constraints':len(graph['edges']),'all_complete_rows':sum(x['all_original_operation_rows'] for x in graph['enumeration']),'C':cert['C'],'potential_range':cert['potential_range'],'status':'FINITE_CERTIFICATE_READY_SYMBOLIC_LIFT_REQUIRES_SEPARATE_PROOF'}


if __name__=='__main__':
    print(json.dumps(run(HERE/'run_001')))
