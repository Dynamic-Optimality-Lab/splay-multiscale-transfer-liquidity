"""Correct target-index conversion; reusable independent checked intervals.
Pure memoization changes no source grammar. The failed audit is retained.
"""
import functools,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];sys.path.insert(0,str(F))
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];PART=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    spec=importlib.util.spec_from_file_location('independent_low2_checkpoint',F/'independent_H2_grammar.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    for name in ('vals','canonical','hasmark','reduce'):setattr(g,name,functools.lru_cache(maxsize=20000)(getattr(g,name)))
    g.p.frames.apply=functools.lru_cache(maxsize=20000)(g.p.frames.apply)
    prod=read(F/'branch_H2_r7.json');one=read(F/'branch_H1_r7.json');pin=read(F/'independent_LOW2_template_audit.json')
    assert pin['status']=='PASS' and pin['templates']==30 and pin['frame_library_sha256']==sha(F/'cached_low_frames.py')
    assert prod['native_cache_sha256']==sha(B/'native10_source_actions.json')
    for p,h in prod['input_sha256'].items():assert sha(F/p)==h
    if PART==1:start=0;count1=count2=0
    else:
        prev=read(F/f'independent_H2_checked_{PART-1:02d}.json');assert prev['status']=='CHECKPOINT'
        assert prev['input_sha256']['branch_H2_r7.json']==sha(F/'branch_H2_r7.json')
        start=prev['next_A'];count1=prev['H1_checked'];count2=prev['H2_checked']
    begin=start;want1=[set() for _ in range(5947)];want2=[set() for _ in range(5947)]
    for row in one['H1_rows']:want1[row[0]].add(tuple(row))
    for row in prod['H2_rows']:want2[row[0]].add(tuple(row))
    while start<5947 and time.process_time()-START<CAP-4:
        end=min(start+100,5947);g.A_START=start;g.A_END=end;made=g.generate()
        # The C14 grammar's x field is ONE-based. New certificate is ZERO-based.
        got1={(a,x-1,b) for a,x,b in made['H1']};got2={(a,x-1,b) for a,x,b in made['H2']}
        expected1=set().union(*want1[start:end]);expected2=set().union(*want2[start:end])
        assert got1==expected1,('H1',start,end,len(got1),len(expected1))
        assert got2==expected2,('H2',start,end,len(got2),len(expected2))
        count1+=len(got1);count2+=len(got2);start=end
    r={'status':'PASS_COMPLETE_H1_H2_SOURCE_COVER' if start==5947 else 'CHECKPOINT',
       'checked_source_A_interval':[begin,start],'next_A':start,'H1_checked':count1,'H2_checked':count2,
       'cached_source_identity_substitutions_this_phase':g.calls,'source_queries':0,'source_engine_calls':0,
       'fresh_mutable_template_queries_already_charged_in_failed_verify106':30,
       'prior_failed_audit_retained':True,'index_conversion':'old x1..7 mapped to new x0..6',
       'source_scope':'all seven-mark original H1/H2 macros, arbitrary anonymous ancestors/private populations; source coverage only',
       'JR35':'OPEN','not_a_full_path_realization_bridge':True,
       'input_sha256':{p:sha(F/p) for p in ('branch_H1_r7.json','branch_H2_r7.json','independent_H2_grammar.py','independent_LOW2_template_audit.json')}}
    with (F/f'independent_H2_checked_{PART:02d}.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
