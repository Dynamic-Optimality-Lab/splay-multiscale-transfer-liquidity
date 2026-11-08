import sys
sys.path.append('DO_RESEARCH_REBOOT/M3_GAPINT01')
import json,time,copy
from pathlib import Path
from potential_v3 import InteriorPotential,BASE
from framework_v2 import S,V,decode,collapse,iscore,PORT
from interior_original import DAG,build_slow,build_shigh,low,high,fill
def scale(t):return S.LEAF if t==S.LEAF else S.node(16*t[1],scale(t[2]),scale(t[3]))
def mirror(t):return t if t[0]=='leaf' else S.node(128-t[1],mirror(t[3]),mirror(t[2]))
def concrete(t,n,g):
    k=sum(not iscore(x) for x in S.inorder(t));assert n>=k and n-k<=7
    extra=S.balanced(range(16*g-15,16*g-15+n-k));cuts=[];used=False
    def go(t,lo,hi):
        nonlocal used
        ch=[]
        for b,z in enumerate(t[2:]):
            l,h=(lo,t[1]) if b==0 else (t[1],hi)
            if z[0]=='leaf':
                cuts.append((t[1],b));take=not used and extra!=S.LEAF and l<extra[1]<h
                ch.append(extra if take else S.LEAF)
                if take:used=True
            else:ch.append(go(z,l,h))
        return S.node(t[1],*ch)
    ans=go(t,-10000,10000);assert used or n==k;return ans,cuts
