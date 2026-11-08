"""Original low-root certificates for sharp negative runs and helper resetting."""
import sys,json,time
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import verify_full_mixed as V
import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
OUT=Path('DO_RESEARCH_REBOOT/M3_LDR01/full_run_controls.json')
def erase(t):
    if t==S.LEAF:return t
    if t[1] not in range(9):
        assert t[2]==t[3]==S.LEAF;return S.LEAF
    return S.node(t[1],erase(t[2]),erase(t[3]))
def main():
    assert not OUT.exists();start=time.process_time();V.start=start
    c=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text())
    psi={V.from_serial(n['tree']):n['psi'] for n in c['nodes']}
    d=DAG();L=build_slow(d,'MXL');assert len(d.nodes)<=4000000
    records=[];runs=[]
    def check_run(label,A,B,legs=None,targets=None,fringe=False):
        initial_B=B;ac=A;bc=B;out=[]
        if legs is None:legs=[{'target':x} for x in targets]
        for j,e in enumerate(legs):
            srcA=V.from_serial(e['A_source']) if 'A_source' in e else ac
            if out:assert V.shadow(srcA)==out[-1]['destination']['alpha']
            else:assert V.shadow(srcA)==V.shadow(A)
            oldB=bc;ac,bc,r=V.low(d,L,srcA,bc,[('K',e['target'])],True,f'{label}_{j}')
            r['psi_source']=psi[erase(oldB)];r['psi_destination']=psi[erase(bc)]
            r['Xi_change']=r['psi_source']-r['psi_destination']
            r['Xi_edge_residual']=r['w']-r['Xi_change']
            if r['w']<0:assert r['psi_destination']-r['psi_source']>=-r['w']
            if 'w' in e:assert (r['H'],r['q'],r['w'])==(e['H'],e['q'],e['w'])
            if out:assert out[-1]['destination']==r['source']
            records.append(r);out.append(r)
        weights=[r['w'] for r in out]
        run={'label':label,'labels':[r['label'] for r in out],'weights':weights,
             'total_weight':sum(weights),'D_L':sum(max(0,-w) for w in weights),
             'P_L':sum(max(0,w) for w in weights),'full_shared_states':True,
             'psi_start':psi[erase(initial_B)],'psi_end':psi[erase(bc)],'closed':False}
        runs.append(run);return run
    leaf=S.LEAF
    A=S.node(8,S.node(0,leaf,S.balanced(range(1,8))),leaf)
    B=leaf
    for i in range(9):B=S.node(i,B,leaf)
    sharp=check_run('sharp_minus2',A,B,targets=[0]);assert sharp['weights']==[-2]
    fringe=check_run('sharp_minus2_gap0',V.insert(A,-1),V.insert(B,-1),targets=[0])
    assert fringe['weights']==[-2]
    tail=S.node(6,S.node(5,S.node(4,leaf,leaf),leaf),S.node(7,leaf,S.node(8,leaf,leaf)))
    for i in (3,2,1,0):tail=S.node(i,leaf,tail)
    A2=S.node(0,leaf,S.node(8,S.node(4,S.balanced(range(1,4)),S.balanced(range(5,8))),leaf))
    two=check_run('two_minus1',A2,tail,targets=[8,4]);assert two['weights']==[-1,-1]
    helper=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/helper_search.json').read_text())['shortest_hard_prefix']
    assert helper is not None
    run=check_run('helper_reset',V.from_serial(helper['A0']),V.from_serial(helper['B0']),legs=helper['low_legs'])
    assert run['D_L']==helper['D_L']>2 and run['total_weight']==helper['low_weight']
    resets=[r['label'] for r in records if r['w']>=0 and r['Xi_edge_residual']<0]
    assert resets,'Expected an exact obstruction to extending Xi unchanged'
    assert time.process_time()-start<300
    result={'status':'COMPLETE','queries':len(records),'low_DAG_nodes':len(d.nodes),
            'runs':runs,'Xi_global_extension_counterexamples':resets,
            'negative_mixed_cycle_certified':False,
            'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'}),flush=True)
if __name__=='__main__':main()
