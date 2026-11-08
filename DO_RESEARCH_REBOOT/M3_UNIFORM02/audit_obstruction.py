"""Direct promotion evaluation at failed endpoints, without final D labels."""
import json,sys,time,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent;INDEX=int(sys.argv[1]);CAP=min(300,float(sys.argv[2]));OUT=BASE/f'case_{INDEX:03d}'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    start=time.process_time();r=read(OUT/'obstruction.json');build=read(OUT/'construction.json');source=Path(build['source_folder']);c=read(source/'relation.json');B=read(BASE.parent/'M3_UNITPAIR01/B_bank.json');psi=B['psi'];N=c['classes'];identity=read(OUT/'formula_identity_audit.json');p=OUT/'C_values.json'
    assert identity['status']=='INDEPENDENT_SIGN_RUN_FORMULA_IDENTITY_PASS' and hashlib.sha256(p.read_bytes()).hexdigest()==identity['C_sha256']
    Cvalues=read(p)['values'];visited=0
    assert N+c['option_count']+len(Cvalues)+43758<2000000 and c['queries']<=2000000
    def C(b,a):return Cvalues.get(str(b*N+a),psi[b])
    def direct(bv,av):
        nonlocal visited
        base=C(bv,av)
        if psi[bv]==2 or base==2:return {'D_run':2,'C':base,'psi':psi[bv],'reason':'seed_or_C_already_two','attainment':None}
        if psi[bv]==0:return {'D_run':base,'C':base,'psi':0,'reason':'negative_core_debt_law_excludes_incoming_negative_rows','attainment':None}
        assert psi[bv]==base==1;incoming={}
        for b,t in enumerate(B['trees']):
            if psi[b]!=0:continue
            for x in range(9):
                depth=B['depths'][b][x]
                if depth and 2-depth//2==-1 and B['destinations'][b][x]==bv:incoming.setdefault((x,t[0]),[]).append(b)
        for a,options in enumerate(c['options']):
            root=c['shadows'][a][0][2]
            for oi,o in enumerate(options):
                H,x,aa,g,fi,code=o
                if H!=1 or aa!=av:continue
                for bs in incoming.get((x,root),()):
                    visited+=1
                    if C(bs,a)>0:return {'D_run':2,'C':1,'psi':1,'reason':'attained_negative_promotion_with_universal_upper_two','attainment':{'source_B':bs,'source_A':a,'option_index':oi,'weight':-1,'source_C':C(bs,a)}}
            if a%256==0:assert time.process_time()-start<CAP,'UNKNOWN direct promotion audit CPU cap'
        return {'D_run':1,'C':1,'psi':1,'reason':'all_incoming_promotion_candidates_exhausted','attainment':None}
    s=direct(r['source_B'],r['source_A']);t=direct(r['destination_B'],r['destination_A'])
    assert s['D_run']==r['D_run_source'] and t['D_run']==r['D_run_destination']
    o=c['options'][r['source_A']][r['option_index']];assert o==r['option'] and o[2]==r['destination_A'];H,x,aa,g,fi,code=o;b=r['source_B']
    pair=(B['destinations'][b][x],2-B['depths'][b][x]//2) if H==1 else B['kernels'][str(g)][b][x]
    assert tuple(pair)==(r['destination_B'],r['weight']);res=pair[1]+t['D_run']-s['D_run'];assert res==r['candidate_residual']<0
    out={'status':'INDEPENDENT_PROMOTION_ENDPOINT_AUDIT_PASS','source':s,'destination':t,'candidate_residual':res,'direct_promotion_candidates_visited':visited,'final_candidate_labels_read':False,'C_input_identity_independently_proved':True,'old_original_controls_repeated':0,'new_source_word_queries':0,'CPU_seconds':time.process_time()-start,'CPU_cap':CAP,'refutes_M3':False,'original_negative_cycle_certified':False}
    write(OUT/'obstruction_audit.json',out);print(json.dumps(out),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error={'type':type(e).__name__,'message':str(e)};raise
    finally:write(OUT/'obstruction_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
