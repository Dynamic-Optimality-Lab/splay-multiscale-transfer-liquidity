"""Instantiate the explicit prepared-family donor rule on the audited core13 source."""
import json,time,sys,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    sp=importlib.util.spec_from_file_location('old_natural_owner_frame137',P/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/source_funding.py');M=importlib.util.module_from_spec(sp);sp.loader.exec_module(M)
    z=json.loads((B/'core13_framed_activation_closed_source.json').read_text());rows=[{'occurrence':r['absolute_t'],'a':r['H'],'qF':r['QF'],'genuine_F':r['kind']=='K' and r['key']!=r['BF_before'][0]} for r in z['period_rows']];v=M.own_map(rows);h=dict(v['h0']);critical=[];donors=[]
    for i,m in enumerate(v['macros']):
        missing=[d for d in m['demands'] if d not in h]
        if not missing:continue
        critical.append(i);pre=v['macros'][i-1];assert (m['H'],m['Q'])==(2,6) and pre['Q']==1 and pre['H']>=7
        supply=pre['units'][1:1+len(missing)]
        for d,u in zip(missing,supply):assert u not in h.values();h[d]=u;donors.append({'demand':d,'unit':u,'source_predecessor_macro':i-1,'zero_based_unit_ordinal':pre['units'].index(u)})
    assert len(critical)==1 and len(donors)==2 and set(h)==v['D'] and len(set(h.values()))==36 and set(h.values())<=v['U'] and all(h[d]==u for d,u in v['h0'].items())
    out('framed_core13_full_matching.json',{'status':'EXPLICIT_SOURCE_DERIVED_PREPARED_FAMILY_FULL_MATCHING','period':z['period'],'full_pairs':[{'demand':d,'unit':u} for d,u in sorted(h.items())],'natural_h0':[{'demand':d,'unit':u} for d,u in sorted(v['h0'].items())],'donor_additions':donors,'total_demands':len(h),'actual_unit_inventory':len(v['U']),'all_original_ids_in_one_period':True,'no_old_owner_changed':True,'supplied_fE':'none invented; frozen-owner extension theorem remains conditional on its original input and eligibility licenses','Bank25_interface':'not promoted from a matching; chronological/block working interface separate','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('FRAMED_FAMILY_PHYSICAL_REPAYMENT.md','core13_framed_activation_closed_source.json','framed_return_and_core13_independent_audit.json')}});print(json.dumps({'status':'PASS_SOURCE_DONOR_RULE_INSTANCE','full_demands':36,'new_donors':donors,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof137_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
