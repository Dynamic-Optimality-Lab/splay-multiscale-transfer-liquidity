"""Independent comparison padding and deficiency-one geometry controls.
No frozen graph/solver/row generation or debt-value oracle is invoked.
"""
import collections,importlib.util,json,sys,time
from fractions import Fraction as F
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
spec=importlib.util.spec_from_file_location('separate_bridge10',ROOT/'python/independent/splay.py')
I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)
calls=0;started=time.process_time();CAP=min(50,float(sys.argv[1])-4)
def move(t,x):
    global calls
    calls+=1;assert calls<1000000 and time.process_time()-started<CAP
    return I.trace(t,x)
def conv(v):return ('leaf',v) if isinstance(v,str) else I.node(v[0],conv(v[1]),conv(v[2]))
def path(t,x):
    w=[];ks=[]
    while t[0]!='leaf' and t[1]!=x:
        d=int(x>t[1]);w.append(d);ks.append(t[1]);t=t[2+d]
    assert t[0]!='leaf';return tuple(w),ks
def get(t,w):
    for d in w:t=t[2+d]
    return t
def put(t,w,v):
    if not w:return v
    return I.node(t[1],put(t[2],w[1:],v),t[3]) if not w[0] else I.node(t[1],t[2],put(t[3],w[1:],v))
def keys(t):return set() if t[0]=='leaf' else keys(t[2])|keys(t[3])|{t[1]}
def core(t,M):
    if t[0]=='leaf':return set()
    L,R=core(t[2],M),core(t[3],M)
    return L|R|{t[1]} if t[1] in M or L or R else set()
def chain(kk,tail):
    for k in reversed(kk):tail=I.node(k,('leaf',),tail)
    return tail
def padA(t,kk):
    if t[0]=='leaf':return chain(kk,('leaf',))
    return I.node(t[1],padA(t[2],kk),t[3])
def padB(t,kk,minimum_score):
    if t[1]==minimum_score:return I.node(t[1],chain(kk,t[2]),t[3])
    return I.node(t[1],padB(t[2],kk,minimum_score),t[3])
def erase(t,kk):
    if t[0]=='leaf':return t
    if t[1] in kk:
        L,R=erase(t[2],kk),erase(t[3],kk)
        assert L[0]=='leaf' or R[0]=='leaf'
        return R if L[0]=='leaf' else L
    return I.node(t[1],erase(t[2],kk),erase(t[3],kk))
def material(t):
    if t[0]=='leaf':
        i=int(t[1][1:]);k=F(i)-F(1,3)
        return I.node(k,('leaf',),('leaf',))
    return I.node(t[1],material(t[2]),material(t[3]))
def q(ev):return sum(e[0]!='ZIG' for e in ev)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    families=json.loads((B/'deficient_source_schemas.json').read_text())['families'];padding=[]
    for fam in families:
        c=fam['core']
        if c>9:continue
        for private in (False,True):
            old=conv(fam['initial_A_BF'])
            if private:old=material(old)
            elif c<9:
                # Empty the symbolic holes for this concrete comparison
                # regression. The general graft proof permits ANY old BST.
                def empty(t):return ('leaf',) if t[0]=='leaf' else I.node(t[1],empty(t[2]),empty(t[3]))
                old=empty(old)
            kk=tuple(range(-100-(9-c),-100));A=BF=old;Ap=padA(old,kk);Bp=padB(old,kk,1)
            assert erase(Ap,set(kk))==A and erase(Bp,set(kk))==BF
            assert len(set(range(1,c+1))|set(kk))==9
            word=[tuple(w) for w in fam['word']]
            if private:word += [('D',F(2)-F(1,3)),('D',F(1)-F(1,3)),('D',c),('K',1)]
            for m,x in word:
                A,ev=move(A,x);Ap,ep=move(Ap,x)
                assert len(ev)==len(ep) and erase(Ap,set(kk))==A
                if m=='K':
                    BF,ev=move(BF,x);Bp,ep=move(Bp,x)
                    assert q(ev)==q(ep) and erase(Bp,set(kk))==BF
                assert Ap[1]==A[1] and Bp[1]==BF[1]
            padding.append({'core':c,'private_helper_control':private,'operations':len(word),'cost_preserved':True})
    geometry=collections.Counter();details=[]
    for fam in families:
        if fam['core']!=10:continue
        M=set(fam['marks'])
        for row,chart in zip(fam['rows'],fam['charts']):
            if not chart['cold']:continue
            bf=conv(row['before'][1]);recent=chart['recent_before'];z=recent[-1];v=recent[-2];U=set(recent[:4])
            cu=core(bf,U);assert len(cu) in (6,7) and not({v,z}&cu)
            w,anc=path(bf,z);Q=row['qF'];ancestor=v in anc
            if not ancestor:
                assert core(get(bf,path(bf,v)[0]),M)=={v}
                geometry['no_peel']+=1
            else:
                dist=len(w)-anc.index(v);assert dist in (1,2)
                midlocal,ev=move(get(bf,w[:-2]),z);assert len(ev)==1 and ev[0][0]!='ZIG'
                mid=put(bf,w[:-2],midlocal)
                assert core(mid,M)==set(range(1,11))
                vv=get(mid,path(mid,v)[0]);assert core(vv,M)=={v} and keys(vv)&set(range(1,11))=={v}
                if Q>=2:
                    assert mid[1]==bf[1]
                    after,ee=move(mid,z);assert q(ee)==Q-1
                    assert set(path(mid,z)[1])|{z}<=set(range(1,11))-{v}
                    geometry['internal_one_double_peel']+=1
                else:geometry['root_or_low_q_peel_separate']+=1
            details.append({'occurrence':row['occurrence'],'cold':z,'evicted':v,'Q':Q,'ancestor':ancestor,'recent4_core':len(cu)})
    result={'status':'PASS_LOCAL_BRIDGES_ONLY_SIGNED_REPAYMENT_OPEN','padding_controls':padding,
        'core10_geometry_cases':dict(geometry),'core10_cold_source_details':details,
        'universal_padding_proof':'old-key paths unchanged; rotations commute with gap/leaf grafts; comparison only, no new A donor',
        'universal_deficiency1_proof':'recent r-2 complement has3/4 nodes; forbidden processed unmarked loss; v first-double demotion',
        'M3_application':'inherited universal LOCAL nine-Score theorem permits unmarked Score leaves; no graph/solver modified',
        'repayment_signs':'NOT_PROVED','uniform_source_supply':'OPEN','new_finite_tests':len(padding),
        'source_engine_calls':calls}
    out('bridge_audit.json',result);print(json.dumps({'status':result['status'],'padding_controls':len(padding),
        'geometry':dict(geometry),'source_engine_calls':calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_bridges_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls,'new_finite_tests':8})
