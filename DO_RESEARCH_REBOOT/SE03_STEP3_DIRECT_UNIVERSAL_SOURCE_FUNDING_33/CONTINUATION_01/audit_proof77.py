"""Exact event-weighted directed source distances and a full lambda-family test."""
import json,time,sys,heapq,fractions,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time();F=fractions.Fraction
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'geodesic_seven_metric_table.json').read_text());T=z['trees'];D=z['source_destinations'];H=z['source_H'];Q=z['source_Q'];N=len(T);dist=[]
    for s in range(N):
        dd=[10**9]*N;dd[s]=0;heap=[(0,s)]
        while heap:
            value,v=heapq.heappop(heap)
            if value!=dd[v]:continue
            for u,w in zip(D[v],H[v]):
                cand=value+w
                if cand<dd[u]:dd[u]=cand;heapq.heappush(heap,(cand,u))
        assert max(dd)<10**9;dist.append(dd)
    out('directed_source_event_distances7.json',{'definition':'minimum total actual ceil(depth/2) ordinary splay costs','all_pairs':dist,'source_kernel':'geodesic_seven_metric_table.json','source_kernel_sha256':hashlib.sha256((B/'geodesic_seven_metric_table.json').read_bytes()).hexdigest(),'native_keys':7,'new_source_queries':0,'independent_audit':'PENDING'})
    roots={g:[i for i,t in enumerate(T) if t[0]==g] for g in range(1,8)};lower=F(0);upper=F(1);le=ue=constant=unchanged=None;checks=0
    for a in range(N):
        for b in roots[T[a][0]]:
            forward=dist[a][b];reverse=dist[b][a]
            for y in range(8):
                aa=D[a][y-1] if y else a;hy=H[a][y-1] if y else 0
                for x in range(1,8):
                    if x==T[b][0]:continue
                    at=D[aa][x-1];bt=D[b][x-1];h=hy+H[aa][x-1];q=Q[b][x-1];w=2*h-q;df=dist[at][bt]-forward;dr=dist[bt][at]-reverse;C=w-2*dr;S=2*(df+dr);checks+=1;e={'A':a,'B':b,'DELETE_helper_or_0':y,'KEEP_target':x,'A_after':at,'B_after':bt,'H':h,'Q':q,'price':w,'ell_A_to_B_before':forward,'ell_B_to_A_before':reverse,'ell_A_to_B_after':dist[at][bt],'ell_B_to_A_after':dist[bt][at],'margin_constant':C,'margin_lambda_coefficient':S}
                    if S==0 and C<0:
                        if constant is None or C<constant['margin_constant']:constant=e
                    elif S>0:
                        bound=F(-C,S)
                        if bound>lower:lower=bound;le=e
                    elif S<0:
                        bound=F(C,-S)
                        if bound<upper:upper=bound;ue=e
                    if w<0 and df==dr==0 and unchanged is None:unchanged=e
        if time.process_time()-START>CAP-2:raise TimeoutError('DISTANCE_FAMILY_CPU')
    empty=constant is not None or lower>upper;result={'status':'DIRECTED_SOURCE_DISTANCE_FAMILY_EMPTY_INTERVAL_CANDIDATE' if empty else 'FINITE_LAMBDA_INTERVAL_NOT_UNIVERSAL_PROOF','family':'Phi=2lambda ell(A,B)-2(1-lambda)ell(B,A), 0<=lambda<=1','lambda_lower':str(lower),'lambda_upper':str(upper),'lower_edge':le,'upper_edge':ue,'constant_negative_edge':constant,'unchanged_both_directed_distances_negative_edge':unchanged,'synchronized_natural_packet_checks':checks,'new_source_queries':0,'original_source_closed_embeddings':'PENDING for selected counterconstraints','principal_U33':'OPEN'};out('directed_source_distance_family_candidate.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof77_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
