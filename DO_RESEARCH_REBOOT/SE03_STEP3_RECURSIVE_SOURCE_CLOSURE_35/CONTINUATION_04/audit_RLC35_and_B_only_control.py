"""New reverse-relay identities reuse accepted source rotations.

The eight B-only control operations are separately replayed by Mutable.
No full historical verifier or old full-source graph audit is repeated.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def anc(t,y,x):
    while t[0]!=x:
        if t[0]==y:return True
        t=t[1] if x<t[0] else t[2]
    return False
def main():
    global V
    fp=F/'independent_fresh_proxy_loss.json';fa=json.loads(fp.read_text());pins=[fp,F/'REVERSE_LOSS_COLLISION_NORMAL_FORM.md'];reports=[]
    for name,p in [('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'),('CCR',F/'cluster_collateral_closed_source.json')]:
        assert fa['input_sha256'][str(p)]==sha(p);pins.append(p)
        rows=json.loads(p.read_text())['period_rows'];n=len(rows);by={r['t']:i for i,r in enumerate(rows)}
        M={r['key'] for r in rows if r['genuine_F']};ends=[i for i,r in enumerate(rows) if r['genuine_F']]
        rotations={};inventory=set();reserve=set();h0={}
        for r in rows:
            for e in r['A_events']:
                for b in (0,1):inventory.add((r['t'],e['j'],b))
                have=set()
                for z in e['rotations']:
                    u=(r['t'],e['j'],z['bit']);rotations[u]=z;have.add(z['bit'])
                    if z['pivot'] not in M:reserve.add(u)
                for b in {0,1}-have:reserve.add((r['t'],e['j'],b))
        def arc(s,t):return [rows[(by[s]+j)%n] for j in range(1,(by[t]-by[s])%n+1)]
        for j,end in enumerate(ends):
            start=ends[j-1];mac=[rows[(start+k)%n] for k in range(1,(end-start)%n+1)]
            units=[(r['t'],e['j'],b) for r in mac for e in r['A_events'] for b in (0,1)]
            for k,u in enumerate(units[:rows[end]['qF']],1):h0[u]=(rows[end]['t'],k)
        def first_loss(s,t,y,x):
            assert rows[by[s]]['A_after'][0]==y and rows[by[t]]['A_after'][0]==x and y!=x
            for r in arc(s,t):
                for e in r['A_events']:
                    for z in e['rotations']:
                        if anc(z['before'],y,x) and not anc(z['after'],y,x):
                            assert z['pivot']==y;return (r['t'],e['j'],z['bit'])
            raise AssertionError('missing original root-contact loss')
        control=next(z for z in fa['controls'] if z['source']==name);groups=collections.defaultdict(list)
        for mac in control['macros']:
            for d in mac['proxies']:
                u=tuple(d['actual_first_loss_bit']);assert rotations[u]['pivot']==d['tag'][1]
                groups[u].append((tuple(d['demand']),mac['target'],d['tag'][1]))
        assigned=[]
        for u,ds in groups.items():
            ds.sort(key=lambda a:(by[a[0][0]]-by[u[0]])%n);assert len({a[1] for a in ds})==len(ds)
            local=[]
            for (d,x,y),(d2,x2,y2) in zip(ds,ds[1:]):
                v=first_loss(d[0],d2[0],x,x2);local.append({'demand':d,'key':x,'type':'SELF','bit':v,'pivot':x,'next_consumer':d2[0]})
            d,x,y=ds[-1];local.append({'demand':d,'key':x,'type':'DIRECT','bit':u,'pivot':y})
            assert len({a['bit'] for a in local})==len(ds);assigned+=local
        assert len(assigned)==control['Q'] and len({a['demand'] for a in assigned})==len(assigned)
        owners=collections.defaultdict(list)
        for a in assigned:
            assert a['bit'] in inventory and a['bit'] not in reserve and rotations[a['bit']]['pivot']==a['pivot']
            owners[a['bit']].append(a)
        same=forward=0;collisions=[];h0forward=0
        for u,aa in owners.items():
            direct=[a for a in aa if a['type']=='DIRECT'];selfs=[a for a in aa if a['type']=='SELF'];assert len(direct)<=1
            assert len({a['key'] for a in selfs})<=1
            if len(selfs)>1:same+=1
            if direct and selfs:
                for a in selfs:
                    d=direct[0];assert d['pivot']==a['key'] and d['key']!=a['key']
                    left=(by[u[0]]-by[a['demand'][0]])%n;right=(by[d['demand'][0]]-by[u[0]])%n
                    assert left>0 and left+right<n;forward+=1
            for a in selfs:
                if u in h0:
                    assert (by[h0[u][0]]-by[a['demand'][0]])%n>0;h0forward+=1
            if len(aa)>1:collisions.append({'unit':u,'claims':aa})
        reports.append({'source':name,'demands':len(assigned),'direct_groups':len(groups),'SELF_claims':sum(a['type']=='SELF' for a in assigned),
          'same_key_SELF_collision_units':same,'forward_DIRECT_SELF_pairs':forward,'forward_SELF_h0_checks':h0forward,
          'raw_unmarked_or_virtual_reserve_units':len(reserve),'collisions':collisions,'raw_assignment':assigned,
          'h0_or_fE_mutated':False})
    # Exact countercontrol to the new B-only two-per-macro route.
    rp=F/'maximal_B_only_bound_result.json';res=json.loads(rp.read_text());w=res['witness'];assert w['Q']==22 and w['genuine_macros']==8
    gp=F/'maximal_B_grammar.json';model=json.loads(gp.read_text());trees=[tup(t) for t in model['trees']]
    sp=importlib.util.spec_from_file_location('B_only_distinct_control',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    initial=trees[w['B_edges'][0]['source']];b=V.Mutable(initial);actual=[];marks=set(w['keys_used'])
    def in_core(t):
        keys=set()
        for x in marks:
            u=t
            while True:
                keys.add(u[0])
                if u[0]==x:break
                u=u[1] if x<u[0] else u[2]
        return keys
    for e in w['B_edges']:
        before=tup(b.snapshot());assert before==trees[e['source']] and in_core(before)==set(range(1,14))
        h,q,events=b.splay(e['key'],True);assert q==e['q'] and h==q and all(z['pattern'] in ('LL','RR') for z in events)
        assert tup(b.snapshot())==trees[e['target']]
        actual.append({'KEEP':e['key'],'before':before,'after':tup(b.snapshot()),'H_when_A_equals_B':h,'Q':q,'events':events})
    assert tup(b.snapshot())==initial and marks==set(range(1,14,2))
    # Reach the literal initial B from the ordinary right-vine diagonal using
    # the accepted full source edge table, without another semantic replay.
    bp=F/'active_a10_model.json';tab=json.loads(bp.read_text());out=collections.defaultdict(list)
    for e in tab['B_edges']:out[e['source']].append(e)
    vine=None
    for k in range(13,0,-1):vine=(k,None,vine)
    start=trees.index(vine);target=w['B_edges'][0]['source'];todo=collections.deque([start]);prev={start:None}
    while todo and target not in prev:
        s=todo.popleft()
        for e in out[s]:
            t=e['target']
            if t not in prev:prev[t]=(s,e['key']);todo.append(t)
    assert target in prev;prefix=[];v=target
    while v!=start:v,x=prev[v];prefix.append(x)
    prefix.reverse()
    pins += [rp,gp,bp,F/'audit_RLC35_and_B_only_control.py',P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md']
    result={'status':'PASS_UNIFORM_RLC35_IDENTITIES_AND_EXACT_B_ONLY_SOURCE_COUNTERCONTROL',
      'RLC_controls':reports,'B_only_countercontrol':{'initial_A_and_B':initial,'source_prefix_from_right_vine':prefix,
        'word':[e['KEEP'] for e in actual],'source_rows':actual,'genuine_support':sorted(marks),'full_core':13,
        'Q':22,'A':22,'Q_minus_2_genuine_macros':6,'original_CD_margin_2A_minus_Q':22,
        'full_A_B_closure':'literal; A=B source invariant at every operation',
        'erased_chart_closure':'accepted actual finite recurrence after warmup on repeated literal word; numeric u,L not newly replayed',
        'claim':'B-only Q<=2 macro bound REFUTED; not Coarse-Double or JR35'},
      'uniform_proof_review':'common proxy tenure; earlier-to-next actual root-loss; distinct within each group; all collision type/pivot and time implications; raw reserve exclusion; cyclic seam caveat',
      'RLC_universal_joint_injection':'NOT_PROVED','JR35':'OPEN','reservation':'DEFERRED',
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'independent_is_same_agent_distinct_implementation':True,
      'input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'independent_RLC35_and_B_only_control.json').open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    print(json.dumps({'status':result['status'],'RLC_controls':[{k:v for k,v in r.items() if k not in ('collisions','raw_assignment')} for r in reports],
      'B_only_word':result['B_only_countercontrol']['word'],'Q':22,'A':22,'source_queries':V.CALLS}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/'audit_verify151_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
