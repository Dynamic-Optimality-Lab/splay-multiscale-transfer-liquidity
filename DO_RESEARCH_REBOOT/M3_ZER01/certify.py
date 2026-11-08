"""No-fit zero-fringe transfer, finite identities and complete original controls."""
import sys,json,time,copy
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_ZER01','DO_RESEARCH_REBOOT/M3_ACL01']
from zero_potential import ZeroPotential,augment,S,V
from original_controls import DAG,build_slow,build_shigh,low,high,exact_witness,AState,ED,alpha_prefix,splay_event,Box
BASE=Path('DO_RESEARCH_REBOOT/M3_ZER01')
def main():
    out=BASE/'certificate.json';assert not out.exists();prereq=json.loads(Path('DO_RESEARCH_REBOOT/M3_MSK01/replay_v2/original_audit_v2.json').read_text());assert prereq['status']=='PASS'
    start=time.process_time();P=ZeroPotential();N=0
    for t in P.positive.trees:
        ft=augment(t);assert tuple(tuple(r) for r in V.shadow(ft)) in P.positive.sid
        for x in range(9):
            assert S.lookup(t,x)[1]==S.lookup(ft,x)[1]
            assert augment(S.trace(t,x)[0])==S.trace(ft,x)[0];N+=1
        assert time.process_time()-start<120
    finite_cpu=time.process_time()-start;d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');V.start=time.process_time();V.MU=79;records=[]
    def add(r):
        s=P.inspect(r['source']);t=P.inspect(r['destination']);res=r['w']+s['value']-t['value'];assert res>=0
        r.update(potential_source=s,potential_destination=t,residual=res)
        if r['kind']=='HIGH':r.update(OM_residual=r['w']+s['value'],MO_residual=-t['value']);assert r['OM_residual']>=0 and r['MO_residual']>=0
        records.append(r);return r
    z=S.LEAF;A=S.node(2,S.node(0,z,S.node(1,z,z)),S.node(6,S.node(3,z,S.node(4,z,S.node(5,z,z))),S.node(8,S.node(7,z,z),z)))
    ac,bc,r=low(d,L,A,A,[(6,0)],[['K',6]],'zero_signature_multiport_low',mu=79);r=add(r)
    h=high(dh,H,ac,bc,A,2,[0]*10,79,'zero_signature_shared_high_return');e=h['environment']
    for tag,s in (('MXHs',r['destination']),('MXHt',r['source'])):
        for j,(k,ss,ix) in enumerate(s['alpha']):e[f'{tag}_ak{j}']=k;e[f'{tag}_aS{j}']=bool(ss);e[f'{tag}_aI{j}']=ix
    h['source']['alpha']=copy.deepcopy(r['destination']['alpha']);h['destination']['alpha']=copy.deepcopy(r['source']['alpha']);assert dh.ev_ground(H['root'],e);h=add(h)
    assert r['source']==h['destination'] and r['destination']==h['source'] and r['w']+h['w']==8
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/original_h2_controls.json').read_text())
    s=next(r for r in old['records'] if r['label']=='unmarked_KEEP_KEEP_plus1')
    _,_,r=low(d,L,V.from_serial(s['A_source_physical']),V.from_serial(s['B_source']),[],s['word'],'zero_signature_whole_macro',mu=s['source']['mu']);add(r)
    A=S.node(1,S.node(0,z,z),S.node(8,S.balanced(range(2,8)),z));B=z
    for k in reversed(range(2,9)):B=S.node(k,z,B)
    B=S.node(1,S.node(0,z,z),B)
    _,_,r=low(d,L,A,B,[],[['K',8]],'zero_signature_dangling_negative',mu=341);e=r['environment'];w=exact_witness(e)
    target=next(i for i in range(127) if e[f'MXLw_p{i}'] and e[f'MXLw_isS{i}'] and e[f'MXLw_sidx{i}']==8)
    assert e[f'MXLw_kr{target}']==2;e[f'MXLw_kr{target}']=0;e[f'MXLw_cr{target}']=255
    w=exact_witness(e);st=AState(ED,w);sa=alpha_prefix(w,st);st=splay_event(ED,w,st,0,Box(True));ta=alpha_prefix(w,st)
    for tag,a in (('MXLs',sa),('MXLt',ta)):
        for j,(k,ss,ix) in enumerate(a):e[f'{tag}_ak{j}']=k;e[f'{tag}_aS{j}']=bool(ss);e[f'{tag}_aI{j}']=ix
    r['source']['alpha']=sa;r['destination']['alpha']=ta;V.bounds(d,e);assert d.ev_ground(L['root'],e);assert r['w']==-1;add(r)
    for r in records:
        dd,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root']);assert dd.ev_ground(root,r['environment'])
    result={'status':'PASS','finite_augmentation_cases':N,'all_core_depths_preserved':True,
      'physical_U9_trees':len(P.positive.trees),'original_controls':len(records),'original_roots_independently_replayed':len(records),
      'closed_mixed_cycle':{'mu':79,'weight':8,'full_state_closure':True,'same_high_midpoint':True},
      'new_fit':False,'finite_cpu_seconds':round(finite_cpu,3),'original_cpu_seconds':round(time.process_time()-start-finite_cpu,3),
      'DAG_nodes':[len(d.nodes),len(dh.nodes)],'records':records}
    assert result['original_cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
