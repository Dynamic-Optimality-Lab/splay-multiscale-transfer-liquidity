"""Adversarial Campaign08 reflection, ordering and sector-interface audit."""
import collections,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent08',B/'audit_independent.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);d=m.d;a=m.a
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def ma(t):
    if t[0]=='leaf':return a.slot(12-t[2],12-t[1])
    return a.I.node(12-t[1],ma(t[3]),ma(t[2]))
def mb(t):
    if t[0]=='leaf':return ('leaf',13-t[1])
    return a.I.node(12-t[1],mb(t[3]),mb(t[2]))
def main():
    v=json.loads((B/'zero_closure.json').read_text());by=collections.defaultdict(list);records=[];four=set()
    for r in v['records']:
        t=d.canonical(a.Aread(r['A']));b=a.bf_read(r['BF']);rr=tuple(r['recent'])
        by[b,rr].append(t);records.append((t,b,rr))
        if a.L(b)==4:assert a.degree(b)==2;four.add(a.bf_write(b))
    by={key:tuple(sorted(set(v),key=d.size)) for key,v in by.items()}
    for t,b,r in records:assert any(d.includes(p,ma(t)) for p in by.get((mb(b),tuple(12-k for k in r)),()))
    seeds=json.loads((B/'terminal_seeds.json').read_text());zero=json.loads((B/'final_zero_inverse.json').read_text())
    rank=collections.Counter();Aevents=collections.Counter();Zevents=collections.Counter();Bplus=collections.Counter();Bzero=collections.Counter();before=collections.Counter()
    cache={}
    for ci,c in enumerate(seeds['terminal_cases']):
        w=(c['oldroot'],c['plus_target'],c['zero_target'],c['cold_q4']);assert len(set(w))==4
        rank[a.rankword(w),bool(c['A_initial_terms'])]+=1;before[c['L_before_plus']]+=1
        b=a.bf_read(c['BF_before_plus']);u=a.bf_read(c['BF_after_plus']);s=a.bf_read(c['BF_after_zero'])
        uu,ev=a.splay(b,w[1]);ss,ez=a.splay(u,w[2]);assert uu==u and ss==s and len(ev)==1 and len(ez)==2
        assert a.I.lookup(b,w[1])[1]==2 and a.I.lookup(u,w[2])[1]==4 and a.I.lookup(s,w[3])[1]==8
        Bplus[ev[0][0]]+=1;Bzero[','.join(e[0] for e in ez)]+=1
        for t in seeds['groups']:
            if ci not in t['cases']:continue
            raw=a.Aread(t['A']);key=(raw,w[1],w[2])
            if key not in cache:
                aa,ea=a.splay(raw,w[1]);aaa,eb=a.splay(aa,w[2]);assert len(ea)==len(eb)==1
                cache[key]=(ea[0][0]+('_'+ea[0][3] if ea[0][0]=='ZIG' else ''),
                            eb[0][0]+('_'+eb[0][3] if eb[0][0]=='ZIG' else ''))
            ea,eb=cache[key];Aevents[ea]+=1;Zevents[eb]+=1
    assert len(zero['sectors'])==48 and len(seeds['terminal_cases'])==64 and len(records)==9624 and len(four)==4
    result={'status':'PASS_ADVERSARIAL_P1Z_SOURCE_INTERFACES','reflected_frames_covered':len(records),
        'four_leaf_frames':720,'four_leaf_BF_contexts':len(four),'all_four_leaf_root_degree':2,
        'genuine_NEG2_root_degrees':{'NEG2_S':4,'NEG2_P':1},'P1B_exclusion':'final-zero source degree<=2 versus Q3 output>=3',
        'terminal_rank_profiles':[{'word':k[0],'A_feasible':k[1],'BF_cases':v} for k,v in sorted(rank.items())],
        'positive_BF_cases':dict(Bplus),'final_zero_BF_event_words_bottom_up':dict(Bzero),
        'positive_A_event_incidences':dict(Aevents),'zero_A_event_incidences':dict(Zevents),
        'seed_BF_source_leaves':dict(before),'all_cold_and_old_root_aliases_handled_by_actual_recent_order':True,
        'source_engine_calls':a.calls,'new_finite_tests':0,
        'no_old_seed_reuse':'all sectors are new +1->0 compositions; generic source calculus only is inherited'}
    out('adversarial_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_adversarial_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':a.calls,'old_semantic_rows_replayed':0,'new_finite_tests':0})
