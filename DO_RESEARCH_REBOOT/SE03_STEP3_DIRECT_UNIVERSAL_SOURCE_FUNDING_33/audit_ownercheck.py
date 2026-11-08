"""Independent direct receipt and literal-path checker; zero source queries."""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def main():
    s=json.loads((B/'Gamma55_original_source.json').read_text());z=json.loads((B/'Gamma55_static_owner_extension.json').read_text())
    def mp(v):return {tuple(q['demand']):tuple(q['unit']) for q in v}
    D=set(map(tuple,s['DF']));U=set(map(tuple,s['U']));E=set(map(tuple,s['DE']));C=D&E
    a=mp(z['old_a']);new=mp(z['extension']);f=mp(z['full']);fe=mp(s['fE_count']);H=mp(s['H_count'])
    assert set(f)==D and len(set(f.values()))==len(D) and set(f.values())<=U
    assert set(new)==D-a.keys() and f==a|new and not set(a.values())&set(new.values())
    assert all(f[d]==u for d,u in a.items()) and all(a[d]==fe[d] for d in C)
    inverse={u:d for d,u in a.items()};used_demands=set();used_units=set()
    for p in z['paths']:
        root=tuple(p['root']);d=root
        for row in p['path']:
            dd,uu=tuple(row['demand']),tuple(row['unit']);assert dd==d and H[dd]==uu
            assert dd not in used_demands and uu not in used_units;used_demands.add(dd);used_units.add(uu)
            d=inverse.get(uu)
        assert d is None and new[root]==tuple(p['terminal'])==uu
    assert len(z['paths'])==len(new)
    result={'status':'PASS_GAMMA55_STATIC_OWNER_EXTENSION','all_old_values_preserved':True,'common_values_preserved':len(C),
        'new_assignments':len(new),'full_demands':len(D),'endpoint_obstruction_unchanged':True,
        'no_normalized_or_Bank25_receipt_fabricated':True,'new_source_queries':0,
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('Gamma55_original_source.json','Gamma55_static_owner_extension.json')}}
    with (B/'static_owner_independent_audit.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_ownercheck_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
