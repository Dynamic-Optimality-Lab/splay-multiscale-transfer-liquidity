"""Independent marked-fringe and return-channel checks on accepted traces.

Uniform conclusions use the written marked-parent/shrinkage proof.
No new source engine or bounded-population lifting premise is used.
"""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def anc(t,y,x):
    while t[0]!=x:
        if t[0]==y:return True
        t=t[1] if x<t[0] else t[2]
    return False
def subtree(t,y):
    while t[0]!=y:t=t[1] if y<t[0] else t[2]
    return t
def keys(t):return set() if t is None else keys(t[1])|{t[0]}|keys(t[2])
def main():
    mp=F/'marked_demotion_relation.json';m=json.loads(mp.read_text());pins=[mp,F/'MAXIMAL_SELF_FRINGE_RETURN_THEOREM.md'];reports=[]
    for p,h in m['input_sha256'].items():assert sha(Path(p))==h
    for control in m['controls']:
        p=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json' if control['source']=='AF' else F/'cluster_collateral_closed_source.json'
        pins.append(p);rows=json.loads(p.read_text())['period_rows'];by={r['t']:i for i,r in enumerate(rows)};n=len(rows)
        M={r['key'] for r in rows if r['genuine_F']};r=len(M);groups=collections.defaultdict(list);macs=collections.defaultdict(list)
        for d in control['source_demands']:
            u=tuple(d['loss_rotations'][0]);groups[u].append(d);macs[d['demand'][0]].append(d)
        for t,ds in macs.items():
            sets=[keys(subtree(rows[by[t]]['BF_after'],d['G']))&M for d in ds]
            for i,a in enumerate(sets):
                for b in sets[i+1:]:assert not a&b
        selfs=[]
        for u,ds in groups.items():
            ds.sort(key=lambda a:(by[a['demand'][0]]-by[u[0]])%n)
            assert len({d['x'] for d in ds})==len(ds)
            for d,d2 in zip(ds,ds[1:]):
                t=d['demand'][0];x=d['x'];g=d['G'];z=d2['x'];contact=d2['demand'][0]
                fringe=keys(subtree(rows[by[t]]['BF_after'],g))&M
                assert z in fringe-{g} and z!=x
                reset=next(rows[(by[t]+j)%n]['t'] for j in range(1,n+1) if rows[(by[t]+j)%n]['genuine_F'] and rows[(by[t]+j)%n]['key']==g)
                assert 0<(by[contact]-by[t])%n<(by[reset]-by[t])%n
                donor=None
                for j in range(1,(by[reset]-by[contact])%n+1):
                    row=rows[(by[contact]+j)%n]
                    for ev in row['A_events']:
                        for rot in ev['rotations']:
                            if anc(rot['before'],z,g) and not anc(rot['after'],z,g):
                                assert rot['pivot']==z;donor=(row['t'],ev['j'],rot['bit']);break
                        if donor:break
                    if donor:break
                assert donor is not None
                selfs.append({'demand':d['demand'],'consumer':t,'x':x,'old_proxy':g,'contact':contact,'z':z,'reset':reset,'bit':donor})
        cgroups=collections.defaultdict(list);ggroups=collections.defaultdict(list);owners=collections.defaultdict(list)
        for a in selfs:cgroups[a['consumer']].append(a);ggroups[a['old_proxy']].append(a);owners[a['bit']].append(a)
        bounds=[]
        for t,ss in cgroups.items():
            oldG={d['G'] for d in macs[t]};zs={d['z'] for d in ss};q=len(macs[t])
            assert len(zs)==len(ss) and not zs&oldG and len(ss)+q<=r-1
            assert len({d['bit'] for d in ss})==len(ss)
            bounds.append({'consumer':t,'Q':q,'SELF':len(ss),'r_minus_1':r-1})
        for g,ss in ggroups.items():assert len({d['bit'] for d in ss})==len(ss)
        crossed=[]
        for u,ss in owners.items():
            if len(ss)<2:continue
            assert len({d['consumer'] for d in ss})==len(ss) and len({d['old_proxy'] for d in ss})==len(ss)
            assert len({d['z'] for d in ss})==1
            crossed.append({'bit':u,'claims':ss})
        reports.append({'source':control['source'],'r':r,'SELF_claims':len(selfs),'fringe_bounds':bounds,
          'per_consumer_injection':True,'per_old_proxy_key_injection':True,'crossed_return_collisions':crossed,'return_map':selfs})
    pins += [P/'SE03_STEP2_DONOR05/CLOSED_MAXIMAL_SAME_SIDE.md',P/'SE03_STEP2_DONOR05/MARKED_PARENT_PROJECTION.md',F/'audit_MFR35_theorem.py']
    out={'status':'PASS_UNIFORM_MFR35_PROOF_AND_STORED_SOURCE_IDENTITIES',
      'uniform_review':['actual post-consumer marked-parent children; disjoint full rooted subtrees',
        'old proxy shrinkage before its next genuine reset; contacts proper and distinct',
        'q+SELF<=r-1 by original marked labels, not abstract edge count',
        'real A root contact-to-reset loss with pivot z and one-period event IDs',
        'per-consumer different pivots; per-proxy tenure disjointness over all repetitions',
        'crossed channels and raw/frozen owners explicitly remain unresolved'],
      'controls':reports,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','reservation':'DEFERRED',
      'independent_is_same_agent_distinct_implementation':True,'verification_boundary':'written proof inspection plus accepted-trace identities; not external/formal',
      'input_sha256':{str(p):sha(p) for p in pins}}
    with (F/'independent_MFR35_theorem.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'controls':[{k:v for k,v in a.items() if k not in ('return_map','crossed_return_collisions','fringe_bounds')} for a in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify152_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
