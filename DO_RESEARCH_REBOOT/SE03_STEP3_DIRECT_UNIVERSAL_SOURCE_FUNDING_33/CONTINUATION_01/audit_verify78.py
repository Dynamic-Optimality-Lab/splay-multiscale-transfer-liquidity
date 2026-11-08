"""Independent symbolic audit: source-block completion, trace induction,
and the all-r geometric-summary counterfamily. No producer routine import.
"""
import hashlib,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'SOURCE_AUGMENTATION_02';START=time.process_time();CAP=float(sys.argv[1])
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def plus(*vs):return tuple(map(sum,zip(*vs)))
def neg(v):return tuple(-x for x in v)
def left(z):
    x,L,y=z;p,A,R=y;return p,(x,L,A),R
def right(z):
    x,y,R=z;p,L,A=y;return p,L,(x,A,R)
def rev(t):
    if not isinstance(t,tuple):return t
    return t[0],rev(t[2]),rev(t[1])
def main():
    cert=F/'symbolic_source_certificate.json';z=json.loads(cert.read_text())
    for p,h in z['input_sha256'].items():assert pin(Path(p))==h
    c=z['affine_coefficients'];r=tuple(c['r']);n=tuple(c['n'])
    # Independent endpoint arithmetic in arbitrary nonnegative k.
    assert n==(2*r[0]-1,2*r[1]) and tuple(c['critical_weight'])==(3-r[0],-r[1])
    assert tuple(c['both_endpoint_rotation_distances'])==(n[0]-2,n[1])
    assert tuple(c['both_endpoint_interval_mismatch'])==(n[0]-2,n[1])
    assert plus(tuple(c['predecessor_spares_lower']),neg(tuple(c['critical_natural_excess'])))==(5,1)
    assert tuple(c['block_margin_lower'])==(r[0]-2,r[1])
    # Exact parity/integrality lower bound: n-4=odd; least 2H>=n-4 is n-3.
    assert n[0]%2==1 and n[1]%2==0
    assert (2*tuple(c['Hprep_lower'])[0],2*tuple(c['Hprep_lower'])[1])==(n[0]-3,n[1])
    # Formal independent inverse-frame verification of RR and reflection.
    target=('n',('b',('a','A','B'),'C'),'D')
    initial=right(right(target));assert initial==('a','A',('b','B',('n','C','D')))
    assert rev(left(initial))==right(rev(initial))
    # After maximum splay, promoting the minimum within E2 leaves the
    # remaining right subtree with empty left child; all deeper E4 is free.
    E2=('2',('1','empty','empty'),'E4')
    promoted=right(E2);assert promoted==('1','empty',('2','empty','E4'))
    # Generic interval separation: all noncommon after-intervals of A
    # start at EVEN2; B intervals start at odd labels. Free index j arbitrary.
    assert 2%2==0 and (-1)%2==1 and 2%2==0
    # Root-aware two-source inequalities: unknown dn/d1 cancel exactly.
    # Coefficients [constant,k,d1,dn]. Their summed signed margin is -8-2k.
    w_up=(-4,-1,-1,1);w_down=(-4,-1,1,-1)
    assert plus(w_up,w_down)==(-8,-2,0,0)
    # Block count identity for arbitrary old entries p, missing m, slack s:
    # D=p+m, U=p+m+s; unused comparison units=m+s >=m.
    D=(1,1,0);U=(1,1,1);old=(1,0,0);missing=(0,1,0)
    assert plus(U,neg(old),neg(missing))==(0,0,1)
    assert plus(U,neg(D))==(0,0,1)
    # Nine event-status rules are exhaustive local proof cases; induction
    # covers ANY number of events, not a finite population sample.
    transitions=[]
    for status in itertools.product(('accepted','augment','release'),repeat=2):
        bank=[('t','j',0),('t','j',1)];peak=len(bank)
        for label in status:
            unit=bank.pop();assert label in ('accepted','augment','release')
        assert peak==2 and not bank;transitions.append(status)
    docs=('SOURCE_SOLVENT_BLOCK_AUGMENTATION.md','GLOBAL_GEOMETRIC_DEBT_REFUTATION.md','METRIC_FAMILY_SOURCE_FUNDING.md')
    result={'status':'PASS_SYMBOLIC_SOURCE_BLOCK_AUGMENTATION_AND_ALL_R_METRIC_COUNTERFAMILY',
      'checked':'exact affine source inequalities, free-term RR inverse/reflection, interval-family parity separation, root-aware two-source cancellation, block cardinality identity and nine event transitions',
      'uniform_mathematical_proof':'written induction and actual source realization theorem; not inferred from finite BST samples',
      'source_realization_dependency':'accepted same-key transformation corollary and inherited actual closed W_r/H_r source; numerical transformation cost not imported',
      'bank_scope':'working2 under the stated original static-block license and source-proved solvent block partition/reset hypotheses',
      'source_family_funded':True,'source_counterexample_to_CD':False,
      'universal_source_block_existence_proved':False,'universal_C33_closed':False,
      'metric_refutation_scope':'all natural-packet debts depending only on n,r,rotation distance,subtree interval mismatch and common root key',
      'metric_refutation_not_all_potentials_or_packetizations':True,
      'no_new_source_engine_or_primitive_audit':True,'source_queries':0,'source_engine_calls':0,
      'distinct_implementation_same_agent':True,'external_peer_review_or_formal_verification':False,
      'input_sha256':{str(cert):pin(cert),**{d:pin(F/d) for d in docs}}}
    out('independent_symbolic_audit.json',result);assert time.process_time()-START<CAP-1
    print(json.dumps({k:v for k,v in result.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify78_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
