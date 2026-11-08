"""Universal affine derivation certificates; no finite histories are tested."""
import ast,hashlib,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
start=time.process_time();cap=float(sys.argv[1]);error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def add(*ps):
    r={}
    for p in ps:
        for v,c in p.items():r[v]=r.get(v,0)+c
    return {v:c for v,c in r.items() if c}
def scale(k,p):return {v:k*c for v,c in p.items() if k*c}
def eq(n,l,r,records):
    assert add(l,scale(-1,r))=={},n
    records.append({'name':n,'left':l,'right':r,'status':'FORMAL_AFFINE_IDENTITY'})
try:
    records=[]
    h={'H':1};c={'C':1};q={'Q':1};d={'D':1};e={'E':1};m={'M':1}
    b=add(m,scale(-1,d));bn=add(m,scale(-1,e))
    s=add(scale(2,c),scale(-1,q),e,scale(-1,d))
    tail=add(scale(2,h),scale(-2,c))
    eq('post_payment_bank',add(b,scale(2,c),scale(-1,q)),add(bn,s),records)
    eq('reserve_per_macro',add(tail,s),add(scale(2,h),scale(-1,q),e,scale(-1,d)),records)
    eq('physical_local_conservation',add(scale(2,h),b),add(q,tail,s,bn),records)
    eq('bank_upper_bound',add({'one':2},scale(-1,b)),add({'one':2},scale(-1,m),d),records)
    eq('queue_peak_bound',add({'one':8},scale(-1,b),scale(-2,c)),
       add({'one':2},scale(-1,b),{'one':6},scale(-2,c)),records)
    # The two symbolic integer H branches, not a sample of H values.
    low_c=h; high_h=add({'one':3},{'T':1});high_c={'one':3}
    eq('LOW_exact_clipped_price',add(scale(2,h),scale(-1,q)),add(scale(2,low_c),scale(-1,q)),records)
    eq('HIGH_exact_clipped_price',add({'one':6},scale(-1,q)),add(scale(2,high_c),scale(-1,q)),records)
    eq('HIGH_tail_for_all_H_ge3',add(scale(2,high_h),scale(-2,high_c)),{'T':2},records)
    phi_s=add(scale(-1,d),{'chi':-5});phi_t=add(scale(-1,e),{'chi':-5})
    eq('constant_raw_chi_endpoint_difference',add(phi_t,scale(-1,phi_s)),add(d,scale(-1,e)),records)
    eq('signed_surplus_is_imported_edge_slack',s,
       add(scale(2,c),scale(-1,q),scale(-1,add(phi_t,scale(-1,phi_s)))),records)
    # Pure signed cancellation interfaces, with no desired bound assumed.
    u={'A2':1,'QE':-1};n={'N':1};p={'P':1}
    eq('available_pool',add(u,n),{'A2':1,'QE':-1,'N':1},records)
    eq('remaining_original_slack',add(u,n,scale(-1,p)),
       add({'A2':1,'QE':-1},scale(-1,add(p,scale(-1,n)))),records)
    cert=json.loads((ROOT/'DO_RESEARCH_REBOOT/M3_XFER21/M3_CERTIFICATE.json').read_text())
    assert cert['status']=='PROVED_UNIVERSAL_FULL_M3' and cert['debt_range']==[0,2]
    assert cert['corrected_h0']=={'actual_depth':0,'declared_depth':18,'q':9,'weight':-3}
    assert 'max(F4' in cert['ordinary_debt_equation']
    parsed=ast.parse((B/'source_allocation.py').read_text())
    imports={a.name for x in ast.walk(parsed) if isinstance(x,ast.Import) for a in x.names}
    froms={x.module for x in ast.walk(parsed) if isinstance(x,ast.ImportFrom)}
    assert not imports and froms=={'collections','dataclasses','typing'}
    assert not any(isinstance(x,(ast.Import,ast.ImportFrom)) and 'splay' in ast.unparse(x) for x in ast.walk(parsed))
    assert time.process_time()-start<cap
    out('derivation.json',{'status':'PASS_UNIVERSAL_AFFINE_PROOF_SCHEMAS','identities':records,
       'nonnegative_premises':['0<=D,E<=M<=2','C=min(H,3)','S=2C-Q+E-D>=0 from actual M3/source bridge'],
       'actual_source_event_IDs_required':True,'initial_bank':'M-D=0 at selected maximum debt',
       'cyclic_closure':'all source/abstract endpoints fully equal; D_end=D_start=M',
       'allocation_new_finite_inputs_run':0,'source_engine_calls':0,'old_semantic_rows_replayed':0,
       'Step1_scope':'auxiliary funding and explicit unused source units only',
       'original_marginal_repayment_proved':False,'uniform_support_induction_proved':False})
    print('PASS: universal clipped-bank/reserve identities; no finite input traces executed')
except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_derivation_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
