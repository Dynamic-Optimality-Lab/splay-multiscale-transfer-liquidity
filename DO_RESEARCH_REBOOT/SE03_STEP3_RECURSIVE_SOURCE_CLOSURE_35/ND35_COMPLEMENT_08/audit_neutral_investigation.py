"""Independent lifetime graph, terminal-release proof and exact-source challenges.

Old source audits are reused by their exact receipts. New source controls
are checked with the distinct mutable implementation. Not external/formal
verification, and no finite controls prove a universal donor theorem.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;O=C/'CONTINUATION_04';B=C.parent/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def labels(t):
    out=set()
    def go(v):
        if v is None:return frozenset()
        a=go(v[1])|go(v[2])|{v[0]};out.add(a);return a
    go(t);return out
def left(t):
    p,a,u=t;x,b,c=u;return (x,(p,a,b),c)
def right(t):
    p,u,c=t;x,a,b=u;return (x,a,(p,b,c))
def main():
    global V
    names=['lifetime_controls.json','root_entry_graph_controls.json','terminal_neutral_controls.json','terminal_complement_graph_controls.json','control_complete_complements.json','exact_challenge_sources.json','zig_release_complement_controls.json']
    data={n:json.loads((F/n).read_text()) for n in names}
    for r in data.values():
        for p,h in r['input_sha256'].items():assert sha(Path(p))==h
    prior=json.loads((O/'independent_core_sector_neutral.json').read_text());component_reports=[]
    for r in data['lifetime_controls.json']['controls']:
        fine=r['fine_steps'];n=len(fine);Z=[{tuple(v) for v in f['before_missing']} for f in fine];vertices={(i,L) for i in range(n) for L in Z[i]};nxt={};prev={};birth={};death={};Bneutral_edges={};Atransfer=set()
        def edge(a,b):assert a not in nxt and b not in prev;nxt[a]=b;prev[b]=a
        old=next(x for x in prior['controls'] if x['source']==r['source']);profile={}
        for p in old['cyclic_level_pairings']:
            profile[p['positive_source_step']]=1;profile[p['decrease_source_step']]=-1
        for i,f in enumerate(fine):
            q=(i+1)%n;new={tuple(v) for v in f['after_missing']};assert new==Z[q]
            gone=Z[i]-new;added=new-Z[i];assert gone=={tuple(x) for x in f['removed']} and added=={tuple(x) for x in f['added']}
            assert len(added)-len(gone)==profile.get(i,0)
            for L in Z[i]&new:edge((i,L),(q,L))
            if gone and added:
                a,b=(i,next(iter(gone))),(q,next(iter(added)));edge(a,b)
                if f['kind']=='A':Atransfer.add(a)
                elif f['neutral_double']:Bneutral_edges[a]=tuple(f['demand'])
            elif added:assert f['kind']=='A';birth[(q,next(iter(added)))]=tuple(f['unit'])
            elif gone:death[(i,next(iter(gone)))]=i
            if f['kind']=='B':
                assert len(gone)==1 and f['access_key'] in next(iter(gone))
                if added:assert f['access_key'] not in next(iter(added))
        assert set(birth)==vertices-set(prev) and set(death)==vertices-set(nxt)
        seen=set();gp={};cyc=bonly=0
        for start,u in birth.items():
            v=start
            while v in nxt:assert v not in seen;seen.add(v);v=nxt[v]
            assert v in death and v not in seen;seen.add(v);f=fine[death[v]]
            if f['slot']=='PAYMENT':gp[tuple(f['demand'])]=u
        for start in vertices-seen:
            if start in seen:continue
            v=start;members=[]
            while v not in seen:seen.add(v);members.append(v);v=nxt[v]
            assert v==start;cyc+=1;bonly+=int(any(v in Bneutral_edges for v in members) and not any(v in Atransfer for v in members))
        assert seen==vertices and gp=={tuple(a['demand']):tuple(a['unit']) for a in r['g_life']}
        assert cyc==sum(x['cyclic'] for x in r['components']) and bonly==r['B_only_neutral_cycles']
        component_reports.append({'source':r['source'],'fine_boundary_vertices':len(vertices),'directed_cycles':cyc,'B_only_neutral_cycles':bonly})
    assert next(r for r in component_reports if r['source']=='CCR')['B_only_neutral_cycles']==7
    # Independently challenge actual partial/full maps and restricted cuts.
    for e in data['root_entry_graph_controls.json']['controls']:
        graph={tuple(x['demand']):{tuple(u) for u in x['units']} for x in e['graph']};h={tuple(x['demand']):tuple(x['unit']) for x in e['matching']}
        assert len(h)==e['Q'] and len(set(h.values()))==len(h) and all(u in graph[d] for d,u in h.items())
        life=next(r for r in data['lifetime_controls.json']['controls'] if r['source']==e['source']);fixed={tuple(a['unit']) for a in life['g_life']};S={tuple(d) for d in e['fixed_lifetime_cut']['demands']};neighbors=set().union(*(graph[d]-fixed for d in S)) if S else set()
        assert neighbors=={tuple(u) for u in e['fixed_lifetime_cut']['units']} and len(S)-len(neighbors)==e['fixed_lifetime_cut']['deficiency']
    for t in data['terminal_neutral_controls.json']['controls']:
        r=next(x for x in data['lifetime_controls.json']['controls'] if x['source']==t['source']);fine=r['fine_steps'];U={tuple(u) for u in r['U']};dp={tuple(d) for d in r['Dplus']};gt={tuple(a['demand']):tuple(a['unit']) for a in t['g_T']};terminal={tuple(e['last_double']) for e in t['source_seeds'] if e['last_double'] is not None}
        assert set(gt)==dp|terminal and len(set(gt.values()))==len(gt) and set(gt.values())<=U
        for e in t['source_seeds']:
            f=fine[e['last_loss_step']];assert e['side_cluster'] in f['added'] and len(f['added'])-len(f['removed'])==1 and tuple(f['unit'])==tuple(e['positive_bit'])
            z=fine[e['final_B_decrease_slot']];assert len(z['removed'])-len(z['added'])==1
        internal={tuple(d) for d in t['D_internal_neutral']};assert internal=={tuple(d) for d in r['D0']}-terminal
        full=next(x for x in data['control_complete_complements.json']['controls'] if x['source']==t['source']);h={tuple(a['demand']):tuple(a['unit']) for a in full['full_matching']}
        assert set(h)=={tuple(d) for d in r['D']} and len(set(h.values()))==len(h) and all(h[d]==u for d,u in gt.items()) and set(h.values())<=U
    # Free ordered-tree identity, with B,C arbitrary subtree variables.
    g,p,x,u='g','p','x','u';source=(g,'A',(p,'B',(u,(x,'C','D'),'E')))
    inner=(p,'B',right(source[2][2]));inner=left(inner);actual=left((g,'A',inner))
    assert actual==(x,(g,'A',(p,'B','C')),(u,'D','E'))
    trimmed=(g,None,(p,'B',(x,'C',None)));ordinary=left(left(trimmed));assert ordinary==(x,(p,(g,None,'B'),'C'),None)
    assert ordinary!=(x,(g,None,(p,'B','C')),None)
    # NEW concrete sources: distinct mutable ordinary-splay replay.
    spec=importlib.util.spec_from_file_location('ND08_distinct_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    ch=data['exact_challenge_sources.json'];v=ch['vine_family_control'];a=V.Mutable(tup(v['initial']));b=V.Mutable(tup(v['initial']));fine_v=[];gp={};d0=set();qby={};lastslot={}
    def step(before,after,kind,unit=None,demand=None,slot=None,t=None):fine_v.append({'before':before,'after':after,'kind':kind,'unit':unit,'demand':demand,'slot':slot,'t':t})
    for r in v['rows']:
        assert tup(a.snapshot())==tup(r['A_before']) and tup(b.snapshot())==tup(r['BF_before']);h,_,ae=a.splay(r['key'],True);assert h==r['H'] and tup(a.snapshot())==tup(r['A_after'])
        jb=labels(tup(b.snapshot()))
        for e in ae:
            for rot in e['rotations']:step(len(jb-labels(tup(rot['before']))),len(jb-labels(tup(rot['after']))),'A',(r['t'],e['j'],rot['bit']))
        if r['kind']=='K':
            _,q,be=b.splay(r['key'],True);assert q==r['Q'];ja=labels(tup(a.snapshot()));dindex=0
            for e in be:
                double=len(e['pattern'])==2;d=(r['t'],dindex+1) if double else None;rr=[(len(labels(tup(z['before']))-ja),len(labels(tup(z['after']))-ja)) for z in e['rotations']];drops=sum(a-b for a,b in rr)
                if double:dindex+=1;d0.update([d] if drops==0 else [])
                first=True
                for aa,bb in rr:
                    slot=None
                    if aa>bb:slot='PAYMENT' if double and first else ('B2_RELEASE' if double else 'BZIG_RELEASE');first=False
                    step(aa,bb,'B',demand=d,slot=slot,t=r['t'])
                lastslot[r['t']]=len(fine_v)-1
            qby[r['t']]=q
        assert tup(b.snapshot())==tup(r['BF_after'])
    assert tup(a.snapshot())==tup(b.snapshot())==tup(v['initial'])
    # Stack-based cyclic level pairing, independently of producer bisect.
    levels=collections.defaultdict(list)
    for i,s in enumerate(fine_v):
        if s['after']>s['before']:levels[s['after']].append((i,1,s['unit']))
        elif s['after']<s['before']:levels[s['before']].append((i,-1,None))
    cross={}
    for level,events in levels.items():
        last_up=next(e[2] for e in events[::-1] if e[1]==1)
        for i,sign,unit in events:
            if sign==1:last_up=unit
            else:cross[i]=last_up
    for i,s in enumerate(fine_v):
        if s['slot']=='PAYMENT':gp[tuple(s['demand'])]=cross[i]
    extra={}
    for d in d0:
        if d[1]==qby[d[0]]:
            z=lastslot[d[0]];assert fine_v[z]['slot']=='BZIG_RELEASE';extra[d]=cross[z]
    zc=next(r for r in data['zig_release_complement_controls.json']['controls'] if r['source']=='VINE8')
    gz=dict(gp);gz.update(extra);assert gz=={tuple(a['demand']):tuple(a['unit']) for a in zc['g_Z']} and len(set(gz.values()))==len(gz) and len(d0-set(extra))==2 and len(extra)>=1
    pr=ch['projection_control'];full=V.Mutable(tup(pr['initial']));H,Q,ev=full.splay(7,True);small=V.Mutable(tup(pr['projected_initial']));h,q,_=small.splay(7,True)
    assert (H,Q,h,q)==(2,1,1,1) and tup(full.snapshot())==tup(pr['full_after']) and tup(small.snapshot())==tup(pr['projected_ordinary_after']) and tup(small.snapshot())!=tup(pr['trimmed_full_after'])
    state=V.Mutable((4,None,(6,None,(7,None,(8,None,None)))))
    for r in pr['reaching_prefix']+pr['closed_period']:
        assert tup(state.snapshot())==tup(r['before']);h,q,_=state.splay(r['key'],True);assert (h,q)==(r['H'],r['Q']) and tup(state.snapshot())==tup(r['after'])
    assert tup(state.snapshot())==tup(pr['initial']) and V.CALLS==55
    proof_names=['SOURCE_SPEC.md','ND35_UNIVERSAL_AUDIT.md','LIFETIME_NORMAL_FORM.md','ROOT_ENTRY_LEMMA.md','TERMINAL_NEUTRAL_ELIMINATION.md','ZIG_RELEASE_COMPLEMENT_THEOREM.md','COMPLETE_MATCHING_NORMALIZATION.md','SEQUENTIAL_VINE_NEUTRAL_FAMILY.md','INTERVAL_PROJECTION_OBSTRUCTION.md','audit_neutral_investigation.py']
    review=['ND35 local SET changes, fixed B carrier and cyclic crossing proof cover all original nonempty supports; zero support Q0 separate',
      'lifetime normal form is paths/cycles, permits multiwinding and is forward annotation only, not reverse source grammar',
      'root-entry existence follows actual A-root change, but is not independent endpoint expansion',
      'old-root side disappearance is +1 because a new strict-superset pivot label contains old B root; unary duplicates handled at SET disappearance',
      'last B rotation creates common whole root-side cluster, so drops1; neutral LAST double requires a subsequent decreasing zig',
      'direct ZRC35 uses distinct already released crossing bits, leaves all original g+ values, eliminates terminal neutral claims uniformly',
      'optional root-pair transpositions preserve provisional crossing bijection, cover nonneutral plus last, change no frozen map',
      'only INTERNAL-neutral labels remain after alternating with h0; zero-internal-neutral class has full raw matching and conditional original static bank2',
      'vine construction/sweep induction is uniform in even support, has unbounded internal neutrals but complete own funding',
      'projection RL+zig vs trimmed RR identity refutes naive interval ordinary-splay induction; no scalar counterexample',
      'complete-matching normalization and explicit source controls do not prove universal endpoint existence or Gate U compatibility']
    out={'status':'PASS_ND08_UNIFORM_PARTIAL_PROOFS_AND_DISTINCT_SOURCE_CHALLENGES','component_checks':component_reports,
      'source_proof_review':review,'new_original_source_calls':V.CALLS,'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'old_source_checks_reused':'exact ND35 receipt/profile and pinned original source traces; no old search rerun',
      'ZRC35':'PROVED_AT_STATED_UNIFORM_RAW_SCOPE','universal_complete_matching':'OPEN','Gate_U_compatibility':'DEFERRED',
      'formal_or_external_review':False,'same_agent_distinct_implementation':True,
      'input_sha256':{str(p):sha(p) for p in [F/n for n in names+proof_names]+[O/'independent_core_sector_neutral.json']}}
    with (F/'independent_audit.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('input_sha256','source_proof_review')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/'audit_verify159_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
