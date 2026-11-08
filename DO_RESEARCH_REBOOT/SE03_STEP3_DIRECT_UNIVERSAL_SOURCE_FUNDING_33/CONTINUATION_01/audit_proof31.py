"""Apply the source-coarsening bridge without modifying archived allocations."""
import json,time,sys,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def mp(z):return {tuple(p['demand']):tuple(p['unit']) for p in z}
def pack(z):return [{'demand':d,'unit':u} for d,u in sorted(z.items())]
def main():
    z=json.loads((B/'native10_normalized_owner_chain.json').read_text());accepted=json.loads((B/'native10_normalized_composition_independent_audit.json').read_text());assert hashlib.sha256((B/'native10_normalized_owner_chain.json').read_bytes()).hexdigest()==accepted['input_sha256']['native10_normalized_owner_chain.json'];sys.path.insert(0,str(P/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'));from source_funding import own_map,with_owners
    records=[]
    for stage in z['stages']:
        rows=stage['rows'];sel={tuple(u) for rec in stage['raw_source_receipt'] for u in rec['selected']};h0=mp(stage['h0']);inv={u:d for d,u in h0.items()};D=set(map(tuple,stage['demands']));missing=iter(sorted(D-h0.keys()));target=next(missing,None);h={};released=[];log=[];peak=0
        source_margins=sum(rec['margin'] for rec in stage['raw_source_receipt']);c=sum(rec['c'] for rec in stage['raw_source_receipt']);assert source_margins==2*c-len(D)>=0 and len(sel)==2*c
        for row in rows:
            for j in range(1,row['a']+1):
                units=[(row['occurrence'],j,b) for b in (0,1)];peak=max(peak,len(units));actions=[]
                for unit in units:
                    if unit in inv:h[inv[unit]]=unit;actions.append({'unit':unit,'status':'fixed','demand':inv[unit]})
                    elif unit in sel and target is not None:h[target]=unit;actions.append({'unit':unit,'status':'new','demand':target});target=next(missing,None)
                    else:released.append(unit);actions.append({'unit':unit,'status':'released'})
                log.append({'event':units[0][:2],'actions':actions,'outgoing_unassigned':0})
        assert target is None and set(h)==D and len(set(h.values()))==len(D) and all(h[d]==u for d,u in h0.items());v=own_map(rows);v['h']=h;fE=mp(stage['input_fE']);owners=with_owners(v,set(fE),fE);a=owners['prior']['allocation'];f=owners['extension']['allocation'];assert a==mp(stage['old_effective_a']) and all(f[d]==u for d,u in a.items())
        records.append({'support':stage['support'],'actual_period':z['period'],'selected_c':c,'Q':len(D),'telescoped_margin':source_margins,'working_peak':peak,'raw_h':pack(h),'fixed_h0':stage['h0'],'all_events':log,'input_fE_kept_literal':True,'old_effective_owners_preserved':len(a),'licensed_exchange_additions':pack(owners['extension']['additions']),'existing_archived_full_f_NOT_replaced':True,'additional_eligibility_assumed':'original same-period static independent-block license, then unchanged original common exchange'})
    out('coarsened_native10_source_receipt.json',{'status':'COMPLETE_ALTERNATIVE_STATIC_BLOCK_WORKING_TWO','theorem':'COARSENED_SOURCE_CREDIT_THEOREM.md','records':records,'original_source_replayed':False,'source_and_local_laws_reused_by_hash':True,'no_existing_allocation_modified':True,'new_source_queries':0,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_normalized_owner_chain.json','native10_normalized_composition_independent_audit.json','COARSENED_SOURCE_CREDIT_THEOREM.md')}});print(json.dumps({'status':'COMPLETE_WORKING_TWO','records':[{'r':r['support'],'Q':r['Q'],'source_margin':r['telescoped_margin'],'old_a':r['old_effective_owners_preserved'],'working':r['working_peak']} for r in records]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof31_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
