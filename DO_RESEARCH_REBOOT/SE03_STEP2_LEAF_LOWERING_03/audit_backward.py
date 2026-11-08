"""Source-exact predecessor shapes; no replay of completed control words."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01';PREV=B.parent/'SE03_STEP2_FORCED_ZERO_INCOMING_02'
sys.path.insert(0,str(OLD))
from source_model import N,trace,core,path
M={1,3,5,7,9,11};account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(freeze(q) for q in v) if isinstance(v,list) else v
def leaves(t):return 0 if t is None else int(t[0] in M) if t[1] is None and t[2] is None else leaves(t[1])+leaves(t[2])
def unary(t):return t is None or ((t[0] in M or t[1] is None or t[2] is None) and unary(t[1]) and unary(t[2]))
def step(t,x):
    account['source_engine_calls']+=1
    return trace(t,x)
def main():
    records=json.loads((PREV/'forced_regions.json').read_text())['records'];rr=[]
    for r in records:
        a=freeze(r['F_state']['A']);bf=freeze(r['F_state']['BF']);pa=path(a,3)
        rec={'family':r['family'],'F_leaf_count':leaves(core(bf,M)),'F_A_path_to_old_B_root3':pa,
             'exact_F_state':r['F_state'],'exact_T_state':r['T_state']}
        if r['family']=='Gamma_pair':
            assert len(pa)>2
            rec['plus_one_predecessors']='NONE: only possible old BF root3 is deeper than2 in final A'
            rr.append(rec);continue
        assert pa=='R' and bf[0]==1 and bf[2][0]==2 and bf[2][2][0]==3
        # Unique inverse LL q1 full B input at old root3.
        left=bf[1];u=bf[2];g=u[2]
        b3=N(3,N(2,N(1,left,u[1]),g[1]),g[2])
        got,_,ev=step(b3,1);assert got==bf and len(ev)==1
        assert b3[1][0]==2 and b3[1][1][0]==1 and b3[2][0]==4 and b3[2][2][0]==5
        # Every q2 input yielding this B3 has path marks1,5,3; two orders.
        L2=b3[1];R4=b3[2];m1=L2[1];m5=R4[2]
        A,Bb=m1[1:];C=L2[2];D=R4[1];E,F=m5[1:]
        b1=N(1,A,N(2,Bb,N(5,N(4,N(3,C,D),E),F)))
        b5=N(5,N(4,N(1,A,N(2,Bb,N(3,C,D))),E),F)
        for q in (b1,b5):
            dest,_,ev=step(q,3);assert dest==b3 and len(ev)==2
        c=core(b1,M);assert c[0]==1 and unary(c) and leaves(c)<=3
        # Actual +1 A predecessor with zig; second family has an anonymous
        # parent rooted in F0 and old1 at LR, impossible for an H1 old root.
        assert a[2][0]==3 and a[2][1][0]==2
        az=N(3,N(1,a[1],a[2][1]),a[2][2]);got,_,ev=step(az,1);assert got==a and len(ev)==1
        assert len(path(az,5))>2
        # All ZIG-family zero predecessors have old root1, BF=b1.
        pz=N(1,az[1][1],N(3,az[1][2],az[2]));got,_,ev=step(pz,3);assert got==az and len(ev)==1
        right=az[2];pr=N(1,az[1][1],N(right[0],N(3,az[1][2],right[1]),right[2]))
        got,_,ev=step(pr,3);assert got==az and len(ev)==1
        rec.update({'plus_one_B_source':b3,'plus_one_B_source_leaf_count':leaves(core(b3,M)),
            'zig_A_source':az,'A_path_to_inadmissible_oldroot5':path(az,5),
            'q2_inverse_B_old1':b1,'q2_inverse_B_old5':b5,
            'old1_B_leaf_count':leaves(c),'old1_B_extreme_unary':True,
            'zig_family_A_zero_predecessors':[pz,pr],
            'anonymous_LR_family_old1_position':'LR; an H1 event cannot leave its old root there',
            'zero_backward_depth_into_plus_one_predecessors_at_most':1,
            'no_zero_T11_to_any_plus_one_predecessor':'PROVED_BY_SOURCE_CASES_NOT_BY_SEARCH'})
        rr.append(rec)
    actual=json.loads((PREV/'incoming_family_v2.json').read_text())
    pc=leaves(core(freeze(actual['predecessor']['BF']),M));assert pc==3
    out('backward_source_audit.json',{'status':'PASS_RESTRICTED_RETURN_SOURCE_SHAPES','records':rr,
        'C3_extension':'root extreme, unary unmarked separators, at most3 marked leaves; no incoming zero or negative packet',
        'Sigma_prior_prose_leaf_count_correction':{'actual':pc,'previous_prose':2,'previous_data_and_cap':'unchanged and valid'},
        'scope':'all actual states with these exact known A/BF source terms, arbitrary gaps, BE, erasure/recent context; not arbitrary F11',
        'general_R0_R1':'OPEN',**account})
    print(json.dumps({'status':'PASS_RESTRICTED_RETURN_SOURCE_SHAPES',
        'families':[{'name':r['family'],'path3':r['F_A_path_to_old_B_root3'],
            'predecessor_leaves':r.get('plus_one_B_source_leaf_count'),'C3_predecessor_leaves':r.get('old1_B_leaf_count')} for r in rr],
        'Sigma_corrected_leaf_count':pc,**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_backward_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
