"""Independent block-receipt replay; no producer allocator/kernel import.
Only saved certified source data, actual identities and accounting steps.
"""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def rd(p):return json.loads(p.read_text())
def main():
    z=rd(B/'Gamma55_streamed_source_license.json');src=rd(B.parent/'Gamma55_original_source.json')
    assert z['status']=='COMPLETE_GAMMA55_STATIC_BLOCK_LICENSE'
    rows={v['occurrence']:v for v in src['rows']};D=set(map(tuple,src['DF']));U=set(map(tuple,src['U']));full={};released=set();occ=[];peak=0
    for p in z['packets']:
        dd=set(map(tuple,p['demands']));ss=set(map(tuple,p['selected']));fixed={tuple(v['demand']):tuple(v['unit']) for v in p['fixed']}
        pairs={tuple(v['demand']):tuple(v['unit']) for v in p['payments']};events=list(map(tuple,p['events']))
        assert ss<=U and len(ss)==2*p['c'] and len(ss)>=len(dd) and set(fixed.values())<=ss
        expected_events=[(t,j) for t in p['occurrences'] for j in range(1,rows[t]['a']+1)]
        assert events==expected_events
        assert dd=={(t,j) for t in p['occurrences'] for j in range(1,rows[t]['qF']+1)}
        inv={u:d for d,u in fixed.items()};queue=[];emitted={};seen=set();next_event=0
        for step in p['trace']:
            if 'event' in step:
                ev=tuple(step['event']);assert next_event<len(events) and ev==events[next_event];next_event+=1
                # K=0, so event loading never occurs with an unassigned
                # previous event's unit left pending. Fixed pairs are
                # static within-block output, NOT a native-time payment.
                assert queue==list(map(tuple,step['before']))
                peak=max(peak,len(queue)+2);created=[ev+(b,) for b in (0,1)];actual_fixed=[];actual_free=[]
                assert not seen.intersection(created);seen.update(created)
                for u in created:
                    if u in inv:emitted[inv[u]]=u;actual_fixed.append((inv[u],u))
                    elif u in ss:queue.append(u);actual_free.append(u)
                assert actual_fixed==[(tuple(d),tuple(u)) for d,u in step['fixed_emitted']]
                assert actual_free==list(map(tuple,step['free_added']))
                assert queue==list(map(tuple,step['bank_after_visit']))
                # Producer releases excess at the end of this accounting
                # phase; the next record declares the retained queue.
            else:
                d,u=tuple(step['pay_missing']),tuple(step['unit']);assert d in dd-fixed.keys() and d not in emitted
                assert queue and queue.pop(0)==u;emitted[d]=u
                assert queue==list(map(tuple,step['bank_after_payment']))
            # For these zero-carry inputs, a queue excess after paying
            # all missing demands is permanently released before advancing.
            if len(emitted.keys() & (dd-fixed.keys()))==len(dd-fixed.keys()):queue=[]
        assert next_event==len(events) and emitted==pairs and not queue
        assert set(pairs)==dd and len(set(pairs.values()))==len(pairs)
        assert all(pairs[d]==u for d,u in fixed.items())
        local_released=set(map(tuple,p['released']));assert not set(pairs.values())&local_released
        assert set(pairs.values())|local_released==seen
        assert not set(full)&dd and not set(full.values())&set(pairs.values())
        full.update(pairs);released.update(local_released);occ+=p['occurrences']
    assert set(full)==D and set(full.values())|released==U and not set(full.values())&released
    assert peak<=2 and sorted(occ)==list(range(223,445)) and len(occ)==222
    expected={tuple(v['demand']):tuple(v['unit']) for v in src['H_count']};assert full==expected
    result={'status':'PASS_SELECTED_BIT_STATIC_BLOCK_SCHEDULE','working_peak':peak,'full_demands':len(full),'all_original_ids':True,
        'uniform_proof_review':'queue/unread-free invariant, K+2 loading bound, Gamma_r exact preparation geometry and selected h0 ordinals inspected',
        'applicability':'OFFLINE STATIC within-block commitment license ONLY; no native timing or additional immutable reservation license proved',
        'no_all_event_endpoint_bound':True,'new_source_queries':0,'principal_U33':'OPEN',
        'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('Gamma55_streamed_source_license.json','STREAMED_BLOCK_THEOREM.md','GAMMA_R_PREPARATION_LICENSE.md')}}
    with (B/'streamed_block_independent_audit.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_independent_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
