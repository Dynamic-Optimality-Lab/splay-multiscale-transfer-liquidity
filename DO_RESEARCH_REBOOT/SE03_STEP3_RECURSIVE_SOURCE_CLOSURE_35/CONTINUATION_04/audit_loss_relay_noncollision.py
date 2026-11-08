"""Check LR35 relay identities without rerunning accepted splay actions."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ancestor(t,y,x):
    while t[0]!=x:
        if t[0]==y:return True
        t=t[1] if x<t[0] else t[2]
    return False
def main():
    fp=F/'independent_fresh_proxy_loss.json';md=F/'marked_demotion_relation.json'
    fa,ma=(json.loads(p.read_text()) for p in (fp,md))
    results=[];pins=[fp,md,F/'LOSS_RELAY_NONCOLLISION.md']
    for name,p in [('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'),('CCR',F/'cluster_collateral_closed_source.json')]:
        assert fa['input_sha256'][str(p)]==sha(p);pins.append(p)
        rows=json.loads(p.read_text())['period_rows'];by={r['t']:i for i,r in enumerate(rows)};n=len(rows)
        def loss(s,t,y,x):
            assert y!=x and rows[by[s]]['A_after'][0]==y and rows[by[t]]['A_after'][0]==x
            for d in range(1,(by[t]-by[s])%n+1):
                r=rows[(by[s]+d)%n]
                for e in r['A_events']:
                    for a in e['rotations']:
                        if ancestor(a['before'],y,x) and not ancestor(a['after'],y,x):
                            assert a['pivot']==y
                            return (r['t'],e['j'],a['bit'])
            raise AssertionError('no actual relay rotation')
        f=next(z for z in fa['controls'] if z['source']==name)
        m=next(z for z in ma['controls'] if z['source']==name)
        groups=collections.defaultdict(list)
        for mac in f['macros']:
            for z in mac['proxies']:groups[tuple(z['actual_first_loss_bit'])].append((tuple(z['demand']),mac['target']))
        full_provisional=collections.defaultdict(list);lg=[]
        for u,ds in groups.items():
            ds.sort(key=lambda v:(by[v[0][0]]-by[u[0]])%n)
            assert len({x for _,x in ds})==len(ds)
            assigned=[(ds[0][0],u)]
            for ((d0,y),(d,x)) in zip(ds,ds[1:]):
                assigned.append((d,loss(d0[0],d[0],y,x)))
            assert len({v for _,v in assigned})==len(ds)
            for d,v in assigned:full_provisional[v].append(d)
            if len(ds)>1:lg.append({'shared_loss_bit':u,'relay_pairs':assigned})
        residual=[{'unit':u,'claims':v} for u,v in sorted(full_provisional.items()) if len(v)>1]
        usable=[d for d in m['source_demands'] if d['prior_genuine_G_t']<d['loss_rotations'][0][0]<=d['demand'][0]]
        bymacro=collections.defaultdict(dict)
        for d in usable:bymacro[d['demand'][0]][tuple(d['loss_rotations'][0])]=d
        ordered=sorted(bymacro);pair_tests=0;later=[];repeat=0
        for j,t in enumerate(ordered):
            earlier={}
            for s in ordered[:j]:
                common=set(bymacro[s])&set(bymacro[t]);assert len(common)<=1;pair_tests+=1
                for u in common:earlier.setdefault(u,bymacro[s][u])
            classes=collections.defaultdict(list)
            for u,d in earlier.items():classes[d['x']].append((d['demand'][0],d,u))
            relay=[]
            for y,owners in classes.items():
                owners.sort()
                for (s,d,u),(s1,d1,_) in zip(owners,owners[1:]):
                    v=next(r['t'] for r in reversed(rows) if s<r['t']<s1 and r['genuine_F'] and r['key']==d1['G'])
                    relay.append((u,loss(s,v,y,d1['G'])));repeat+=1
                s,d,u=owners[-1];relay.append((u,loss(s,t,y,rows[by[t]]['key'])))
            assert len({v for _,v in relay})==len(relay)==len(earlier)
            assert all(u[0]<v[0] for u,v in relay)
            if relay:later.append({'destination_t':t,'blocked_bit_and_relay_bit':relay})
        results.append({'source':name,'FP_collision_groups':lg,'cross_group_or_singleton_collisions':residual,
          'nonwrap_MD_macro_pair_checks':pair_tests,'destination_relay_controls':later,
          'repeated_MD_owner_reset_controls':repeat,
          'h0_or_fE_mutated':False,'new_universal_license_claimed':False})
    report={'status':'PASS_LR35_LOCAL_RELAY_IDENTITIES',
      'source_queries':0,'source_engine_calls':0,'controls':results,
      'independent_scope':'same-agent separate identity checker; universal statements use the written source proof',
      'JR35':'OPEN','reservation':'DEFERRED','input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'independent_loss_relay_noncollision.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({'status':report['status'],'controls':[{'source':r['source'],'groups':len(r['FP_collision_groups']),
      'cross_group_or_singleton_collisions':len(r['cross_group_or_singleton_collisions']),
      'MD_macro_pairs':r['nonwrap_MD_macro_pair_checks'],'destinations':len(r['destination_relay_controls']),
      'repeated_owner_resets':r['repeated_MD_owner_reset_controls']} for r in results],'JR35':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify132_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
