"""Construct two selected lifetimes from separated zero-tail producer pairs."""
import collections,functools,json,pickle,sys,time
import audit_construct as C
B=C.B;p=C.p;L=C.L;M=C.M;V=C.V;START=time.process_time();CAP=float(sys.argv[1])
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    with (B/'product5_graph_cache.pkl').open('rb') as f:g=pickle.load(f)
    with (B/'product5_components.pkl').open('rb') as f:s=pickle.load(f)
    states=g['states'];adj=g['adj'];rev=g['rev'];parent=g['parent'];comp=s['components'];edges=[dict(a) for a in adj]
    @functools.lru_cache(None)
    def shape(t):return L.marked_tree(t,M)
    found=None;attempts=[]
    for critical in s['critical']:
        if critical['x']!=7:continue
        ci=critical['component'];back={critical['start']:None};queue=collections.deque(back)
        while queue:
            z=queue.popleft()
            for a,k in rev[z]:
                if a in back or comp[a]!=ci:continue
                par,ch=shape(states[a][0])
                if not ch[5] or not ch[9]:continue
                back[a]=(k,z);queue.append(a)
        for i,(bf,be) in enumerate(states):
            if bf[0]!=1 or comp[i]!=ci:continue
            a=i;ok=True;profile=[]
            for j,k in enumerate((3,13,5,11,5,7,9)):
                par,ch=shape(states[a][0]);v=par[k];anc=[]
                while v is not None:anc.append(v);v=par[v]
                beta=sum(len(ch[v])>=2 for v in anc);z=int(not ch[k])
                if j in (1,5) and beta+z<2:ok=False;break
                if j in (2,6) and (len(anc),beta,z)!=(2,2,1):ok=False;break
                if j>2 and not ch[5]:ok=False;break
                profile.append((k,len(anc),beta,z));a=edges[a].get(k)
                if a is None or comp[a]!=ci:ok=False;break
                if j>=2 and not shape(states[a][0])[1][5]:ok=False;break
            if ok and a in back:
                route=[];z=a
                while back[z] is not None:k,z=back[z];route.append(k)
                ret={critical['end']:None};queue=collections.deque(ret)
                while queue and i not in ret:
                    z=queue.popleft()
                    for k,v in adj[z]:
                        if v not in ret and comp[v]==ci:ret[v]=(z,k);queue.append(v)
                assert i in ret;returnword=[];z=i
                while ret[z] is not None:z,k=ret[z];returnword.append(k)
                returnword.reverse();reach=[];z=i
                while parent[z] is not None:z,k=parent[z];reach.append(k)
                reach.reverse();found={'initial_BF':bf,'initial_BE':be,'route':route,'return':returnword,
                    'reach':reach,'critical':critical,'profile':profile,'tour':g['tour'],'base_u':g['u']};break
        attempts.append({'critical':critical,'backward_states':len(back),'found':found is not None})
        if found:break
    out('separated_B_search.json',{'status':'ACTUAL_SOURCE_CONSTRUCTION_BRANCH','attempts':attempts,'found':found})
    if not found:
        print('NO_SEPARATED_PREFIX_IN_CURRENT_CLOSED_COMPONENT',flush=True);return
    a=V;bf=found['initial_BF'];be=found['initial_BE'];word=[];tags={}
    def add(mode,k,label=None):
        nonlocal a,bf,be
        if label:tags[label]=len(word)+1
        a,_,_=C.tr(a,k);word.append((mode,k))
        if mode=='K':
            bf,_,_=C.tr(bf,k)
            if k!=11:be,_,_=C.tr(be,k)
    def dels(ks):
        for k in ks:add('D',k)
    def pad():
        root=a[0];child=a[2] if p.node(a[2]) else a[1];y=child[0]
        for _ in range(2):add('D',y);add('D',root)
    dels((12,5,4,3,5,13,4,3));add('K',3,'prep_first')
    add('K',13,'producer13');add('K',5,'zero5');pad();add('K',11)
    dels(range(13,0,-1));dels((12,1,11,1,13,1,12,1,11,13,1));dels((7,5,11,13,1,5))
    add('K',5,'prep_second');add('K',7,'producer7');add('K',9,'zero9')
    for k in found['route']:pad();add('K',k)
    dels(range(13,0,-1));dels((12,1,11,1,13,1,12,1,11,13,1));dels((7,1,13,1))
    for label,k in zip(('j','h','g','s','t','v','p','e'),(13,1,13,11,1,13,1,7)):add('K',k,label)
    for k in found['return']:pad();add('K',k)
    dels(range(13,0,-1));assert (a,bf,be)==(V,found['initial_BF'],found['initial_BE'])
    rows,end=C.replay(V,bf,be,word);assert end==(V,bf,be)
    for label in ('producer13','zero5','producer7','zero9','h','g','s','t','v','p','e'):
        assert rows[tags[label]-1]['a']==1,(label,rows[tags[label]-1]['A_path'])
    assert [rows[tags[k]-1]['qE'] for k in ('v','p','e')]==[1,1,4]
    v,pp,pairs,transport=C.selection(rows);arrived=[z for z in transport if z['birth'][0]==tags['e']]
    assert len(arrived)==2 and {z['key'] for z in arrived}=={5,9},arrived
    reach=[('K',k) for k in found['tour']*found['base_u']+found['reach']]+[('D',k) for k in range(13,0,-1)]
    pr,pend=C.replay(V,V,V,reach);assert pend==(V,bf,be)
    assert {r['target'] for r in rows if r['genuine_F']}==M
    out('construction_candidate.json',{'status':'GUARDED_SOURCE_CONSTRUCTION_PENDING_BACKEND_AND_INDEPENDENT_AUDIT',
        'original_common_tree':V,'original_reaching_prefix':reach,'period':word,'initial_A':V,'initial_BF':bf,'initial_BE':be,
        'rows':rows,'tags':tags,'route':found['route'],'return':found['return'],'x':7,'full_marks':sorted(M),'erased':11,
        'auxiliary_core':len(p.labels(p.core(be,C.E))),'creator_pairs':pairs,'creator_claims':pp['claims'],
        'selected_transports':transport,'selected_at_e':arrived,'physical_owner_receipt':'PENDING','independent_audit':False,
        'source_engine_calls':C.calls,'source_queries':C.queries})
    print(json.dumps({'status':'GUARDED_SOURCE_CANDIDATE_FOUND','length':len(word),'tags':tags,'selected_at_e':arrived,
        'auxiliary_core':len(p.labels(p.core(be,C.E))),'route':found['route'],'return':found['return']}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_separated_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,
        'source_engine_calls':C.calls,'source_queries':C.queries})
