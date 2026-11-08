"""Realize one saved closed B source with exact separated zero-tail A producers."""
import json,sys,time
import audit_construct as C
B=C.B;p=C.p;V=C.V;M=C.M
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(t):return tuple(freeze(x) for x in t) if isinstance(t,list) else t
def main():
    r=json.loads((B/'backward_source_skeletons.json').read_text())['answers'][0]
    prefix=r['prefix_keep_word'];assert prefix[:6]==[1,7,9,7,3,5] and r['critical']['x']==7
    initialBF=freeze(r['initial_BF']);initialBE=freeze(r['initial_BE']);a=V;bf=initialBF;be=initialBE;word=[];tags={}
    def add(mode,x,label=None):
        nonlocal a,bf,be
        if label:tags[label]=len(word)+1
        a,_,_=C.tr(a,x);word.append((mode,x))
        if mode=='K':
            bf,_,_=C.tr(bf,x)
            if x!=11:be,_,_=C.tr(be,x)
    def dels(xs):
        for x in xs:add('D',x)
    def prep(tail):
        dels(range(13,0,-1));dels((12,1,11,1,13,1,12,1,11,13,1));dels(tail)
    def pad():
        root=a[0];y=(a[2] if p.node(a[2]) else a[1])[0]
        for _ in range(2):add('D',y);add('D',root)
    prep((7,1,13,11,1));add('K',1,'gap1')
    add('K',7,'producer7');add('K',9,'zero9')
    prep((7,1,13,1,3,7));add('K',7,'gap7')
    add('K',3,'producer3');add('K',5,'zero5')
    for x in prefix[6:]:pad();add('K',x)
    prep((7,1,13,1))
    for label,x in zip(('j','h','g','s','t','v','p','e'),(13,1,13,11,1,13,1,7)):add('K',x,label)
    for x in r['return']:pad();add('K',x)
    dels(range(13,0,-1));assert (a,bf,be)==(V,initialBF,initialBE)
    rows,end=C.replay(V,initialBF,initialBE,word);assert end==(V,initialBF,initialBE)
    for k in ('producer7','zero9','producer3','zero5','h','g','s','t','v','p','e'):
        assert rows[tags[k]-1]['a']==1,(k,rows[tags[k]-1]['A_path'])
    assert [rows[tags[k]-1]['qE'] for k in ('v','p','e')]==[1,1,4]
    v,profile,pairs,transport=C.selection(rows)
    arrived=[z for z in transport if z['birth'][0]==tags['e']]
    assert len(arrived)==2 and {z['key'] for z in arrived}=={5,9},arrived
    for name in ('producer7','producer3'):
        m=next(m for m in v['macros'] if tags[name] in m['occurrences'])
        assert m['H']==1 and len(m['branch'])+m['z']>=2
    for label,producer in (('zero9','producer7'),('zero5','producer3')):
        cl=next(c for c in profile['claims'] if c['frontier']==(tags[label],2))
        assert cl['creator']['source_occurrence']==tags[producer]
    reaching=[('K',x) for x in r['tour']*r['base_u']+r['reach']]+[('D',x) for x in range(13,0,-1)]
    _,reach_end=C.replay(V,V,V,reaching);assert reach_end==(V,initialBF,initialBE)
    assert {t['target'] for t in rows if t['genuine_F']}==M
    out('construction_candidate.json',{'status':'EXACT_GUARDED_SOURCE_CONSTRUCTION_OWNERS_AND_INDEPENDENT_AUDIT_PENDING',
        'original_common_tree':V,'original_reaching_prefix':reaching,'period':word,'initial_A':V,'initial_BF':initialBF,
        'initial_BE':initialBE,'rows':rows,'tags':tags,'x':7,'full_marks':sorted(M),'erased':11,
        'auxiliary_core':len(p.labels(p.core(initialBE,C.E))),'creator_pairs':pairs,'creator_claims':profile['claims'],
        'selected_transports':transport,'selected_at_e':arrived,'physical_owner_receipt':'PENDING','independent_audit':False,
        'source_engine_calls':C.calls,'source_queries':C.queries})
    print(json.dumps({'status':'EXACT_SOURCE_CANDIDATE_FOUND','operations':len(word),'tags':tags,
        'selected_at_e':arrived,'auxiliary_core':len(p.labels(p.core(initialBE,C.E))),
        'source_engine_calls':C.calls,'source_queries':C.queries}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_realize_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries})
