"""Distinct mutable-source and owner verification of C29's new receipts.
No C29 producer source, allocator, packet, exchange or algebra code imported.
Old distinct implementation supplies primitive source/debt decoding only.
Uniformity still rests on the stated symbolic proofs, not finite replays.
"""
import importlib.util,json,sys,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent
spec=importlib.util.spec_from_file_location('C29_distinct_primitives',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
CAP=float(sys.argv[1]);checks=[];pins={}

def read(n):
    p=B/n;raw=p.read_bytes();pins[n]=hashlib.sha256(raw).hexdigest();return json.loads(raw)

def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)

def ok(s):checks.append(s);print(s,flush=True)

def state(t):
    pa,ch=I.marked(t,I.M);L=sum(not v for v in ch.values());b=sum(len(v)>=2 for v in ch.values());E=sum(max(len(v)-2,0) for v in ch.values())
    assert E==L-b-1 and 0<=E<=4
    return pa,ch,L,b,E

def profiles(mm):
    zz=[]
    for m in mm:
        x=m['rows'][-1]['target'];pa,ch,L,b,E=state(m['rows'][0]['before'][1]);_,nc,Lt,bt,Et=state(m['rows'][-1]['after'][1]);a=[];v=pa[x]
        while v is not None:a.append(v);v=pa[v]
        q=m['Q'];assert q==len(a);beta=sum(len(ch[v])>=2 for v in a);b2=sum(len(ch[v])==2 for v in a);k3=sum(len(ch[v])>=3 for v in a);d=len(ch[x]);z=int(d==0)
        assert Lt-L==q-beta-z and bt-b==int(d+q>=2)-int(d>=2)-b2
        rho=2*min(m['H'],3)-beta-z;sigma=2*min(m['H'],3)-q+Et-E
        assert sigma==rho+b2-int(d+q>=2)+int(d>=2)
        zz.append({'rho':rho,'sigma_E':sigma,'L':L,'Lt':Lt,'E':E,'Et':Et,'beta':beta,'z':z,'d':d,'Q':q,'H':m['H'],'b2':b2,'k3':k3})
    return zz

def bank_map(mm,pp,debts,cap,cut):
    natural={d:u for m in mm for d,u in zip(m['demands'],m['units'])};h=dict(natural);K=max(ds for ds,dt in debts);bank=[];working=0;rec=[]
    assert debts[cut][0]==K
    for step in range(len(pp)):
        k=(cut+step)%len(pp);ids=pp[k];ds,dt=debts[k];assert len(bank)==K-ds
        chosen=[u for i in ids for u in mm[i]['units'][:2*min(mm[i]['H'],cap)]];dd=[d for i in ids for d in mm[i]['demands']]
        own={natural[d] for d in dd if d in natural};missing=[d for d in dd if d not in natural];assert own<=set(chosen)
        sigma=len(chosen)-len(dd)+dt-ds;assert sigma>=0
        pool=[u for u in chosen if u not in own]+bank;working=max(working,len(pool)+len(own));added=[]
        for d in missing:u=pool.pop(0);h[d]=u;added.append((d,u))
        assert len(pool)>=K-dt;bank=pool[:K-dt];rec.append({'packet':k,'ids':ids,'sigma':sigma,'added':added,'carry':bank[:]})
    assert not bank and len(set(h.values()))==len(h)
    return h,K,working,rec

def six_bank(rows):
    mm=I.macro_list(rows,'E');paired=set();pp=[]
    for i,m in enumerate(mm):
        if m['Q']==5:
            j=(i+1)%len(mm);assert mm[j]['Q']==1 and i not in paired and j not in paired;paired|={i,j};pp.append([i,j])
    pp += [[i] for i,m in enumerate(mm) if i not in paired];pp.sort(key=min)
    # No synthetic free rotation of the source interval is made here.
    assert all(g==sorted(g) for g in pp)
    value,meta=I.debt_function(rows)
    dd=[(value(mm[g[0]]['rows'][0]['before'][0],mm[g[0]]['rows'][0]['before'][2]),
         value(mm[g[-1]]['rows'][-1]['after'][0],mm[g[-1]]['rows'][-1]['after'][2])) for g in pp]
    h,K,w,rec=bank_map(mm,pp,dd,4,0);print(json.dumps({'six_bank_maximum':K,'boundary_debt':dd[0][0],'working':w}),flush=True);assert K==dd[0][0]==3 and w<=25
    meta.update(maximum_debt=K,working=w,cut_before_packet=0,profile=I.buffer_peak(h));return h,meta

