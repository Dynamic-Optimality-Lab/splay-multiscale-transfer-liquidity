"""Independent sparse conversion, part1: values, geometry and causal state.
verify67 failed on a legacy optional H1 field at the first edge-retention
check. Its charge and original script are retained. Edge retention is part2.
"""
import hashlib,json,pickle,sys,time
from pathlib import Path
from audit_verify67 import skeleton,reconstruct
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    with (B/'full_geometry_compressed_work_08.pkl').open('rb') as f:w=pickle.load(f)
    with (B/'full_geometry_sparse_work_00.pkl').open('rb') as f:s=pickle.load(f)
    Z=json.loads((B/'native10_source_actions.json').read_text());N=len(Z['trees']);assert s['N']==N==16796
    def strip(v):return tuple(map(strip,v)) if isinstance(v,list) else v
    T=[skeleton(strip(t)) for t in Z['trees']];bypi={};geometry=0
    for a,pi in w['projections'].items():
        if len(pi)>1:
            assert reconstruct([T[v] for v in pi])==skeleton(w['A'][a],2)
            assert pi not in bypi;bypi[pi]=a;geometry+=1
    codes=[bypi[pi]*N+b for b,pi in w['features']];assert len(set(codes))==len(codes)
    assert s['A']==w['A'] and s['A_index']==w['A_index'] and s['cursor']==w['cursor'] and s['source_couplings']==w['source_couplings'] and s['actions']==w['actions'] and s['actions2']==w['actions2'] and s['projections']==w['projections']
    assert s['lower']=={c:v for c,v in zip(codes,w['lower']) if v>0}
    assert s['pred']=={c:j for c,j in zip(codes,w['pred']) if c in s['lower']}
    assert len(s['updates'])==len(w['updates'])
    for old,new in zip(w['updates'],s['updates']):
        assert all(new[k]==v for k,v in old.items())
        assert new['source_code']==(None if old['source_feature'] is None else codes[old['source_feature']]) and new['target_code']==codes[old['target_feature']]
    assert all(u is None or w['lower'][j]<=u for j,u in enumerate(w['upper'])) and not w['pending'] and w['counter'] is None
    groups={k:[] for k in range(1,11)}
    for b,t in enumerate(Z['trees']):groups[t[0]].append(b)
    rank={b:i for bb in groups.values() for i,b in enumerate(bb)};ap,bp,xp=w['cursor'];expected=[]
    for c in s['lower']:
        a,b=divmod(c,N)
        if a>ap or a==ap and rank[b]>=bp:expected.append(c)
    assert expected==s['pending'] and len(codes)==546701 and len(s['lower'])==21887 and len(s['updates'])==24320
    files=('SPARSE_SOURCE_REGENERATION.md','full_geometry_compressed_work_08.pkl','full_geometry_sparse_work_00.pkl','full_geometry_sparse_conversion.json','audit_verify68.py','audit_verify67.py','run_verify67_result.json')
    receipt={'status':'PASS_EXACT_SPARSE_CONVERSION_VALUES_GEOMETRY_CAUSAL_CURSOR','profiles_including_implicit_zero':len(codes),'positive_labels':len(s['lower']),'causal_records':len(s['updates']),'branched_geometry_reconstructions':geometry,'cursor':s['cursor'],'pending_positive_source_rows':len(s['pending']),'edge_retention':'PENDING separate part2; no full conversion acceptance before that check','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}}
    assert time.process_time()-START<CAP-1
    out('sparse_conversion_values_independent_audit.json',receipt);print(json.dumps({k:v for k,v in receipt.items() if k!='input_sha256'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify68_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
