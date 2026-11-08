"""Actual diagonal-reaching prefix and mixed-cost A-core6/core9 sources."""
import collections,hashlib,importlib.util,json,time
from pathlib import Path
from a_core6_funding import build
from source_funding import with_owners
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
I=load('immutable_A6_period13',ROOT/'python/independent/splay.py')
P=load('original_A6_period13',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py');calls=0
def move(t,x):
    global calls
    calls+=1;assert calls<1800000 and I.lookup(t,x)[0];return I.trace(t,x)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def tree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],tree(t[1]),tree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def ser(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):ser(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [ser(x) for x in v]
    return v
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def run(t,word,erased=None):
    for m,x in word:
        if m=='K' and x!=erased:t=move(t,x)[0]
    return t
def main():
    ref=json.loads((B/'bf_source_refinement.json').read_text())['reports'][0];M=ref['marks'];R=tree(ref['initial_A_BF']);W=[tuple(v) for v in ref['source_word']]
    def gap(j):
        lo=M[j-1] if j else 0;hi=M[j] if j<6 else 10;t=('leaf','F'+str(hi-1))
        for x in range(hi-1,lo,-1):t=I.node(x,('leaf','F'+str(x-1)),t)
        return t
    def marked(lo,hi,root=None):
        if lo>hi:return gap(hi+1)
        j=(lo+hi)//2 if root is None else root
        return I.node(M[j],marked(lo,j-1),marked(j+1,hi))
    target=marked(0,5,M.index(R[1]));q=collections.deque([R]);prev={R:None}
    while target not in prev:
        assert q and len(prev)<=4862
        a=q.popleft()
        for x in range(1,10):
            if x==a[1]:continue
            b=move(a,x)[0]
            if b not in prev:prev[b]=(a,x);q.append(b)
    prefix=[];cur=target
    while cur!=R:a,x=prev[cur];prefix.append(('D',x));cur=a
    prefix.reverse();cur=R
    for m,x in prefix:cur=move(cur,x)[0]
    assert cur==target
    seen={};cur=target;j=0
    while cur not in seen:
        seen[cur]=j;j+=1;assert j<=133;cur=run(cur,W)
    ua=seen[cur];la=j-ua;A0=cur;WW=W*la;z=M[0];E=run(R,W*ua,erased=z);seenE={};j=0
    while E not in seenE:
        seenE[E]=j;j+=1;assert j<=100;E=run(E,WW,erased=z)
    ue=seenE[E];le=j-ue;E0=E;period=WW*le
    # Prefix is source-exact: DELETE preparation, then actual K word copies.
    reaching=prefix+W*ua+WW*ue
    AA=FF=EE=R
    for m,x in reaching:
        AA=move(AA,x)[0]
        if m=='K':
            FF=move(FF,x)[0]
            if x!=z:EE=move(EE,x)[0]
    assert (AA,FF,EE)==(A0,R,E0)
    comparison=json.loads((B/'cheap_A_comparison.json').read_text())['reports'][0];reports=[]
    def helper(t):
        if t[0]=='leaf':return I.node(0,('leaf','Eminus'),('leaf','Ezero')) if t[1]=='F0' else t
        return I.node(t[1],helper(t[2]),helper(t[3]))
    for with_helper in (False,True):
        A,F,E=(helper(t) for t in (A0,R,E0)) if with_helper else (A0,R,E0);initial=(A,F,E)
        word=[];inserted=False
        for m,x in period:
            word.append((m,x))
            if with_helper and not inserted and x==1:word += [('D',0),('D',1)];inserted=True
        rows=[]
        for t,(m,x) in enumerate(word,1):
            before=(A,F,E);genuine=m=='K' and x!=F[1];A,ae=move(A,x);be=ee=[]
            if m=='K':
                F,be=move(F,x)
                if x!=z:E,ee=move(E,x)
            pa=P.trace(plain(before[0]),x);pb=P.trace(plain(before[1]),x) if m=='K' else (plain(before[1]),'',[])
            pe=P.trace(plain(before[2]),x) if m=='K' and x!=z else (plain(before[2]),'',[])
            global calls
            calls+=1+int(m=='K')+int(m=='K' and x!=z)
            assert (pa[0],pb[0],pe[0])==tuple(plain(v) for v in (A,F,E))
            assert [len(ae),len(be),len(ee)]==[len(pa[2]),len(pb[2]),len(pe[2])]
            rows.append({'occurrence':t,'mode':m,'target':x,'genuine_F':genuine,'a':len(ae),
                'qF':sum(v[0]!='ZIG' for v in be),'qE':sum(v[0]!='ZIG' for v in ee),
                'before':tuple(plain(v) for v in before),'after':tuple(plain(v) for v in (A,F,E))})
        assert (A,F,E)==initial
        v=build(rows,comparison);Eids={(r['occurrence'],j) for r in rows for j in range(1,r['qE']+1)}
        units=sorted(v['U']);fE=dict(zip(sorted(Eids),units[2:]+units[:2]));ex=with_owners(v,Eids,fE)
        reports.append({'helper_excursion':with_helper,'initial_A_BF_BE':tuple(plain(t) for t in initial),'word':word,'rows':rows,
            'source_reaching_prefix':reaching,'prefix_helper_interpretation':'same F0 substitution at diagonal and every prefix state',
            'A_marked_core_boundary':6,'BF_core':9,'marks':M,'erased':z,'alignment':{'A_period_multiplier':la,'E_period_multiplier':le},
            'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'R':v['R'],'h0':pack(v['h0']),'h':pack(v['h']),
            'local_signed_receipt':v['source_receipt'],'logical_owner_fixture_not_sealed_numeric_fE':True,
            'fE':pack(fE),'paid':pack(ex['prior']['allocation']),'extension_paths':ex['extension']['paths'],
            'final':pack(ex['extension']['allocation'])})
    out('core9_A6_source_certificate.json',ser({'status':'RESTRICTED_CORE9_A6_SOURCE_FUNDING_AUDITED','reports':reports,
        'reachability_proved_by_explicit_original_prefix':True,'source_engine_calls':calls}))
    names=['CORE9_A6_RESTRICTED.md','a_core6_funding.py','cheap_A_comparison.json','h2_release_audit.json','A6_independent_audit.json','core9_A6_source_certificate.json']
    out('core9_A6_seal.json',{'status':'PROVED_RESTRICTED_SOURCE_SCOPE','domain':'core9 BF mask{1,2,3,5,7,9}, A marked core6 at every macro boundary; arbitrary H/private helpers',
        'not_claimed':'unrestricted core9, other BF masks or anonymous marked-core A ancestors',
        'files':[{'path':n,'sha256':hashlib.sha256((B/n).read_bytes()).hexdigest()} for n in names],
        'full_core9_status':'OPEN','Step2':'OPEN'})
    print(json.dumps({'status':'PASS_RESTRICTED_CORE9_A6_SEAL','source_reports':len(reports),'prefix_DELETES':len(prefix),'source_calls':calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_A6_source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
