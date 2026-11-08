"""Independent free-term terminal identities for the manuscript parity proof.

No producer search, finite-population experiment or new source replay.
The unbounded-depth lifting is the manuscript's common-prefix induction;
this checks its exhaustive terminal identities using the existing zipper.
"""
import hashlib,json,sys,time
from pathlib import Path
from audit_verify36 import calc,mirror

B=Path(__file__).resolve().parent
CAP=float(sys.argv[1]);START=time.process_time()

def out(name,value):
    with (B/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2)

def leaves(t):
    return leaves(t[1])+leaves(t[2]) if isinstance(t,tuple) else [t]

def main():
    G,p,R=0,2,10
    rows=[]
    for kind in ('EVEN','ODD_LEFT','ODD_RIGHT'):
        if kind=='EVEN':
            y=5;X=(y,'L','U')
            targets=((y,(p,(G,'A','J'),'L'),(R,'U','E')),)*2
            costs=(2,1)
        elif kind=='ODD_LEFT':
            y,z=4,6;X=(z,(y,'L','U'),'V')
            targets=((y,(G,'A',(p,'J','L')),(R,(z,'U','V'),'E')),
                     (y,(p,(G,'A','J'),'L'),(R,(z,'U','V'),'E')))
            costs=(2,2)
        else:
            y,z=6,4;X=(z,'V',(y,'L','U'))
            targets=((y,(G,'A',(z,(p,'J','V'),'L')),(R,'U','E')),
                     (y,(z,(p,(G,'A','J'),'V'),'L'),(R,'U','E')))
            costs=(2,2)
        sources=((R,(G,'A',(p,'J',X)),'E'),
                 (R,(p,(G,'A','J'),X),'E'))
        for i in range(2):
            actual,h=calc(sources[i],y)
            assert actual==targets[i] and h==costs[i]
            assert sorted(leaves(sources[i]))==sorted(leaves(actual))
            reflected,rh=calc(mirror(sources[i],20),20-y)
            assert reflected==mirror(targets[i],20) and rh==h
        assert (targets[0]==targets[1])==(kind=='EVEN')
        rows.append({'terminal_class':kind,'source_terms':sources,
                     'target':y,'result_terms':targets,'event_costs':costs,
                     'reflected_identity_checked':True})
    assert time.process_time()-START<CAP-1
    names=('FRAMED_FIRST_CONSUMER_PARITY.md','audit_verify64.py',
           'audit_verify36.py','framed_return_and_core13_independent_audit.json')
    prior=json.loads((B/names[-1]).read_text())
    assert prior['status']=='PASS_UNIFORM_FRAME_RETURN_IDENTITIES_AND_ORIGINAL_CORE13_CLOSED_SOURCE'
    result={'status':'PASS_FRAMED_PARITY_FREE_TERM_BASE_IDENTITIES',
            'method':'separate zipper kernel; manual producer algebra has no executable search',
            'terminal_classes':rows,'original_identities':6,'reflected_identities':6,
            'arbitrary_depth_lifting':'manuscript common-X bottom-up-double induction; not a finite-depth test',
            'arbitrary_ordered_subtree_payloads':True,
            'physical_funding_theorem':False,'normalized_owner_theorem':False,
            'Bank25_theorem':False,'principal_U33':'OPEN',
            'source_queries':0,'source_engine_calls':0,
            'fresh_source_replay':False,'external_or_formal_verification':False,
            'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}}
    out('framed_first_consumer_parity_independent_audit.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('terminal_classes','input_sha256')}))

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('audit_verify64_exit.json',{'whole_process_CPU_seconds':time.process_time(),
                                         'error':error,'source_queries':0,'source_engine_calls':0})
