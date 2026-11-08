"""New source-block construction using ONLY the independently saved Gamma55.
No source query. This verifies an instantiation; uniformity is manuscript.
"""
import json,time,sys,math
from pathlib import Path
from stream_allocator import allocate
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    z=json.loads((B.parent/'Gamma55_original_source.json').read_text());rows=z['rows'];r=z['r'];ends=[i for i,v in enumerate(rows) if v['genuine_F']];mm=[];h0={}
    for j,i in enumerate(ends):
        prev=ends[j-1];seg=rows[prev+1:i+1] if prev<i else rows[prev+1:]+rows[:i+1]
        events=[(v['occurrence'],e) for v in seg for e in range(1,v['a']+1)];units=[e+(b,) for e in events for b in (0,1)]
        demands=[(rows[i]['occurrence'],k) for k in range(1,rows[i]['qF']+1)]
        h0.update(zip(demands,units));mm.append({'rows':seg,'events':events,'units':units,'demands':demands,'H':len(events),'Q':len(demands),'target':rows[i]['target']})
    ci=next(i for i,m in enumerate(mm) if m['rows'][-1]['occurrence']==333);pi=ci-1
    assert (mm[pi]['target'],mm[pi]['H'],mm[pi]['Q'])==(1,r,1)
    assert (mm[ci]['target'],mm[ci]['H'],mm[ci]['Q'])==(109,1,r-1)
    full={};packets=[];released=[];peak=0;coverage=[]
    for i,m in enumerate(mm):
        if i==ci:continue
        ids=[i,ci] if i==pi else [i];ms=[mm[j] for j in ids]
        events=sum((p['events'] for p in ms),[]);demands=sum((p['demands'] for p in ms),[])
        if i==pi:
            c=(r+1)//2;prep=next(v for v in m['rows'] if v['mode']=='D' and v['target']==109)
            selected_events=[(prep['occurrence'],j) for j in range(1,c)]+mm[ci]['events'];assert len(selected_events)==c
        else:
            assert m['H']>=m['Q'];c=(m['Q']+1)//2;selected_events=events[:c]
        selected={e+(b,) for e in selected_events for b in (0,1)};fixed={d:h0[d] for d in demands if d in h0}
        assert set(fixed.values())<=selected and 2*c-len(demands)>=0
        v=allocate(events,selected,fixed,demands,[],0);assert v['peak']<=2 and not v['carry']
        assert not set(full)&set(v['payments']);full.update(v['payments']);released+=v['released'];peak=max(peak,v['peak'])
        occs=sum(([q['occurrence'] for q in p['rows']] for p in ms),[]);coverage+=occs
        packets.append({'natural_indices':ids,'occurrences':occs,'events':events,'demands':demands,'selected':sorted(selected),
                        'fixed':[{'demand':d,'unit':u} for d,u in sorted(fixed.items())],'c':c,'Q':len(demands),'D':0,'margin':2*c-len(demands),
                        'payments':[{'demand':d,'unit':u} for d,u in sorted(v['payments'].items())],'released':v['released'],'peak':v['peak'],'trace':v['trace']})
    expected={tuple(v['demand']):tuple(v['unit']) for v in z['H_count']}
    assert full==expected and all(full[d]==u for d,u in h0.items())
    assert sorted(coverage)==list(range(223,445)) and len(coverage)==222
    assert set(full.values()).isdisjoint(released) and set(full.values())|set(released)==set(map(tuple,z['U']))
    out('Gamma55_streamed_source_license.json',{'status':'COMPLETE_GAMMA55_STATIC_BLOCK_LICENSE','source_support':55,'source_period':[223,444],
        'uniform_source_theorem':'GAMMA_R_PREPARATION_LICENSE.md','working_peak':peak,'endpoint_peak_inherited':54,'all_natural_h0_preserved':True,
        'full_demands':len(full),'all_original_occurrences_covered_once':True,'D_width':0,'empty_packet_boundaries':True,
        'packets':packets,'raw_map_equals_saved_count_map':True,'new_source_queries':0,
        'bank_semantics':'original independent offline block working queue; assigned static output is not an unassigned token; NOT an endpoint schedule',
        'extra_native_timing_or_reserved_owner_license_claimed':False,'principal_U33':'OPEN'})
    print(json.dumps({'status':'COMPLETE_GAMMA55_STATIC_BLOCK_LICENSE','working_peak':peak,'packets':len(packets),'full_demands':len(full),'queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
