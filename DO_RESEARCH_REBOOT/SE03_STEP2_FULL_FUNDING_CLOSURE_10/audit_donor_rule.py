"""Attack the only NEW local repair generalization, using pinned source rows.
Rule: each deficit packet borrows solely the immediately preceding full
packet's unused own capacity after that packet pays its own full demands.
This is stronger than raw capacity bookkeeping and has a specified donor
choice, but is NOT assumed true and does not assume fixed fE availability.
"""
import collections,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_FINAL_PLUS_ONE_07'
spec=importlib.util.spec_from_file_location('source_controls07',OLD/'audit_controls2.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    src=[]
    p=B.parent/'SE03_STEP2_COLD_NEG2_01/symbolic_replay.json'
    for f in json.loads(p.read_text())['families']:src.append((p,f['name'],f))
    for folder,file in [('SE03_STEP2_FORCED_ZERO_INCOMING_02','incoming_family_v2.json'),
        ('SE03_STEP2_LEAF_LOWERING_03','pattern_family.json'),('SE03_STEP2_FIRST_LOWERING_04','entry_family.json'),
        ('SE03_STEP2_FIRST_LOWERING_04','e1_family.json'),('SE03_STEP2_POST_LOWERING_05','partial_family.json'),
        ('SE03_STEP2_FINAL_PLUS_ONE_07','delete_event_control.json')]:
        p=B.parent/folder/file;f=json.loads(p.read_text());src.append((p,folder,f))
    checks=[];failures=[]
    for p,name,f in src:
        rows=f['rows'];raw=[{'occurrence':i,'a':r['a'],'qF':r['qF'],'genuine_F':r['genuine_F']} for i,r in enumerate(rows,1)]
        packets,macros=d.packets(raw)
        # Independent source chronology uses genuine ending occurrence order.
        packets=sorted(packets,key=lambda v:v[0][-1]);n=len(rows)
        for i,(occ,H,Q,w) in enumerate(packets):
            if 2*H>=Q:continue
            po,ph,pq,pw=packets[(i-1)%len(packets)];required=Q-2*H;available=max(0,2*ph-pq)
            result={'source':p.relative_to(B.parent.parent).as_posix(),'family':name,
                'deficit_packet':{'occurrences':occ,'H':H,'Q':Q,'w':w,'unpaid_after_own_bits':required},
                'preceding_packet':{'occurrences':po,'H':ph,'Q':pq,'w':pw,'own_surplus':available},
                'rule_passes_capacity':required<=available}
            checks.append(result)
            if required>available:
                result=dict(result);result['source_word']=f.get('word',f.get('source_word'))
                result['initial_A_BF_BE']=rows[0]['before'];result['source_period_rows']=rows
                result['full_period_closed']=True;result['scope']='exact source counterexample to adjacent-full-packet repair ONLY'
                failures.append(result)
    status='REFUTED_ADJACENT_FULL_PACKET_REPAIR' if failures else 'NO_FAILURE_IN_PINNED_CONTROLS_NOT_A_PROOF'
    out('donor_rule_audit.json',{'status':status,'checks':checks,'counterexamples':failures,
        'independent_historical_source_replay':'accepted09 receipt; no source costs regenerated or assumed from abstract graph',
        'new_Fi_source_words':'all six new families pass this local repair, but this does not establish arbitrary histories',
        'fixed_fE':'even successful local raw supply would still need ownership exchange',
        'CD6':'OPEN; no source cost violation','new_finite_tests':0,'source_engine_calls':0})
    print(json.dumps({'status':status,'negative_packets_checked':len(checks),'failed_local_repairs':len(failures),
        'first_failure':{k:v for k,v in failures[0].items() if k not in ('source_period_rows','source_word','initial_A_BF_BE')} if failures else None}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_donor_rule_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'new_finite_tests':0})
