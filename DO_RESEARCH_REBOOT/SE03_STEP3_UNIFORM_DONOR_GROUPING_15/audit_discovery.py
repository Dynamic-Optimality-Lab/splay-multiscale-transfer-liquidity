"""Source-exact campaign witnesses, not support sampling for a proof."""
import importlib.util,json,sys,time
from pathlib import Path
from leaf_channels import build,augment_partial,marked_tree
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent
s=importlib.util.spec_from_file_location('original_leaf15',P/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
sys.path.insert(0,str(P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14'))
from cd6_allocator import allocate
sys.path.insert(0,str(P/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'))
from source_funding import X
calls=0;original=p.trace
def trace(t,x):
    global calls
    calls+=1;assert calls<1900000;return original(t,x)
p.trace=trace
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def pack(m):return [{'demand':d,'unit':u} for d,u in sorted(m.items())]
def ser(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):ser(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [ser(x) for x in v]
    return v
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def gamma_word(r):
    marks=list(range(1,2*r,2));n=marks[-1];W=[('K',x) for x in marks[1:]+marks[-2::-1]]
    return W[:-1]+[('D',n),('D',1),('K',1),('K',n),('K',1)]+[('D',x) for x in (n,2,n,1)]+[('K',x) for x in marks[1:]+marks[-2::-1]]
def main():
    old=json.loads((P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/donor_rule_audit.json').read_text())['counterexamples'][0]
    base=old['source_period_rows'];assert freeze(base[0]['before'][0])==freeze(base[0]['before'][1])==p.vine(11)
    word0=[(z['mode'],z['target']) for z in base];reports=[]
    for r in (7,8):
        n=2*r-1;marks=set(range(1,n+1,2));pos=next(j for j,z in enumerate(word0) if z==('K',11))
        pulse=[('K',x) for x in list(range(13,n+1,2))+list(range(n-2,10,-2))]
        sigma=word0[:pos+1]+pulse+word0[pos+1:];word=gamma_word(r)+sigma
        for mirrored in (False,True):
            def mirror(t):return t if isinstance(t,str) else (n+1-t[0],mirror(t[2]),mirror(t[1]))
            initial=mirror(p.vine(n)) if mirrored else p.vine(n);ww=[(m,n+1-x if mirrored else x) for m,x in word];z=n-2 if mirrored else 3
            E=initial;seen={};u=0
            while E not in seen:
                assert u<50;seen[E]=u;u+=1
                for m,x in ww:
                    if m=='K' and x!=z:E=trace(E,x)[0]
            start=seen[E];L=u-start;E0=E
            rows,end=p.replay(initial,ww*L,erased=z,erased_start=E0);assert end==(initial,initial,E0)
            assert {x['target'] for x in rows if x['genuine_F']}==marks
            assert all(p.labels(p.core(row['before'][1],marks))==set(range(1,n+1)) for row in rows)
            v=build(rows,marks);bad=[e for e in v['macros'] if e['signed_leaf_residual']<0];assert bad
            owner=None
            if r==7:
                aux=[]
                for row in rows:
                    m='D' if row['mode']=='K' and row['target']==z else row['mode'];before=row['before'];after=row['after']
                    aux.append(dict(row,mode=m,genuine_F=m=='K' and before[2][0]!=row['target'],qF=row['qE'],qE=0,
                        before=(before[0],before[2],before[2]),after=(after[0],after[2],after[2])))
                fE=allocate(aux)['f'];Eids=set(fE);C=v['D']&Eids;l={d:fE[d] for d in C}
                prior=X.exchange(v['D'],v['U'],l,v['h0']);a=prior['allocation'];ext=augment_partial(v['D'],v['U'],a,v['h'])
                Rnat=v['D']-set(v['h0']);alpha={d:d if d in Rnat else prior['blocked'][d]['owner'] for d in v['D']-set(a)}
                deepR={tuple(d) for e in v['deep'] for d in e['natural_excess']}
                owner={'actual_f6_from_sealed_CD6':True,'auxiliary_rows':aux,'fE':pack(fE),'common':C,'prior':pack(a),
                    'additions':pack(ext['additions']),'final_partial':pack(ext['allocation']),'frontiers':pack(ext['blocked_frontier']),
                    'paths':ext['paths'],'old_unpaid':len(v['D']-set(a)),'remaining_unpaid':len(ext['blocked_frontier']),
                    'deep_anchored_old_unpaid':[d for d in alpha if alpha[d] in deepR],
                    'deep_anchored_blocked':[d for d in ext['blocked_frontier'] if alpha[d] in deepR]}
            report={'r':r,'mirrored':mirrored,'initial_A_BF':initial,'initial_BE':E0,'erased':z,'word':ww*L,'base_word':ww,
                'source_reaching_prefix_word_copies':start,'L':L,'rows':rows,'A':sum(z['a'] for z in rows),
                'QF':sum(z['qF'] for z in rows),'QE':sum(z['qE'] for z in rows),'maximal_full_core':n,
                'leaf_partial_h':pack(v['h']),'branch_frontier':v['R'],'channels':v['channels'],'macros':v['macros'],
                'deep_packets':v['deep'],'leaf_D_counterexamples':bad,'owners':owner}
            reports.append(report)
            print(json.dumps({'r':r,'mirror':mirrored,'length':len(rows),'deep':len(v['deep']),'leaf_law_failures':len(bad),'branch_slots':len(v['R']),
                'remaining_after_f6_exchange':owner['remaining_unpaid'] if owner else None,'deep_blocked':owner['deep_anchored_blocked'] if owner else None}),flush=True)
    out('leaf_source_certificates.json',ser({'status':'SOURCE_EXACT_PARTIAL_CHANNEL_AND_CANDIDATE_REFUTATION','reports':reports,
        'scope':'finite source-exact audits; universal lemmas are separate symbolic proofs, not extrapolated support tests',
        'no_CD_counterexample':True,'source_engine_calls':calls}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_discovery_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls,'new_finite_tests':4})
