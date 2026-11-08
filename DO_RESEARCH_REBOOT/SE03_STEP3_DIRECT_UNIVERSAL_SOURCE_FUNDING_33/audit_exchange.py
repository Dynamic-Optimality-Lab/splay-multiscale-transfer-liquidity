"""Exact static owner extension on the NEW Gamma55, not a Bank25 receipt."""
import json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    z=json.loads((B/'Gamma55_original_source.json').read_text());rows=z['rows'];D=set(map(tuple,z['DF']));E=set(map(tuple,z['DE']));U=set(map(tuple,z['U']))
    H={tuple(v['demand']):tuple(v['unit']) for v in z['H_count']};fE={tuple(v['demand']):tuple(v['unit']) for v in z['fE_count']}
    C=D&E;l={d:fE[d] for d in C};h0={};ends=[i for i,v in enumerate(rows) if v['genuine_F']]
    for j,i in enumerate(ends):
        prev=ends[j-1];seg=rows[prev+1:i+1] if prev<i else rows[prev+1:]+rows[:i+1]
        units=[(v['occurrence'],k,b) for v in seg for k in range(1,v['a']+1) for b in (0,1)]
        h0.update(zip([(rows[i]['occurrence'],k) for k in range(1,rows[i]['qF']+1)],units))
    assert all(H[d]==u for d,u in h0.items())
    linv={u:d for d,u in l.items()};a=dict(l);partial_stops=[]
    for root in sorted(D-C):
        d=root;seen=set()
        while d in h0:
            assert d not in seen;seen.add(d);u=h0[d]
            if u not in linv:a[root]=u;break
            d=linv[u]
        else:partial_stops.append(root)
    assert len(set(a.values()))==len(a) and set(a.values())<=U
    inv={u:d for d,u in a.items()};extension={};paths=[]
    for root in sorted(D-a.keys()):
        d=root;seen=set();path=[]
        while True:
            assert d not in seen;seen.add(d);u=H[d];path.append({'demand':d,'unit':u})
            if u not in inv:extension[root]=u;break
            d=inv[u]
        paths.append({'root':root,'path':path,'terminal':u})
    full=dict(a);full.update(extension);assert set(full)==D and len(set(full.values()))==len(full) and set(full.values())<=U
    assert all(full[d]==u for d,u in a.items()) and all(full[d]==fE[d] for d in C)
    def entries(mp):return [{'demand':d,'unit':u} for d,u in sorted(mp.items())]
    result={'status':'COMPLETE_STATIC_COUNT_OWNER_EXTENSION','source_period':[223,444],'common_count':len(C),'natural_count':len(h0),
        'frozen_partial_count':len(a),'unpaid_before':len(D-a.keys()),'extension_count':len(extension),'full_count':len(full),
        'old_a':entries(a),'extension':entries(extension),'full':entries(full),'paths':paths,'partial_stops':partial_stops,
        'all_old_values_unchanged':True,'count_eligibility':'all actual U in same period, E-only claims retired only in alternative full ledger',
        'raw_aux_map_is_original_normalized_I54_receipt':False,'original_Bank25_working_license_claimed':False,
        'endpoint_Bank25_possible':False,'new_source_queries':0}
    out('Gamma55_static_owner_extension.json',result)
    print(json.dumps({k:result[k] for k in ('status','common_count','frozen_partial_count','unpaid_before','extension_count','full_count')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_exchange_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
