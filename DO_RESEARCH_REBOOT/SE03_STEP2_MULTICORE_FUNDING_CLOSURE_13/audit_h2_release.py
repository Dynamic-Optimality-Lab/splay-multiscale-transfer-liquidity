"""Exact free-gap H2 grammar for marked-A-core6 before/after.
Tests a candidate extension of the new cheap-A comparison; any adverse
edge is only a local necessary-source obstruction until period-realized.
"""
import functools,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
s=importlib.util.spec_from_file_location('original_h2_source13',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p);calls=0
def trace(t,x):
    global calls
    calls+=1;assert calls<2000000;return p.trace(t,x)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def tree(t,lo=1,hi=6):return 'F'+str(hi) if t is None else (10*t[0],tree(t[1],lo,t[0]-1),tree(t[2],t[0]+1,hi))
def prune(t):
    M=set(range(10,61,10));u=p.core(t,M)
    if p.labels(u)!=M:return None
    def conv(v):return None if v is None else (v[0]//10,conv(v[1]),conv(v[2]))
    return conv(u)
def freeze(t):return tuple(map(freeze,t)) if isinstance(t,list) else t
def replace(t,gap,value):
    if isinstance(t,str):return value if t==gap else t
    return (t[0],replace(t[1],gap,value),replace(t[2],gap,value))
def gaps(t,depth=0):
    if isinstance(t,str):return [(t,depth)]
    return gaps(t[1],depth+1)+gaps(t[2],depth+1)
def main():
    source=json.loads((B/'cheap_A_comparison.json').read_text());ats=source['reports'][0]['A_trees'];aid={freeze(t):i for i,t in enumerate(ats)}
    transitions=set();witness={}
    for a,raw in enumerate(ats):
        T=tree(raw);g=T[0];first=[(T,10*y,'marked') for y in range(1,7) if 1<=len(p.path(T,10*y))<=2]
        for gap,d in gaps(T):
            if d>2:continue
            z=int(gap[1:]);base=10*z;F=[gap+str(i) for i in range(3)]
            first.append((replace(T,gap,(base+4,F[0],F[1])),base+4,'private_gap_root'))
            if d==1:
                first.append((replace(T,gap,(base+6,(base+3,F[0],F[1]),F[2])),base+3,'private_left_grandchild'))
                first.append((replace(T,gap,(base+3,F[0],(base+6,F[1],F[2]))),base+6,'private_right_grandchild'))
        for x in range(1,7):
            key=10*x
            if key==g:continue
            depth=len(p.path(T,key))
            if depth in (3,4):
                dest,_,ev=trace(T,key);assert len(ev)==2;b=aid[freeze(prune(dest))]
                transitions.add((a,x,b));witness[a,x,b]={'source_A':T,'positive_accesses':[key],
                    'source_word':[('K',key)],'target_A':dest,'kind':'one_two-event_marked_access'}
        for TT,y,kind in first:
            mid,_,ev=trace(TT,y);assert len(ev)==1
            for x in range(1,7):
                key=10*x
                if key==g or not 1<=len(p.path(mid,key))<=2:continue
                dest,_,ev2=trace(mid,key);assert len(ev2)==1
                pr=prune(dest)
                if pr is None:continue
                b=aid[freeze(pr)];transitions.add((a,x,b));witness[a,x,b]={'source_A':TT,'positive_accesses':[y,key],
                    'source_word':[('D',y),('K',key)],'target_A':dest,'kind':kind}
    reports=[]
    for report in source['reports']:
        k=report['core'];states=[tuple(v) for v in report['states']];ix={v:i for i,v in enumerate(states)};D=report['debt']
        bf=json.loads((B/('bf'+str(k)+'_comparison.json')).read_text());bad=[];checked=0
        byA={}
        for a,x,b in transitions:byA.setdefault((a,x),set()).add(b)
        for s,t,key,q in bf['edges']:
            if s>=len(report['BF_trees']):continue
            rank=report['BF_marks'].index(key)+1
            for a in range(len(ats)):
                if (a,s) not in ix:continue
                for b in byA.get((a,rank),()):
                    left=4-q+D[ix[b,t]]-D[ix[a,s]];checked+=1
                    if left<0 and len(bad)<12:
                        bad.append({'A_source':a,'A_target':b,'BF_source':s,'BF_target':t,'full_target_key':key,
                            'Q':q,'H':2,'debt_before':D[ix[a,s]],'debt_after':D[ix[b,t]],'signed_residual':left,
                            'A_symbolic_receipt':witness[a,rank,b],
                            'status':'LOCAL_NECESSARY_SOURCE_RELEASE_FAILURE; full period embedding not established'})
        reports.append({'core':k,'H2_edges_checked':checked,'failures':bad,
            'status':'H2_RELEASE_PRESERVED_ON_THIS_RESTRICTED_GRAMMAR' if not bad else 'H2_CANDIDATE_EXTENSION_OPEN_WITH_ADVERSE_LOCAL_EDGES',
            'scope':'marked A core6 before/after, first BF mask; not whole original source domain'})
    out('h2_release_audit.json',{'status':'SOURCE_LEVEL_H2_GRAMMAR_RECURSION_RECORDED','A_H2_boundary_transitions':len(transitions),
        'coverage':'one depth3/4 marked access, or two depth1/2 accesses; first marked or exposed private root/grandchild; arbitrary rigid private hangers',
        'reports':reports,'source_engine_calls':calls,'counterexample_scope':'no local edge is promoted to full closed-period refutation'})
    print(json.dumps({'status':'PASS_H2_ROUTE_AUDIT','transitions':len(transitions),'reports':[{'core':r['core'],'checked':r['H2_edges_checked'],'adverse_recorded':len(r['failures']),'status':r['status']} for r in reports],'calls':calls}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_h2_release_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
