"""Independent complete batch coverage and relation-union audit. No source run."""
import json,hashlib,time
from pathlib import Path
B=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def main():
    sets={};coverage={};pins={};excluded={}
    for name,prefix in [('producer','cold'),('independent','verify')]:
        rel={1:set(),2:set()};cov=set();exc=set()
        for p in sorted(B.glob(prefix+'*_source_relation.json')):
            d=read(p)
            if p.name=='verify001_source_relation.json':continue # failed adapter retained, not accepted
            phase=p.name.removesuffix('_source_relation.json')
            assert read(B/('run_'+phase+'_result.json'))['status']=='PASS'
            assert d['backend']==name and d['total_seven_source_bases']==5577
            cov.update(d['completed_source_bases']);exc.update(d.get('depth_excluded_source_bases',[]))
            for h in (1,2):rel[h].update(map(tuple,d['LOW'][str(h)]))
            pins[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
        assert cov==set(range(5577)),(name,len(cov),sorted(set(range(5577))-cov)[:5])
        sets[name]=rel;coverage[name]=len(cov);excluded[name]=len(exc)
    assert sets['producer']==sets['independent']
    result={'status':'PASS_COMPLETE_SOURCE_UNION_AGREEMENT','covered_bases':coverage,'depth_excluded':excluded,
            'LOW':{str(h):sorted(sets['producer'][h]) for h in (1,2)},'source_queries_this_phase':0,
            'input_sha256':pins,'trust':'distinct rotation and projection kernels; shared complete active-frame syntax requires symbolic lifting proof'}
    with (B/'cold_source_relation_complete.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'covered':coverage,'LOW':{h:len(v) for h,v in sets['producer'].items()}}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_coldmerge2_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
