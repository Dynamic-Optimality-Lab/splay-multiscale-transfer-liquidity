"""Check a new actual-ID allocation using saved rows; no source engine calls."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def mapping(rows):return {tuple(z['demand']):tuple(z['unit']) for z in rows}
def main():
    cert=read(F/'degree_allocator_receipt.json')
    assert cert['status']=='COMPLETE_NEW_SEVEN_KEY_DEGREE_SOURCE_CERTIFICATE'
    for n,h in cert['input_sha256'].items():assert sha(P/n)==h
    src=read(B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json')
    own=read(B/'SOURCE_JOINT_REPAIR_03/actual_auxiliary_owner_extension.json')
    rows={r['t']:r for r in src['period_rows']};mm=src['funding']['macros'];M={m['target'] for m in mm}
    h=mapping(cert['h']);h0=mapping(src['funding']['h0']);current=mapping(own['full_allocation'])
    U={tuple(u) for m in mm for u in m['units']};D={tuple(d) for m in mm for d in m['demands']}
    assert set(h)==D==set(current) and len(set(h.values()))==len(h)==36 and set(h.values())<=U
    assert all(h[d]==u for d,u in h0.items())
    # Independent marked degree computation by separate root searches for each mark.
    def levels(t):
        deg={k:0 for k in M}
        for key in M:
            u=t;parent=None
            while u[0]!=key:
                if u[0] in M:parent=u[0]
                u=u[1 if key<u[0] else 2]
            if parent is not None:deg[parent]+=1
        return sum(max(v-2,0) for v in deg.values())
    bank=[];new_seen=set();selected_seen=set();peak=0;K=cert['K_actual'];cut=cert['cut_before_macro']
    for j,law in enumerate(cert['receipt']):
        m=mm[(cut+j)%len(mm)];rs=[rows[t] for t in m['rows_t']]
        ds,dt=levels(rs[0]['BF_before']),levels(rs[-1]['BF_after'])
        assert (ds,dt)==(law['D_source'],law['D_target'])
        assert len(bank)==K-ds and law['margin']==2*min(m['H'],3)-m['Q']+dt-ds>=0
        selected=list(map(tuple,law['selected_units']));assert selected==list(map(tuple,m['units'][:2*min(m['H'],3)]))
        assert not selected_seen.intersection(selected);selected_seen.update(selected)
        fixed={tuple(d):tuple(u) for d,u in law['fixed']};assert all(h0[d]==u for d,u in fixed.items())
        available=(set(selected)-set(fixed.values()))|set(bank)
        added=mapping(law['new']);assert set(added)==set(map(tuple,m['demands']))-set(fixed)
        assert set(added.values())<=available and len(set(added.values()))==len(added)
        assert all(h[d]==u for d,u in added.items()) and not new_seen.intersection(added)
        new_seen.update(added)
        out=set(map(tuple,law['carry']));released=set(map(tuple,law['released']))
        assert not out.intersection(released) and out|released==available-set(added.values())
        assert len(out)==K-dt;peak=max(peak,len(bank)+len(selected));bank=list(out)
    assert not bank and peak==cert['working_peak_selected_plus_carry']==10
    assert set(h)-set(h0)==new_seen
    assert all(66<=u[0]<=130 for u in h.values()) and all(66<=d[0]<=130 for d in h)
    assert cert['current_owner_sha256']==sha(B/'SOURCE_JOINT_REPAIR_03/actual_auxiliary_owner_extension.json')
    assert len(current)==36 and cert['new_actual_physical_owner_assignments'] is False
    report={'status':'PASS_ACTUAL_ID_NEW_DEGREE_CERTIFICATE','source_queries':0,'source_engine_calls':0,
      'source_primitive_replay':False,'source_period':[66,130],'full_demands':36,
      'D_actual_max':K,'working_peak':peak,'original_natural_h0_preserved':True,
      'physical_units_all_on_one_original_period':True,'current_frozen_full36_unchanged':True,
      'scope':'this saved original seven-key source; universal complement proof is the separate SE35 derivation',
      'proof_cut':'internal cyclic full comparison cut; original auxiliary cut unchanged; no online endpoint-bank assertion',
      'trust':'different marked-degree and allocation verifier, same agent; not external or formal review',
      'UCF35':'OPEN','all_exceptional_periods_covered':False,
      'input_sha256':{'degree_allocator_receipt.json':sha(F/'degree_allocator_receipt.json')}}
    with (F/'independent_degree_allocation_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print('ACTUAL_SOURCE36_DEGREE_COMPARISON_INDEPENDENTLY_CHECKED; WORKING10',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify94_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
