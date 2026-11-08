"""Independent immutable rotations, actual replay, reverse exchange checker.
No primary rotation/source replay code is imported. Allocator is a black box.
"""
import collections,functools,importlib.util,itertools,json,sys,time
from pathlib import Path
from two_slot_allocator import extend_two
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
spec=importlib.util.spec_from_file_location('independent_immutable12',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
calls=0;started=time.process_time();CAP=min(90,float(sys.argv[1])-4)
def move(t,x):
    global calls
    calls+=1;assert calls<1500000 and time.process_time()-started<CAP
    assert I.lookup(t,x)[0]
    return I.trace(t,x)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def readtree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],readtree(t[1]),readtree(t[2]))
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def core(t,M):
    if t[0]=='leaf':return set()
    l,r=core(t[2],M),core(t[3],M)
    return l|r|{t[1]} if l or r or t[1] in M else set()
def chart(t,M):
    def shape(t):
        if t[0]=='leaf':return None
        l,r=shape(t[2]),shape(t[3])
        return (t[1],l,r) if l is not None or r is not None or t[1] in M else None
    s=sorted(core(t,M));ix={k:i for i,k in enumerate(s)}
    def conv(u):return None if u is None else (ix[u[0]],conv(u[1]),conv(u[2]))
    return {'marks':sorted(M),'Scores':s,'tree':conv(shape(t)),'size':len(s)}
def qb(events):return sum(e[0]!='ZIG' for e in events)
def leaves(t):return 0 if t[0]=='leaf' else 1 if t[2][0]==t[3][0]=='leaf' else leaves(t[2])+leaves(t[3])
@functools.lru_cache(None)
def trees(lo,hi):
    if lo>hi:return (('leaf','F'+str(hi)),)
    return tuple(I.node(k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))
def reflect(t):return ('leaf','F'+str(7-int(t[1][1:]))) if t[0]=='leaf' else I.node(8-t[1],reflect(t[3]),reflect(t[2]))
def backward_endpoints(D,U,a,h):
    """Start at EVERY FREE unit and trace inverse h, then a backwards.
    This is a different traversal from the producer's missing-root walk.
    """
    inverse_h={u:d for d,u in h.items()};missing=D-set(a);ends={}
    for free in U-set(a.values()):
        u=free;seen=set()
        while u in inverse_h:
            d=inverse_h[u]
            if d in missing:
                assert d not in ends;ends[d]=free;break
            if d in seen:break
            seen.add(d);u=a[d]
    assert set(ends)==missing and len(set(ends.values()))==len(missing)
    return ends
def locked_backward(D,U,l,h):
    inv={u:d for d,u in h.items()};result=dict(l)
    for u0 in U-set(l.values()):
        u=u0;seen=set()
        while u in inv:
            d=inv[u]
            if d not in l:
                assert d not in result;result[d]=u0;break
            assert d not in seen;seen.add(d);u=l[d]
    return result
def check_path_receipts(ex,a,h):
    inv={u:d for d,u in a.items()};allnodes=set();allunits=set()
    for v in ex['paths']:
        d=freeze(v['root']);assert d not in a
        for dd,uu in v['steps']:
            dd,uu=freeze(dd),freeze(uu);assert dd==d and h[d]==uu
            assert d not in allnodes and uu not in allunits
            allnodes.add(d);allunits.add(uu)
            if uu in inv:d=inv[uu]
        u=freeze(v['terminal_unit']);assert u==uu and u not in inv
