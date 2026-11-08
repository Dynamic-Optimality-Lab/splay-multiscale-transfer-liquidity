"""Exact symbolic source-block/metric-family certificate, no source sampling."""
import hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'SOURCE_AUGMENTATION_02';P=B.parent.parent
START=time.process_time();CAP=float(sys.argv[1])
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(c,a):return tuple(c*x for x in a)
def left(t):
    x,A,u=t;y,B,C=u;return y,(x,A,B),C
def main():
    # Coefficients [constant,k], r=7+k for EVERY integer k>=0.
    r=(7,1);n=(13,2);one=(1,0);Hprep=(5,1);Qcrit=(6,1)
    assert sub(scale(2,r),one)==n
    weight=sub(scale(2,one),Qcrit);deficit=sub(Qcrit,scale(2,one))
    spare=sub(scale(2,Hprep),one);Hblock=add(Hprep,one);Qblock=add(Qcrit,one)
    margin=sub(scale(2,Hblock),Qblock);distance=sub(n,scale(2,one))
    assert weight==(-4,-1) and deficit==(4,1) and spare==(9,2)
    assert all(x>=0 for x in sub(spare,deficit)) and margin==(5,1)
    assert sub(scale(2,Hprep),sub(n,scale(4,one)))==one
    # Universal free-term RR identity, inherited odd-vine induction step.
    t=('a','A',('b','B',('n','C','D')))
    assert left(left(t))==('n',('b',('a','A','B'),'C'),'D')
    assert left(('1','empty',('n','L','empty')))==('n',('1','empty','L'),'empty')
    source=P/'SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md'
    prior=json.loads((B/'framed_family_repayment_independent_audit.json').read_text())
    assert pin(source)==prior['input_sha256'][str(source)]
    realization=B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md';rr=json.loads((B/'uniform_A_realization_independent_audit.json').read_text())
    assert rr['status']=='PASS_UNIFORM_SOURCE_REALIZATION_COROLLARY_INTERFACE_AUDIT'
    assert pin(realization)==rr['input_sha256'][realization.name]
    bank=B/'prepared_frame_static_bank_independent_audit.json';br=json.loads(bank.read_text())
    assert br['status']=='PASS_PREPARED_ALL_R_SOURCE_LICENSE_A_STATIC_WORKING_BANK2'
    cert={'status':'PRODUCER_UNIFORM_SOURCE_BLOCK_AND_GEOMETRIC_DEBT_CERTIFICATE',
      'quantifier':'all integers r=7+k, k>=0; no bounded source/population enumeration',
      'affine_coefficients':{'r':r,'n':n,'Hprep_lower':Hprep,'Qcritical':Qcrit,'critical_weight':weight,'critical_natural_excess':deficit,'predecessor_spares_lower':spare,'block_H_lower':Hblock,'block_Q':Qblock,'block_margin_lower':margin,'both_endpoint_rotation_distances':distance,'both_endpoint_interval_mismatch':distance},
      'RR_free_term_identity':'PASS','A_zig_free_term_identity':'PASS',
      'source_realization':'inherited exact same-key transformation corollary over the independently proved closed W_r/H_r B trajectory; all prep/reset operations retained',
      'metric_refutation_scope':'any debt of (n,r,rotation_distance,subtree_interval_mismatch) on every natural packet; not all source debts or all packetizations',
      'source_counterfamily':'mathematical existence via pinned transformation words; no new finite explicit Gamma replay claimed',
      'family_source_funding':'explicit previous-macro spare ordinals and source-solvent two-macro block; all other macros Q<=2,H>=1; static working2',
      'arbitrary_dirty_source_augmentation':'OPEN','universal_bank25':'OPEN','principal_C33':'OPEN',
      'source_queries':0,'source_engine_calls':0,
      'input_sha256':{str(source):pin(source),str(realization):pin(realization),str(B/'uniform_A_realization_independent_audit.json'):pin(B/'uniform_A_realization_independent_audit.json'),str(bank):pin(bank),str(B/'PREPARED_FRAME_STATIC_BANK25.md'):pin(B/'PREPARED_FRAME_STATIC_BANK25.md')}}
    out('symbolic_source_certificate.json',cert);assert time.process_time()-START<CAP-1
    print(json.dumps({k:cert[k] for k in ('status','quantifier','source_queries','principal_C33')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof165_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
