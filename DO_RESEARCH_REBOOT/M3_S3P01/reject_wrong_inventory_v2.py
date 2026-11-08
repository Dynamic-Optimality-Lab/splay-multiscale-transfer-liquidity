"""Negative input controls for source-forced singleton contents, both observed orientations."""
import sys,json,time
sys.path[:0]=['DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
             'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
             'DO_RESEARCH_REBOOT/M3_S3P01','DO_RESEARCH_REBOOT/M3_PHI01']
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from certify_core3_v2 import BASE
import verify_full_mixed as V
OUT=BASE/'wrong_inventory_controls.json'
def main():
    assert not OUT.exists();start=time.process_time();old=json.loads((BASE/'original_core3_controls.json').read_text())
    d=DAG();L=build_slow(d,'MXL');records=[]
    for reason in ('orientation_RL','orientation_LR'):
        r=next(z for z in old['records'] if reason in z.get('reasons',[]))
        inv=next(p for p in r['port_inventory'] if p['hidden_S']==[3] and p['population']==[0]*10)
        slot=inv['slot'];side=inv['side']
        for mode in ('missing_S3','forbidden_gap3_population'):
            e=dict(r['environment'])
            field=f'MXLv_hs{slot}_{side}_3' if mode=='missing_S3' else f'MXLv_z3_{slot}_{side}'
            before=e[field];e[field]=False if mode=='missing_S3' else 1
            V.bounds(d,e);assert not d.ev_ground(L['root'],e),(reason,mode)
            records.append({'label':reason+'_'+mode,'original_low_root':False,'base_control':r['label'],
                'mutated_field':field,'old_value':before,'new_value':e[field],
                'source_and_destination_state_fields_changed':False,'environment':{nm:e[nm] for nm in d.vars}})
    out={'status':'COMPLETE','rejected_original_roots':4,'low_DAG_nodes':len(d.nodes),
         'both_orientations':True,'production_predicates_modified':False,
         'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert out['cpu_seconds']<300
    with OUT.open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()


