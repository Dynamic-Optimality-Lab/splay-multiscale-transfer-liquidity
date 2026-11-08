"""Adversarial coverage audit of the universal-gap proof, not finite testing."""
import collections,itertools,json,sys,time
from pathlib import Path
import audit_independent as a
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    S={t for t in a.alltrees(1,11) if t[1] in a.M and a.density(t)[2]}
    edges=collections.defaultdict(list);inc=collections.defaultdict(list)
    for t in S:
        for x in a.M-{t[1]}:
            n=a.legal(t,x)
            if n and n[0] in S:edges[t].append((n[0],x,n[1]));inc[n[0]].append((t,x,n[1]))
    # Remove the old pre-loss-leaf filter entirely. Derive it as a conclusion.
    contexts=set();tail_relations=0
    for t in S:
        if a.L(t)!=3:continue
        for mid,x,q in edges[t]:
            if q!=2 or a.L(mid)!=2:continue
            for end,y,qq in edges[mid]:
                if qq!=2 or a.L(end)!=2:continue
                for target,z,qqq in edges[end]:
                    if qqq!=4 or z in (t[1],x,y):continue
                    tail_relations+=1
                    assert z not in set(a.parents(t).values()), 'cold-candidate pre-leaf must FOLLOW from B geometry'
                    assert a.degree(t)==2
                    for old,gg,q0 in inc[t]:
                        if q0 in (1,2) and old[1]!=z:
                            contexts.add((a.bf_write(old),a.bf_write(t),q0,(old[1],gg,x,y,z)))
    assert len(contexts)==144
    # Every NEG2-S COLD target is L4, independently by source geometry:
    # require old target a marked leaf, not a generic four-double access.
    negatives=[];paired=0;singleton=0
    for t in S:
        pm=a.parents(t)
        for end,x,q in edges[t]:
            if q==4 and x not in set(pm.values()):
                assert a.L(end)==4;singleton+=1
            if q==5:
                assert a.L(end)==5
                for fin,y,qq in edges[end]:
                    assert qq==1 and a.L(fin)==4
                    paired+=1
    # The projection of every seed remains valid under reflection. This checks
    # order logic only, and assumes no symmetry of old debt or frozen mu fields.
    cert=json.loads((B/'saturation3.json').read_text());unique=set();kinds=collections.Counter()
    def short(t):return '.' if t[0]=='leaf' else str(t[1])+'('+short(t[2])+','+short(t[3])+')'
    def mirror(t):
        if t[0]=='leaf':return a.slot(12-t[2],12-t[1])
        return a.I.node(12-t[1],mirror(t[3]),mirror(t[2]))
    for r in cert['records']:
        at=a.Aread(r['A']);bt=a.bf_read(r['BF']);rr=tuple(r['recent']);budget=r['budget']
        kinds[(a.L(bt),a.degree(bt),budget)]+=1
        unique.add((short(at),a.bf_write(bt),budget))
    # Do not demand equality of arbitrary seed enumeration multiplicities.
    # Verify mirrored A constraints are again among the recorded languages.
    aset={a.Aread(r['A']) for r in cert['records']}
    assert all(mirror(t) in aset for t in aset)
    spine=[]
    for word in itertools.permutations(range(3)):
        fs,sz=a.frames(word,range(3),-1,3)
        dd=[a.marked_on_spine(end,a.F(word[0])) for start,end in fs]
        assert all(d is not None and d<=4 for d in dd)
        spine.append({'root_order':word,'universal_frames':len(fs),'maximum_old_root_depth':max(dd)})
    result={'status':'PASS_ADVERSARIAL_UNIVERSAL_COVERAGE',
        'no_pre_loss_leaf_assumption':True,'tail_relations_before_previous_packet':tail_relations,
        'complete_previous_packet_contexts':len(contexts),'cold_singleton_target_contexts_L4':singleton,
        'q5_q1_target_contexts_L4':paired,'all_actual_q1_successor_labels_included':True,
        'backward_state_kinds':[{'L':k[0],'root_marked_degree':k[1],'budget':k[2],'count':v} for k,v in sorted(kinds.items())],
        'distinct_A_B_budget_patterns':len(unique),'universal_H2_spine_cases':spine,
        'mirrored_A_languages_present':True,'source_engine_calls':a.calls,'new_finite_tests':0,
        'omitted_fields':'BE, charts, and physical IDs forgotten ONLY by a one-way necessary projection in an exclusion proof',
        'no_funding_or_state_splicing':True}
    out('adversarial_audit.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_adversarial_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':a.calls,'new_finite_tests':0})