def main():
    ts=set(trees(1,7));edges=set();incoming=collections.defaultdict(list);hin=collections.Counter()
    for t in ts:
        for x in range(1,8):
            d,ev=move(t,x);q=qb(ev);assert d in ts
            if q==3:assert I.lookup(t,x)[1]==6 and leaves(t)==1
            if leaves(d)==1:assert q<=1;hin[q]+=1
            edges.add((t,x,d,q));incoming[d].append((t,x,q))
    primary=json.loads((B/'geometry_certificate.json').read_text());pt=[readtree(t) for t in primary['trees']]
    assert {(pt[e['source']],e['target_key'],pt[e['destination']],e['Q']) for e in primary['transitions']}==edges
    classes=[];pred=0
    for unmarked in range(2,7):
        M=set(range(1,8))-{unmarked};valid={t for t in ts if t[1] in M and core(t,M)==set(range(1,8))}
        admitted=[e for e in edges if e[0] in valid and e[2] in valid and e[1] in M and e[1]!=e[0][1]]
        dd=[e for e in admitted if e[3]==3]
        for t,x,end,q in dd:
            pp=[e for e in incoming[t] if e[0] in valid and e[1] in M and e[1]!=e[0][1]]
            assert pp and all(e[2]<=1 for e in pp);pred+=len(pp)
        classes.append((unmarked,len(valid),len(admitted),len(dd)))
    assert classes==[(v['unmarked'],v['core_contexts'],v['admitted_genuine_edges'],v['Q3_sectors']) for v in primary['classes']]
    assert pred==198 and all((reflect(t),8-x,reflect(d),q) in edges for t,x,d,q in edges)
    src=json.loads((B/'physical_receipts2.json').read_text());reports=[];fixtures=0;cuts=0;branches=collections.Counter();events=0
    for fam in src['families']:
        word=[tuple(v) for v in fam['word']];M=set(fam['marks']);z=fam['erased'];A=F=R=readtree(fam['initial_A_BF']);E=E0=readtree(fam['initial_BE'])
        prefix=R
        for _ in range(fam['alignment']['u']):
            for m,x in word:
                if m=='K' and x!=z:prefix=move(prefix,x)[0]
        assert prefix==E0 and fam['alignment']['L']==1
        U=set();D=set();Ed=set();rows=fam['rows'];ends=[];tot=[0,0,0]
        lru=[]
        for m,x in reversed(word):
            if m=='K' and x not in lru:lru.append(x)
        initial_lru=lru[:]
        for idx,((m,x),row,ch) in enumerate(zip(word,rows,fam['charts'])):
            t=idx+1;assert row['occurrence']==t and (A,F,E)==tuple(readtree(s) for s in row['before'])
            assert len(core(F,M))==7 and core(F,M)==core(R,M)
            old_chart=chart(F,set(lru[:5]));old_recent=lru[:]
            assert row['genuine_F']==(m=='K' and x!=F[1])
            if row['genuine_F']:ends.append(idx)
            old_depth=I.lookup(A,x)[1];A,ae=move(A,x);be=ee=[]
            if m=='K':
                F,be=move(F,x)
                if x!=z:E,ee=move(E,x)
                lru.remove(x);lru.insert(0,x)
            assert len(ae)==(old_depth+1)//2
            assert (A,F,E)==tuple(readtree(s) for s in row['after'])
            for ev,sup in ((ae,row['A_events']),(be,row['BF_events']),(ee,row['BE_events'])):
                assert [('ZIG' if q[0]=='ZIG' else 'DOUBLE',q[3] if q[0]=='ZIG' else q[0]) for q in ev]==[(q['kind'],q['case']) for q in sup]
            assert [len(ae),qb(be),qb(ee)]==[row['a'],row['qF'],row['qE']]
            assert ch['recent_before']==old_recent and ch['recent_after']==lru
            for a,b in ((old_chart,ch['old_chart']),(chart(F,set(lru[:5])),ch['new_chart'])):
                assert a['marks']==b['marks'] and a['Scores']==b['Scores'] and a['size']==b['size'] and freeze(a['tree'])==freeze(b['tree'])
            assert ch['cold']==(m=='K' and x not in old_recent[:5])
            U|={(t,j,b) for j in range(1,len(ae)+1) for b in (0,1)}
            D|={(t,k) for k in range(1,qb(be)+1)};Ed|={(t,k) for k in range(1,qb(ee)+1)}
            tot=[a+b for a,b in zip(tot,(len(ae),qb(be),qb(ee)))];events+=len(ae)+len(be)+len(ee)
        assert (A,F,E)==(R,R,E0) and lru==initial_lru and {rows[i]['target'] for i in ends}==M
        # Independently partition natural macros from actual genuine endpoints.
        mm=[];h0={};critical=[];Rset=set()
        for j,end in enumerate(ends):
            prev=ends[j-1];ii=list(range(prev+1,end+1)) if prev<end else list(range(prev+1,len(rows)))+list(range(end+1))
            ts0=[i+1 for i in ii];uu=[u for t in ts0 for u in sorted(U) if u[0]==t];dd=[d for t in ts0 for d in sorted(D) if d[0]==t]
            H=len(uu)//2;Q=len(dd);assert H>=1 and Q<=3
            mm.append((ts0,H,Q,uu,dd));n=min(len(uu),len(dd));h0.update(zip(dd[:n],uu[:n]));Rset|=set(dd[n:])
            if Q>2*H:critical.append(j)
            declared=fam['macros'][j];assert [H,Q]==[declared['H'],declared['Q']] and ts0==declared['occurrences']
        assert len(Rset)==len(critical)==2 and Rset==set(map(tuple,fam['R']))
        h=dict(h0);seeds=[]
        for c in critical:
            pre=(c-1)%len(mm);a,H,Q,uu,dd=mm[c];p0,Hp,Qp,up,dp=mm[pre]
            assert H==1 and Q==3 and Qp<=1 and Hp>=1
            r=dd[2];v=up[Qp];h[r]=v;seeds.append((c,pre,r,v))
        assert len({v[1] for v in seeds})==2 and len({v[3] for v in seeds})==2
        assert h0==unpack(fam['h0']) and h==unpack(fam['independent_h'])
        assert fam['positive_surplus']==sum(max(2*m[1]-m[2],0) for m in mm)>=2
        # Independent chronological receipt at a cut before a predecessor.
        start=seeds[0][1];seed_at={v:r for c,pre,r,v in seeds};critical_r={r for c,pre,r,v in seeds};carry={};own=[];paidstream={};clock={};maxwork=0;timepos=0
        for step in range(len(mm)):
            a,H,Q,uu,dd=mm[(start+step)%len(mm)];selected=set(uu[:min(2*H,Q)])
            for t in a:
                timepos+=1;clock[t]=timepos
                for j in range(1,rows[t-1]['a']+1):
                    for b in (0,1):
                        u=(t,j,b)
                        if u in selected:own.append(u)
                        if u in seed_at:carry[seed_at[u]]=u
                        maxwork=max(maxwork,len(own)+len(carry))
                for k in range(1,rows[t-1]['qF']+1):
                    d=(t,k)
                    paidstream[d]=carry.pop(d) if d in critical_r else own.pop(0)
            assert not own and len(carry)<=1
        assert not carry and paidstream==h and maxwork<=4
        assert all(clock[u[0]]<=clock[d[0]] for d,u in h.items())
        for f in fam['fixtures']:
            fE=unpack(f['fE']);C=D&Ed;l={d:fE[d] for d in C};a=unpack(f['paid'])
            assert set(fE)==Ed and set(fE.values())<=U and len(set(fE.values()))==len(fE)
            assert set(map(tuple,f['common']))==C and set(map(tuple,f['full_only']))==D-Ed and set(map(tuple,f['auxiliary_only']))==Ed-D
            assert a==locked_backward(D,U,l,h0)
            P=D-set(a);W=U-set(a.values());anchors=unpack(f['anchors'])
            assert set(map(tuple,f['uncovered']))==P and set(map(tuple,f['Wstar']))==W
            assert set(anchors)==P and set(anchors.values())<=Rset and len(set(anchors.values()))==len(P)
            adds=unpack(f['additions']);assert adds==backward_endpoints(D,U,a,h)
            final=unpack(f['final']);assert final=={**a,**adds}==locked_backward(D,U,l,h)
            assert set(final)==D and len(set(final.values()))==len(final)
            assert all(final[d]==u for d,u in a.items()) and all(final[d]==fE[d] for d in C)
            oldpaths={tuple(v['root']):v for v in f['partial_paths']};newpaths={tuple(v['root']):v for v in f['licensed_paths']}
            assert all(newpaths[k]==v for k,v in oldpaths.items())
            ex={'paths':f['extension_paths']};check_path_receipts(ex,a,h)
            branches[str(len(P))]+=1;fixtures+=1
        for delta in range(len(rows)):
            tau=lambda t:t if t>delta else t+len(rows)
            units={(tau(t),j,b) for t,j,b in U};demands={(tau(t),k) for t,k in D}
            mapped={(tau(d[0]),d[1]):(tau(u[0]),u[1],u[2]) for d,u in h.items()}
            assert set(mapped)==demands and set(mapped.values())<=units and len(set(mapped.values()))==len(mapped)
            cuts+=1
        reports.append({'variant':fam['variant'],'reflected':fam['reflected'],'erased':z,'A_QF_QE':tot,
            'actual_R':sorted(Rset),'seeds':seeds,'max_working_units':maxwork,'closed_A_BF_BE':True,
            'source_rows':len(rows),'full_demands':len(D),'bit_units':len(U)})
    one=src['one_residual_paid_control'];last=src['families'][-1];h=unpack(last['independent_h']);D=set(h);U={(r['occurrence'],j,b) for r in last['rows'] for j in range(1,r['a']+1) for b in (0,1)}
    a=unpack(one['paid']);assert unpack(one['extension'])==backward_endpoints(D,U,a,h)
    # Tight and spare inventories; zero, one and two holes against ALL paid
    # owners, with backwards independently computed endpoints.
    generic=0;generic_branches=collections.Counter();maxpath=0
    for nU in (4,5):
        D=set(range(4));U=set(range(nU))
        for hs in itertools.permutations(sorted(U),4):
            h=dict(zip(sorted(D),hs))
            for holes in (0,1,2):
                for missing in itertools.combinations(sorted(D),holes):
                    ds=sorted(D-set(missing))
                    for aa in itertools.permutations(sorted(U),len(ds)):
                        a=dict(zip(ds,aa));result=extend_two(D,U,a,h)
                        assert result['additions']==backward_endpoints(D,U,a,h)
                        assert result['allocation']=={**a,**result['additions']}
                        check_path_receipts(result,a,h);generic+=1;generic_branches[str(holes)]+=1
                        maxpath=max(maxpath,sum(len(v['steps']) for v in result['paths']))
    result={'status':'PASS_DISTINCT_IMMUTABLE_SOURCE_AND_REVERSE_OWNERSHIP_AUDIT',
        'seven_Score_trees':429,'source_access_edges':len(edges),'Hamiltonian_incoming_by_Q':dict(hin),
        'classes':classes,'critical_sectors':132,'predecessor_incidences':pred,'source_reports':reports,
        'actual_source_owner_fixtures':fixtures,'source_fixture_branches':dict(branches),'one_hole_source_ID_control':True,
        'actual_period_cut_transports':cuts,'all_source_events_compared':events,
        'generic_owner_cases':generic,'generic_owner_branches':dict(generic_branches),'maximum_total_path_steps':maxpath,
        'source_engine_calls':calls,'new_finite_tests':generic+fixtures+1,
        'universal_proof':'free-tree predecessor induction, distinct cyclic predecessor positions, terminating disjoint owner paths; finite tests are audits only',
        'trust':'same-agent distinct immutable engine and backwards checker; no external or formal peer certification'}
    out('independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('source_reports','classes')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