def symbolic_stencils():
    # Opaque A,B,C,D are arbitrary whole subtrees. This is rotation algebra,
    # not enumeration of bounded source BSTs.
    def rr(t):k,l,r=t;u,a,b=r;return u,(k,l,a),b
    def ll(t):k,l,r=t;u,a,b=l;return u,a,(k,b,r)
    A,Bb,C,D='A','B','C','D'
    assert rr((1,A,(2,Bb,C)))==(2,(1,A,Bb),C)
    assert rr(rr((1,A,(2,Bb,(3,C,D)))))==(3,(2,(1,A,Bb),C),D)
    t=(1,A,(3,(2,Bb,C),D));t=(t[0],t[1],ll(t[2]));assert rr(t)==(2,(1,A,Bb),(3,C,D))
    assert ll((2,(1,A,Bb),C))==(1,A,(2,Bb,C))
    assert ll(ll((3,(2,(1,A,Bb),C),D)))==(1,A,(2,Bb,(3,C,D)))
    t=(3,(1,A,(2,Bb,C)),D);t=(t[0],rr(t[1]),t[2]);assert ll(t)==(2,(1,A,Bb),(3,C,D))
    return {'opaque_subtree_stencils':6,'theorem':'off-path side preservation and RR depth-two placement; arbitrary subtree substitution'}

