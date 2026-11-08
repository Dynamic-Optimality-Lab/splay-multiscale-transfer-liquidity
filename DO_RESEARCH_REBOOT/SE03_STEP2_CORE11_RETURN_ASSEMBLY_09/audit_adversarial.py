"""New09 reflection, actual paired chronology, aliases and order coverage.
All source terms have arbitrary ordered private slots; no population test.
"""
import collections,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('checker09',B/'audit_independent.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);a=m.a;d=m.d
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def ma(t):
    if t[0]=='leaf':return a.slot(12-t[2],12-t[1])
    return a.I.node(12-t[1],ma(t[3]),ma(t[2]))
def mb(t):
    if t[0]=='leaf':return ('leaf',13-t[1])
    return a.I.node(12-t[1],mb(t[3]),mb(t[2]))
def main():
    cert=json.loads((B/'zero_closure.json').read_text());by=collections.defaultdict(list)
    for v in cert['records']:
        t=d.canonical(a.Aread(v['A']));b=a.bf_read(v['BF']);r=tuple(v['recent'])
        by[b,r].append(t)
    by={k:tuple(sorted(set(v),key=d.size)) for k,v in by.items()}
    for (b,r),terms in by.items():
        for t in terms:assert any(d.includes(p,ma(t)) for p in by[mb(b),tuple(12-k for k in r)])
    pair=json.loads((B/'paired_destination_seeds.json').read_text());seed=json.loads((B/'terminal_seeds.json').read_text())
    pairkeys=set();rank=collections.Counter();Aev=collections.Counter();Bev=collections.Counter();miss=0;chronology=0
    for v in pair['sectors']:
        f,mid,end=(a.bf_read(v[k]) for k in ('BF_before_pair','BF_between_macros','BF_after_pair'))
        x,z=v['first_target'],v['actual_successor'];key=(f,mid,end,x,z);pairkeys.add(key)
        mm,ee=a.splay(f,x);e,ff=a.splay(mid,z)
        assert mm==mid and e==end and len(ee)==5 and len(ff)==1
        assert all(k[0] in ('LL','RR') for k in ee+ff)
        assert a.I.lookup(f,x)[1]==10 and a.I.lookup(mid,z)[1]==2
        Bev[','.join(k[0] for k in ee)+'|'+ff[0][0]]+=1
        if v['successor_is_chart_miss']:miss+=1
        for raw in v['A_before_pair_terms']:
            t=a.Aread(raw);assert t[1]==f[1]
            u,one=a.splay(t,x);w,two=a.splay(u,z)
            assert len(one)==len(two)==1 and u[1]==x and w[1]==z
            Aev[one[0][0]+','+two[0][0]]+=1;chronology+=1
    for f,mid,end,x,z in pairkeys:assert (mb(f),mb(mid),mb(end),12-x,12-z) in pairkeys
    casekeys=set();aliases=collections.Counter();plusA=collections.Counter();sourceinc=0
    for ci,c in enumerate(seed['terminal_cases']):
        word=(c['oldroot'],c['plus_target'],c['first_target'],c['actual_successor'])
        assert len(set(word)) in (3,4);aliases[c['alias']]+=1;rank[a.rankword(word)]+=1
        bf=tuple(a.bf_read(c[k]) for k in ('BF_before_plus','BF_before_pair','BF_between_macros','BF_after_pair'))
        cur=bf[0]
        for j,target in enumerate(word[1:],1):
            cur,ev=a.splay(cur,target);assert cur==bf[j] and len(ev)==(5 if j==2 else 1)
        casekeys.add((bf,word))
        for v in seed['groups']:
            if ci not in v['cases']:continue
            cur=a.Aread(v['A']);assert cur[1]==word[0]
            for j,target in enumerate(word[1:],1):
                cur,ev=a.splay(cur,target);assert len(ev)==1
                plusA[j,ev[0][0]]+=1
            sourceinc+=1
    for bf,word in casekeys:assert (tuple(mb(t) for t in bf),tuple(12-k for k in word)) in casekeys
    result={'status':'PASS_REFLECTION_PAIRED_CHRONOLOGY_AND_ALIAS_COVERAGE',
        'reflected_backward_records':len(cert['records']),'reflected_paired_sectors':len(pairkeys),
        'reflected_plus1_compositions':len(casekeys),'paired_successor_chart_miss_sectors':miss,
        'paired_A_two_actual_events_incidences':chronology,'paired_A_event_types':dict(Aev),'paired_BF_event_words':dict(Bev),
        'source_seed_three_actual_events_incidences':sourceinc,
        'three_event_A_kinds':[{'position':k[0],'kind':k[1],'incidences':v} for k,v in sorted(plusA.items())],
        'rank_profiles':[{'root_word':k,'BF_cases':v} for k,v in sorted(rank.items())],
        'aliases':dict(aliases),'private_gap_reflection':'all intervals reversed, fixed Score k->12-k, ordered roles relabeled',
        'DELETE_or_KEEP_event_timing':'same endpoint splay and same one-event count; original regular source words preserved',
        'source_engine_calls':a.calls,'new_finite_tests':0}
    out('adversarial_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('rank_profiles','paired_A_event_types','paired_BF_event_words','three_event_A_kinds')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_adversarial_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':a.calls,'new_finite_tests':0})
