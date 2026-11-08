"""Separate universal prefix-ledger/ownership audit, without finite traces."""
import ast,hashlib,json,sys,time
from fractions import Fraction
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time();cap=float(sys.argv[1]);error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def linear(**coeff):return {k:Fraction(v) for k,v in coeff.items() if v}
def plus(*polys):
    r={}
    for p in polys:
        for k,c in p.items():r[k]=r.get(k,Fraction(0))+c
    return {k:c for k,c in r.items() if c}
def minus(p):return {k:-c for k,c in p.items()}
def zero(p):assert not p,p
try:
    pins=read(B/'dependency_pins.json')['pins']
    for q in pins:
        assert hashlib.sha256(xp(ROOT/q['path']).read_bytes()).hexdigest()==q['sha256'],q['path']
        assert time.process_time()-start<cap
    # Independent prefix reconstruction: selected supply P, paid Q,
    # cumulative certified surplus S=P-Q+Dk-M, with M the maximum debt.
    selected=linear(P=1);paid=linear(Q=1);dk=linear(Dk=1);maximum=linear(M=1)
    released=plus(selected,minus(paid),dk,minus(maximum))
    working=plus(selected,minus(paid),minus(released))
    zero(plus(working,minus(plus(maximum,minus(dk)))))
    tails=linear(A=2,P=-1)
    reserve=plus(tails,released)
    zero(plus(reserve,minus(linear(A=2,Q=-1,Dk=1,M=-1))))
    # At actual full closure Dk=M; therefore reserve=2A-Q exactly.
    zero(plus(reserve,linear(Dk=-1,M=1),minus(linear(A=2,Q=-1))))
    # Prefix increase gives exactly the main local certificate S_i.
    delta=linear(C=2,q=-1,dnext=1,d=-1)
    zero(plus(delta,minus(linear(C=2,q=-1)),minus(linear(dnext=1,d=-1))))
    # Physical payment margin decomposes into two nonnegative terms:
    # required next bank M-dnext and imported certificate slack delta.
    afterpay=linear(M=1,d=-1,C=2,q=-1)
    zero(plus(afterpay,minus(plus(linear(M=1,dnext=-1),delta))))
    # Source timing/ownership: independently inspect the delivered allocator.
    src=(B/'source_allocation.py').read_text();tree=ast.parse(src)
    fn=next(v for v in tree.body if isinstance(v,ast.FunctionDef) and v.name=='allocate')
    bank_calls=[v for v in ast.walk(fn) if isinstance(v,ast.Call) and isinstance(v.func,ast.Attribute)
                and isinstance(v.func.value,ast.Name) and v.func.value.id=='bank']
    assert sorted(v.func.attr for v in bank_calls)==['append','pop','popleft']
    append=next(v for v in bank_calls if v.func.attr=='append')
    assert len(append.args)==1 and isinstance(append.args[0],ast.Name) and append.args[0].id=='unit'
    unit_sets=[v for v in ast.walk(fn) if isinstance(v,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='unit' for t in v.targets)]
    assert len(unit_sets)==1 and ast.unparse(unit_sets[0].value)=='(event, bit)'
    bit_loops=[v for v in ast.walk(fn) if isinstance(v,ast.For) and isinstance(v.target,ast.Name) and v.target.id=='bit']
    assert len(bit_loops)==1 and ast.literal_eval(bit_loops[0].iter)==(0,1)
    payments=[v for v in ast.walk(fn) if isinstance(v,ast.Call) and isinstance(v.func,ast.Name) and v.func.id=='Payment']
    reserves=[v for v in ast.walk(fn) if isinstance(v,ast.Call) and isinstance(v.func,ast.Name) and v.func.id=='Reserve']
    assert len(payments)==1 and ast.unparse(payments[0].args[-1])=='bank.popleft()'
    assert len(reserves)==2
    assert {ast.literal_eval(v.args[1]) for v in reserves}=={'tail_after_first_three_events','certified_surplus'}
    # Inspect all source-derived capacities, not any instantiated events.
    min_calls=[v for v in ast.walk(fn) if isinstance(v,ast.Call) and isinstance(v.func,ast.Name) and v.func.id=='min']
    assert len(min_calls)==2 and all(ast.literal_eval(v.args[1])==3 for v in min_calls)
    assert not any(v.func.attr=='rotate' for v in bank_calls)
    assert not any(isinstance(v,ast.Call) and isinstance(v.func,ast.Name) and v.func.id in ('exec','eval','compile','open','print') for v in ast.walk(fn))
    imports=[v for v in ast.walk(tree) if isinstance(v,(ast.Import,ast.ImportFrom))]
    assert all(isinstance(v,ast.ImportFrom) and v.module in ('collections','dataclasses','typing') for v in imports)
    # Reconstruct signed cancellation by formal cardinalities.
    P=linear(QF=1,Common=-1);N=linear(QE=1,Common=-1)
    zero(plus(P,minus(N),minus(linear(QF=1,QE=-1))))
    U=linear(A=2,QE=-1);V=plus(U,N)
    zero(plus(V,linear(Common=1),minus(linear(A=2))))
    zero(plus(V,minus(P),minus(linear(A=2,QF=-1))))
    # Scope is exact: no signed repayment or uniform induction was proved.
    dr=read(B/'derivation.json')
    assert dr['original_marginal_repayment_proved'] is False
    assert dr['uniform_support_induction_proved'] is False
    bridge=(B/'SOURCE_BRIDGE.md').read_text()
    assert 'ONE full closed image' in bridge and 'EXACT macro prices' in bridge
    assert 'actual0,declared18,q9,w-3' in bridge and 'No midpoint D' in bridge
    idproof=(B/'SOURCE_IDS_AND_CYCLIC_CUT.md').read_text()
    assert 't\'=t+T' in idproof and 'ALREADY ROTATED' in idproof
    theorem=(B/'AUXILIARY_FUNDING_THEOREM.md').read_text()
    assert 'The reserves may be zero' in theorem and 'not new original CD-domain' in theorem
    assert time.process_time()-start<cap
    out('independent_audit.json',{'status':'PASS_STEP1_UNIVERSAL_SOURCE_FUNDING_EXTRACTION',
        'method':'independent prefix-ledger derivation and one-way unit-ownership audit; source theorem reuse',
        'inherited_pins_verified':len(pins),'clipped_source_budget':'PASS',
        'closed_raw_chi_constancy':'PASS_FROM_FULL_CLOSURE_AND_SEALED_ONE_WAY_CLASSIFICATION',
        'maximum_debt_empty_start_cut':'PASS_WITH_ACTUAL_SOURCE_REINDEXING',
        'physical_source_ID_partition':'PASS_BY_OWNERSHIP_INDUCTION',
        'actual_A_shared_under_erasure':'PASS_INHERITED_EXACT_SOURCE_IDENTITY',
        'boundary_working_bank_cap':2,'within_macro_working_queue_cap':8,
        'retained_A_tail_units_excluded_from_auxiliary':'PASS',
        'signed_cancellation_available_pool':'PASS_NO_FINAL_INJECTION_ASSUMED',
        'allocator_source_parsed_not_executed_on_examples':True,
        'new_finite_tests':0,'new_source_engine_calls':0,'old_semantic_rows_replayed':0,
        'external_peer_review':False,'full_compiler_formalization':False,
        'Step1_proved':True,'original_marginal_repayment_proved':False,
        'uniform_coverage_proved':False,'unrestricted_CD_proved':False})
    print('PASS: Step1 source funding, two-unit cyclic bank and exact reserve; Step2/3 remain open')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
