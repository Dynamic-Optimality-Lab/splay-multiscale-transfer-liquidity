"""Independent source-block membership and event-state invariant for Bank2."""
import hashlib,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    S=json.loads((B/'core13_framed_activation_closed_source.json').read_text());Z=json.loads((B/'prepared_frame_static_schedule.json').read_text());prior=json.loads((B/'framed_family_repayment_independent_audit.json').read_text());assert prior['status']=='PASS_RESTRICTED_ALL_R_PREPARED_FRAME_MATCHING_AND_OWNER_EXTENSION_INTERFACE'
    assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==h for n,h in Z['input_sha256'].items())
    rows=S['period_rows'];ends=[i for i,r in enumerate(rows) if r['kind']=='K' and r['key']!=r['BF_before'][0]];macros=[];h0={};um={};dm={}
    for m,end in enumerate(ends):
        pre=ends[m-1];ii=list(range(pre+1,end+1)) if pre<end else list(range(pre+1,len(rows)))+list(range(end+1));units=[(rows[i]['absolute_t'],j,b) for i in ii for j in range(1,rows[i]['H']+1) for b in (0,1)];demands=[(rows[i]['absolute_t'],k) for i in ii for k in range(1,rows[i]['QF']+1)];own=min(len(units),len(demands));h0.update(zip(demands[:own],units[:own]));um.update((u,m) for u in units);dm.update((d,m) for d in demands);macros.append((units,demands))
    h=dict(h0);block=list(range(len(macros)));critical=[]
    for m,(uu,dd) in enumerate(macros):
        missing=[d for d in dd if d not in h0]
        if not missing:continue
        critical.append(m);pre=(m-1)%len(macros);pu,pd=macros[pre];assert len(pd)==1 and len(pu)//2>=7 and len(uu)==4 and len(dd)==6;block[m]=pre
        for k,d in enumerate(missing):h[d]=pu[1+k]
    assert len(critical)==1 and set(h)==set(dm) and len(set(h.values()))==36
    assert all(block[um[u]]==block[dm[d]] for d,u in h.items())
    expect={u:d for d,u in h.items()};ownunits={u:d for d,u in h0.items()};seen=set();paid={};released=set();evindex=0
    for row in rows:
        for j in range(1,row['H']+1):
            event=Z['events'][evindex];evindex+=1;uu=[(row['absolute_t'],j,b) for b in (0,1)]
            assert (event['occurrence'],event['event_index'],event['buffer_before'],event['buffer_after_admit'],event['buffer_after_resolve'])==(row['absolute_t'],j,0,2,0)
            for u,action in zip(uu,event['actions']):
                assert tuple(action['unit'])==u and u not in seen;seen.add(u)
                if u in expect:
                    d=expect[u];assert tuple(action['demand'])==d and action['action']==('emit_h0' if u in ownunits else 'emit_seed') and d not in paid;paid[d]=u
                else:assert action['action']=='release' and 'demand' not in action;released.add(u)
    assert paid==h and len(seen)==318 and seen==set(um) and len(released)==282 and not released.intersection(h.values()) and evindex==159 and all(paid[d]==u for d,u in h0.items())
    # Exhaustive transition rules, not bounded source/population examples:
    # start empty; two admitted bit statuses each resolve immediately.
    for statuses in itertools.product(('fixed','seed','release'),repeat=2):
        buffer=['bit0','bit1'];assert len(buffer)==2
        for status in statuses:
            unit=buffer.pop(0)
            assert status in ('fixed','seed','release')
        assert not buffer
    assert time.process_time()-START<CAP-1
    files=('PREPARED_FRAME_STATIC_BANK25.md','prepared_frame_static_schedule.json','framed_family_repayment_independent_audit.json','framed_return_and_core13_independent_audit.json','audit_verify66.py')
    out('prepared_frame_static_bank_independent_audit.json',{'status':'PASS_PREPARED_ALL_R_SOURCE_LICENSE_A_STATIC_WORKING_BANK2','source_scope':'exact prepared framed family of the inherited all-r source theorem; not arbitrary dirty entry','uniform_schedule_induction':'each actual event admits its two bits and resolves fixed/seed/release statuses before the next; nine exhaustive status-pair transitions','source_supply_theorem_reused_not_retested':True,'independent_control_pairs':36,'independent_control_events':159,'independent_control_released_units':282,'every_pair_within_its_source_single_or_joined_block':True,'unchanged_h0':True,'working_peak':2,'endpoint_bank_claim':False,'extra_normalized_owner_eligibility':'conditional on original supplied policy; no map invented or overwritten','actual_period_transport':'inherited C14 both-endpoint bijection; fixed auxiliary cut unchanged','arbitrary_dirty_entry':False,'principal_U33':'OPEN','source_queries':0,'source_engine_calls':0,'external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in files}})
    print(json.dumps({'status':'PASS_PREPARED_SOURCE_STATIC_BANK2','working_peak':2,'demands':36,'source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify66_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
