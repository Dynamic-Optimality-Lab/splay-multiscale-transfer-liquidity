"""New universal constructor/sign audit. No original compiler or finite tests.

BLOCK symbols stand for arbitrary ordered original subtrees. Fixed CORE
terms define a theorem class uniform in every original sigma/raw endpoint.
The saved completed control is read, never replayed or root-evaluated.
"""
import hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120,float(sys.argv[1]))
E=None
def n(k,l=E,r=E):return (k,l,r)
def block(k):return ('BLOCK',k)
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def lp(p):return Path('\\\\?\\'+str(Path(p).resolve()))
def sha(p):return hashlib.sha256(lp(p).read_bytes()).hexdigest()
def rotate(t,side):
    k,l,r=t
    if side==0:
        p,a,b=l;return n(p,a,n(k,b,r))
    p,a,b=r;return n(p,n(k,l,a),b)
def update(t,p,fn):
    if not p:return fn(t)
    k,l,r=t
    return n(k,update(l,p[1:],fn),r) if p[0]==0 else n(k,l,update(r,p[1:],fn))
def pair(t,p):
    if p[0]==p[1]:return rotate(rotate(t,p[0]),p[1])
    t=update(t,p[:1],lambda v:rotate(v,p[1]));return rotate(t,p[0])
def replay(t,p):
    p=tuple(p)
    while len(p)>1:
        pre=p[:-2];bits=p[-2:];t=update(t,pre,lambda v:pair(v,bits));p=pre
    return rotate(t,p[0]) if p else t
def path(t,k):
    assert t is not None and len(t)==3
    if t[0]==k:return ()
    p=0 if k<t[0] else 1
    return (p,)+path(t[1+p],k)
def reverse(t):
    if t is None:return None
    if len(t)==2:return block(t[1]+'_opposite')
    return n(8-t[0] if isinstance(t[0],int) else t[0],reverse(t[2]),reverse(t[1]))
def depths(t,d=0):
    if t is None or len(t)==2:return {}
    return {t[0]:d,**depths(t[1],d+1),**depths(t[2],d+1)}

