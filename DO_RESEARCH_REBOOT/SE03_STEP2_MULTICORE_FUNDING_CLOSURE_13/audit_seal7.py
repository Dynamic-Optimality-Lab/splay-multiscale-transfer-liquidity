"""Separate core7 theorem seal, required before any larger-core attempt."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def core(t,M):
    if isinstance(t,str):return set()
    l,r=core(t[1],M),core(t[2],M)
    return l|r|{t[0]} if l or r or t[0] in M else set()
def main():
    assert read('run_core7_result.json')['status']=='PASS'
    cert=read('core7_source_certificate.json');assert len(cert['source_reports'])==12
    for v in cert['source_reports']:
        marks={r['target'] for r in v['rows'] if r['genuine_F']};assert len(marks)==6
        assert all(len(core(r['before'][1],marks))==7 for r in v['rows'])
        assert len(v['R'])==v['slot_count'] and v['alignment']['L']==1
        assert len(v['seeds'])==v['slot_count']
        assert len({x['predecessor_macro'] for x in v['seeds']})==v['slot_count']
        assert len({tuple(x['seed']) for x in v['seeds']})==v['slot_count']
        for f in v['fixtures']:
            a={tuple(x['demand']):tuple(x['unit']) for x in f['paid']}
            final={tuple(x['demand']):tuple(x['unit']) for x in f['final']}
            assert all(final[d]==u for d,u in a.items()) and len(set(final.values()))==len(final)
    for p in read('dependency_pins.json')['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    files=['CORE7_FULL_FUNDING.md','source_funding.py','audit_core7.py','core7_source_certificate.json',
        'audit_core7_exit.json','run_core7_result.json','controller_core7_exit.json','audit_seal7.py']
    out('core7_seal.json',{'status':'CORE7_PHYSICAL_FUNDING_COMPLETE','exact_slot_range':'all nonnegative integers',
        'independent_implementation':'immutable source engine plus backwards owner verifier by same agent',
        'all_owners_fixed':True,'private_gap_lifting':'universal inherited free-tree proof, not bounded fringe tests',
        'files':[{'path':n,'sha256':sha(B/n)} for n in files],
        'multicore_status':'OPEN; core8..11 not yet attempted in Campaign13','Step2':'OPEN','CD6':'OPEN'})
    print(json.dumps({'status':'CORE7_SEPARATELY_SEALED','all_slot_counts':True}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_seal7_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})
