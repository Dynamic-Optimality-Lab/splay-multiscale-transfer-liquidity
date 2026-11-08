"""Independent coarsened selection/bit/owner reconstruction. No source rerun."""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def mp(z):return {tuple(v['demand']):tuple(v['unit']) for v in z}
def main():
    src=json.loads((B/'native10_normalized_owner_chain.json').read_text());z=json.loads((B/'coarsened_native10_source_receipt.json').read_text());prior=json.loads((B/'native10_normalized_composition_independent_audit.json').read_text());assert hashlib.sha256((B/'native10_normalized_owner_chain.json').read_bytes()).hexdigest()==prior['input_sha256']['native10_normalized_owner_chain.json'];assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in z['input_sha256'].items());summary=[]
    for stage,record in zip(src['stages'],z['records']):
        rows=stage['rows'];ends=[i for i,r in enumerate(rows) if r['genuine_F']];sel=set();h0={};D=set();sum_margin=0;sum_delta=0;sum_c=0;covered=[]
        for j,end in enumerate(ends):
            p=ends[j-1];rr=rows[p+1:end+1] if p<end else rows[p+1:]+rows[:end+1];ev=[(r['occurrence'],k) for r in rr for k in range(1,r['a']+1)];dd=[(r['occurrence'],k) for r in rr for k in range(1,r['qF']+1)];uu=[e+(b,) for e in ev for b in (0,1)];h0.update(zip(dd,uu));D.update(dd);c=min(len(ev),3);ss={e+(b,) for e in ev[:c] for b in (0,1)};assert sel.isdisjoint(ss);sel.update(ss);rec=next(r for r in stage['raw_source_receipt'] if r['macro_index']==j);ds,dt=rec['D_source'],rec['D_target'];delta=dt-ds;assert 2*c-len(dd)+delta==rec['margin']>=0;sum_margin+=rec['margin'];sum_delta+=delta;sum_c+=c;covered+=rec['occurrences']
        assert sum_delta==0 and sum_margin==2*sum_c-len(D)>=0 and sorted(covered)==[r['occurrence'] for r in rows];assert h0==mp(record['fixed_h0']) and set(h0.values())<=sel;inv={v:k for k,v in h0.items()};expected_missing=sorted(D-h0.keys());cursor=0;actual={};units=set();peak=0;evlog=iter(record['all_events'])
        for row in rows:
            for k in range(1,row['a']+1):
                rec=next(evlog);assert rec['event']==[row['occurrence'],k] and rec['outgoing_unassigned']==0;event_units={(row['occurrence'],k,b) for b in (0,1)};peak=max(peak,len(event_units));assert len(rec['actions'])==2
                for action in rec['actions']:
                    u=tuple(action['unit']);assert u in event_units and u not in units;units.add(u)
                    if u in inv:assert action['status']=='fixed' and tuple(action['demand'])==inv[u];actual[inv[u]]=u
                    elif u in sel and cursor<len(expected_missing):
                        d=expected_missing[cursor];cursor+=1;assert action['status']=='new' and tuple(action['demand'])==d;actual[d]=u
                    else:assert action['status']=='released' and 'demand' not in action
        assert next(evlog,None) is None and len(units)==106 and cursor==len(expected_missing) and actual==mp(record['raw_h']) and set(actual)==D and len(set(actual.values()))==len(D) and all(actual[d]==u for d,u in h0.items());assert peak==record['working_peak']==2
        fE=mp(stage['input_fE']);common=D&fE.keys();locked={d:fE[d] for d in common};inverse={u:d for d,u in locked.items()}
        def exchange(h):
            result=dict(locked);paths={}
            for root in sorted(h.keys()-common):
                d=root;seen=set();path=[]
                while d in h:
                    assert d not in seen;seen.add(d);u=h[d];path.append((d,u))
                    if u not in inverse:result[root]=u;paths[root]=path;break
                    d=inverse[u]
            return result,paths
        a,ap=exchange(h0);full,fp=exchange(actual);assert a==mp(stage['old_effective_a']) and all(full[d]==u for d,u in a.items()) and all(fp[d]==p for d,p in ap.items());assert record['existing_archived_full_f_NOT_replaced'] and len(set(full.values()))==len(full)==len(D);summary.append({'r':stage['support'],'demands':len(D),'selected_events':sum_c,'derived_source_margin':sum_margin,'old_effective_owners_preserved':len(a),'working_peak':peak})
    out('coarsened_source_independent_audit.json',{'status':'PASS_EXACT_SOURCE_COARSENED_WORKING_TWO_INSTANCES','scope':'four actual source instantiations plus independent invariant review of the stated static-superblock proof; no universal source sign theorem','records':summary,'all_original_physical_units_accounted_once':True,'no_source_replay_or_query':True,'new_source_queries':0,'prior_allocations_modified':False,'extra_E3_eligibility_discharged':False,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('coarsened_native10_source_receipt.json','COARSENED_SOURCE_CREDIT_THEOREM.md','native10_normalized_owner_chain.json')}});print(json.dumps({'status':'PASS_COARSENED_WORKING_TWO','records':summary,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify22_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
