"""All common-hanging-path contexts, rather than enumerating support9 trees."""
import json
from itertools import product
import context as C
K=C.K


def all_cores(limit):
    answer=[((0,),(0,))]
    for n in range(2,limit+1):
        trees=[K.encode(t,n) for t in K.shapes(1,n)]
        answer.extend((a,b) for a in trees for b in trees if C.size(C.reduce_pair(a,b))==n)
    return answer


def gap_depth(t,gap):
    if t==(0,):return 0
    x=gap+0.5;k=t[0];d=0
    while k:
        d+=1;k=t[2*k-(x<k)]
    return d


def path_trees(lo,hi):
    """Every binary search path, with its bottom vertex as the access target."""
    if lo==hi:
        yield (lo,None,None),lo;return
    for rest,x in path_trees(lo+1,hi):yield (lo,None,rest),x
    for rest,x in path_trees(lo,hi-1):yield (hi,rest,None),x


def insert_path(core,gap,path,count):
    m=(len(core)-1)//2;n=m+count
    if m==0:return K.encode(path,n)
    rank=lambda k:k+(count if k>gap else 0)
    def build(k):
        if not k:return None
        return (rank(k),build(core[2*k-1]),build(core[2*k]))
    tree=build(core[0]);newroot=path[0];out=list(K.encode(tree,n))
    # The inserted path occupies the unique full ordered gap in either tree.
    at=out[0];probe=gap+0.5
    while True:
        oldkey=at-count if at>gap+count else at
        side=int(probe>oldkey);index=2*at-1+side
        if not out[index]:out[index]=newroot;break
        at=out[index]
    encoded=K.encode(path,n)
    for k in range(gap+1,gap+count+1):out[2*k-1:2*k+1]=encoded[2*k-1:2*k+1]
    return tuple(out)


def compile_paths(limit=5):
    assert limit in (3,5)
    cores=all_cores(limit);states=list(cores);index={C.core_key(p):i for i,p in enumerate(cores)}
    edges=[];rows=[];seen=set();counters={'raw_context_rows':0,'endpoint_filtered':0,'core_targets':0,'keep_gap_tails':0,'delete_gap_paths':0,'diagonal_delete_paths':0}
    def emit(a,b,x,mode,kind):
        counters['raw_context_rows']+=1
        aa,da=K.original_splay(a,x)
        if mode=='K':bb,db=K.original_splay(b,x)
        else:bb,db=b,0
        before=C.reduce_pair(a,b);after=C.reduce_pair(aa,bb)
        assert C.size(before)<=limit
        if C.size(after)>limit:counters['endpoint_filtered']+=1;return
        u=index[C.core_key(before)];v=index[C.core_key(after)];row=(u,v,(da+1)//2,db//2)
        counters[kind]+=1
        if row in seen:return
        seen.add(row);edges.append([*row,mode,x]);rows.append({'A':a,'B':b,'target':x,'mode':mode,'kind':kind})
    for core in cores:
        a,b=core;m=C.size(core)
        if m:
            for x in range(1,m+1):
                for mode in ('D','K'):emit(a,b,x,mode,'core_targets')
            for gap in range(m+1):
                for p in (1,2):
                    for path,x in path_trees(gap+1,gap+p):
                        emit(insert_path(a,gap,path,p),insert_path(b,gap,path,p),x,'K','keep_gap_tails')
                for p in range(1,limit-gap_depth(b,gap)+1):
                    for path,x in path_trees(gap+1,gap+p):
                        emit(insert_path(a,gap,path,p),insert_path(b,gap,path,p),x,'D','delete_gap_paths')
        else:
            for p in range(1,limit+1):
                for path,x in path_trees(1,p):
                    tree=K.encode(path,p);emit(tree,tree,x,'D','diagonal_delete_paths')
    return {'support':2*limit-1,'boundary_core_limit':limit,'pairs':states,'edges':edges,'row_provenance':rows,'counters':counters,'scope':'All irreducible paired cores through the declared limit and every derived hanging-path context. The symbolic completeness argument is a separate proof, not inferred from sample agreement.'}


def main():
    out=C.HERE/'core5_001';out.mkdir(exist_ok=False)
    g=compile_paths(5);C.write(out/'CONTEXT_GRAPH.json.gz',g)
    z=C.solve(g);C.write(out/'CONTEXT_CERTIFICATE.json',z)
    answer={'states':len(g['pairs']),'constraints':len(g['edges']),'counters':g['counters'],'C':z['C'],'potential_range':z['potential_range']}
    C.write(out/'SUMMARY.json',answer);print(json.dumps(answer))


if __name__=='__main__':main()
