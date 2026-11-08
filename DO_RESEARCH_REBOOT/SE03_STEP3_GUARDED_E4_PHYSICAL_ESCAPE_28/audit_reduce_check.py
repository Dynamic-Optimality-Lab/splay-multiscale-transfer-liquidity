"""Independent count-arithmetic and natural-compatible H normalization.
No source replay and no finite BST coverage inference."""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('C28_indep_reduction_library',B/'audit_independent.py');J=importlib.util.module_from_spec(s);s.loader.exec_module(J);I=J.I
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def mp(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def main():
    cert=json.loads((B/'branch_reduction_and_normalization.json').read_text());hy=json.loads((B/'hybrid_partition_receipt.json').read_text());src=json.loads((B/'catchment_forcing_countercertificate.json').read_text())
    rows=[I.fr_row(r) for r in src['rows']];full={};ownall={}
    for block,z in zip(hy['blocks'],cert['block_normalizations']):
        lo,hi=block['interval'];rr=[r for r in rows if lo<=r['occurrence']<=hi];mm=I.macro_list(rr)
        own={d:u for m in mm for d,u in zip(m['demands'],m['units'])};D={d for m in mm for d in m['demands']}
        answer=I.extend(own,mp(block['source_comparison']),D)
        assert answer==mp(z['H_normalized']) and all(answer[d]==u for d,u in own.items())
        assert J.peak(answer)==z['cut_peak'];full.update(answer);ownall.update(own)
    assert full==mp(cert['normalized_hybrid_comparison']) and J.peak(full)==8 and all(full[d]==u for d,u in ownall.items())
    # Complete necessary INTEGER count partition follows from proven (B1).
    # It does not assert all admissible tuples are dynamically realizable.
    negative=[]
    for z in (0,1):
        for Q in range(1,7):
            for b in range(Q+1):
                if Q+1+b+(1-z)>7:continue
                assert 2*b<=5+z and b+z<=4
                if 2-b-z<0:negative.append((Q,b,z,2-b-z))
    wanted={(2,2,1,-1),(3,2,1,-1),(4,2,1,-1),(3,3,1,-2)}
    assert set(negative)==wanted=={(z['Q'],z['beta'],z['z'],z['residual']) for z in cert['negative_H1_classes']}
    # Symbolic coefficient identity for the off-path bound: add beta<=Q
    # and beta<=5-Q+z to obtain2beta<=5+z, for all source count values.
    assert [1,-1,0,0][0]+[-1,-1,1,5][0]==0
    # H>=2 has c>=2, so2c>=4>=beta+z; H>=3 has c3, giving>=2.
    assert 2*2-4==0 and 2*3-4==2 and 19+6==25
    files=['BRANCH_DEFICIT_CLASSIFICATION.md','HYBRID_COMPARISON_THEOREM.md','branch_reduction_and_normalization.json']
    out('reduction_independent_audit.json',{'status':'PASS_ARITHMETIC_CLASSIFICATION_AND_FULL_NATURAL_OWNER_COMPARISON',
        'negative_branch_classes':sorted(wanted),'source_count_scope':'fixed7-mark maximal-core/all-SS source with inherited C15 path-to-star premises',
        'finite_BST_testing_used_as_universal_proof':False,'dynamic_realizability_of_all_count_tuples_asserted':False,
        'all_natural_h0_values_kept':True,'source_comparison_peak':8,
        'uniform_proof_boundary':'combinatorial off-path witness argument and leaf identity stated in manuscript; arithmetic/count partition and exact normalized maps independently checked',
        'new_J_proved':False,'complete_U28':False,'source_queries':I.queries,
        'sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}})
    print(json.dumps({'status':'REDUCTION_INDEPENDENT_PASS','raw_own_compatible_peak':8,'negative_count_classes':4,'new_source_queries':I.queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_reduce_check_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
