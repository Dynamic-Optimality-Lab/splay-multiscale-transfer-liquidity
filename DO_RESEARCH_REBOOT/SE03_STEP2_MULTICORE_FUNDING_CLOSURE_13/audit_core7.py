"""Independent all-count core7 source audit and parameterized exchange check."""
import importlib.util,itertools,json,time
from pathlib import Path
from source_funding import core7,with_owners,extend
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
I=load('immutable_all_count13',ROOT/'python/independent/splay.py');calls=0
def move(t,x):
    global calls
    calls+=1;assert calls<2000000 and I.lookup(t,x)[0];return I.trace(t,x)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def readtree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],readtree(t[1]),readtree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def qb(ev):return sum(x[0]!='ZIG' for x in ev)
def unpack(v):return {tuple(x['demand']):tuple(x['unit']) for x in v}
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def ser(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):ser(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [ser(x) for x in v]
    return v
def reverse(D,U,a,h):
    inv={u:d for d,u in h.items()};P=D-set(a);ans={}
    for end in U-set(a.values()):
        u=end;seen=set()
        while u in inv:
            d=inv[u]
            if d in P:assert d not in ans;ans[d]=end;break
            if d in seen:break
            seen.add(d);u=a[d]
    assert set(ans)==P and len(set(ans.values()))==len(P);return ans
def main():
    src=json.loads((B.parent/'SE03_STEP2_CORE7_TWO_EXCESS_12/physical_receipts2.json').read_text());reports=[];fixtures=0
    for template in (src['families'][0],src['families'][6]):
        assert template['variant']=='plain'
        R=readtree(template['initial_A_BF']);base=[tuple(x) for x in template['word'][:23]];M=set(template['marks']);z=template['erased']
        for count in (0,1,2,3,5,9):
            word=[x for x in base if x[0]=='K'] if count==0 else base*count
            E=R;seen={};prefix=0
            while E not in seen:
                seen[E]=prefix;prefix+=1
                for mode,x in word:
                    if mode=='K' and x!=z:E=move(E,x)[0]
            assert prefix-seen[E]==1;E0=E;u=seen[E]
            A=F=R;rows=[]
            for t,(mode,x) in enumerate(word,1):
                before=(A,F,E);genuine=mode=='K' and x!=F[1];A,ae=move(A,x);be=ee=[]
                if mode=='K':
                    F,be=move(F,x)
                    if x!=z:E,ee=move(E,x)
                rows.append({'occurrence':t,'mode':mode,'target':x,'genuine_F':genuine,
                    'a':len(ae),'qF':qb(be),'qE':qb(ee),'before':tuple(plain(v) for v in before),
                    'after':tuple(plain(v) for v in (A,F,E)),
                    'A_events':ae,'BF_events':be,'BE_events':ee})
            assert (A,F,E)==(R,R,E0)
            v=core7(rows);assert len(v['R'])==count and v['Splus']>=count
            D,U=v['D'],v['U'];Ed={(r['occurrence'],j) for r in rows for j in range(1,r['qE']+1)}
            checks=[]
            for shift in (0,1,3):
                units=sorted(U);fE=dict(zip(sorted(Ed),units[shift:]+units[:shift]));s=with_owners(v,Ed,fE)
                a=s['prior']['allocation'];ex=s['extension'];assert ex['additions']==reverse(D,U,a,v['h'])
                checks.append({'logical_owner_fixture':True,'not_numerical_sealed_fE':True,'fE':pack(fE),'paid':pack(a),
                    'anchors':pack(s['anchors']),'paths':ex['paths'],'additions':pack(ex['additions']),'final':pack(ex['allocation'])})
                fixtures+=1
            reports.append({'slot_count':count,'reflected':template['reflected'],'initial_A_BF':plain(R),'initial_BE':plain(E0),
                'erased':z,'alignment':{'u':u,'L':1},'word':word,'rows':rows,'seeds':v['seeds'],
                'h0':pack(v['h0']),'h':pack(v['h']),'R':v['R'],'Splus':v['Splus'],'fixtures':checks})
    cases=0
    for n in range(1,7):
        D=set(range(n));U=set(range(n+1));h={d:d for d in D}
        for holes in range(n+1):
            for pp in itertools.combinations(sorted(D),holes):
                ds=sorted(D-set(pp))
                for shift in range(n+1):
                    aa={d:(d+shift)%(n+1) for d in ds};e=extend(D,U,aa,h)
                    assert e['additions']==reverse(D,U,aa,h);cases+=1
    out('core7_source_certificate.json',ser({'status':'CORE7_ALL_COUNTS_SOURCE_FUNDING_PROVED',
        'exact_slot_count_range':'all nonnegative integers by symbolic repetition plus zero witness',
        'source_reports':reports,'source_owner_fixtures':fixtures,'generic_arbitrary_hole_cases':cases,
        'source_engine_calls':calls,'proof':'CORE7_FULL_FUNDING.md; source repetition and injective cyclic predecessor proof, not finite inference',
        'new_finite_tests':fixtures+cases,'trust':'same agent distinct immutable source engine/backwards checker'}))
    print(json.dumps({'status':'PASS_CORE7_ALL_COUNTS','reports':len(reports),'fixtures':fixtures,'generic':cases,'source_calls':calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_core7_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
