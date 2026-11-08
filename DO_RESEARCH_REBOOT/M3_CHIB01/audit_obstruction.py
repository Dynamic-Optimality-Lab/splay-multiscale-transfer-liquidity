import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_GAPINT01','DO_RESEARCH_REBOOT/M2_SEP01']
from interior_original import S,V,bmodel,ix
from experiment import trace,D,verify_bpath,b_splay_event,unpack,structure
BASE=Path('DO_RESEARCH_REBOOT/M3_CHIB01')
def scale(t):return S.LEAF if t==S.LEAF else S.node(16*t[1],scale(t[2]),scale(t[3]))
def main():
    out=BASE/'obstruction_audit.json';assert not out.exists();c=json.loads((BASE/'completion.json').read_text());path=c['obstruction']['path'];bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());ts=[V.from_serial(r['tree']) for r in bc['nodes']]
    assert c['status']=='RANGE_TWO_TEMPLATE_REFUTED_EXACT' and sum(r['w'] for r in path)==-3
    mu=path[0]['mu'];assert mu==93 and mu.bit_count()==5
    B=V.insert(V.insert(scale(ts[path[0]['source_B']]),-8),24);origin=bmodel(B);rows=[]
    for r in path:
        assert r['mu']==mu and r['kind']=='H1' and mu>>r['target']&1
        h=S.lookup(B,16*r['target'])[1];assert h//2==r['q'] and 2-h//2==r['w']
        sb=bmodel(B);bb,bt,pa,di=trace(sb,r['target'],h);assert verify_bpath(D,bb,bt,0).v
        raw=unpack(b_splay_event(D,bb,bt,0,D.const_bool(False)));B=S.trace(B,16*r['target'])[0];dest=bmodel(B)
        assert structure(raw)==structure(dest);rows.append({'q':r['q'],'w':r['w'],'B_source':sb,'B_destination':dest,'original_B_path':pa[:h+1],'original_dirs':di[:h]})
    end=bmodel(B);returns=[]
    for dd in range(19):
        bb,bt,pa,di=trace(end,origin['root'],dd);valid=verify_bpath(D,bb,bt,0).v;raw=unpack(b_splay_event(D,bb,bt,0,D.const_bool(False))) if valid else None
        equal=valid and structure(raw)==structure(origin);returns.append({'declared_depth':dd,'path_valid':valid,'returns_full_structure':equal,'weight':6-dd//2,'total':-3+6-dd//2})
    negative=[r for r in returns if r['returns_full_structure'] and r['total']<0];assert not negative
    result={'status':'EXACT_RANGE_TWO_B_ONLY_TEMPLATE_OBSTRUCTION','mu':mu,'low_path_weight':-3,'path_vertices_distinct':len({path[0]['source']}|{r['destination'] for r in path})==len(path)+1,
      'range_contradiction':'Q(end)<=Q(start)-3, inconsistent with Q in[-2,0]',
      'original_B_replay_verified':True,'full_original_low_roots_verified':False,'negative_original_cycle_certified':False,
      'fixed_two_gap_signature':[1,0,1]+[0]*7,'one_high_negative_return_candidates':negative,'high_return_tests':returns,'rows':rows,
      'A_lift_not_run_reason':'No negative B-closed cycle or one-high return candidate in the registered obstruction path.'}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','high_return_tests')},indent=2))
if __name__=='__main__':main()
