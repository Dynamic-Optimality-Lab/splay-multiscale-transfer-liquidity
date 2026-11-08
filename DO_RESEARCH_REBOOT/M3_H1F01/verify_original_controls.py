"""Full original helper roots, macro variants, closed mixed cycle and anomalous high control."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H1F01','DO_RESEARCH_REBOOT/M3_FRC01',
             'DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
from verify_original_compensation import high
from one_gap_potential import OneGapPotential
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from build_fragment import BASE
OUT=BASE/'original_controls.json'
def main():
    assert not OUT.exists();start=time.process_time();V.start=start;V.MU=341;P=OneGapPotential()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH')
    assert len(d.nodes)<4000000 and len(dh.nodes)<4000000
    audit=json.loads((BASE/'edge_audit.json').read_text());records=[];variants=[]
    def append(r):
        a=P.inspect(r['source']);b=P.inspect(r['destination'])
        oldr=r['w']-b['compensated_joint']+a['compensated_joint'];newr=r['w']-b['one_gap_joint']+a['one_gap_joint']
        assert newr>=0,(r['label'],newr)
        r.update(potential_source=a,potential_destination=b,FRC_reduced_weight=oldr,joint_reduced_weight=newr)
        if r['kind']=='HIGH':
            r.update(midpoint_correction=0,OM_reduced_weight=r['w']+a['one_gap_joint'],MO_reduced_weight=-b['one_gap_joint'])
            assert r['OM_reduced_weight']>=0 and r['MO_reduced_weight']>=0
        records.append(r);assert time.process_time()-start<300,'UNKNOWN: controls cap'
        print(json.dumps({'label':r['label'],'w':r['w'],'old_r':oldr,'new_r':newr}),flush=True)
        return r
    samples=audit['sample_edges'];sample_records={}
    for name,row in samples.items():
        A=V.from_serial(P.c['A_trees'][row['A_tree']]);B=V.insert(P.old.old.trees[row['source_B']],-1)
        _,_,r=V.low(d,L,A,B,row['word'],True,name);r=append(r)
        assert r['potential_source']['table_node']==row['source'] and r['potential_destination']['table_node']==row['destination']
        assert r['H']==row['H'] and r['w']==row['weight'];sample_records[name]=r
        if name.startswith('H1_'):assert r['FRC_reduced_weight']<0 and r['potential_source']['core_tree_id'] not in P.old.R
    # Whole-macro controls with the exact SAME full endpoints and weight.
    h1=sample_records['H1_w0_oldr-2'];x=h1['word'][0][1]
    _,_,r=V.low(d,L,V.from_serial(h1['A_source']),V.from_serial(h1['B_source']),[['D',x],['K',x]],True,'H1_DELETE_zeroKEEP_same_endpoints')
    r=append(r);assert r['source']==h1['source'] and r['destination']==h1['destination'] and r['H']==1 and r['w']==h1['w']
    variants.append({'original':h1['label'],'variant':r['label'],'full_states_and_weight_equal':True})
    h2=sample_records['FRC_exception_952'];x=h2['word'][-1][1]
    for j,word in enumerate(([['D',-1],['K',-1],['K',x]],
                            [['K',-1],['D',x],['K',x]],
                            [['D',-1],['K',-1],['D',x],['K',x]])):
        _,_,r=V.low(d,L,V.from_serial(h2['A_source']),V.from_serial(h2['B_source']),word,True,'H2_macro_variant_'+str(j))
        r=append(r);assert r['source']==h2['source'] and r['destination']==h2['destination'] and r['H']==2 and r['w']==h2['w']
        variants.append({'original':h2['label'],'variant':r['label'],'full_states_and_weight_equal':True})
    # A fully closed original mixed cycle in this nonempty-fringe sector.
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_PHI01/full_mixed_controls.json').read_text());legs=[]
    for j in range(3):
        z=next(r for r in old['records'] if r['label']==f'cycle_3_p1_low{j}')
        A=V.insert(V.from_serial(z['A_source']),-1);B=V.insert(V.from_serial(z['B_source']),-1)
        if j==0:A0=A;B0=B
        ac,bc,r=V.low(d,L,A,B,z['word'],True,'one_gap_closed_cycle_low'+str(j));legs.append(append(r))
    r=high(dh,H,ac,bc,A0,A0[1],[1]+[0]*9,341,'one_gap_closed_cycle_high')
    assert V.from_serial(r['B_destination'])==B0;legs.append(append(r))
    for left,right in zip(legs,legs[1:]+legs[:1]):assert left['destination']==right['source']
    assert sum(r['w'] for r in legs)==4 and sum(r['joint_reduced_weight'] for r in legs)==4
    # Genuine noncanonical high depth 9 over a true depth-eight core path.
    z=S.LEAF;B=z
    for x in reversed(range(9)):B=S.node(x,z,B)
    B=V.insert(B,-1);A=V.insert(S.node(0,z,S.balanced(range(1,9))),-1)
    Ad=V.insert(S.node(8,S.balanced(range(8)),z),-1)
    r=high(dh,H,A,B,Ad,8,[1]+[0]*9,341,'noncanonical_high_abstract_shadow')
    env=r['environment'];env['MXHbt_bd0']=9;env['MXHbt_bp0_9']=19;env['MXHbt_bdir0_8']=False
    abstract=[[0,1,8]]+[[2,0,0] for _ in range(6)]
    for j,(k,s,x) in enumerate(abstract):env[f'MXHt_ak{j}']=k;env[f'MXHt_aS{j}']=bool(s);env[f'MXHt_aI{j}']=x
    V.bounds(dh,env);assert dh.ev_ground(H['root'],env)
    r['destination']['alpha']=abstract;r.update(d=9,true_core_depth=8,noncanonical_high=True,abstract_destination_shadow=True)
    append(r)
    result={'status':'COMPLETE','low_DAG_nodes':len(d.nodes),'high_DAG_nodes':len(dh.nodes),
            'controls':len(records),'original_low_roots':sum(r['kind']=='LOW' for r in records),
            'original_high_roots':sum(r['kind']=='HIGH' for r in records),
            'cheap_H1_old_failures_repaired':3,'full_macro_variants':variants,
            'closed_mixed_cycle':{'labels':[r['label'] for r in legs],'full_state_closure':True,'high_midpoint_shared':True,
                                  'weight':4,'joint_reduced_weight':4,'mu':341,'sigma':[1]+[0]*9},
            'noncanonical_high_control':True,'negative_mixed_cycles_certified':0,
            'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
