"""Independent full comparison regeneration and original-source physical audit."""
import functools,hashlib,importlib.util,itertools,json,time
from pathlib import Path
from debt_funding import build
from source_funding import with_owners
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
s=importlib.util.spec_from_file_location('immutable_comparison13',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(s);s.loader.exec_module(I);calls=0
def move(t,x):
    global calls
    calls+=1;assert calls<2000000 and I.lookup(t,x)[0];return I.trace(t,x)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
@functools.lru_cache(None)
def trees(lo,hi):
    if lo>hi:return (('leaf','F'+str(hi)),)
    return tuple(I.node(k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))
def tree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],tree(t[1]),tree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def density(t,M):
    if t[0]=='leaf':return 0,0,True
    a,b,good=density(t[2],M);c,d,other=density(t[3],M);nn=a+c+1;mm=b+d+int(t[1] in M)
    return nn,mm,good and other and 2*mm-nn>=int(t[1] in M)
def qb(ev):return sum(x[0]!='ZIG' for x in ev)
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def ser(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):ser(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [ser(x) for x in v]
    return v
def main(k):
    cert=json.loads((B/('bf'+str(k)+'_comparison.json')).read_text());assert cert['status']=='PROVED_COMPLETE_NECESSARY_BF_COMPARISON'
    delta=11-k;masks=[]
    for middle in itertools.combinations(range(2,k),4):
        marks=(1,)+middle+(k,);P=[2*j-x+1 for j,x in enumerate(marks)]
        if P[0]==0 and P[-1]==delta and all(0<=x<=delta for x in P):masks.append(marks)
    assert masks==[tuple(v['marks']) for v in cert['mask_summaries']]
    alltrees=trees(1,k);off=0;edges_checked=0;cache={};reflection={}
    for marks,summary in zip(masks,cert['mask_summaries']):
        M=set(marks);valid={t for t in alltrees if t[1] in M and density(t,M)[2]}
        nn=summary['states'];declared=[tree(t) for t in cert['trees'][off:off+nn]];assert set(declared)==valid
        potential={t:d for t,d in zip(declared,cert['debt'][off:off+nn])}
        expected=set()
        for t in valid:
            for x in marks:
                if x==t[1]:continue
                if (t,x) not in cache:
                    dest,ev=move(t,x);cache[t,x]=(dest,qb(ev))
                dest,q=cache[t,x]
                if dest not in valid:continue
                assert 2-q+potential[dest]-potential[t]>=0
                expected.add((t,x,dest,q))
        given={(declared[a-off],x,declared[b-off],q) for a,b,x,q in cert['edges'] if off<=a<off+nn}
        assert expected==given and len(expected)==summary['edges'];edges_checked+=len(expected);off+=nn
    assert off==len(cert['trees']) and edges_checked==len(cert['edges'])
    # Original actual family: source-full q/periods independently rebuilt.
    old=json.loads((B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/deficient_source_schemas.json').read_text())
    fam=next(v for v in old['families'] if v['core']==k);R=tree(fam['initial_A_BF']);base=[tuple(v) for v in fam['word']]
    reports=[];fixtures=0;cuts=0
    for reflected in (False,True):
        def mirror(t):return ('leaf','F'+str(k-int(t[1][1:]))) if t[0]=='leaf' else I.node(k+1-t[1],mirror(t[3]),mirror(t[2]))
        R0=mirror(R) if reflected else R;bw=[(m,k+1-x if reflected else x) for m,x in base]
        for count in (0,1,3,7):
            word=[v for v in bw if v[0]=='K'] if count==0 else bw*count
            for z in sorted({x for m,x in word if m=='K'}):
                E=R0;seen={};n=0
                while E not in seen:
                    seen[E]=n;n+=1
                    for m,x in word:
                        if m=='K' and x!=z:E=move(E,x)[0]
                assert n-seen[E]==1;E0=E;A=F=R0;rows=[]
                for t,(m,x) in enumerate(word,1):
                    before=(A,F,E);genuine=m=='K' and x!=F[1];A,ae=move(A,x);be=ee=[]
                    if m=='K':
                        F,be=move(F,x)
                        if x!=z:E,ee=move(E,x)
                    rows.append({'occurrence':t,'mode':m,'target':x,'genuine_F':genuine,'a':len(ae),'qF':qb(be),'qE':qb(ee),
                        'before':tuple(plain(v) for v in before),'after':tuple(plain(v) for v in (A,F,E))})
                assert (A,F,E)==(R0,R0,E0)
                v=build(rows,cert);D,U=v['D'],v['U'];Eids={(r['occurrence'],j) for r in rows for j in range(1,r['qE']+1)}
                if k==8:assert len(v['R'])==count
                ff=[]
                for shift in (0,1,3):
                    uu=sorted(U);fE=dict(zip(sorted(Eids),uu[shift:]+uu[:shift]));r=with_owners(v,Eids,fE);ex=r['extension']
                    assert len(set(ex['allocation'].values()))==len(D)
                    ff.append({'logical_owner_fixture_not_sealed_numeric_fE':True,'fE':pack(fE),'paid':pack(r['prior']['allocation']),
                        'anchors':pack(r['anchors']),'paths':ex['paths'],'additions':pack(ex['additions']),'final':pack(ex['allocation'])});fixtures+=1
                for delta0 in range(len(rows)):
                    tau=lambda t:t if t>delta0 else t+len(rows)
                    hh={(tau(d[0]),d[1]):(tau(u[0]),u[1],u[2]) for d,u in v['h'].items()}
                    assert len(hh)==len(set(hh.values()))==len(D);cuts+=1
                reports.append({'reflected':reflected,'erased':z,'requested_count_control':count,'word':word,'rows':rows,
                    'initial_A_BF':plain(R0),'initial_BE':plain(E0),'R':v['R'],'h0':pack(v['h0']),'h':pack(v['h']),
                    'debt_receipts':v['debt_receipts'],'full_cut_before_macro':v['full_cut_before_macro'],
                    'max_working_units':v['max_working_units'],'owner_fixtures':ff})
    names=['CORE'+str(k)+'_FULL_FUNDING.md','bf'+str(k)+'_comparison.json','debt_funding.py','audit_bf_independent.py']
    result={'status':'CORE'+str(k)+'_PHYSICAL_FUNDING_COMPLETE','core':k,'all_masks':masks,
        'states_independently_generated':off,'edges_independently_generated':edges_checked,'max_debt':max(cert['debt']),
        'source_reports':reports,'source_owner_fixtures':fixtures,'cut_transports':cuts,'source_engine_calls':calls,
        'all_old_values_and_common_owners_fixed':True,'not_formal_or_external_review':True,
        'scope':'actual original fixed full core, all source lengths/private BSTs; no reverse abstract realizability assumption',
        'files':[{'path':n,'sha256':hashlib.sha256((B/n).read_bytes()).hexdigest()} for n in names]}
    out('core'+str(k)+'_seal.json',ser(result))
    print(json.dumps({'status':result['status'],'states':off,'edges':edges_checked,'source_reports':len(reports),'fixtures':fixtures,'calls':calls}),flush=True)