def main():
    out=BASE/'original_audit.json';assert not out.exists();start=time.process_time();P=InteriorPotential();d=DAG();L=build_slow(d,'MXL');dh=DAG();H=build_shigh(dh,'MXH');records=[]
    samples=json.loads((BASE/'edge_audit.json').read_text())['samples'];c=P.c
    def add(r):
        s=P.inspect(r['source']);t=P.inspect(r['destination']);res=r['w']+s['value']-t['value'];assert res>=0,(r['label'],res)
        r.update(potential_source=s,potential_destination=t,residual=res)
        if r['kind']=='HIGH':r.update(OM_residual=r['w']+s['value'],MO_residual=-t['value']);assert r['OM_residual']>=0 and r['MO_residual']>=0
        records.append(r);assert time.process_time()-start<300
        print(json.dumps({'label':r['label'],'sigma':r['source']['sigma'],'w':r['w'],'residual':res}),flush=True);return r
    specs=[(samples['w-2'],0),(samples['w-2'],1)]
    # Find a genuine two-node anonymous source and a compatible B depth.
    census=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text());two=None
    for ai,os in enumerate(c['low_options']):
        if two:break
        for o in os:
            t=decode(c['witnesses'][o['witness']])
            if sum(not iscore(x) for x in S.inorder(t))!=2:continue
            for bi,b in enumerate(P.trees):
                if b[1]==t[1]//16 and census['B_depth'][bi][o['target']]>=4:two={**o,'source_B':bi};break
            if two:break
    assert two;specs.append((two,2))
    tri=next(r for k,r in samples.items() if k.startswith('three_fringe_fork'));specs.extend(((tri,3),(tri,4)))
    anchor=None
    for row,n in specs:
        proto=decode(c['witnesses'][row['witness']]);A,cuts=concrete(proto,n,c['gap']);B=scale(P.trees[row['source_B']]);B=V.insert(B,16*c['gap']-8) if n else B
        x=row['target'];mu=sum(1<<k for k in [x]+[k for k in range(9) if k!=x][:4]);_,_,r=low(d,L,A,B,cuts,[['K',16*x]],'gap'+str(c['gap'])+'_population_'+str(n),mu);r=add(r)
        if n==3:anchor=(proto,row,r)
    proto,row,r=anchor;mg=9-c['gap'];A,cuts=concrete(mirror(proto),3,mg);B=V.insert(scale(P.trees[P.bid[V.from_serial(r['source']['b_tree'])]]) if 'b_tree' in r['source'] else mirror(scale(P.trees[row['source_B']])),16*mg-8)
    x=8-row['target'];mu=sum(1<<k for k in [x]+[k for k in range(9) if k!=x][:4]);_,_,rr=low(d,L,A,B,cuts,[['K',16*x]],'reflected_gap7_three_node_fork',mu);rr=add(rr)
    assert rr['w']==r['w'] and rr['potential_source']['value']==r['potential_source']['value'] and rr['potential_destination']['value']==r['potential_destination']['value']
    # Wrong-side boundary-touching inventory is ORIGINAL-legal; do not
    # infer literal physical key contents from the weak LE compatibility.
    g=c['gap'];proto=collapse(scale(S.balanced(range(9))));A,cuts=concrete(proto,1,g);B=V.insert(scale(S.balanced(range(9))),16*g-8)
    _,_,base=low(d,L,A,B,cuts,[['K',32]],'base_for_boundary_payload',47);base=add(base)
    for n in (2,266):
        rr=copy.deepcopy(base);rr['label']='wrong_side_gap'+str(g)+'_payload_'+str(n);e=rr['environment'];port=next(p for p in rr['port_inventory'] if p['upper']==g-1 and not p['hidden_S_indices'])
        key=f'MXLv_z{g}_{port["slot"]}_{port["side"]}';e[key]+=n-1;port['population'][g]+=n-1
        rr['source']['sigma'][g]=rr['destination']['sigma'][g]=n
        for s in (L['s'],L['t']):V.put(d,e,s.sig[g],n)
        V.bounds(d,e);assert d.ev_ground(L['root'],e);rr['additional_hidden_population']=n-1;rr['serial_tree_is_rank_skeleton']=True;add(rr)
    # Whole Gamma0 unmarked-core macro with positive interior population.
    old=json.loads(Path('DO_RESEARCH_REBOOT/M3_H2R01/original_h2_controls.json').read_text());s=next(r for r in old['records'] if r['label']=='unmarked_KEEP_KEEP_plus1')
    Ap=collapse(scale(V.from_serial(s['A_source_physical'])));A,cuts=concrete(Ap,1,g);B=V.insert(scale(V.from_serial(s['B_source'])),16*g-8)
    _,_,rr=low(d,L,A,B,cuts,[[mode,16*x] for mode,x in s['word']],'interior_Gamma0_unmarked_core_whole_macro',s['source']['mu']);rr=add(rr);assert rr['H']==2 and rr['q']==3
    # Reversible core zig with a retained anonymous fork and an opaque S port.
    z=S.LEAF;croot=g+1;right=S.balanced([16*k for k in range(g+2,9)]);rkey=right[1]//16
    core= S.node(croot,S.balanced(range(g+1)),S.balanced(range(g+2,9)))
    Afork=S.node(16*croot,S.node(16*g-8,S.balanced([16*k for k in range(g)]),S.node(16*g,z,z)),right)
    A,cuts=concrete(collapse(Afork),3,g);cuts.append((16*rkey,0));B=V.insert(scale(core),16*g-8)
    marks=[croot,rkey]+[k for k in range(9) if k not in (croot,rkey)][:3];cycle_mu=sum(1<<k for k in marks)
    ac,bc,l=low(d,L,A,B,cuts,[['K',16*rkey]],'interior_fork_cycle_low',cycle_mu);l=add(l)
    h=high(dh,H,bc,16*croot,l['destination'],l['source'],'interior_fork_cycle_high');h=add(h)
    assert l['source']==h['destination'] and l['destination']==h['source'] and l['w']+h['w']==8
    for rr in records:
        dd,root=(d,L['root']) if rr['kind']=='LOW' else (dh,H['root']);V.bounds(dd,rr['environment']);assert dd.ev_ground(root,rr['environment'])
    res={'status':'PASS','original_roots':len(records),'gaps':[g,9-g],'populations':sorted({max(r['source']['sigma']) for r in records}),
      'wrong_side_positive_population_originally_valid':True,'mirror_is_profile_only':True,
      'closed_mixed_cycle':{'mu':cycle_mu,'n':3,'gap':g,'weight':8,'full_state_closure':True,'same_midpoint':True},
      'DAG_nodes':[len(d.nodes),len(dh.nodes)],'cpu_seconds':round(time.process_time()-start,3),'records':records}
    assert res['cpu_seconds']<300
    with out.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
    print(json.dumps({k:v for k,v in res.items() if k!='records'},indent=2),flush=True)
if __name__=='__main__':main()
