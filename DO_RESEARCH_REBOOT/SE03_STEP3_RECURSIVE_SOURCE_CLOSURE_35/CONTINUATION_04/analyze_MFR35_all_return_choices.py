"""Separate a selector failure from the entire frozen return eligibility rule."""
import collections,hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def anc(t,y,x):
    while t[0]!=x:
        if t[0]==y:return True
        t=t[1] if x<t[0] else t[2]
    return False
def match(g):
    owners={};chosen={}
    def go(d,seen):
        for u in sorted(g[d]):
            if u in seen:continue
            seen.add(u)
            if u not in owners or go(owners[u],seen):owners[u]=d;chosen[d]=u;return True
        return False
    for d in sorted(g):go(d,set())
    S=set(g)-set(chosen);todo=list(S);N=set()
    while todo:
        d=todo.pop()
        for u in g[d]:
            N.add(u);assert u in owners
            if owners[u] not in S:S.add(owners[u]);todo.append(owners[u])
    assert len(S)-len(N)==len(g)-len(chosen)
    return chosen,{'demands':sorted(S),'neighborhood':sorted(N),'deficiency':len(S)-len(N)}
def main():
    mp=F/'marked_demotion_relation.json';rp=F/'independent_MFR35_theorem.json';md=json.loads(mp.read_text());ret=json.loads(rp.read_text());reports=[]
    for mc in md['controls']:
        name=mc['source'];rc=next(c for c in ret['controls'] if c['source']==name)
        path=B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json' if name=='AF' else F/'cluster_collateral_closed_source.json'
        rows=json.loads(path.read_text())['period_rows'];by={r['t']:i for i,r in enumerate(rows)};n=len(rows)
        groups=collections.defaultdict(list);allgraph={};fresh={};details=[]
        for d in mc['source_demands']:groups[tuple(d['loss_rotations'][0])].append(d)
        for u,ds in groups.items():
            ds.sort(key=lambda a:(by[a['demand'][0]]-by[u[0]])%n);d=tuple(ds[-1]['demand'])
            allgraph[d]={(u[0],u[1],b) for b in (0,1)};fresh[d]=u
        for a in rc['return_map']:
            d=tuple(a['demand']);contact=a['contact'];reset=a['reset'];z=a['z'];g=a['old_proxy'];length=(by[reset]-by[contact])%n
            rr=[rows[(by[contact]+j)%n] for j in range(1,length+1)]
            latest=contact
            for row in rr:
                if row['genuine_F'] and row['key']==z:latest=row['t']
            options=[];freshbit=None
            for row in rr:
                for ev in row['A_events']:
                    for rot in ev['rotations']:
                        if anc(rot['before'],z,g) and not anc(rot['after'],z,g):
                            assert rot['pivot']==z;bit=(row['t'],ev['j'],rot['bit']);options.append(bit)
                            if freshbit is None and (by[row['t']]-by[contact])%n>(by[latest]-by[contact])%n:freshbit=bit
            assert options and freshbit is not None;allgraph[d]={(t,j,b) for t,j,_ in options for b in (0,1)};fresh[d]=freshbit
            details.append({**a,'last_genuine_contact_key_before_reset':latest,'all_return_rotation_bits':options,'fresh_tenure_first_bit':freshbit})
        assert len(allgraph)==len(fresh)==mc['Q'];chosen,cut=match(allgraph);load=collections.Counter(u[:2] for u in fresh.values())
        reports.append({'source':name,'Q':mc['Q'],'all_return_event_pool_matching_size':len(chosen),'all_return_cut':cut,
          'matching':[{'demand':d,'unit':u} for d,u in sorted(chosen.items())],
          'fresh_tenure_event_load_peak':max(load.values()),'return_options':details,
          'pools':[{'demand':d,'units':sorted(us)} for d,us in sorted(allgraph.items())]})
    out={'status':'EXACT_COMPLETE_RETURN_OPTION_CONTROL_ANALYSIS','controls':reports,'source_queries':0,'source_engine_calls':0,
      'frozen_initial_DIRECT_groups':'MD first-loss groups, last owner; no group was patched',
      'return_eligibility':'all actual z->G losses after original next-group contact before original next genuine G; both actual event units',
      'source_ops_and_h0_fE_unchanged':True,'JR35':'OPEN','finite_controls_not_universal':True,
      'input_sha256':{str(p):sha(p) for p in (mp,rp,F/'analyze_MFR35_all_return_choices.py')}}
    with (F/'MFR35_all_return_options.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'controls':[{k:v for k,v in a.items() if k in ('source','Q','all_return_event_pool_matching_size','all_return_cut','fresh_tenure_event_load_peak')} for a in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof290_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
