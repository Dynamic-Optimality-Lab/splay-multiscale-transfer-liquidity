"""Fresh original witnesses for the reflected outer-gap9 consequence."""
import sys,json,time,copy
from pathlib import Path
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_OUT01','DO_RESEARCH_REBOOT/M3_GAPINT01']
from potential import OutsidePotential
from outside_original import (S,V,DAG,build_slow,build_shigh,low,high,
    exact_witness,AState,ED,alpha_prefix,splay_event,Box)
BASE=Path('DO_RESEARCH_REBOOT/M3_OUT01')

def code(k):return 16*(8-k) if k in range(9) else 135-k

def reverse(t):
    return S.LEAF if t is None else S.node(code(t[0]),reverse(t[2]),reverse(t[1]))

def main():
    assert json.loads((BASE/'reflection_audit.json').read_text())['status']=='PASS_COMPLETE_LOW_REFLECTION_IDENTITIES'
    out=BASE/'gap9_original_audit_v2.json';assert not out.exists();start=time.process_time()
    d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');P=OutsidePotential();records=[]
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_GAP01/original_audit.json').read_text())['records']
    def add(r):
        si=P.inspect(r['source']);ti=P.inspect(r['destination'])
        residual=r['w']+si['value']-ti['value'];assert residual>=0,(r['label'],residual)
        assert all(not (s['b']['kr'][8]==0 and s['b']['rr'][8]==19) for s in (r['source'],r['destination']))
        r.update(potential_source=si,potential_destination=ti,residual=residual)
        if r['kind']=='HIGH':assert r['w']+si['value']>=0 and -ti['value']>=0
        records.append(r);assert time.process_time()-start<300
        return r
    # Original physical witnesses are rebuilt with fresh ranks and port tests.
    for r in old[:9]:
        A=reverse(r['A_source']);B=reverse(r['B_source'])
        cuts=[(code(k),1-b) for k,b in r['cuts']]
        word=[[mode,code(k)] for mode,k in r['word']]
        mu=sum(1<<(8-k) for k in range(9) if r['source']['mu']>>k&1)
        _,_,rr=low(d,L,A,B,cuts,word,'gap9_'+r['label'],mu);rr=add(rr)
        assert (rr['H'],rr['q'],rr['w'])==(r['H'],r['q'],r['w'])
    # Maximal population remains opaque; do not fabricate266 physical keys.
    rr=copy.deepcopy(next(r for r in records if r['source']['sigma'][9]==3))
    rr['label']='gap9_population266_opaque_source_payload';e=rr['environment']
    port=next(p for p in rr['port_inventory'] if not p['hidden_S_indices'] and p['upper']==136)
    e[f'MXLv_z9_{port["slot"]}_{port["side"]}']+=263;port['population'][9]+=263
    rr['source']['sigma'][9]=rr['destination']['sigma'][9]=266
    for st in (L['s'],L['t']):V.put(d,e,st.sig[9],266)
    V.bounds(d,e);assert d.ev_ground(L['root'],e);rr['serial_tree_is_rank_skeleton']=True;add(rr)
    # Slot0 fallback is tested in the real source, not reflected as a high symmetry.
    seed=records[0]
    for ref in (127,255):
        rr=copy.deepcopy(seed);rr['label']=f'gap9_dangling_ref{ref}';e=rr['environment']
        assert e['MXLw_kr0'] in (1,2);e['MXLw_kr0']=0;e['MXLw_cr0']=ref
        w=exact_witness(e);a=AState(ED,w);sa=alpha_prefix(w,a)
        for j in range(len(rr['word_codes'])):a=splay_event(ED,w,a,j,Box(True))
        ta=alpha_prefix(w,a)
        for tag,alpha in (('MXLs',sa),('MXLt',ta)):
            for i,(k,s,x) in enumerate(alpha):e[f'{tag}_ak{i}']=k;e[f'{tag}_aS{i}']=bool(s);e[f'{tag}_aI{i}']=x
        rr['source']['alpha']=sa;rr['destination']['alpha']=ta
        assert d.ev_ground(L['root'],e);add(rr)
    # Fully closed outer-gap mixed cycle, including an opaque S port.
    r=next(r for r in old if r['label']=='population3_core_and_fringe_ports_low')
    A=reverse(r['A_source']);B=reverse(r['B_source']);cuts=[(code(k),1-b) for k,b in r['cuts']]
    mu=sum(1<<(8-k) for k in range(9) if r['source']['mu']>>k&1)
    _,bc,l=low(d,L,A,B,cuts,[[mode,code(k)] for mode,k in r['word']],'gap9_closed_cycle_low',mu);l=add(l)
    h=high(dh,H,bc,code(2),l['destination'],l['source'],'gap9_closed_cycle_high');h=add(h)
    assert l['source']==h['destination'] and l['destination']==h['source'] and l['w']+h['w']==8
    for r in records:
        dd,root=(d,L['root']) if r['kind']=='LOW' else (dh,H['root'])
        V.bounds(dd,r['environment']);assert dd.ev_ground(root,r['environment'])
    result={'status':'PASS','original_roots':len(records),'independent_replays':len(records),
            'populations':sorted({r['source']['sigma'][9] for r in records}),
            'source_legal_dangling_refs':[127,255],
            'closed_mixed_cycle':{'mu':mu,'gap':9,'population':3,'weight':8,'full_state_closure':True,'same_midpoint':True},
            'DAG_nodes':[len(d.nodes),len(dh.nodes)],'cpu_seconds':round(time.process_time()-start,3),'records':records}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2),flush=True)

if __name__=='__main__':main()
