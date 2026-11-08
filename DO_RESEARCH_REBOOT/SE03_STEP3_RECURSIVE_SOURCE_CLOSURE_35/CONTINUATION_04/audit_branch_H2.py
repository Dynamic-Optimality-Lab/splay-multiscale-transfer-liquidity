"""Independent full relation regeneration, with fresh prototype-only audit.
The old C14 grammar is rebound to certified WHOLE-source-action identities.
All such substitutions are reported; only new mutable source calls count
as fresh source queries. No producer-side audit allowance is used.
"""
import hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];sys.path.insert(0,str(F))
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();PHASE=sys.argv[3];PART=int(sys.argv[4]);CALLS=0
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def empty(t):return None if isinstance(t,str) or t is None else (t[0],empty(t[1]),empty(t[2]))
def main():
    global CALLS
    g=module(F/'independent_H2_grammar.py','independent_low2_grammar35');prod=read(F/'branch_H2_r7.json');one=read(F/'branch_H1_r7.json')
    assert prod['native_cache_sha256']==sha(B/'native10_source_actions.json')
    for p,h in prod['input_sha256'].items():assert sha(F/p)==h
    if PART==1:
        v=module(B/'audit_verify79.py','mutable_prototype_CF35');v.CAP=CAP;v.START=START;v.QCAP=QCAP;v.CALLS=0
        native=read(B/'native10_source_actions.json');count=0
        for path,z in g.p.frames.templates.items():
            before=empty(native['trees'][z['native_source']]);expected=empty(native['trees'][z['native_target']])
            tree=v.Mutable(before);h,q,events=tree.splay(z['target_rank'],True);CALLS=v.CALLS
            assert h==z['H'] and tree.snapshot()==expected
            k=len(path)+1
            for event in events:
                for rotation in event['rotations']:assert rotation['pivot']<=k
            def find(t,key):
                while t and t[0]!=key:t=t[1 if key<t[0] else 2]
                return t
            assert find(before,k+1)==find(expected,k+1);count+=1
        assert count==30 and CALLS==30
        pin={'status':'PASS','templates':30,'source_queries':CALLS,'source_engine_calls':CALLS,
          'purpose':'new arbitrary-port/filler invariance audit, not repetition of old cost checks alone',
          'native_cache_sha256':sha(B/'native10_source_actions.json'),'frame_library_sha256':sha(F/'cached_low_frames.py')}
        with (F/'independent_LOW2_template_audit.json').open('x',encoding='utf-8') as f:json.dump(pin,f,indent=2)
    else:
        pin=read(F/'independent_LOW2_template_audit.json');assert pin['status']=='PASS' and pin['frame_library_sha256']==sha(F/'cached_low_frames.py')
    lo=(PART-1)*2000;hi=min(PART*2000,5947);g.A_START=lo;g.A_END=hi
    generated=g.generate();actual1=set(map(tuple,generated['H1']));actual2=set(map(tuple,generated['H2']))
    expected1={tuple(row) for row in one['H1_rows'] if lo<=row[0]<hi}
    expected2={tuple(row) for row in prod['H2_rows'] if lo<=row[0]<hi}
    assert actual1==expected1 and actual2==expected2
    assert generated['states']==g.bases()
    r={'status':'PASS_SOURCE_UNIFORM_H2_INTERVAL','source_A_interval':[lo,hi],'A_total':5947,
       'H1_rows':len(actual1),'H2_rows':len(actual2),'cached_source_identity_substitutions':generated['cached_source_identity_substitutions'],
       'fresh_source_queries':CALLS,'source_queries':CALLS,'source_engine_calls':CALLS,
       'scope':'complete source LOW2 relation at seven marks for this source interval, arbitrary unary/private populations; not path realization or credit',
       'JR35':'OPEN','verification':'separate accepted C14 grammar parameterization, exact set equality, distinct mutable prototype audit; same agent, not external/formal review',
       'input_sha256':{p:sha(F/p) for p in ('branch_H1_r7.json','branch_H2_r7.json','independent_H2_grammar.py','independent_LOW2_template_audit.json')}}
    with (F/f'independent_branch_H2_part{PART:02d}.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':CALLS,'source_engine_calls':CALLS},f)
