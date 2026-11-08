"""Independent immutable source/marked-parent and reverse-owner audit.
No old six-key proof/table replay; only the NEW exact source histories.
"""
import hashlib,importlib.util,json,subprocess,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent
s=importlib.util.spec_from_file_location('immutable_leaf_channels15',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I);calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def tree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],tree(t[1]),tree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def move(t,x):
    global calls
    calls+=1;assert calls<2000000;return I.trace(t,x)
def parent_map(t,M):
    par={}
    def go(u,last=None):
        if u[0]=='leaf':return
        if u[1] in M:par[u[1]]=last;last=u[1]
        go(u[2],last);go(u[3],last)
    go(t);return par
def core(t,M):
    if t[0]=='leaf':return set()
    l,r=core(t[2],M),core(t[3],M)
    return l|r|{t[1]} if l or r or t[1] in M else set()
def unpack(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def backward(D,U,a,h):
    inv={u:d for d,u in h.items()};Pmissing=D-set(a);extra={};blocked={}
    for endpoint in U-set(a.values()):
        u=endpoint;seen=set()
        while u in inv:
            d=inv[u]
            if d in Pmissing:assert d not in extra;extra[d]=endpoint;break
            if d in seen:break
            seen.add(d);u=a[d]
    for frontier in D-set(h):
        d=frontier;seen=set()
        while True:
            if d in Pmissing:assert d not in blocked;blocked[d]=frontier;break
            if d in seen or d not in a or a[d] not in inv:break
            seen.add(d);d=inv[a[d]]
    assert set(extra).isdisjoint(blocked) and set(extra)|set(blocked)==Pmissing
    assert len(set(extra.values()))==len(extra) and len(set(blocked.values()))==len(blocked)
    return {**a,**extra},blocked
def main():
    src=json.loads((B/'leaf_source_certificates2.json').read_text());reports=[]
    assert src['status']=='SOURCE_EXACT_UNIFORM_LEMMA_AUDITS_AND_RESTRICTED_FAMILY_FUNDING'
    zero=json.loads((B/'zero_run_source_certificates.json').read_text())
    for f in src['reports']+zero['reports']:
        r=f['r'];M=set(range(1,2*r,2));R=tree(f['initial_A_BF']);E0=tree(f['initial_BE']);z=f['erased'];A=F=E=R
        # Exact diagonal-reaching prefix, kept OUT of the donor inventory.
        for copy in range(f['actual_reaching_prefix_copies']):
            for mode,x in f['base_word']:
                A=move(A,x)[0]
                if mode=='K':
                    F=move(F,x)[0]
                    if x!=z:E=move(E,x)[0]
        assert (A,F,E)==(R,R,E0);initial=(A,F,E);leaf_events=0
        for expected,(mode,x) in zip(f['rows'],f['word']):
            assert tuple(plain(t) for t in (A,F,E))==freeze(expected['before'])
            parent0=parent_map(F,M);_,ad=I.lookup(A,x);A,ae=move(A,x);be=ee=[]
            if mode=='K':
                _,bd=I.lookup(F,x);F,be=move(F,x)
                assert len(be)==bd//2 and all(ev[0] in ('LL','RR') for ev in be)
                if x!=z:E,ee=move(E,x)
                anc=[];v=parent0[x]
                while v is not None:anc.append(v);v=parent0[v]
                assert len(anc)==len(be)
                prediction=dict(parent0);prediction[x]=None
                for g in anc:prediction[g]=x
                assert parent_map(F,M)==prediction
                leaf_events+=len(anc)
            assert len(ae)==(ad+1)//2
            assert (len(ae),len(be),sum(ev[0]!='ZIG' for ev in ee))==(expected['a'],expected['qF'],expected['qE'])
            assert tuple(plain(t) for t in (A,F,E))==freeze(expected['after'])
            assert core(F,M)==set(range(1,2*r))
        assert (A,F,E)==initial
        rows=f['rows'];by={t['occurrence']:t for t in rows}
        D={(t['occurrence'],j) for t in rows for j in range(1,t['qF']+1)}
        U={(t['occurrence'],j,b) for t in rows for j in range(1,t['a']+1) for b in (0,1)}
        h=unpack(f['leaf_partial_h']);full=unpack(f['family_full_h']);frontier=set(map(tuple,f['branch_frontier']));h0={};all_birth={};death={};local={}
        for m in f['macros']:
            rr=[by[t] for t in m['occurrences']];units=[(t['occurrence'],j,b) for t in rr for j in range(1,t['a']+1) for b in (0,1)]
            dd=[(t['occurrence'],j) for t in rr for j in range(1,t['qF']+1)];h0.update(zip(dd,units))
            par=parent_map(tree(rr[0]['before'][1]),M);ch={x:[] for x in M}
            for x,g in par.items():
                if g is not None:ch[g].append(x)
            x=rr[-1]['target'];anc=[];g=par[x]
            while g is not None:anc.append(g);g=par[g]
            unary={g for g in anc if len(ch[g])==1};branch={g for g in anc if len(ch[g])>=2};zz=int(not ch[x])
            assert m['Q']==len(anc) and set(m['unary'])==unary and set(m['branch'])==branch and m['z']==zz
            assert m['signed_leaf_residual']==2*sum(t['a'] for t in rr)-len(branch)-zz
            after=parent_map(tree(rr[-1]['after'][1]),M);leaf0=M-set(par.values());leaf1=M-set(after.values())
            assert leaf1-leaf0==unary and leaf0-leaf1==({x} if zz else set())
            if zz:death[m['macro']]=(x,units[0]);assert tuple(m['reserve'])==units[0]
            for d,g in zip(dd,anc):
                if g in unary:all_birth[d]=(m['macro'],g)
            for d,u in m['local_branch_pairs']:local[tuple(d)]=tuple(u)
        used=set(local.values())
        for ch in f['channels']:
            d,u=tuple(ch['demand']),tuple(ch['unit']);birth,key=all_birth[d];j=ch['death_macro']
            assert (birth,key)==(ch['birth_macro'],ch['marked_key']) and death[j]==(key,u)
            prior=[i for i,(k,v) in death.items() if k==key and i<birth]
            expected=max(prior) if prior else max(i for i,(k,v) in death.items() if k==key)
            assert j==expected and u not in used and h[d]==u;used.add(u)
        assert set(h)==D-frontier and len(set(h.values()))==len(h) and set(h.values())<=U
        assert set(full)==D and len(set(full.values()))==len(D) and set(full.values())<=U
        assert len(D)==f['QF'] and len(U)==2*f['A'] and len(D)<=len(U)
        for deep in f['deep_packets']:
            assert set(map(tuple,deep['demands']))<=set(h)
            i,j=deep['macro_indices'];assert f['macros'][i]['Q']==r-1 and f['macros'][j]['Q']==1
        for rep in f['family_repairs']:
            for d,u in rep['actual_pairs']:
                assert tuple(d) in frontier and tuple(u) in U-set(h.values()) and full[tuple(d)]==tuple(u)
        # Normalize to the original h0 by the independently checked complete
        # all-paid algebra; this does not assume frozen owners are free.
        normalized,blocked=backward(D,U,h0,full);assert not blocked and set(normalized)==D
        assert all(normalized[d]==u for d,u in h0.items())
        bad=f['leaf_D_counterexamples']
        assert any((m['H'],m['Q'],len(m['branch']),m['z'])==(1,2,2,1) and len(m['leaf_before'])-len(m['leaf_after'])==1 for m in bad)
        if f.get('family')=='unbounded_zero_run':
            assert len(bad)==r-4 and len(frontier)==r-4
            assert [m['occurrences'][-1] for m in bad]==list(range(5*r+6,6*r+2))
        owner=f['owners'];owner_result=None
        if owner:
            fE=unpack(owner['fE']);a=unpack(owner['prior']);Eids={(t['occurrence'],j) for t in rows for j in range(1,t['qE']+1)}
            assert set(fE)==Eids and len(set(fE.values()))==len(Eids) and set(fE.values())<=U
            Ma={t['target'] for t in owner['auxiliary_rows'] if t['genuine_F']};assert Ma==M-{z} and len(Ma)==6
            assert len(core(E0,Ma))<=11
            C=D&Eids;l={d:fE[d] for d in C}
            # Independently reverse the ORIGINAL natural h0/common exchange.
            natural,_=backward(D,U,l,h0);assert natural==a
            partial,blocks=backward(D,U,a,h);assert blocks==unpack(owner['leaf_only_frontiers'])
            expected_frontier=(41,2) if f.get('family')=='unbounded_zero_run' else (39,2)
            assert blocks[(15,4)]==expected_frontier and (15,4) in {tuple(d) for deep in f['deep_packets'] for d in deep['natural_excess']}
            done,blocks2=backward(D,U,a,full);assert not blocks2 and done==unpack(owner['family_full_after_exchange'])
            assert all(done[d]==u for d,u in a.items()) and all(done[d]==fE[d] for d in C)
            owner_result={'actual_auxiliary_support':6,'auxiliary_core':len(core(E0,Ma)),'deep_root':[15,4],'branch_frontier':expected_frontier,'full_family_completion':True}
        reports.append({'family':f.get('family','fixed11_lower_padding'),'r':r,'reflected':f['mirrored'],'rows':len(rows),'A':f['A'],'QF':f['QF'],'QE':f['QE'],
            'full_and_erased_closure':True,'path_to_star_events':leaf_events,'raw_deep_packets':len(f['deep_packets']),
            'branch_frontier_size':len(frontier),'leaf_formula_refuted':True,'family_full_injection':True,'owners':owner_result})
    image_reports=audit_images(zero)
    out('independent_audit.json',{'status':'PASS_STATED_UNIFORM_PARTIAL_LEMMAS_FAMILY_PROOF_AND_EXACT_COUNTERCERTIFICATES','reports':reports,'owner_image_reports':image_reports,
        'source_engine_calls':calls,'kernel':'python/independent/splay.py','old_exhaustive_checks':'reused with exact pins; no CD6 reproof',
        'main_U_DEEP_GROUP':'OPEN_AFTER_FROZEN_OWNERS_AND_GENERAL_BRANCH_SUPPLY','Gate_U15':'U-OPEN',
        'trust':'same agent, distinct immutable rotations/marked-parent traversal and backwards owner components; not external/formal certification'})
    pins=json.loads((B/'dependency_pins.json').read_text())
    for p in pins['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    for p in pins['external_pins']:assert sha(Path(p['path']))==p['sha256'],p['path']
    git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
    assert not git('status','--porcelain','--untracked-files=no')
    assert not (B/'FULL_PROOF.md').exists()
    names=[p.name for p in sorted(B.glob('*.md'))]+['leaf_channels.py','audit_discovery2.py','leaf_source_certificates2.json','audit_zero_run.py','zero_run_source_certificates.json','audit_owner_images.py','owner_image_source_audit.json','audit_splice.py','splice_image_audit.json','audit_independent.py','independent_audit.json','dependency_ledger.json']
    out('partial_seal.json',{'status':'PROVED_UNIFORM_LEAF_CHANNEL_REDUCTION_AND_RESTRICTED_SOURCE_FAMILY_FUNDING',
        'principal_outcome':'UNRESOLVED','U15':'U-OPEN','inherited_U14':'U-B_UNCHANGED','CD6':'SEALED_UNCHANGED',
        'candidate_refutations':['plain marked-leaf signed debt','specified forward partial leaf-owner walk completes every deep root','fixed bounded-lookback branch repair using only candidate-unused bits'],
        'unrefuted_but_open':['unrestricted post-owner leaf-image capacity; seven finite erasures do not prove it'],
        'not_refuted':['U-DEEP-GROUP','Universal_Coarse_Double'],
        'Bank25':'UNCHANGED; no unproved universal native storage claim','inherited_local_pins_verified':len(pins['pins']),
        'files':[{'path':n,'sha256':sha(B/n)} for n in names]})
    print(json.dumps({'status':'PARTIAL_THEOREMS_AND_SOURCE_COUNTERCERTIFICATES_SEALED','reports':reports,'calls':calls,'principal':'UNRESOLVED','U15':'U-OPEN'}),flush=True)
def audit_images(zero):
    images=json.loads((B/'owner_image_source_audit.json').read_text());results=[]
    source0=zero['reports'][0];T=len(images['source_word']);base_rows=source0['rows'][:T];R0=tree(images['initial_A_BF']);href=unpack(source0['leaf_partial_h'])
    for f in images['reports']:
        E=R0;z=f['erased'];Einit=tree(f['rows'][0]['before'][2]);Ma=set(range(1,14,2))-{z}
        for u in range(f['u']):
            for mode,x in images['source_word']:
                if mode=='K' and x!=z:E=move(E,x)[0]
        assert E==Einit and f['L']==1
        for j,t in enumerate(f['rows']):
            old=base_rows[j%T]
            assert freeze(t['before'][:2])==freeze(old['before'][:2]) and freeze(t['after'][:2])==freeze(old['after'][:2])
            assert (t['a'],t['qF'])==(old['a'],old['qF']) and plain(E)==freeze(t['before'][2])
            ev=[]
            if t['mode']=='K' and t['target']!=z:E,ev=move(E,t['target'])
            assert plain(E)==freeze(t['after'][2]) and sum(v[0]!='ZIG' for v in ev)==t['qE']
            assert core(E,Ma)==core(Einit,Ma)
        assert E==Einit and len(core(E,Ma))==f['actual_auxiliary_core']<=11
        rr=f['rows'];D={(t['occurrence'],j) for t in rr for j in range(1,t['qF']+1)}
        U={(t['occurrence'],j,b) for t in rr for j in range(1,t['a']+1) for b in(0,1)}
        Eids={(t['occurrence'],j) for t in rr for j in range(1,t['qE']+1)}
        small=unpack(f['f6']);a=unpack(f['prior']);h=unpack(f['leaf_comparison_h']);assert h==href
        assert set(small)==Eids and len(set(small.values()))==len(small) and set(small.values())<=U
        C=D&Eids;l={d:small[d] for d in C};h0={}
        for m in source0['macros']:
            seg=[rr[i-1] for i in m['occurrences']]
            dd=[(t['occurrence'],j) for t in seg for j in range(1,t['qF']+1)]
            uu=[(t['occurrence'],j,b) for t in seg for j in range(1,t['a']+1) for b in(0,1)];h0.update(zip(dd,uu))
        prior,_=backward(D,U,l,h0);assert prior==a
        _,blocked=backward(D,U,a,h);assert blocked==unpack(f['partial_forward_blocks'])
        free=set(h.values())-set(a.values());assert free==set(map(tuple,f['candidate_free_image_units']))
        assert len(free)==f['candidate_free_image_count'] and len(D-set(a))==f['old_unpaid']
        candidate=unpack(f['candidate_completed_map']);assert set(candidate)==D and len(set(candidate.values()))==len(D) and set(candidate.values())<=U
        assert all(candidate[d]==u for d,u in a.items()) and all(candidate[d]==small[d] for d in C)
        results.append({'erased':z,'auxiliary_core':f['actual_auxiliary_core'],'old_unpaid':f['old_unpaid'],'free_image':len(free),'passes_this_source_only':True})
    splice=json.loads((B/'splice_image_audit.json').read_text())
    for report in splice['reports']:
        raw=json.loads((B/report['source']).read_text())
        f=next(f for f in raw['reports'] if f['r']==report['r'] and f['mirrored']==report['reflected'])
        hh=unpack(f['leaf_partial_h']);aa=unpack(f['owners']['prior']);free=set(hh.values())-set(aa.values())
        assert free==set(map(tuple,report['comparison_units_outside_old_image'])) and bool(free)==(not report['all_comparison_units_already_owned'])
    return results
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls,'new_finite_tests':4})
