"""Bounded new source schemas, physical packet supply and deficient cases.
All traces use arbitrary rigid gap BST variables; concrete population tests
are not used to promote any arbitrary-history theorem.
"""
import collections,importlib.util,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('source01',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
started=time.process_time();calls=0;CAP=min(25,float(sys.argv[1])-4)
original=p.trace
def trace(t,x):
    global calls
    calls+=1;assert time.process_time()-started<CAP and calls<1000000
    return original(t,x)
p.trace=trace
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def shape(n,marks):
    h=marks[1];last=n
    word=[('K',h),('D',n),('D',1),('K',1),('K',n),('K',1)]
    word += [('K',x) for x in marks[1:]]+[('K',x) for x in marks[-2::-1]]
    word += [('D',x) for x in range(n,0,-1)]
    return word
def align(R,word,z):
    E=R;seen={};states=[]
    for u in range(16):
        if E in seen:
            j=seen[E];return j,u-j,states[j]
        seen[E]=u;states.append(E)
        for mode,x in word:
            if mode=='K' and x!=z:E=trace(E,x)[0]
    return None
def main():
    trials=[];families=[]
    for c in range(6,12):
        accepted=[]
        for gaps in itertools.combinations(range(5),c-6):
            marks=[1]
            for j in range(5):marks.append(marks[-1]+1+int(j in gaps))
            assert marks[-1]==c
            R=p.vine(c);word=shape(c,marks);rows,end=p.replay(R,word)
            closed=end[0]==end[1]==R
            trial={'core':c,'marks':marks,'closed':closed,'first_A_B_equal':True}
            if closed:
                assert all(p.labels(p.core(r['before'][1],set(marks)))==set(range(1,c+1)) for r in rows)
                ps=p.packets(rows);bad=[v for v in ps if v['Q']>2*v['H']]
                trial['deficit_packets']=[{'H':v['H'],'Q':v['Q'],'w':v['w'],'end':v['end']} for v in bad]
                accepted.append((marks,word,rows,ps,bad))
            trials.append(trial)
        if not accepted:continue
        marks,word,rows,ps,bad=next((v for v in accepted if v[-1]),accepted[0])
        R=p.vine(c);erasure=[]
        for z in marks:
            al=align(R,word,z)
            if al is None:erasure.append({'erased':z,'status':'BOUNDED_NO_RECURRENCE_CERTIFICATE'});continue
            u,L,E=al
            rr,end=p.replay(R,word*L,erased=z,erased_start=E)
            assert end==(R,R,E)
            ec=len(p.labels(p.core(E,set(marks)-{z})))
            erasure.append({'erased':z,'status':'EXACT_SOURCE_ALIGNMENT','u':u,'L':L,'initial_BE':E,
                'aux_core':ec,'QE':sum(r['qE'] for r in rr),'cost_period_multiplier':L})
        families.append({'name':'core'+str(c)+'_source','core':c,'marks':marks,'initial_A_BF':R,
            'word':word,'rows':rows,'packets':ps,'deficit_packets':bad,'charts':p.charts(rows,marks),
            'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),
            'full_closure':True,'all_gaps':'independent arbitrary ordered BSTs F0..Fc',
            'erasure_alignments':erasure})
    core6=next(v for v in families if v['core']==6)
    h={};units=set();demands=set()
    for r in core6['rows']:
        for j in range(1,r['a']+1):
            for bit in (0,1):units.add((r['occurrence'],j,bit))
        for k in range(1,r['qF']+1):demands.add((r['occurrence'],k))
    for packet in core6['packets']:
        aa=[u for t in packet['occurrences'] for u in sorted(units) if u[0]==t]
        dd=[d for t in packet['occurrences'] for d in sorted(demands) if d[0]==t]
        assert len(dd)<=len(aa)
        h.update(zip(dd,aa))
    assert set(h)==demands and len(set(h.values()))==len(h)
    out('core6_physical_receipt.json',{'status':'COMPLETE_THIS_SYMBOLIC_SOURCE','domain':'one explicit arbitrary-gap source family',
        'allocation':[{'demand':d,'unit':u} for d,u in sorted(h.items())],
        'unused_units':sorted(units-set(h.values())),'no_source_unit_reused':True,
        'universal_core6_theorem':'separate analytic per-macro Q<=2,H>=1 proof, not inference from this receipt'})
    out('deficient_source_schemas.json',{'status':'EXACT_SYMBOLIC_SOURCE_SCHEMAS_NOT_A_GLOBAL_FUNDING_PROOF',
        'trials':trials,'families':families,'source_engine_calls':calls,
        'coverage_limit':'32 specified free-gap words; source identities universal over gaps, not all histories',
        'new_finite_tests':len(trials)})
    print(json.dumps({'status':'PASS','source_engine_calls':calls,'trials':len(trials),
        'families':[{'core':v['core'],'marks':v['marks'],'A':v['A'],'QF':v['QF'],
            'negative_packets':[(x['H'],x['Q'],x['w']) for x in v['deficit_packets']],
            'aux_core_sizes':[x.get('aux_core') for x in v['erasure_alignments']]} for v in families]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_sources_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':calls,'new_finite_tests':32})
