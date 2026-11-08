"""Complete original roots for population opacity, multi-spines and T saturation."""
import sys,json,time,copy
from pathlib import Path
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_GAP01')
from original_factory import S,V,DAG,build_slow,build_shigh,low,high
from potential import GapPotential,BASE
from build import decorate
from core_refinement_v2 import rho
def concrete(t,n):
    k=len([x for x in S.inorder(t) if x<0]);assert n>=k;extra=S.balanced(range(-n,-k));used=False;cuts=[]
    def go(z):
        nonlocal used
        assert z[0]!='leaf';ch=[]
        for side,b in enumerate(z[2:]):
            if b[0]=='leaf':
                cuts.append((z[1],side));ch.append(extra if not used else S.LEAF);used=True
            else:ch.append(go(b))
        return S.node(z[1],*ch)
    return go(t),cuts
def main():
    out=BASE/'original_audit.json';assert not out.exists();start=time.process_time();V.start=start;P=GapPotential();c=P.c
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');records=[];samples=json.loads((BASE/'edge_audit.json').read_text())['samples']
    def add(r):
        si=P.inspect(r['source']);ti=P.inspect(r['destination']);rr=r['w']+si['value']-ti['value'];assert rr>=0,(r['label'],rr)
        r.update(potential_source=si,potential_destination=ti,residual=rr)
        if r['kind']=='HIGH':r.update(OM_residual=r['w']+si['value'],MO_residual=-ti['value']);assert r['OM_residual']>=0 and r['MO_residual']>=0
        records.append(r);assert time.process_time()-start<300,'UNKNOWN original audit cap'
        print(json.dumps({'label':r['label'],'n':r['source']['sigma'][0],'w':r['w'],'residual':rr}),flush=True);return r
    cases=[('H1w-2',0),('H1w-2',1),('double_anonymous_source_H1w-1',2),('H2w0',1),
      ('double_anonymous_source_H2w0',2),('three_anonymous_H2_w1',3),('three_anonymous_H2_w0',3),('three_anonymous_H2_w1',4)]
    anchor=None
    for name,n in cases:
        o=samples[name];m=c['models'][o['model']];proto=decorate(P.trees[m['core']],m['counts']);A,cuts=concrete(proto,n)
        B=P.trees[o['source_B']];B=V.insert(B,-1) if n else B;x=o['target'];marks=[x]+[k for k in range(9) if k!=x][:4];mu=sum(1<<k for k in marks)
        _,_,r=low(d,L,A,B,cuts,o['word'],name+'_population_'+str(n),mu=mu);r=add(r)
        assert r['w']==o['w'] and r['source']['alpha']==c['shadows'][o['source_shadow']]
        if name=='three_anonymous_H2_w1' and n==3:anchor=(A,B,cuts,r,o)
    A,B,cuts,r,o=anchor;f=o['word'][0][1];x=o['target']
    _,_,whole=low(d,L,A,B,cuts,[['D',f],['K',f],['D',x],['K',x]],'three_spine_whole_macro',mu=r['source']['mu']);whole=add(whole)
    assert whole['source']==r['source'] and whole['destination']==r['destination'] and whole['w']==r['w']
    # Large hidden population stays in an existing opaque source port.
    big=copy.deepcopy(r);big['label']='population_266_opaque_payload';e=big['environment'];base_n=r['source']['sigma'][0]
    port=next(v for v in big['port_inventory'] if not v['hidden_S'] and v['lower']<=base_n)
    key=f'MXLv_z0_{port["slot"]}_{port["side"]}';e[key]+=266-base_n;port['population'][0]+=266-base_n
    big['source']['sigma'][0]=big['destination']['sigma'][0]=266
    for st in (L['s'],L['t']):V.put(d,e,st.sig[0],266)
    V.bounds(d,e);assert d.ev_ground(L['root'],e);big['additional_hidden_population']=266-base_n;big['A_serial_is_rank_skeleton']=True;add(big)
    # Previously obstructed identical states with different fringe allocations.
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_SIG02/obstruction.json').read_text());pair=[]
    for rr in old['records']:
        rr=copy.deepcopy(rr);assert d.ev_ground(L['root'],rr['environment']);pair.append(add(rr))
    assert pair[0]['source']==pair[1]['source'] and pair[0]['destination']==pair[1]['destination']
    assert pair[0]['potential_source']['image_alpha']==pair[1]['potential_source']['image_alpha']
    # A full mixed cycle with opaque S and fringe ports at population3.
    z=S.LEAF;fr=S.balanced(range(-3,0));A=S.node(2,S.node(0,fr,S.node(1,z,z)),
      S.node(6,S.node(3,z,S.node(4,z,S.node(5,z,z))),S.node(8,S.node(7,z,z),z)))
    core=S.node(2,S.node(0,z,S.node(1,z,z)),S.node(6,S.node(3,z,S.node(4,z,S.node(5,z,z))),S.node(8,S.node(7,z,z),z)))
    B=V.insert(core,-1);ac,bc,l=low(d,L,A,B,[(0,0),(6,0)],[['K',6]],'population3_core_and_fringe_ports_low',mu=79);l=add(l)
    h=high(dh,H,ac,bc,A,2,[3]+[0]*9,79,'population3_shared_high_return');e=h['environment']
    for tag,s in (('MXHs',l['destination']),('MXHt',l['source'])):
        for j,(k,ss,ix) in enumerate(s['alpha']):e[f'{tag}_ak{j}']=k;e[f'{tag}_aS{j}']=bool(ss);e[f'{tag}_aI{j}']=ix
    h['source']['alpha']=copy.deepcopy(l['destination']['alpha']);h['destination']['alpha']=copy.deepcopy(l['source']['alpha']);assert dh.ev_ground(H['root'],e);h=add(h)
    assert l['source']==h['destination'] and l['destination']==h['source'] and l['w']+h['w']==8
    mutants=json.loads(Path('DO_RESEARCH_REBOOT/M3_ACL_AUD02/dangling_audit.json').read_text())['accepted_rows']
    assert all(v['w']+P(v['source'])-P(v['destination'])>=0 for v in mutants)
    # Independent replay of every saved total environment, not only construction-time asserts.
    for rr in records:
        dd,root=(d,L['root']) if rr['kind']=='LOW' else (dh,H['root']);assert dd.ev_ground(root,rr['environment']);V.bounds(dd,rr['environment'])
    result={'status':'PASS','complete_original_roots':len(records),'populations_verified':sorted({r['source']['sigma'][0] for r in records}),
      'same_state_different_population_allocations_same_image':True,'whole_macro_same_endpoints_and_source_q':True,
      'prior_dangling_mutants_inequalities':len(mutants),'closed_mixed_cycle':{'mu':79,'n':3,'weight':8,'full_state_closure':True,'same_midpoint':True},
      'DAG_nodes':[len(d.nodes),len(dh.nodes)],'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert result['cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
