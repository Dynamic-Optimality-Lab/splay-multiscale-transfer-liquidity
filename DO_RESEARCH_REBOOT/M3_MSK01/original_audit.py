"""Full original roots for every legal mask, cheap Gamma1 and genuine mixed sharing."""
import sys,json,time,copy,itertools
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_MSK01','DO_RESEARCH_REBOOT/M3_ACL01']
from uniform_potential import UniformPotential,BASE
from original_controls import V,S,DAG,build_slow,build_shigh,low
def main():
    out=BASE/'original_audit.json';assert not out.exists();start=time.process_time();d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');P=UniformPotential();V.start=start
    seeds={};runs=[];extra=[];z=S.LEAF
    A=S.node(8,S.balanced(range(-1,8)),z);B=z
    for x in range(9):B=S.node(x,B,z)
    B=V.insert(B,-1)
    for x in range(5):
        marks=[x]+[k for k in range(9) if k!=x][:4];mu=sum(1<<k for k in marks)
        _,_,r=low(d,L,A,B,[],[['K',x]],'minimum_marked_'+str(x),mu=mu);seeds[x]=r
    for marks in itertools.combinations(range(9),5):
        mu=sum(1<<k for k in marks);x=marks[0];r=seeds[x];e=dict(r['environment'])
        V.put(d,e,L['s'].mu,mu);V.put(d,e,L['t'].mu,mu);V.bounds(d,e);assert d.ev_ground(L['root'],e)
        s={**r['source'],'mu':mu};t={**r['destination'],'mu':mu};ps=P(s);pt=P(t);res=r['w']+ps-pt;assert res>=0
        runs.append({'mu':mu,'seed':x,'root':True,'H':r['H'],'q':r['q'],'w':r['w'],'potential_source':ps,'potential_destination':pt,'residual':res})
        assert time.process_time()-start<300,'UNKNOWN original mask audit cap'
        if len(runs)%21==0:print(json.dumps({'masks_verified':len(runs),'cpu':round(time.process_time()-start,2)}),flush=True)
    assert len(runs)==126
    def append(r):
        ps=P.inspect(r['source']);pt=P.inspect(r['destination']);res=r['w']+ps['value']-pt['value'];assert res>=0
        r.update(potential_source=ps,potential_destination=pt,residual=res)
        if r['kind']=='HIGH':
            r.update(OM_residual=r['w']+ps['value'],MO_residual=-pt['value']);assert r['OM_residual']>=0 and r['MO_residual']>=0
        extra.append(r);return r
    # Actual cheap internal-gap whole macros from the new graph.
    cat=json.loads((BASE/'edge_audit.json').read_text());pc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/graph_catalog.json').read_text())
    for weight in (0,1):
        row=next(r for r in cat['samples'] if r['H']==2 and r['w']==weight);x=row['target'];marks=[x]+[k for k in range(9) if k!=x][:4];mu=sum(1<<k for k in marks)
        A0=V.from_serial(pc['A_trees'][row['A_tree']]);B0=V.insert(P.trees[row['source_B']],-1)
        _,_,r=low(d,L,A0,B0,[],row['word'],'Gamma1_weight_'+str(weight),mu=mu);r=append(r);assert r['w']==weight
    # Gamma0 may include a changing unmarked CORE KEEP; it is covered
    # by the actual PRETERMINAL debt floor, not by an entry-depth shortcut.
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/original_h2_controls.json').read_text())
    seed=next(r for r in old['records'] if r['label']=='unmarked_KEEP_KEEP_plus1')
    _,_,r=low(d,L,V.insert(V.from_serial(seed['A_source']),-1),V.insert(V.from_serial(seed['B_source']),-1),[],seed['word'],'Gamma0_unmarked_core_KEEP',mu=seed['source']['mu']);r=append(r)
    assert r['H']==2 and r['w']==1
    # New mask, same full coarse-port closed mixed cycle and shared midpoint.
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_ACL01/original_controls.json').read_text());mu=79;cycle=[]
    for label in ('multi_S_port_RL_to_LR','multi_S_port_mixed_return'):
        r=copy.deepcopy(next(r for r in old['records'] if r['label']==label));r['source']['mu']=mu;r['destination']['mu']=mu;e=r['environment']
        if r['kind']=='LOW':
            V.put(d,e,L['s'].mu,mu);V.put(d,e,L['t'].mu,mu);assert d.ev_ground(L['root'],e)
        else:
            V.put(dh,e,H['s'].mu,mu);V.put(dh,e,H['t'].mu,mu);V.put(dh,e,H['g'].mu,mu);r['shared_midpoint']['mu']=mu;assert dh.ev_ground(H['root'],e)
        cycle.append(append(r))
    assert cycle[0]['source']==cycle[1]['destination'] and cycle[0]['destination']==cycle[1]['source']
    assert sum(r['w'] for r in cycle)==sum(r['residual'] for r in cycle)==8
    # Corrected dangling-reference case in the original compiler, using the uniform table.
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_AER01/original_replay.json').read_text())['records'][0]
    assert d.ev_ground(L['root'],old['environment']);r={**old,'kind':'LOW','label':'dangling_reference_uniform','H':old['environment']['MXL_H'],'q':old['environment']['MXLbt_q']};append(r)
    result={'status':'PASS','all_126_legal_masks_original_roots':True,'mask_runs':runs,'base_environments':seeds,
      'additional_original_roots':len(extra),'additional_records':extra,'closed_mixed_cycle':{'mu':mu,'weight':8,'full_state_closure':True,'same_midpoint':True},
      'source_credit_preserved':True,'DAG_nodes':[len(d.nodes),len(dh.nodes)],'cpu_seconds':round(time.process_time()-start,3)}
    assert result['cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('mask_runs','base_environments','additional_records')},indent=2),flush=True)
if __name__=='__main__':main()
