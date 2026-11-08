"""Separate unary theorem seal before continuing to larger source classes."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    for phase in ('grammar','lift','independent','source'):assert read('run_'+phase+'_result.json')['status']=='PASS'
    s=read('independent_unary_audit.json');assert s['correction']==0 and s['old_A6_debt_unchanged']
    assert s['LOW_rows']=={'1':437068,'2':1225153} and s['range']==[0,2]
    src=read('unary_source_receipt.json');assert src['status']=='PASS_REACHABLE_NONVACUOUS_UNARY_SOURCE_FUNDING'
    assert src['rows'][-1]['after']==src['rows'][0]['before'] and src['all_old_values_fixed']
    assert any(1 in row['anon_counts'] for row in src['source_receipt'])
    for p in read('dependency_pins.json')['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    names=['UNARY_LIFT_THEOREM.md','unary_grammar.py','unary_grammar.json','unary_funding.py',
        'unary_lift_certificate.json','independent_unary_audit.json','unary_source_receipt.json']
    out('unary_seal.json',{'status':'PROVED_UNIVERSAL_NAMED_UNARY_SOURCE_DOMAIN','correction':0,
        'domain':'core9 BF mask{1,2,3,5,7,9}; zero/one unmarked unary A marked-core vertex at natural boundaries',
        'all_private_hangers':'arbitrary ordered BSTs, exact free-gap lifting','all_prior_owners':'fixed',
        'files':[{'path':n,'sha256':sha(B/n)} for n in names],
        'core9_full':'OPEN','core10_11_full':'OPEN','Step2':'OPEN','CD6':'OPEN'})
    print(json.dumps({'status':'CORE9_UNARY_LIFT_SEPARATELY_SEALED','correction':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal_unary_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})