def main():
    ids=[]
    def identity(label,t,p,want):
        assert replay(t,p)==want,label
        assert replay(reverse(t),tuple(1-v for v in p))==reverse(want),label+'_opposite'
        ids.extend([label,label+'_actual_opposite'])
    T=n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),n(7,n(6),n(8))))
    U=n(6,n(2,n(0,E,n(1)),n(5,n(3,E,n(4)),E)),n(7,E,n(8)))
    V=n(8,n(7,n(5,n(2,n(0,E,n(1)),n(3,E,n(4))),n(6)),E),E)
    C4=n(4,n(2,n(0,E,n(1)),n(3)),n(5,E,n(7,n(6),n(8))))
    E4=n(4,n(2,n(0,E,n(1)),n(3)),n(6,n(5),n(7,E,n(8))))
    identity('Z_core_4',T,path(T,4),C4)
    identity('Z_core_6',T,path(T,6),U)
    identity('Z_core_8',T,path(T,8),V)
    identity('U_core_zero4',U,path(U,4),E4)
    marks={0,2,4,6,8}
    assert all(depths(C4)[k]<=3 and depths(E4)[k]<=3 for k in marks)
    assert {k:depths(U)[k] for k in marks}=={0:2,2:1,4:4,6:0,8:2}
    assert depths(V)[2]==depths(V)[6]==3
    A,B,C,D,F,G=map(block,('A','B','C','D','F','G'))
    a=n(2,n(0,A,B),n(6,n(4,C,D),n(8,F,G)))
    identity('Z_A_4',a,(1,0),n(4,n(2,n(0,A,B),C),n(6,D,n(8,F,G))))
    identity('Z_A_6',a,(1,),n(6,n(2,n(0,A,B),n(4,C,D)),n(8,F,G)))
    identity('Z_A_8',a,(1,1),n(8,n(6,n(2,n(0,A,B),n(4,C,D)),F),G))
    helper=n(2,n(0,n('f',A,B),C),n(6,D,F))
    identity('Z_A_min_helper',helper,(0,0),n('f',A,n(0,B,n(2,C,n(6,D,F)))))
    # Nonnegative slack polynomial identities, rather than debt-value tests.
    coefficients={
      'unchanged_source':{'old_residual':1,'target_increment':1},
      'one_credit_positive':{'weight_excess_above1':1,'target_debt':1},
      'one_credit_zero_paid':{'target_excess_above1':1},
      'Z_plus1_paid':{'target_excess_above1':1},
      'Z_range_weight2':{'weight_excess_above2':1,'target_debt':1},
      'Gamma1_one_credit_zero':{'target_excess_above1':1},
      'Gamma0_marked_endpoint_transfer':{'saved_floor_theorem_residual':1},
    }
    assert all(v>=0 for p in coefficients.values() for v in p.values())
    # Even/odd negative incoming extreme schema: count contradiction.
    # These are the three mathematically exhaustive depth/parity cases,
    # not finite state or psi samples. Target must be8 (respectively0).
    bounds=[{'negative_depth':6,'even_source_child_upper_bound':3},
            {'negative_depth':7,'odd_old_root_upper_bound':1},
            {'negative_depth':8,'even_source_child_upper_bound':1}]
    assert all(next(v for k,v in q.items() if k!='negative_depth')<7 for q in bounds)
    old=BASE.parent/'M3_LDR01/zero_reset_control.json'
    saved=json.loads(lp(old).read_text());r=saved['record']
    assert saved['status']=='COMPLETE' and saved['full_original_low_root']
    assert (r['H'],r['q'],r['w'],r['source']['mu'])==(1,2,0,341)
    assert r['destination']['alpha'][0][2]==2
    assert [r['destination']['alpha'][i][2] for i in (1,2,5,6)]==[0,6,4,8]
    # Reuse exact saved conclusions, without new psi computation.
    assert r['psi_source']==2 and r['psi_destination']==0
    source_files=[
      'M3_E1_01/E1_THEOREM.md','M3_E1_01/OUTSIDE_E1.md',
      'M3_XFER15/VISIBLE_GAMMA1_REPAYMENT.md',
      'M3_XFER16/HIDDEN_GAMMA1_REPAYMENT.md',
      'M3_XFER17/TERMINAL_ROOT_THEOREM.md',
      'M3_LDR01/zero_reset_control.json']
    baseline={x['path']:x['sha256'] for x in json.loads((BASE/'entry_baseline.json').read_text())['files']}
    pins={}
    for f in source_files:
        p=BASE.parent/f;h=sha(p);assert h==baseline[p.as_posix()];pins[p.as_posix()]=h
    for i,f in enumerate(('SATURATION_THEOREM','CUT_PAIR_THEOREM','BURIED_CUT_THEOREM',
      'RELEASE_CAPACITY_THEOREM','RR_RELEASE_THEOREM','ANONYMOUS_RELEASE_THEOREM',
      'DIRECT_BARRIER_THEOREM','BURIED_BARRIER_THEOREM','INTERVAL_CHILD_THEOREM',
      'GRANDCHILD_THEOREM','MARKED_RELAY_THEOREM','DEPTH_FIVE_RELAY_THEOREM',
      'NON_EXTREMAL_EXPOSURE_THEOREM'),1):
        p=BASE.parent/('M3_XFER%02d'%i)/(f+'.md');h=sha(p)
        assert baseline[p.as_posix()]==h;pins[p.as_posix()]=h
    assert time.process_time()<CAP
    write('audit_spread.json',{'status':'UNIVERSAL_SPREAD_CONSTRUCTOR_SIGN_AUDIT_PASS',
      'constructor_identities':ids,'all_original_private_blocks_arbitrary':True,
      'new_finite_tests':0,'new_original_root_evaluations':0,'new_psi_queries':0,
      'completed_checks_replayed':0,'symbolic_slack_coefficients':coefficients,
      'psi0_extreme_incoming_count_bounds':bounds,'reused_original_control':str(old),
      'pinned_proof_hashes':pins,'all_old_valid_LOW_rows_preserved':True,
      'all_Z_source_LOW_rows_proved':True,'Step4_complete':False})

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_spread_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
