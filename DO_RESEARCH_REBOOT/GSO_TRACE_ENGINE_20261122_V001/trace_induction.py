"""Exact implication teacher; exclusions cannot delete legal successors."""
import sys
sys.dont_write_bytecode=True


def ice_teacher(graph,included):
    included=set(included);diagonals={i for i,(a,b) in enumerate(graph['pairs']) if a==b}
    for i in sorted(diagonals-included):return {'status':'FAILED_INITIALIZATION','state':i,'scope':'Finite full original graph'}
    for eid,(u,v,a,q,mode,x) in enumerate(graph['edges']):
        if u in included and v not in included:return {'status':'FAILED_SUCCESSOR_IMPLICATION','edge':eid,'predecessor':u,'required_successor':v,'mode':mode,'target':x,'reason':'An included reachable predecessor entails its literal legal successor.'}
    return {'status':'FINITE_EXACT_INDUCTIVE_SUBSET','states':len(included),'scope':'This complete fixed-support original graph only; arbitrary-support induction remains a separate proof.'}
