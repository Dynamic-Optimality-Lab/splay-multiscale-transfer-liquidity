"""Independent original-source replay of the counterfamily control and AF."""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def labels(t,C):
    a=collections.Counter()
    def go(u):
        if u is None:return frozenset()
        z=go(u[1])|go(u[2])|({u[0]} if u[0] in C else set());a[frozenset(z)]+=1
        return frozenset(z)
    go(t);return a
def phi(a,b,C):return sum((labels(b,C)-labels(a,C)).values())
def main():
    global V
    sp=importlib.util.spec_from_file_location('independent_PC35_Mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    path=F/'projected_cluster_closed_counter_source.json';src=json.loads(path.read_text())
    for p,h in src['input_sha256'].items():assert sha(Path(p))==h
    ini=tup(src['initial_diagonal']);A=V.Mutable(ini);BF=V.Mutable(ini);BE=V.Mutable(ini);cf=ce=()
    C=set(src['M']);assert C==set(src['S'])==set(src['physical_keys'])
    full=list(src['prefix_rows'])+list(src['period_rows']);cuts=[];drops=None
    start=len(src['prefix_rows']);Acount=QF=QE=0
    for i,r in enumerate(full):
        a,b,e=map(tup,(A.snapshot(),BF.snapshot(),BE.snapshot()))
        if i==start:cuts.append((a,b,e,cf,ce))
        assert r['t']==i+1 and (a,b,e)==tuple(tup(r[k]) for k in ('A_before','BF_before','BE_before'))
        x=r['key'];kind=r['kind'];h,_,_=A.splay(x,False);q=qe=0;gf=ge=False;bv=[]
        if kind=='K':
            gf=b[0]!=x;_,q,bv=BF.splay(x,r['t']==src['target_t'])
            if gf:cf=(x,)+tuple(y for y in cf if y!=x)
            if x!=src['erased_key']:
                ge=e[0]!=x;_,qe,_=BE.splay(x,False)
                if ge:ce=(x,)+tuple(y for y in ce if y!=x)
        az,bz,ez=map(tup,(A.snapshot(),BF.snapshot(),BE.snapshot()))
        assert (az,bz,ez)==tuple(tup(r[k]) for k in ('A_after','BF_after','BE_after'))
        assert (h,q,qe,gf,ge,cf,ce)==(r['a'],r['qF'],r['qE'],r['genuine_F'],r['genuine_E'],tuple(r['chart_F']),tuple(r['chart_E']))
        if i>=start:Acount+=h;QF+=q;QE+=qe
        if r['t']==src['target_t']:
            assert i==start and (h,q)==(1,5) and [ev['pattern'] for ev in bv]==['RR']*5
            assert phi(a,b,C)==9 and phi(az,b,C)==10 and phi(az,bz,C)==9
            drops=[sum(phi(az,tup(z['before']),C)-phi(az,tup(z['after']),C) for z in ev['rotations']) for ev in bv]
            assert drops==[0,0,0,0,1]
    cuts.append(tuple(map(tup,(A.snapshot(),BF.snapshot(),BE.snapshot())))+(cf,ce,))
    assert cuts[0]==cuts[1] and (Acount,QF,QE)==(27,11,12)
    assert full[-1]['genuine_F'] and full[-1]['a']==0 and full[-1]['key']==1
    assert {r['key'] for r in full[start:] if r['genuine_F']}==C
    t=src['target_t'];demands=[(t,j) for j,x in enumerate(drops,1) if x==0];bits=[(t,1,b) for b in (0,1)]
    assert demands==[tuple(x) for x in src['target_macro']['neutral_demand_ids']]
    assert bits==[tuple(x) for x in src['target_macro']['candidate_local_neighborhood']]
    assert len(demands)-len(bits)==2
    # Reuse AF full closure and A source events; annotate its new M projection.
    ap=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json';old=json.loads(ap.read_text())
    ann=json.loads((F/'independent_core_sector_neutral.json').read_text())
    assert ann['input_sha256'][str(ap)]==sha(ap)
    af=next(z for z in ann['controls'] if z['source']=='AF');C=set(af['M'])
    assert set(af['S'])==set(old['physical_keys'])
    rows=old['period_rows'];ends=[i for i,r in enumerate(rows) if r['genuine_F']]
    macros=[];h0={};decreases=[]
    for k,end in enumerate(ends):
        a=(ends[k-1]+1)%len(rows);seg=rows[a:end+1] if a<=end else rows[a:]+rows[:end+1]
        r=seg[-1];bf=tup(r['BF_before']);aa=tup(r['A_after']);z=V.Mutable(bf);_,q,ev=z.splay(r['key'],True)
        assert q==r['qF'] and tup(z.snapshot())==tup(r['BF_after'])
        for e in ev:
            ds=[phi(aa,tup(v['before']),C)-phi(aa,tup(v['after']),C) for v in e['rotations']]
            assert all(d in (0,1) for d in ds)
            if len(ds)==2:assert sum(ds)>0;decreases.append((r['t'],e['j'],sum(ds)))
        units=[(v['t'],j,b) for v in seg for j in range(1,v['a']+1) for b in (0,1)]
        dd=[(r['t'],j) for j in range(1,q+1)];h0.update(zip(dd,units))
        ps=phi(tup(seg[0]['A_before']),tup(seg[0]['BF_before']),C);pt=phi(aa,tup(r['BF_after']),C)
        assert len(units)-q-(pt-ps)>=0
        macros.append({'before':ps,'after':pt,'units':units,'demands':dd,'end_t':r['t']})
    saved={tuple(z['demand']):tuple(z['unit']) for z in old['funding']['h0']};assert saved==h0
    mn=min(m['after'] for m in macros);ends=[j for j,m in enumerate(macros) if m['after']==mn]
    fullh={};release=set();visits=set();trace=[];working=0
    for k,end in enumerate(ends):
        a=(ends[k-1]+1)%len(macros);group=macros[a:end+1] if a<=end else macros[a:]+macros[:end+1]
        assert group[0]['before']==group[-1]['after']==mn
        units=[u for m in group for u in m['units']];dd=[d for m in group for d in m['demands']]
        assert len(units)>=len(dd)
        inv={h0[d]:d for d in dd if d in h0};missing=collections.deque(d for d in dd if d not in h0)
        trace0=[]
        for j in range(0,len(units),2):
            pair=units[j:j+2];assert pair[0][:2]==pair[1][:2] and not visits.intersection(pair)
            visits.update(pair);free=[]
            for u in pair:
                if u in inv:d=inv[u];assert d not in fullh;fullh[d]=u
                else:free.append(u)
            working=max(working,len(free))
            for u in free:
                if missing:d=missing.popleft();assert d not in fullh;fullh[d]=u
                else:release.add(u)
            trace0.append({'actual_event':pair[0][:2],'free_peak':len(free),'after_event_bank':0})
        assert not missing
        trace.append({'macros':[m['end_t'] for m in group],'H':len(units)//2,'Q':len(dd),'trace':trace0})
    assert len(fullh)==len(decreases)==36 and len(saved)==32 and working<=2
    assert set(fullh.values()).isdisjoint(release) and set(fullh.values())|release==visits
    assert len(visits)==2*old['A'] and len(set(fullh.values()))==len(fullh)
    assert all(fullh[d]==u for d,u in saved.items())
    report={'status':'PASS_PC35_ORIGINAL_PAIRED_CLOSED_CONTROL_AND_AF_PROJECTED_FUNDING',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'closed_counter_control':{'period':src['period'],'A':Acount,'QF':QF,'QE':QE,'target_t':t,
        'B_double_decreases':drops,'neutral_demand_cut':demands,'exact_local_neighborhood':bits,
        'deficiency_in_double_specific_relation':2,'signed_margin':-3,
        'access_level_slot_cap':1,'access_level_max_funding_in_macro':3,
        'full_A_B_E_chart_closure':True,'CD_counterexample':False},
      'AF_alternative_independent_comparison':{'old_h0_preserved':len(saved),'full_demand_count':len(fullh),
        'B0':0,'B1':sum(x[2]==1 for x in decreases),'B2':sum(x[2]==2 for x in decreases),
        'working_bound_observed':working,'actual_period':af['period'],'groups':trace,
        'assignment':[{'demand':d,'unit':u} for d,u in sorted(fullh.items())],
        'historical_comparisons_replaced':False,'additional_fE_lock_compatibility_claimed':False},
      'JR35':'OPEN','reservation':'DEFERRED',
      'input_sha256':{str(p):sha(p) for p in [path,ap,F/'PROJECTED_CLUSTER_ACCESS_THEOREM.md',F/'independent_core_sector_neutral.json']}}
    with (F/'independent_projected_cluster_theorem.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({'status':report['status'],'source_queries':V.CALLS,'counter':report['closed_counter_control'],
      'AF':{k:v for k,v in report['AF_alternative_independent_comparison'].items() if k not in ('groups','assignment')}}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_verify126_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
