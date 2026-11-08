"""Actual closed two-slot words, all six erased executions and physical IDs.
Owner placements are logical adversarial injections, NOT numerical fE claims.
"""
import collections,importlib.util,json,time
from pathlib import Path
from two_slot_allocator import independent_full,from_frozen_auxiliary,extend_two
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('source01_two_slots',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
calls=0;orig=p.trace
def trace(t,x):
    global calls
    calls+=1;assert calls<500000;return orig(t,x)
p.trace=trace
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def serial(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [serial(x) for x in v]
    return v
def enlarged(t):
    if not isinstance(t,str):return (16*t[0],enlarged(t[1]),enlarged(t[2]))
    g=int(t[1:]);return (16*g+8,(16*g+4,'G'+str(g)+'a','G'+str(g)+'b'),(16*g+12,'G'+str(g)+'c','G'+str(g)+'d'))
def reflect(t,ceiling):
    if isinstance(t,str):return 'R'+t
    return (ceiling-t[0],reflect(t[2],ceiling),reflect(t[1],ceiling))
def e_recurrent(R,word,z):
    E=R;seen={};states=[]
    while E not in seen:
        assert len(states)<12
        seen[E]=len(states);states.append(E)
        for mode,x in word:
            if mode=='K' and x!=z:E=trace(E,x)[0]
    assert len(states)-seen[E]==1,'source requires larger actual alignment: do not divide slots'
    return E,seen[E]
def owner_maps(E,D,U,h,h0,R):
    ds=sorted(E);us=sorted(U)
    for k in range(min(len(us),8)):
        yield 'cyclic_aux_ID_placement_'+str(k),dict(zip(ds,us[k:]+us[:k]))
    C=D&E;L={d:h[d] for d in C}
    for blocked in (0,1,2):
        rr=sorted(R&C)[:blocked];pp=sorted(set(h0)-C)
        if len(rr)!=blocked or len(pp)<blocked:continue
        locked={d:h0[q] for d,q in zip(rr,pp)};used=set(locked.values())
        for d in sorted(C-set(locked)):
            v=h[d] if h[d] not in used else next(u for u in us if u not in used)
            locked[d]=v;used.add(v)
        f=dict(locked)
        for d in sorted(E-C):
            v=next(u for u in us if u not in used);f[d]=v;used.add(v)
        yield 'common_seed_forced_blocked_'+str(blocked),f
def main():
    old=json.loads((B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/deficient_source_schemas.json').read_text())
    base=next(f for f in old['families'] if f['core']==7);root=freeze(base['initial_A_BF'])
    raw=[tuple(v) for v in base['word']]*2;families=[];branches=collections.Counter();tests=0
    for variant in ('plain','early_DELETE_and_root_repeats','private_gaps','private_helper_excursion'):
        ext=variant.startswith('private');R0=enlarged(root) if ext else root
        word=[(m,16*x if ext else x) for m,x in raw]
        if variant=='early_DELETE_and_root_repeats':
            word=[v for m,x in word for v in ([('D',x),('K',x),('K',x)] if m=='K' else [(m,x)])]
        if variant=='private_helper_excursion':
            helper=R0[1][0];assert helper==8
            word=[('D',helper),('D',R0[0])]+word
        for mirror in (False,True):
            ceiling=128 if ext else 8
            T0=reflect(R0,ceiling) if mirror else R0
            ww=[(m,ceiling-x if mirror else x) for m,x in word]
            marks={x for m,x in ww if m=='K'};assert len(marks)==6
            for z in sorted(marks):
                E0,u=e_recurrent(T0,ww,z)
                rows,end=p.replay(T0,ww,erased=z,erased_start=E0);assert end==(T0,T0,E0)
                assert {r['target'] for r in rows if r['genuine_F']}==marks
                assert all(len(p.labels(p.core(r['before'][1],marks)))==7 for r in rows)
                build=independent_full(rows);D,U=build['D'],build['U'];E={(r['occurrence'],k) for r in rows for k in range(1,r['qE']+1)}
                fixtures=[]
                for name,fE in owner_maps(E,D,U,build['h'],build['h0'],build['R']):
                    r=from_frozen_auxiliary(rows,fE);ex=r['extension'];a=r['prior']['allocation']
                    assert ex['allocation']==r['licensed']['allocation'] and len(set(ex['additions'].values()))==len(ex['missing'])
                    n=len(ex['missing']);branches[str(n)]+=1
                    if any(p!=r['anchors'][p] for p in ex['missing']):branches['blocked_nonanchor_root']+=1
                    fixtures.append({'label':name,'status':'logical injection on actual source IDs, not numerical sealed fE',
                        'fE':pack(fE),'common':r['common'],'full_only':r['full_only'],'auxiliary_only':r['auxiliary_only'],
                        'paid':pack(a),'anchors':pack(r['anchors']),'uncovered':ex['missing'],'Wstar':U-set(a.values()),
                        'partial_paths':r['prior']['paths'],'blocked':list(r['prior']['blocked'].items()),
                        'extension_paths':ex['paths'],'additions':pack(ex['additions']),'final':pack(ex['allocation']),
                        'licensed_paths':r['licensed']['paths']})
                    tests+=1
                families.append({'variant':variant,'reflected':mirror,'initial_A_BF':T0,'initial_BE':E0,
                    'erased':z,'alignment':{'u':u,'L':1,'word_length':len(ww),'slot_count_before_division':2},
                    'word':ww,'marks':marks,'rows':rows,'charts':p.charts(rows,marks),
                    'macros':build['macros'],'R':build['R'],'seed_receipts':build['seeds'],
                    'h0':pack(build['h0']),'independent_h':pack(build['h']),
                    'positive_surplus':build['source_positive_surplus'],'fixtures':fixtures,
                    'actual_fE':'universal supplied certified input, never guessed from these fixtures'})
    assert set(('0','2'))<=set(branches)
    # Repeating the same closed word makes the two actual erased sectors
    # symmetric. Do not assert asymmetric partial branches are realized.
    p0=sorted(build['R'])[0];a0={d:u for d,u in build['h'].items() if d!=p0}
    one=extend_two(D,U,a0,build['h']);assert len(one['missing'])==1
    one_control={'kind':'source-ID one-hole paid fixture, not claimed to be the partial10 map for this word',
        'paid':pack(a0),'missing':p0,'extension':pack(one['additions']),'paths':one['paths']}
    tests+=1
    out('physical_receipts2.json',serial({'status':'PASS_CLOSED_SOURCE_TWO_SLOT_PHYSICAL_RECEIPTS','families':families,
        'families_count':len(families),'owner_fixture_count':tests,'branches':dict(branches),'one_residual_paid_control':one_control,
        'actual_partial_branch_limit':'these repeated-word erased sectors realize zero/two symmetrically; general one/blocked cases audited separately',
        'source_engine_calls':calls,'new_finite_tests':tests,
        'source_scope':'four exact actual words and reflections, all six erased recurrences; free-gap proof supplies universal lifting',
        'fixture_scope':'logical owner maps test interface only; no proof of numeric sealed fE realization'}))
    print(json.dumps({'status':'PASS','source_families':len(families),'fixtures':tests,'branches':dict(branches),'calls':calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_construction2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
