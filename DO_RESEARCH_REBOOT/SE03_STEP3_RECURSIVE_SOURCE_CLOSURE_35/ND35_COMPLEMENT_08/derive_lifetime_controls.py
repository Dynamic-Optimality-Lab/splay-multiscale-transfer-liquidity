"""New exact cluster-lifetime annotations of already accepted closed sources.

Old A fine traces are reused. Missing fine B traces are materialized only
for the new annotation; all such ordinary source evaluations are charged.
No old search, closure audit, or fixed-population proof is rerun.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;O=C/'CONTINUATION_04';B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def labels(t,S):
    result=set()
    def go(v):
        if v is None:return frozenset()
        q=go(v[1])|go(v[2])|({v[0]} if v[0] in S else set())
        if q:result.add(frozenset(q))
        return q
    go(t);return result
def core(t,M):
    out=set()
    def go(v):
        if v is None:return False
        a,b=go(v[1]),go(v[2]);yes=a or b or v[0] in M
        if yes:out.add(v[0])
        return yes
    go(t);return out
def serial(Z):return sorted([sorted(x) for x in Z])
def main():
    global V
    receipt=O/'independent_core_sector_neutral.json';accepted=json.loads(receipt.read_text())
    paths=[('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'),('CCR',O/'cluster_collateral_closed_source.json'),('NONMAX',O/'maximal_completion_original_source.json')]
    for _,p in paths:assert accepted['input_sha256'][str(p)]==sha(p)
    spec=importlib.util.spec_from_file_location('ND_lifetime_new_B_details',B/'audit_core39.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    sources=[(name,json.loads(p.read_text())['period_rows']) for name,p in paths];known={};reused=0
    for name,rows in sources:
        for r in rows:
            if 'A_events' in r:known[(tup(r['A_before']),r['key'])]=(tup(r['A_after']),r['A_events'])
    reports=[]
    for name,rows in sources:
        M={r['key'] for r in rows if r['genuine_F']};S=core(tup(rows[0]['BF_before']),M)
        assert rows[0]['A_before']==rows[-1]['A_after'] and rows[0]['BF_before']==rows[-1]['BF_after']
        U={(r['t'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)};D={(r['t'],j) for r in rows for j in range(1,r['qF']+1)}
        fine=[];nonneutral=set();neutral=set();Pbits=set();release_counts=collections.Counter();B2=0
        def add(before,after,kind,r,ev,rot,demand=None,neutral_double=False,slot=None):
            removed=before-after;added=after-before
            assert len(removed)<=1 and len(added)<=1
            if kind=='B':assert len(removed)==1 and len(added) in (0,1)
            index=len(fine);unit=(r['t'],ev['j'],rot['bit']) if kind=='A' else None
            fine.append({'index':index,'before_missing':serial(before),'after_missing':serial(after),'removed':serial(removed),'added':serial(added),
              'kind':kind,'t':r['t'],'access_key':r['key'],'event_j':ev['j'],'rotation_bit':rot['bit'],'pattern':ev['pattern'],'pivot':rot['pivot'],
              'unit':unit,'demand':demand,'neutral_double':neutral_double,'slot':slot})
            if kind=='A' and len(added)>len(removed):Pbits.add(unit)
        for r in rows:
            bf=tup(r['BF_before']);aa=tup(r['A_after'])
            if 'A_events' in r:ae=r['A_events']
            else:
                out,h,_,ae=V.splay(tup(r['A_before']),r['key'],True);assert out==aa and h==r['a'];known[(tup(r['A_before']),r['key'])]=(out,ae)
            for ev in ae:
                for rot in ev['rotations']:
                    before=labels(bf,S)-labels(tup(rot['before']),S);after=labels(bf,S)-labels(tup(rot['after']),S)
                    slot='A_RELEASE' if len(after)<len(before) else None
                    release_counts['A_RELEASE']+=int(slot is not None);add(before,after,'A',r,ev,rot,slot=slot)
            if r['qF'] or (r['kind']=='K' and bf[0]!=r['key']):
                key=(bf,r['key'])
                if key in known:out,be=known[key];reused+=1
                else:
                    out,_,_,be=V.splay(bf,r['key'],True);known[key]=(out,be)
                assert out==tup(r['BF_after']);di=0
                for ev in be:
                    isdouble=len(ev['pattern'])==2;d=(r['t'],di+1) if isdouble else None
                    changes=[(labels(tup(z['before']),S)-labels(aa,S),labels(tup(z['after']),S)-labels(aa,S),z) for z in ev['rotations']]
                    drops=sum(len(a)-len(b) for a,b,_ in changes);assert drops in ((0,1,2) if isdouble else (0,1))
                    if isdouble:
                        (nonneutral if drops else neutral).add(d);B2+=int(drops==2);di+=1
                    first=True
                    for a,b,z in changes:
                        assert len(a)-len(b) in (0,1);slot=None
                        if len(a)>len(b):
                            slot='PAYMENT' if isdouble and first else ('B2_RELEASE' if isdouble else 'BZIG_RELEASE');first=False
                            release_counts[slot]+=1
                        add(a,b,'B',r,ev,z,demand=d,neutral_double=isdouble and drops==0,slot=slot)
                assert di==r['qF']
            else:assert r['qF']==0
            assert time.process_time()-START<CAP-3
        assert neutral|nonneutral==D and not neutral&nonneutral
        assert fine and all(fine[i]['after_missing']==fine[i+1]['before_missing'] for i in range(len(fine)-1)) and fine[-1]['after_missing']==fine[0]['before_missing']
        initial=[tuple(x) for x in fine[0]['before_missing']];fragments=[];live={}
        def new(label,birth=None):
            j=len(fragments);fragments.append({'id':j,'initial_label':label,'birth':birth,'steps':[],'end':None,'next':None});live[label]=j;return j
        seam={l:new(l) for l in initial};step_fragment={}
        for f in fine:
            rem=[tuple(x) for x in f['removed']];additions=[tuple(x) for x in f['added']]
            if not rem and not additions:continue
            if rem:
                j=live.pop(rem[0]);fragments[j]['steps'].append(f['index']);step_fragment[f['index']]=j
                if additions:live[additions[0]]=j
                else:fragments[j]['end']=f['index']
            else:
                assert f['kind']=='A' and f['unit'] is not None;j=new(additions[0],f['unit']);fragments[j]['steps'].append(f['index']);step_fragment[f['index']]=j
        assert set(live)==set(initial)
        for label,j in live.items():fragments[j]['next']=seam[label]
        components=[];assigned=set();g_life={};released=set();frag_component={}
        def traverse(start):
            ids=[];j=start
            while j is not None and j not in ids:
                assert j not in assigned;ids.append(j);assigned.add(j);j=fragments[j]['next']
            cyclic=j is not None
            assert not cyclic or j==start
            steps=[i for k in ids for i in fragments[k]['steps']];cid=len(components)
            for k in ids:frag_component[k]=cid
            birth=fragments[start]['birth'];end=fragments[ids[-1]]['end']
            assert (birth is None and end is None) if cyclic else (birth is not None and end is not None)
            if not cyclic:
                u=tuple(birth);slot=fine[end]['slot'];assert u in Pbits
                if slot=='PAYMENT':d=tuple(fine[end]['demand']);assert d not in g_life;g_life[d]=u
                else:assert slot in ('A_RELEASE','B2_RELEASE','BZIG_RELEASE');released.add(u)
            neutral_steps=[i for i in steps if fine[i]['neutral_double']]
            Atransfers=[i for i in steps if fine[i]['kind']=='A' and fine[i]['removed'] and fine[i]['added']]
            components.append({'id':cid,'cyclic':cyclic,'fragments':ids,'seam_crossings':sum(fragments[j]['next'] is not None for j in ids),
              'birth_unit':birth,'death_step':end,'steps':steps,'neutral_steps':neutral_steps,'A_transfer_steps':Atransfers,
              'B_only_neutral_cycle':cyclic and bool(neutral_steps) and not Atransfers})
        for j,f in enumerate(fragments):
            if f['birth'] is not None:traverse(j)
        for j in range(len(fragments)):
            if j not in assigned:traverse(j)
        assert len(assigned)==len(fragments) and set(g_life)==nonneutral and len(set(g_life.values()))==len(g_life)
        R=(U-Pbits)|released;assert not R&set(g_life.values()) and R|set(g_life.values())==U
        incidence=[]
        for d in sorted(neutral):
            ii=[f['index'] for f in fine if f['neutral_double'] and tuple(f['demand'])==d];assert len(ii)==2
            assert step_fragment[ii[0]]!=step_fragment[ii[1]],'same live strand cannot move twice in one B access'
            cc=[frag_component[step_fragment[i]] for i in ii]
            incidence.append({'demand':d,'steps':ii,'components':cc,'same_global_component':cc[0]==cc[1]})
        old=next(x for x in accepted['controls'] if x['source']==name)
        assert len(neutral)==old['B0'] and len(nonneutral)==old['B1']+old['B2'] and len(Pbits)==old['P']
        assert len(R)-len(neutral)==2*sum(r['a'] for r in rows)-len(D)
        reports.append({'source':name,'source_path':str(dict(paths)[name]),'M':sorted(M),'S':sorted(S),'fine_steps':fine,
          'U':sorted(U),'D':sorted(D),'D0':sorted(neutral),'Dplus':sorted(nonneutral),'birth_bits':sorted(Pbits),
          'g_life':[{'demand':d,'unit':u} for d,u in sorted(g_life.items())],'R_life':sorted(R),'fragments':fragments,'components':components,'neutral_incidences':incidence,
          'B_only_neutral_cycles':sum(c['B_only_neutral_cycle'] for c in components),'same_global_component_doubles':sum(d['same_global_component'] for d in incidence),
          'old_owners_modified':False,'Objective_I':'OPEN','Objective_II':'DEFERRED'})
    out={'status':'NEW_EXACT_LIFETIME_SOURCE_ANNOTATIONS','controls':reports,'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'old_fine_primitives_reused':reused,
      'not_a_universal_proof_by_controls':True,'input_sha256':{str(p):sha(p) for p in [receipt]+[p for _,p in paths]+[F/'SOURCE_SPEC.md',F/'ND35_UNIVERSAL_AUDIT.md',F/'LIFETIME_NORMAL_FORM.md',F/'derive_lifetime_controls.py']}}
    with (F/'lifetime_controls.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({'status':out['status'],'source_queries':V.CALLS,'controls':[{'source':r['source'],'D0':len(r['D0']),'paths':sum(not c['cyclic'] for c in r['components']),'cycles':sum(c['cyclic'] for c in r['components']),'B_only_cycles':r['B_only_neutral_cycles'],'same_component_doubles':r['same_global_component_doubles']} for r in reports]}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/'audit_core78_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
