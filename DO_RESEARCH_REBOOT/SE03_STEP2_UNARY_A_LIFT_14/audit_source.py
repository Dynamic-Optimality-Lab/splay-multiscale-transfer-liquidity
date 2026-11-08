"""Reachable paired-closed unary source with physical donors and fixed owners."""
import importlib.util,json,time
from pathlib import Path
from unary_funding import build,with_owners
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
I=load('immutable_unary_period14',ROOT/'python/independent/splay.py')
P=load('original_unary_period14',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py');calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def tree(t):return ('leaf',t) if isinstance(t,str) else I.node(t[0],tree(t[1]),tree(t[2]))
def plain(t):return t[1] if t[0]=='leaf' else (t[1],plain(t[2]),plain(t[3]))
def extra(t):
    if t[0]=='leaf':return I.node(0,('leaf','Uminus'),('leaf','Uzero')) if t[1]=='F0' else t
    return I.node(t[1],extra(t[2]),extra(t[3]))
def move(t,x):
    global calls
    calls+=1;assert calls<1800000 and I.lookup(t,x)[0];return I.trace(t,x)
def runA(t,w):
    for m,x in w:t=move(t,x)[0]
    return t
def pack(v):return [{'demand':d,'unit':u} for d,u in sorted(v.items())]
def ser(v):
    if isinstance(v,set):return sorted(v)
    if isinstance(v,dict):return {str(k):ser(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [ser(x) for x in v]
    return v
def main():
    old=json.loads((OLD/'core9_A6_source_certificate.json').read_text())['reports'][0]
    a0,f0,e0=(extra(tree(t)) for t in old['initial_A_BF_BE']);word=[tuple(v) for v in old['word']]
    pos=next(j for j,(m,x) in enumerate(word) if m=='K' and x!=1);word=word[:pos]+[('D',0)]+word[pos:]
    A=a0;seen={};j=0
    while A not in seen:
        assert j<500;seen[A]=j;j+=1;A=runA(A,word)
    u=seen[A];L=j-u;initialA=A;period=word*L;reaching=[tuple(v) for v in old['source_reaching_prefix']]+word*u
    erased=old['erased'];AA=FF=EE=f0
    for m,x in reaching:
        AA=move(AA,x)[0]
        if m=='K':
            FF=move(FF,x)[0]
            if x!=erased:EE=move(EE,x)[0]
    assert (AA,FF,EE)==(initialA,f0,e0)
    A,F,E=initialA,f0,e0;initial=(A,F,E);rows=[]
    for t,(mode,x) in enumerate(period,1):
        before=(A,F,E);genuine=mode=='K' and x!=F[1];A,ae=move(A,x);be=ee=[]
        if mode=='K':
            F,be=move(F,x)
            if x!=erased:E,ee=move(E,x)
        expected=[]
        for oldtree,ev,enabled in ((before[0],ae,True),(before[1],be,mode=='K'),(before[2],ee,mode=='K' and x!=erased)):
            if enabled:
                global calls
                calls+=1;tt,path,pe=P.trace(plain(oldtree),x)
                assert [(v[0],v[3] if v[0]=='ZIG' else v[0]) for v in ev]==[('ZIG' if v['kind']=='ZIG' else v['case'],v['case']) for v in pe]
                expected.append(tt)
            else:expected.append(plain(oldtree))
        assert tuple(expected)==tuple(plain(v) for v in (A,F,E))
        rows.append({'occurrence':t,'mode':mode,'target':x,'genuine_F':genuine,'a':len(ae),
            'qF':sum(v[0]!='ZIG' for v in be),'qE':sum(v[0]!='ZIG' for v in ee),
            'A_events':ae,'BF_events':be,'BE_events':ee,'before':tuple(plain(v) for v in before),'after':tuple(plain(v) for v in (A,F,E))})
    assert (A,F,E)==initial
    v=build(rows);counts=[r['anon_counts'] for r in v['source_receipt']];assert any(1 in c for c in counts)
    Eids={(r['occurrence'],j) for r in rows for j in range(1,r['qE']+1)};us=sorted(v['U']);fixtures=[]
    for shift in (0,1,3):
        fE=dict(zip(sorted(Eids),us[shift:]+us[:shift]));o=with_owners(v,Eids,fE)
        fixtures.append({'logical_owner_fixture_not_numeric_sealed_fE':True,'fE':pack(fE),'paid':pack(o['prior']['allocation']),
            'anchors':pack(o['anchors']),'paths':o['extension']['paths'],'additions':pack(o['extension']['additions']),
            'final':pack(o['extension']['allocation'])})
    cutcount=0
    for delta in range(len(rows)):
        tau=lambda t:t if t>delta else t+len(rows)
        h={(tau(d[0]),d[1]):(tau(u[0]),u[1],u[2]) for d,u in v['h'].items()}
        assert len(h)==len(set(h.values()))==len(v['D']);cutcount+=1
    out('unary_source_receipt.json',ser({'status':'PASS_REACHABLE_NONVACUOUS_UNARY_SOURCE_FUNDING',
        'initial_A_BF_BE':tuple(plain(vv) for vv in initial),'word':period,'rows':rows,'actual_reaching_prefix':reaching,
        'diagonal_start':plain(f0),'erased':erased,'preperiod_modified_blocks':u,'A_period_multiplier':L,
        'marks':sorted({r['target'] for r in rows if r['genuine_F']}),'BF_core':9,
        'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'R':v['R'],
        'h0':pack(v['h0']),'h':pack(v['h']),'source_receipt':v['source_receipt'],
        'working_bound':6,'owner_fixtures':fixtures,'cut_transports':cutcount,'all_old_values_fixed':True,
        'lifting':'every free gap remains independently named; source identities commute with arbitrary ordered BST substitution',
        'source_engine_calls':calls}))
    print(json.dumps({'status':'PASS_ACTUAL_UNARY_CLOSED_SOURCE','length':len(rows),'R':len(v['R']),'A':sum(r['a'] for r in rows),
        'QF':sum(r['qF'] for r in rows),'source_calls':calls,'source_cuts':cutcount}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_source_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
