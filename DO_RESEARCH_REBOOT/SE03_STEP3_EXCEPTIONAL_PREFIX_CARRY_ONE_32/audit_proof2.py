"""Static arithmetic on ALREADY AUDITED six-key arrays and symbolic ASTs.
No splay, source path primitive, newly generated source edge, or compiler.
The hypothetical-return test uses a proved necessary quotient predicate and
the OLD cached q9 edge, not an evaluated original access to the private7.
This can refute a proposed sufficient bridge on the overapproximation;
it cannot construct a reachable seven-key counterexample.
"""
import json,time,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP2_UNARY_A_LIFT_14'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def fr(v):return tuple(fr(x) for x in v) if isinstance(v,list) else v
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def marked(t,M):
    pa={};ch={x:[] for x in M};nodes={}
    def go(n,p):
        if isinstance(n,str):return
        nodes[n[0]]=n
        if n[0] in M:
            pa[n[0]]=p
            if p is not None:ch[p].append(n[0])
            p=n[0]
        go(n[1],p);go(n[2],p)
    go(t,None);return pa,ch,nodes
def gap_depth_lower_bound(t):
    # Static A-quotient predicate: earliest place at which physical7 could
    # have been an omitted unary/private node, or the gap3500 brancher.
    def marks(n):
        if n is None:return set()
        return marks(n[1])|marks(n[2])|({n[0]} if n[0]%1000==0 else set())
    def visit(n,depth):
        if n is None:return depth
        mm=marks(n)
        if max(mm)<3500 or min(mm)>3500 or n[0]==3500:return depth
        return visit(n[1 if 3500<n[0] else 2],depth+1)
    return visit(t,0)
def main():
    g=read(OLD/'branch_grammar2.json');aa=g['states'];c=read(OLD/'branch_core11_mask0.json');tt=c['BF_trees'];M=c['marks']
    ai={fr(t):i for i,t in enumerate(aa)};bi={fr(t):i for i,t in enumerate(tt)}
    roots={j:[i for i,t in enumerate(aa) if t[0]==1000*j] for j in range(1,7)}
    pos={i:p for rr in roots.values() for p,i in enumerate(rr)};off=[];o=0
    for t in tt:off.append(o);o+=len(roots[M.index(t[0])+1])
    def D(b,a):return c['debt'][off[b]+pos[a]]
    lows={h:collections.defaultdict(list) for h in (1,2)}
    for h in (1,2):
        for a,x,b in g['H'+str(h)]:lows[h][(x,aa[a][0]//1000)].append((a,b))
    single={'H1':{'minimum_margin':99,'violations':0},'H2':{'minimum_margin':99,'violations':0},'HIGH':{'minimum_margin':99,'violations':0}}
    for s,t,x,q in c['BF_relation']:
        if q!=5:continue
        target=M.index(x)+1;root=M.index(tt[s][0])+1
        for h in (1,2):
            for a,b in lows[h][(target,root)]:
                margin=2*h-5+D(t,b)-D(s,a);z=single['H'+str(h)]
                z['minimum_margin']=min(z['minimum_margin'],margin);z['violations']+=int(margin<0)
        ds=c['debt'][off[s]:off[s]+len(roots[root])];tr=M.index(tt[t][0])+1
        dt=c['debt'][off[t]:off[t]+len(roots[tr])];margin=1+min(dt)-max(ds)
        single['HIGH']['minimum_margin']=min(single['HIGH']['minimum_margin'],margin);single['HIGH']['violations']+=int(margin<0)
    lower=(4,(3,(2,(1,'F0','F1'),'F2'),'F3'),'F4')
    F0=(9,(8,(5,lower,(6,'F5',(7,'F6','F7'))),'F8'),(10,'F9',(11,'F10','F11')))
    F9=(7,(6,(5,lower,'F5'),'F6'),(8,'F7',(9,'F8',(10,'F9',(11,'F10','F11')))))
    initial=[]
    for name,small in [('branch',(1500,(1000,None,None),(2000,None,None))),('left_chain',(2000,(1000,None,None),None)),('right_chain',(1000,None,(2000,None,None)))]:
        A0=(5000,(4000,(3000,small,None),None),(6000,None,None))
        A9=(4000,(3000,small,None),(5000,None,(6000,None,None)))
        initial.append({'lower_A_type':name,'initial_old_chart_D':D(bi[F0],ai[A0]),'after9_new_chart_D':D(bi[F9],ai[A9])})
    cached9={s:(t,q) for s,t,x,q in c['BF_relation'] if x==7}
    gapLB=[gap_depth_lower_bound(t) for t in aa]
    violations=[];minimum=99;checked=0;BF=0
    for b,t in enumerate(tt):
        pa,ch,nodes=marked(t,set(M))
        if nodes[7][1]!='F6' or b not in cached9:continue
        BF+=1;Et=sum(max(len(v)-2,0) for v in ch.values());v=pa[7];k3=0
        while v is not None:k3+=int(len(ch[v])>=3);v=pa[v]
        rr=M.index(t[0])+1
        for a in roots[rr]:
            cmin=min(3,(gapLB[a]+1)//2);assert cmin>=1
            bound=2*cmin-2+Et-k3;margin=bound-D(b,a);checked+=1;minimum=min(minimum,margin)
            if margin<0:violations.append({'A_index':a,'BF_index':b,'D6':D(b,a),'quotient_gap_depth_lower_bound':gapLB[a],
                                          'return_H_lower_bound':cmin,'E6':Et,'k3_anc9':k3,'cached_q9':cached9[b][1],
                                          'proposed_terminal_bound':bound,'margin':margin})
    out('six_key_boundary_analysis.json',{'status':'COMPLETE_STATIC_BOUNDARY_AND_PACKET_ANALYSIS','new_source_queries':0,
        'initial_chart_lookups':initial,'q5_singleton_extension':single,'terminal_bridge_checked_states':checked,
        'terminal_bridge_BF_blocks':BF,'terminal_bridge_minimum_margin':minimum,'terminal_bridge_violation_count':len(violations),
        'first_terminal_bridge_violation':violations[0] if violations else None,
        'all_terminal_bridge_violations':violations,
        'boundary_predicate':'passive8(7) lies at F6; a legal7 return requires node9.left=F6. q7=cached_q9+1. E7+sigma7=2c-2+E6-k3_anc9.',
        'A_predicate':'minimum possible depth of omitted/retained physical7 in complete six-mark branch quotient; any actual return macro H is at least its ceil-half',
        'scope':'arithmetic on inherited COMPLETE necessary syntax, not source realization of adverse states or a CARRY1 counterexample'})
    print(json.dumps({'status':'STATIC_BOUNDARY_ANALYSIS','initial':initial,'q5_singles':single,'boundary_bad':len(violations),'boundary_min_margin':minimum,'source_queries':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
