"""Refine the two surviving order words, keeping all eleven fixed identities."""
import json,sys,time
from fractions import Fraction as F
from pathlib import Path
import audit_grammar as g
import audit_backward as p
c=g.c;B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def form(t):
    if isinstance(t,g.Hole):return {'gap':[str(t.lo),str(t.hi)]}
    return [str(t[0]),form(t[1]),form(t[2])]
def expand(t,x):
    u=t;pp=''
    while not isinstance(u,g.Hole):
        if u[0]==x:return [t] if len(pp) in (1,2) else []
        pp+='L' if x<u[0] else 'R'
        if len(pp)>2:return []
        u=u[1 if pp[-1]=='L' else 2]
    if not u.lo<x<u.hi:return []
    result=[g.expand_at(t,pp,g.node(x,u.lo,u.hi))]
    if len(pp)==1:
        keys=sorted(set(g.vars_of(t)+[F(i) for i in range(1,12)]+[u.lo,u.hi]))
        parents=[k for k in keys if u.lo<k<u.hi and k!=x]
        parents += [(l+r)/2 for l,r in zip(keys,keys[1:]) if u.lo<=l<r<=u.hi]
        for y in parents:
            yy=g.node(y,u.lo,u.hi)
            yy=(y,g.node(x,u.lo,y),yy[2]) if x<y else (y,yy[1],g.node(x,y,u.hi))
            result.append(g.expand_at(t,pp,yy))
    return result
def starts(word):
    current={g.node(F(word[0]),F(0),F(12))}
    for x in word[1:]:
        current={c.move(u,F(x))[0] for t in current for u in expand(t,F(x))}
    final=current
    for x in reversed(word[:-1]):current={u for t in current for u in p.inv(t,F(x))}
    return current,final
def parents(t):
    d={}
    def walk(v,pp):
        if not isinstance(v,tuple):return
        k=v[0]
        if k in c.MM:d[k]=pp;pp=k
        walk(v[1],pp);walk(v[2],pp)
    walk(t,None);return d
def main():
    data=json.loads((B/'sourceclosure.json').read_text());rows=[]
    for r in data['remaining_compatible_tails']:
        word=r['word'];initial,final=starts(word);b=freeze(r['previous_BF'])
        rows.append({'word':word,'previous_Q':r['previous_Q'],'previous_BF':b,
            'previous_L':c.leaves(b),'previous_marked_parents':parents(b),'A_initial_patterns':[form(t) for t in sorted(initial,key=str)],
            'A_initial_count':len(initial),'A_final_count':len(final)})
    out('tailrefine.json',{'status':'RECURSIVE_PREDECESSOR_CHILD','profiles':rows,
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0})
    print(json.dumps([{'word':r['word'],'Q':r['previous_Q'],'L':r['previous_L'],
        'Bparents':r['previous_marked_parents'],'Astarts':r['A_initial_count']} for r in rows]),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_tailrefine_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})
