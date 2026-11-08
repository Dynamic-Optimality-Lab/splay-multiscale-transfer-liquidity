"""Complete seven-anchor constraints on the scalar geodesic candidate.
Uses prior charged source rows; no new semantic engine invocation.
"""
import json,time,sys,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'geodesic_seven_metric_table.json').read_text());T=Z['trees'];N=len(T);dest=Z['source_destinations'];H=Z['source_H'];Q=Z['source_Q'];rho=Z['distances'];roots={k:[i for i,t in enumerate(T) if t[0]==k] for k in range(1,8)};lower=fractions.Fraction(0);upper=None;lower_edge=upper_edge=None;constant_failure=None;checks=0
    for a in range(N):
        for b in roots[T[a][0]]:
            for y in range(8):
                aa=dest[a][y-1] if y else a;hy=H[a][y-1] if y else 0
                for x in range(1,8):
                    if x==T[b][0]:continue
                    at=dest[aa][x-1];bt=dest[b][x-1];h=hy+H[aa][x-1];q=Q[b][x-1];w=2*h-q;delta=rho[a][b]-rho[at][bt];checks+=1;edge={'a':a,'b':b,'helper':y,'target':x,'at':at,'bt':bt,'H':h,'Q':q,'weight':w,'rho_delta':delta}
                    if delta==0:
                        if w<0:constant_failure=edge
                    elif delta>0:
                        v=fractions.Fraction(-w,delta)
                        if v>lower:lower=v;lower_edge=edge
                    else:
                        v=fractions.Fraction(w,-delta)
                        if upper is None or v<upper:upper=v;upper_edge=edge
        if time.process_time()-START>CAP-2:raise TimeoutError('SCALAR_CONSTRAINT_CPU')
    empty=constant_failure is not None or (upper is not None and lower>upper)
    out('geodesic_seven_scalar_constraints.json',{'status':'EMPTY_NONNEGATIVE_SCALAR_INTERVAL' if empty else 'FINITE_CONSTRAINT_INTERVAL_NOT_UNIVERSAL_PROOF','lambda_lower':str(lower),'lambda_upper':str(upper),'lower_edge':lower_edge,'upper_edge':upper_edge,'constant_failure':constant_failure,'packet_checks':checks,'source_queries':0,'required_source_realization':'extremal edges are unpromoted until embedded and independently replayed','principal_U33':'OPEN'});print(json.dumps({'status':'EMPTY_INTERVAL' if empty else 'NONEMPTY_FINITE_INTERVAL','lower':str(lower),'upper':str(upper),'checks':checks,'lower_edge':lower_edge,'upper_edge':upper_edge,'constant_failure':constant_failure}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof29_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
