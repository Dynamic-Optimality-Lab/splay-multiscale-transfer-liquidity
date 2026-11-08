"""Independent direct incoming maxima at two endpoints; ignores candidate labels."""
import json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(300,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();r=read(OUT/'obstruction.json');source=Path(read(OUT/'construction.json')['source_folder']);c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');psi=B['psi'];visited=0
    def direct(bv,av):
        nonlocal visited
        incoming={};best=psi[bv];arg=None
        for b,t in enumerate(B['trees']):
            for x in range(9):
                depth=B['depths'][b][x];w=2-depth//2
                if depth and w in (0,1) and B['destinations'][b][x]==bv:incoming.setdefault((1,x,None,t[0]),[]).append((b,w))
                for g in (0,9):
                    pair=B['kernels'][str(g)][b][x]
                    if c['sigma'][g] and pair is not None and pair[0]==bv and pair[1] in (0,1):incoming.setdefault((2,x,g,t[0]),[]).append((b,pair[1]))
        for a,options in enumerate(c['options']):
            root=c['shadows'][a][0][2]
            for oi,o in enumerate(options):
                H,x,aa,g,fi,code=o
                if aa!=av:continue
                for bs,w in incoming.get((H,x,g,root),()):
                    visited+=1;v=psi[bs]-w
                    if v>best:best=v;arg={'source_B':bs,'source_A':a,'option_index':oi,'weight':w,'seed_psi':psi[bs]}
            if a%256==0:assert time.process_time()-start<CAP,'UNKNOWN direct obstruction audit CPU cap'
        return {'D1':best,'attaining_seed':arg,'default_psi':psi[bv]}
    s=direct(r['source_B'],r['source_A']);t=direct(r['destination_B'],r['destination_A'])
    assert s['D1']==r['D1_source'] and t['D1']==r['D1_destination']
    o=c['options'][r['source_A']][r['option_index']];assert o==r['option'] and o[2]==r['destination_A']
    H,x,aa,g,fi,code=o;b=r['source_B']
    pair=(B['destinations'][b][x],2-B['depths'][b][x]//2) if H==1 else B['kernels'][str(g)][b][x]
    assert pair==[r['destination_B'],r['weight']] if isinstance(pair,list) else pair==(r['destination_B'],r['weight'])
    residual=r['weight']+t['D1']-s['D1'];assert residual==r['candidate_residual']<0
    out={'status':'INDEPENDENT_DIRECT_COUNTEREXAMPLE_AUDIT_PASS','source':s,'destination':t,'candidate_residual':residual,'direct_seed_candidates_visited':visited,'candidate_label_file_read':False,'old_production_predicates_replayed':0,'new_source_transition_queries':0,'saved_row_membership_pinned':True,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'original_negative_cycle_certified':False,'refutes_M3':False}
    write(OUT/'obstruction_audit.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(OUT/'obstruction_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