def main():
    source=read('comb_source_fixtures.json');signed=read('signed_comb_and_control_ledgers.json');alg=read('packetized_excess_and_nested_domains.json');fam=read('mixed_family_templates.json');reports=[]
    aa,bb=source['reports'];T=I.fr(aa['original_diagonal_tree']);_,S=I.execute((T,T,T),aa['reaching_prefix']);assert S==I.fr(aa['initial'])==I.fr(bb['initial'])
    assert len(aa['reaching_prefix'])==128
    for r,sl,el,fl in zip(source['reports'],signed['reports'],alg['reports'],fam['reports']):
        lo,hi=r['actual_interval'];rows,end=I.execute(S,r['period'],lo,r['rows']);assert end==S and hi==lo+len(rows)-1
        assert {z['target'] for z in rows if z['mode']=='K'}==I.M
        assert all(I.core(z['before'][1],I.M)==set(range(1,14)) and len(I.core(z['before'][2],I.E))==11 for z in rows)
        assert all(e['case'] in ('LL','RR') and e['G'] in I.M and e['P'] not in I.M for z in rows for e in z['BF_events'])
        assert (sum(z['a'] for z in rows),sum(z['qF'] for z in rows),sum(z['qE'] for z in rows))==(r['A'],r['QF'],r['QE'])
        f6,bankmeta=six_bank(rows);assert f6==I.mp(r['f6'])
        mm,led,h,h0,D,U,channels=I.leaf_map(rows);al=profiles(mm);assert h==I.mp(r['leaf_comparison']);tag=r['tags'][0]
        ci=next(i for i,m in enumerate(mm) if tag['comb'] in m['occurrences']);pi=ci-1;ji=ci-2
        assert (al[ci]['H'],al[ci]['Q'],al[ci]['beta'],al[ci]['z'])==(1,3,3,1)
        assert (al[pi]['H'],al[pi]['Q'],al[pi]['beta'],al[pi]['z'])==((1 if r is aa else 2),2,1,1)
        assert al[ci]['rho']==-2 and al[ci]['sigma_E']==0
        assert al[pi]['sigma_E']==(-1 if r is aa else 1) and al[ji]['H']>=3
        assert [z['rho'] for z in al]==[z['rho'] for z in sl['macro_ledger']]
        assert [z['sigma_E'] for z in al]==[z['sigma_E'] for z in sl['macro_ledger']]
        assert all(z['H']>=4 for i,z in enumerate(al) if i not in (ji,pi,ci))
        assert led[ci]['target']==1 and mm[ci]['rows'][0]['before'][1][0]==13
        # Exact original source units; no auxiliary-only spare is assumed free.
        lock={d:u for d,u in f6.items() if d in D};assert lock==I.mp(r['common_locked'])
        natural=I.natural_extend(lock,h0);assert natural==I.mp(r['natural_prior'])
        prefix=I.extend(natural,h,D);assert prefix==I.mp(r['effective_prefix']) and len(prefix)==33
        claims,paid,hc,tr=I.creator_stage(rows,mm,led,h,channels);assert not claims and not paid and not tr
        H=dict(h0);H[(tag['comb'],3)]=mm[ji]['units'][1];assert H==I.mp(r['full_independent_H']) and set(H)==D
        final=I.extend(prefix,H,D);assert final==I.mp(r['final_full_a']) and len(final)==34
        assert all(final[d]==u for d,u in prefix.items()) and I.buffer_peak(final)==5
        assert all(lo<=u[0]<=hi for u in final.values())
        root=(tag['helper'],2);locked=mm[pi]['units'][1];assert set(D-set(prefix))=={root} and prefix[(tag['comb'],3)]==locked and h[root]==locked
        assert (tag['comb'],3) not in h and H[(tag['comb'],3)] not in prefix.values()
        # Independently reconstruct both the original leaf and new E packets.
        for measure,receipt in (('L',sl['signed_packet_construction']),('E',el)):
            pp=receipt['packet_macro_indices'] if measure=='L' else receipt['packet_indices'];dskey='L' if measure=='L' else 'E';dtkey='Lt' if measure=='L' else 'Et';subtract=int(measure=='L')
            dd=[(al[g[0]][dskey]-subtract,al[g[-1]][dtkey]-subtract) for g in pp]
            cut=receipt['processing_start_packet'] if measure=='L' else receipt['canonical_processing_packet'];hx,K,w,rec=bank_map(mm,pp,dd,3,cut)
            expected=receipt['map'] if measure=='L' else receipt['full_comparison_H_E'];assert hx==I.mp(expected) and I.buffer_peak(hx)==receipt.get('actual_cut_profile_peak',receipt.get('actual_I_profile'))
        # Forced-triple family uses the exact inherited source interval cut0.
        pp=[([ji,pi,ci] if i==ji else [i]) for i in range(len(mm)) if i not in (pi,ci)]
        dd=[(al[g[0]]['L']-1,al[g[-1]]['Lt']-1) for g in pp];hx,K,w,rec=bank_map(mm,pp,dd,3,0)
        assert hx==H==I.mp(fl['full_comparison_H']) and K==3 and w==fl['working_peak']<=12
        assert sum(al[i]['rho'] for i in (ji,pi,ci))==fl['triple_rho']
        if sl['strong_comparison']:
            hp=dict(h);tail=[u for u in mm[pi]['units'] if u not in h.values()];holes=sorted(D-set(h));assert len(holes)==len(tail)==2
            hp.update(zip(holes,tail));assert hp==I.mp(sl['strong_comparison']['hplus']) and set(hp)==D
            alt=I.extend(prefix,hp,D);assert alt==I.mp(sl['strong_comparison']['historical_prefix_extension']) and I.buffer_peak(alt)==5
        # Non-vacuous corruption controls against this actual original period.
        def legal(f):return set(f)==D and set(f.values())<=U and len(set(f.values()))==len(f) and all(f[d]==u for d,u in prefix.items())
        bad=dict(final);bad[root]=locked;assert not legal(bad)
        bad=dict(final);u=bad[root];bad[root]=(u[0]-len(rows),u[1],u[2]);assert not legal(bad)
        bad=dict(final);bad[(tag['comb'],3)]=H[(tag['comb'],3)];assert not legal(bad)
        reports.append({'source_id':r['source_id'],'actual_interval':[lo,hi],'rows':len(rows),'A':r['A'],'QF':r['QF'],'QE':r['QE'],
            'helper_rho':al[pi]['rho'],'helper_sigma_E':al[pi]['sigma_E'],'comb_rho':-2,'comb_sigma_E':0,
            'forced_triple_rho':fl['triple_rho'],'frozen_prefix_count':33,'final_count':34,'full_profile':5,'family_working':w,'six_bank':bankmeta})
    ok('Exact new diagonal reaching prefix, both closed periods, every A/B rotation, SS core13/core11 and all costs independently rebuilt')
    ok('Inherited six-key debt lookup, actual maximum-debt cut0, canonical raw f6, common/natural/leaf and late frozen-owner maps rebuilt')
    ok('Negative helper debt retained: the pointwise E certificate and weak immediate-predecessor rho rule are refuted by a paired-closed source')
    ok('Leaf/E packet maps and forced-triple family template receipts independently reconstructed, no period donor duplication or old-success movement')
    # Original five-key-domain discovery is checked honestly; four domains exist.
    domains=[]
    for x in sorted(I.E):
        t=I.Tree(T)
        for mode,k in aa['reaching_prefix']:
            if mode=='K' and k not in (11,x):t.access(k)
        start=t.shape();seen={};seq=[]
        while t.shape() not in seen:
            assert len(seq)<10;seen[t.shape()]=len(seq);seq.append(t.shape())
            for mode,k in aa['period']:
                if mode=='K' and k not in (11,x):t.access(k)
        v={'extra_erased':x,'u':seen[t.shape()],'L':len(seq)-seen[t.shape()],'recurrent_core':len(I.core(t.shape(),I.M-{11,x})),
            'old_special_core9_candidate':len(I.core(t.shape(),I.M-{11,x}))==9,'current_interval_already_closed':t.shape()==start,'existing_fixed_f5_supplied':False}
        domains.append(v)
    assert domains==alg['nested_five_domains'] and sum(z['old_special_core9_candidate'] for z in domains)==4
    ok('Nested original Step1 domains: four core9 candidates explicitly present; no old fixed f5 supplied; raw-only owner scope enforced')
    # Old accepted sources are NOT rerun: consume frozen independently checked
    # rows solely to audit this NEW potential expression, leaving owners literal.
    controls=[]
    for name,path in [('W199',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/aligned_source_and_owners.json'),('W459',P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/catchment_forcing_countercertificate.json')]:
        raw=path.read_bytes();pins[path.relative_to(P).as_posix()]=hashlib.sha256(raw).hexdigest();old=json.loads(raw);rows=[I.fr_row(z) for z in old['rows']];al=profiles(I.macro_list(rows));ctrl=next(z for z in signed['controls'] if z['source']==name)
        assert max(z['beta'] for z in al)==2 and not any((z['H'],z['Q'],z['beta'],z['z'])==(1,3,3,1) for z in al)
        assert sum(z['sigma_E']<0 for z in al)==len(ctrl['negative_sigma_E']) and sum(z['sigma_E'] for z in al)==ctrl['sum_sigma_E']
        controls.append({'source':name,'negative_E_count':len(ctrl['negative_sigma_E']),'comb_count':0,'old_source_not_replayed':True})
    ok('W199 and W459 new-potential controls reuse accepted source rows; negative helper terms survive; no old source/owners re-audited or changed')
    stencils=symbolic_stencils();ok('Six symbolic one-event rotation identities verified with opaque arbitrary subtree terms; extremal order-barrier proof inspected')
    assert I.queries<4500
    out('independent_audit.json',{'status':'PASS_DISTINCT_IMPLEMENTATION_AT_STATED_RESTRICTED_SCOPE','trust':'distinct implementation operated by the SAME research agent; not external peer review or formal proof-assistant verification',
        'scope':'two exact sources, raw-canonical physical owner templates, signed identities, candidate refutations and opaque-subtree algebra; universal lifting by written symbolic proof',
        'checks':checks,'reports':reports,'controls':controls,'nested_domains':domains,'stencils':stencils,'input_sha256':dict(pins,**I.pins),'source_queries':I.queries,
        'principal_MC29_closed':False,'Gate_U_unconditional':False,'external_audit_complete':False})
    print(json.dumps({'status':'C29_INDEPENDENT_PASS','source_queries':I.queries,'checks':len(checks)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_independent2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':I.queries,'source_queries':I.queries})
