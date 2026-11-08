"""Independent source annotations for CSL35/ND35, all fresh calls charged.
Accepted old A events are reused. New fine B traces are run only when
not already the identical accepted A primitive. One outside-core-helper
control is replayed freshly because its fine events were not stored.
"""
import bisect,collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tup(t):return (t[0],tup(t[1]),tup(t[2])) if isinstance(t,list) else t
def material(t):return (t[0],material(t[1]),material(t[2])) if isinstance(t,(tuple,list)) else None
def physical_keys(t):return set() if t is None else physical_keys(t[1])|physical_keys(t[2])|{t[0]}
def labels(t,S):
    out=set()
    def go(u):
        if u is None:return frozenset()
        v=go(u[1])|go(u[2])|({u[0]} if u[0] in S else set())
        if v:out.add(frozenset(v))
        return frozenset(v)
    go(t);return out
def core(t,M):
    out=set()
    def go(u):
        if u is None:return False
        a,b=go(u[1]),go(u[2]);yes=a or b or u[0] in M
        if yes:out.add(u[0])
        return yes
    go(t);return out
def psi(A,BF,S):return len(labels(BF,S)-labels(A,S))
def main():
    global V
    sp=importlib.util.spec_from_file_location('CSL_ND_distinct_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    cases=[];files=[];identical_reuse=0
    for name,path in [('CCR',F/'cluster_collateral_closed_source.json'),('AF',B/'SOURCE_JOINT_REPAIR_03/actual_monotone_return_source.json'),('NONMAX',F/'maximal_completion_original_source.json')]:
        src=json.loads(path.read_text());rows=src['period_rows'];frozen=src.get('h0',src.get('h0_full_own',src.get('funding',{}).get('h0')))
        cases.append((name,rows,frozen));files.append(path)
    # Full physical source with the A-only key3 outside the ten-anchor B core.
    srcpath=B/'B_full_spectrum_edge_0_closed_source.json';src=json.loads(srcpath.read_text());native=json.loads((B/'native10_source_actions.json').read_text())
    def Btree(i):
        def go(u):
            if isinstance(u,str):return (3,None,None) if u=='F1' else None
            return (2*u[0],go(u[1]),go(u[2]))
        return go(native['trees'][i])
    prows=[]
    for r in src['period_rows']:
        a=src['A_word_source_rows'][r['word_index']];ab=material(a['before']);aa=material(a['after'])
        A=V.Mutable(ab);h,_,ev=A.splay(r['key'],True);assert h==r['H']==a['H'] and tup(A.snapshot())==aa
        bb,ba=Btree(r['BF_before']),Btree(r['BF_after'])
        prows.append({'t':r['absolute_t'],'kind':r['kind'],'key':r['key'],'A_before':ab,'A_after':aa,'BF_before':bb,'BF_after':ba,
          'a':h,'qF':r['QF'],'genuine_F':r['kind']=='K' and bb[0]!=r['key'],'A_events':ev})
    cases.append(('PRIVATE_HELPER',prows,None));files.append(srcpath)
    reports=[]
    for name,raw,frozen in cases:
        rows=[]
        for r in raw:
            rr=dict(r);rr['A_before']=tup(r['A_before']);rr['A_after']=tup(r['A_after']);rr['BF_before']=tup(r['BF_before']);rr['BF_after']=tup(r['BF_after'])
            if 'A_events' not in rr:
                A=V.Mutable(rr['A_before']);h,_,ae=A.splay(rr['key'],True);assert h==rr['a'] and tup(A.snapshot())==rr['A_after'];rr['A_events']=ae
            if rr['kind']=='K' and rr['BF_before'][0]!=rr['key']:
                if rr['A_before']==rr['BF_before']:
                    be=rr['A_events'];assert rr['A_after']==rr['BF_after'];identical_reuse+=1
                else:
                    BF=V.Mutable(rr['BF_before']);_,q,be=BF.splay(rr['key'],True);assert q==rr['qF'] and tup(BF.snapshot())==rr['BF_after']
                rr['BF_events']=be
            else:rr['BF_events']=[];assert rr['qF']==0 and rr['BF_before']==rr['BF_after']
            rows.append(rr)
        assert rows[0]['A_before']==rows[-1]['A_after'] and rows[0]['BF_before']==rows[-1]['BF_after']
        M={r['key'] for r in rows if r['genuine_F']};S=core(rows[0]['BF_before'],M);assert len(S)<=2*len(M)-1
        assert all(core(r['BF_before'],M)==S and core(r['BF_after'],M)==S for r in rows)
        U={(r['t'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
        D={(r['t'],k) for r in rows for k in range(1,r['qF']+1)}
        ends=[i for i,r in enumerate(rows) if r['genuine_F']];h0={};sector_records=[];rho={};allsectorlabels={}
        for j,end in enumerate(ends):
            start=(ends[j-1]+1)%len(rows);ids=list(range(start,end+1)) if start<=end else list(range(start,len(rows)))+list(range(end+1))
            seg=[rows[i] for i in ids];H=sum(r['a'] for r in seg);q=seg[-1]['qF'];x=seg[-1]['key'];units=[(r['t'],k,b) for r in seg for k in range(1,r['a']+1) for b in (0,1)]
            demand=[(seg[-1]['t'],k) for k in range(1,q+1)];own=dict(zip(demand,units));h0.update(own);inverse={u:d for d,u in own.items()}
            node=seg[0]['BF_before'];path=[]
            while True:
                path.append(node)
                if node[0]==x:break
                node=node[1] if x<node[0] else node[2]
            depth=len(path)-1;assert depth//2==q and seg[0]['A_before'][0]==seg[0]['BF_before'][0]
            initial=labels(seg[0]['A_before'],S);chosen={};missing={};sector={}
            for k,d in enumerate(demand,1):
                pair=[]
                for index in (depth-2*k+2,depth-2*k+1):
                    subtree=path[index]
                    def member_keys(u):
                        if u is None:return set()
                        return member_keys(u[1])|member_keys(u[2])|({u[0]} if u[0] in S else set())
                    pair.append(frozenset(member_keys(subtree)))
                assert pair[0]<pair[1] and x in pair[0] and pair[1]<S
                sector[d]=pair;allsectorlabels[d]=pair
                present=next((c for c in pair if c in initial),None)
                if present is None:missing[d]=pair
                else:chosen[d]=present
            assert len(set(chosen.values()))==len(chosen)
            first={};back={c:d for d,c in chosen.items()}
            for r in seg:
                for ev in r['A_events']:
                    for rot in ev['rotations']:
                        lost=labels(tup(rot['before']),S)-labels(tup(rot['after']),S);assert len(lost)<=1
                        for c in lost:
                            if c in back:first.setdefault(back[c],(r['t'],ev['j'],rot['bit']))
            assert set(first)==set(chosen) and len(set(first.values()))==len(first)
            terminalset=set();paths=[]
            for d in demand:
                if d in own:continue
                current=d;seen=[];trace=[]
                while current in chosen:
                    assert current not in seen;seen.append(current);unit=first[current];assert unit in inverse
                    nxt=inverse[unit];trace.append({'demand':current,'actual_first_loss_bit':unit,'frozen_own_demand':nxt});current=nxt
                assert current in missing and current not in terminalset;terminalset.add(current);rho[d]=current
                paths.append({'unpaid':d,'path':trace,'terminal_missing_sector_demand':current,'labels':[sorted(c) for c in sector[current]]})
            sector_records.append({'end_t':seg[-1]['t'],'H':H,'Q':q,'present_sectors':len(chosen),'doubly_missing_sectors':len(missing),'unpaid':len(demand)-len(own),'paths':paths})
        if frozen is not None:assert h0=={tuple(v['demand']):tuple(v['unit']) for v in frozen}
        # Fine-step Psi, respecting actual A-before-B execution.
        fine=[];Pbits=set();negativeA=0;neutral=set();nonneutral=set();B2=Z1=0
        def add(before,after,kind,unit=None,slot=None,demand=None):
            delta=after-before;index=len(fine)
            fine.append({'index':index,'before':before,'after':after,'delta':delta,'kind':kind,'unit':unit,'slot':slot,'demand':demand})
            return delta
        initialpsi=psi(rows[0]['A_before'],rows[0]['BF_before'],S)
        for r in rows:
            for ev in r['A_events']:
                for rot in ev['rotations']:
                    a,b=psi(tup(rot['before']),r['BF_before'],S),psi(tup(rot['after']),r['BF_before'],S)
                    u=(r['t'],ev['j'],rot['bit']);d=add(a,b,'A_ROTATION',u,'A_NEGATIVE_RELEASE' if b<a else None)
                    assert d in (-1,0,1)
                    if d==1:Pbits.add(u)
                    if d==-1:negativeA+=1
            Aafter=r['A_after'];doub=0
            for ev in r['BF_events']:
                isdouble=len(ev['pattern'])==2;d=(r['t'],doub+1) if isdouble else None;drops=0
                for rot in ev['rotations']:
                    a,b=psi(Aafter,tup(rot['before']),S),psi(Aafter,tup(rot['after']),S);assert b-a in (-1,0)
                    slot=None
                    if b<a:
                        slot='GOOD_DOUBLE_PAYMENT' if isdouble and drops==0 else ('B_DOUBLE_EXTRA_RELEASE' if isdouble else 'B_ZIG_RELEASE');drops+=1
                    add(a,b,'B_ROTATION',None,slot,d)
                if isdouble:
                    doub+=1
                    if drops:nonneutral.add(d);B2+=int(drops==2)
                    else:neutral.add(d)
                else:Z1+=drops
            assert doub==r['qF']
        assert all(fine[i]['after']==fine[i+1]['before'] for i in range(len(fine)-1)) and fine[0]['before']==initialpsi==fine[-1]['after']
        ups=collections.defaultdict(list);downs=collections.defaultdict(list)
        for f in fine:
            if f['delta']==1:assert f['unit'] in Pbits;ups[f['after']].append(f['index'])
            if f['delta']==-1:downs[f['before']].append(f['index'])
        paid={};released=set();used=set();pairings=[]
        assert set(ups)==set(downs)
        for level,uu in ups.items():
            dd=downs[level];assert len(uu)==len(dd)
            for di in dd:
                k=bisect.bisect_left(uu,di)-1;ui=uu[k];unit=tuple(fine[ui]['unit']);consumer=fine[di];assert unit not in used;used.add(unit)
                if consumer['slot']=='GOOD_DOUBLE_PAYMENT':
                    demand=tuple(consumer['demand']);assert demand not in paid;paid[demand]=unit
                else:released.add(unit)
                pairings.append({'level':level,'positive_source_step':ui,'actual_bit':unit,'decrease_source_step':di,'slot':consumer['slot'],'demand':consumer['demand']})
        assert used==Pbits and set(paid)==nonneutral and len(set(paid.values()))==len(paid)
        remainder=(U-Pbits)|released;assert not remainder&set(paid.values()) and remainder|set(paid.values())==U
        Acount=sum(r['a'] for r in rows);Q=len(D);Pcount=len(Pbits);B1=len(nonneutral)-B2
        assert Pcount==negativeA+B1+2*B2+Z1
        assert 2*Acount-Q==(2*Acount-Pcount)+negativeA+B2+Z1-len(neutral)
        assert len(remainder)==(2*Acount-Pcount)+negativeA+B2+Z1
        # Global alternating reduction; never move an h0 value.
        inverse={u:d for d,u in h0.items()};added={};neutralends={};paths=[]
        for start in sorted(D-set(h0)):
            current=start;seen=[];trace=[]
            while current in nonneutral:
                assert current not in seen;seen.append(current);u=paid[current];trace.append({'demand':current,'g_plus_bit':u,'h0_owner':inverse.get(u)})
                if u not in inverse:added[start]=u;break
                current=inverse[u]
            else:assert current in neutral;neutralends[start]=current
            paths.append({'unpaid_start':start,'path':trace,'actual_h0_unowned_bit':added.get(start),'neutral_liability':neutralends.get(start)})
        assert len(set(added.values()))==len(added) and not set(added.values())&set(h0.values()) and len(set(neutralends.values()))==len(neutralends)
        reports.append({'source':name,'M':sorted(M),'S':sorted(S),'outside_S_physical_keys':sorted(physical_keys(rows[0]['A_before'])-S),
          'period':[rows[0]['t'],rows[-1]['t']],'A':Acount,'Q':Q,'P':Pcount,'N':negativeA,'B0':len(neutral),'B1':B1,'B2':B2,'Z1':Z1,
          'old_h0_values_preserved':len(h0),'CSL_unpaid_labels':len(rho),'CSL_macro_annotations':sector_records,
          'g_plus':[{'demand':d,'actual_bit':u} for d,u in sorted(paid.items())],'analytical_remainder_bits':sorted(remainder),'cyclic_level_pairings':pairings,
          'h0_preserving_new_partial_pairs':[{'demand':d,'actual_bit':u} for d,u in sorted(added.items())],'neutral_liability_paths':paths,
          'original_owners_modified':False,'Bank25_or_full_frozen_policy_license_claimed':False})
        assert time.process_time()-START<CAP-2
    report={'status':'PASS_CSL_LOCAL_INJECTIONS_AND_NEUTRAL_SOURCE_PARTITIONS','controls':reports,'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'identical_A_B_primitives_reused':identical_reuse,'new_semantics':'fine source observables for new uniform derivations; previously accepted closure/E/charts reused',
      'root_JR35':'OPEN','full_source_funding_or_Bank25_promotion':False,
      'input_sha256':{str(p):sha(p) for p in files+[F/'CORE_SECTOR_LIABILITY_THEOREM.md',F/'NEUTRAL_DOUBLE_SOURCE_DECOMPOSITION.md',F/'ND35_CSL35_PROOF_REVIEW.md',
       F/'independent_source_bridges_collateral_audit.json',B/'SOURCE_JOINT_REPAIR_03/independent_source_audit.json',B/'B_full_spectrum_formula_independent_audit.json']}}
    with (F/'independent_core_sector_neutral.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({'status':report['status'],'source_queries':V.CALLS,'controls':[{k:r[k] for k in ('source','A','Q','P','N','B0','B1','B2','Z1','old_h0_values_preserved','CSL_unpaid_labels')} for r in reports],'JR35':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify124_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
