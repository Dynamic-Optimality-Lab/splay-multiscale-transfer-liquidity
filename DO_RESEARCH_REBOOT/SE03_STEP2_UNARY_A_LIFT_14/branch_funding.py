"""Full actual-ID funding from audited source-uniform branch debt.
Own natural-macro values are fixed even inside a q5/q1 packet.
"""
import collections,functools,importlib.util,json,sys
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
sys.path.insert(0,str(OLD))
from source_funding import own_map,with_owners
from debt_funding import labels_core,normalize,freeze
s=importlib.util.spec_from_file_location('branch_funding_source14',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
P=importlib.util.module_from_spec(s);s.loader.exec_module(P)
@functools.lru_cache(None)
def table(k,marks):
    summary=json.loads((B/'branch_all_construction.json').read_text());row=next(r for r in summary['reports'] if r['core']==k and tuple(r['marks'])==marks)
    assert row['status']=='CANDIDATE_COMPLETE'
    c=json.loads((B/row['file']).read_text());G=json.loads((B/'branch_grammar2.json').read_text())
    assert (B/('audit_'+row['file'])).exists()
    ai={freeze(t):i for i,t in enumerate(G['states'])};bi={freeze(t):i for i,t in enumerate(c['BF_trees'])}
    roots=collections.defaultdict(list)
    for a,t in enumerate(G['states']):roots[t[0]//1000].append(a)
    pos={a:j for aa in roots.values() for j,a in enumerate(aa)};off=[];n=0
    for t in c['BF_trees']:off.append(n);n+=len(roots[marks.index(t[0])+1])
    assert n==len(c['debt']);return c,ai,bi,pos,off
def build(rows):
    assert rows[-1]['after']==rows[0]['before']
    M={r['target'] for r in rows if r['genuine_F']};S=labels_core(freeze(rows[0]['before'][1]),M);k=len(S)
    if len(M)!=6 or k not in (9,10,11):raise ValueError('exact six-mark core9..11 source required')
    mr={x:1000*(j+1) for j,x in enumerate(sorted(M))};sr={x:j+1 for j,x in enumerate(sorted(S))}
    mask=tuple(sorted(sr[x] for x in M));mirror=tuple(sorted(k+1-x for x in mask));flipped=mask>mirror;rep=mirror if flipped else mask
    c,ai,bi,pos,off=table(k,rep)
    def Aproject(t):
        if isinstance(t,str):return None
        l,r=Aproject(t[1]),Aproject(t[2])
        if t[0] in M:return (mr[t[0]],l,r)
        if l is None:return r
        if r is None:return l
        return (1000*sum(x<t[0] for x in M)+500,l,r)
    def reflectA(t):return None if t is None else (7000-t[0],reflectA(t[2]),reflectA(t[1]))
    def reflectB(t):return 'F'+str(k-int(t[1:])) if isinstance(t,str) else (k+1-t[0],reflectB(t[2]),reflectB(t[1]))
    def debt(A,F):
        a=Aproject(freeze(A));b=normalize(freeze(F),S)
        if flipped:a,b=reflectA(a),reflectB(b)
        return c['debt'][off[bi[b]]+pos[ai[a]]]
    v=own_map(rows);by={r['occurrence']:r for r in rows};packets=P.packets(rows);dd=[]
    for pp in packets:
        before=by[pp['occurrences'][0]]['before'];after=by[pp['occurrences'][-1]]['after']
        ds,dt=debt(before[0],before[1]),debt(after[0],after[1]);assert pp['w']+dt-ds>=0
        dd.append((ds,dt))
    top=max(ds for ds,dt in dd);cut=next(j for j,(ds,dt) in enumerate(dd) if ds==top)
    h=dict(v['h0']);bank=[];receipt=[];peak=0
    for j in range(len(packets)):
        i=(cut+j)%len(packets);pp=packets[i];ds,dt=dd[i];assert len(bank)==top-ds
        rr=[by[t] for t in pp['occurrences']]
        uu=[(r['occurrence'],e,b) for r in rr for e in range(1,r['a']+1) for b in (0,1)]
        demands=[(r['occurrence'],e) for r in rr for e in range(1,r['qF']+1)]
        owned={v['h0'][d] for d in demands if d in v['h0']};missing=[d for d in demands if d not in v['h0']]
        # Budget is 2min(H,4). Include ALL old natural owners, even a late
        # successor owner beyond the first four chronological A events.
        budget=2*min(pp['H'],4);assert len(owned)<=budget
        spare=[u for u in uu if u not in owned][:budget-len(owned)]
        assert len(owned)+len(spare)==budget
        pool=spare+bank;peak=max(peak,len(pool)+len(owned));assert len(pool)>=len(missing)+top-dt
        additions=[]
        for d in missing:u=pool.pop(0);h[d]=u;additions.append((d,u))
        bank=pool[:top-dt]
        receipt.append({'packet':i,'macro_indices':pp['macro_indices'],'occurrences':pp['occurrences'],'H':pp['H'],'Q':pp['Q'],'w':pp['w'],
            'D_before':ds,'D_after':dt,'selected_spares':spare,'fixed_own_units':sorted(owned),'new_pairs':additions,'carry':bank[:]})
    assert not bank and set(h)==v['D'] and len(set(h.values()))==len(h) and set(h.values())<=v['U']
    assert all(h[d]==u for d,u in v['h0'].items()) and peak<=11<=25
    v.update({'h':h,'packet_receipt':receipt,'full_cut_before_packet':cut,'max_debt_on_period':top,'working_units':peak,
        'global_working_bound':11,'core':k,'mask':mask,'reflected_certificate':flipped})
    return v
