"""Exact fixed-word overlap proof, not tests over finite BSTs."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    P=(1,2,1,3,1,2,1,6);assert P[-1]==6 and all(q<6 for q in P[:-1]);conflicts=[]
    for shift in range(1,len(P)):
        index=len(P)-1-shift;assert P[-1]!=P[index]
        conflicts.append({'shift':shift,'first_terminal_Q':6,'second_interior_index':index,'second_Q':P[index]})
    theorem=B/'REPEATED_GUARDED_ESCAPE_NONCOLLISION.md'
    out('window_noncollision_audit.json',{'status':'PASS_COMPLETE_FIXED_PATTERN_OVERLAP_PROOF','pattern':P,'proper_shifts':conflicts,
        'scope':'any actual source word containing this exact cost pattern; no claim that all order classes have it',
        'arbitrary_collection_bridge':'pairwise macro-disjointness plus distinct actual unit IDs',
        'effective_freedom_proved':False,'complete_U28':False,'finite_BST_tests':0,'source_queries':0,
        'proof_sha256':hashlib.sha256(theorem.read_bytes()).hexdigest()})
    print('WINDOW_OVERLAP_PROOF_PASS',flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_windows_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
