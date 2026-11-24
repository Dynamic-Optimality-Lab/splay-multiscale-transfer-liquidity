"""Independent full original-source replay and exact rational certificate audit.

Imports only the sealed immutable rotation primitive; no new producer/model.
Cross deficits use independent interval range-minimum queries, rather than the
producer's weighted postorder recurrence. Same-agent implementation independence
is not formal verification or independent peer review.
"""
import bisect
import gzip
import hashlib
import importlib.util
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
spec=importlib.util.spec_from_file_location('sealed_immutable_primitive',ROOT/'DO_RESEARCH_REBOOT/COVER_FLOW_AUDIT_20261121_V001/verify.py')
IMM=importlib.util.module_from_spec(spec);sys.modules[spec.name]=IMM;spec.loader.exec_module(IMM)
START=time.process_time();TOTAL=0


def construct(state):
    ch={int(k):v for k,v in state['children'].items()};done={};todo=[(state['root'],False)]
    while todo:
        k,finished=todo.pop()
        if finished:
            l,r=ch[k];done[k]=IMM.node(k,done.get(l),done.get(r))
        else:
            todo.append((k,True));todo.extend((c,False) for c in ch[k] if c is not None)
    assert len(done)==len(ch)
    return done[state['root']]


def state(t):
    ch={};stack=[t]
    while stack:
        v=stack.pop();ch[str(v.k)]=[v.l.k if v.l else None,v.r.k if v.r else None]
        stack.extend(c for c in (v.l,v.r) if c is not None)
    return {'root':t.k,'children':ch}


def describe(t):
    depths={};labels={};edges=set();stack=[(t,0)]
    while stack:
        v,d=stack.pop();depths[v.k]=d;labels[v.k]=(v.lo,v.hi)
        for side,c in enumerate((v.l,v.r)):
            if c:
                edges.add((v.k,c.k,side));stack.append((c,d+1))
    return depths,labels,edges


class RMQ:
    def __init__(self,depth):
        self.keys=sorted(depth);self.size=1
        while self.size<len(depth):self.size*=2
        self.v=[10**30]*(2*self.size)
        for i,k in enumerate(self.keys):self.v[self.size+i]=depth[k]
        for i in range(self.size-1,0,-1):self.v[i]=min(self.v[2*i],self.v[2*i+1])
    def query(self,lo,hi):
        l=bisect.bisect_left(self.keys,lo)+self.size;r=bisect.bisect_right(self.keys,hi)+self.size;answer=10**30
        while l<r:
            if l%2:answer=min(answer,self.v[l]);l+=1
            if r%2:r-=1;answer=min(answer,self.v[r])
            l//=2;r//=2
        return answer


def features(A,B):
    da,la,ea=describe(A);db,lb,eb=describe(B);ra=RMQ(da);rb=RMQ(db)
    cab=sum(da[k]-ra.query(*label) for k,label in lb.items())
    cba=sum(db[k]-rb.query(*label) for k,label in la.items())
    missing=set(lb.values())-set(la.values())
    sizes=[bisect.bisect_right(ra.keys,hi)-bisect.bisect_left(ra.keys,lo) for lo,hi in missing]
    m=-sum(width>=3 and width&(width+1)==0 for width in sizes)
    return [cab,cba,sum(da.values()),sum(db.values()),db[A.k],da[B.k],len(missing),len(eb-ea),m,sum(sizes)]


def replay(t,x,actor,op,records):
    global TOTAL
    def emit(step,bit,typ,child,parent,demoted):
        global TOTAL
        TOTAL+=1
        if records is not None:records.append({'id':[actor,op,step,bit],'type':typ,'promoted':child.k,'demoted':parent.k,'old_child_span':[child.lo,child.hi],'new_demoted_span':[demoted.lo,demoted.hi]})
        assert time.process_time()-START<=360
    return IMM.rebuild(t,x,emit,lambda *args:None)


def verify(item):
    with gzip.open(HERE/(item['label']+'.json.gz'),'rt',encoding='utf-8') as f:w=json.load(f)
    s=w['source'];initial={a:construct(s['initial_'+a]) for a in ('A','B')}
    diagonal=s.get('diagonal')
    if diagonal is None:
        assert s['initial_A']==s['initial_B'] and not s.get('prefix')
        diagonal=s['initial_A']
    reaching={a:construct(diagonal) for a in ('A','B')}
    for mode,x in s.get('prefix',[]):
        for actor in ('A','B') if mode=='K' else ('A',):reaching[actor],_=replay(reaching[actor],x,actor,0,None)
    assert all(state(reaching[a])==s['initial_'+a] for a in ('A','B'))
    trees=initial.copy();saved={row['op']:row for row in w['rows']};A=Q=0;start=TOTAL
    keep_support={x for mode,x in s['operations'] if mode=='K'}
    assert keep_support and keep_support<=set(map(int,s['initial_A']['children']))
    if not item['label'].startswith('control_'):
        assert keep_support==set(map(int,s['initial_A']['children']))
    for op,(mode,x) in enumerate(s['operations'],1):
        row=saved.get(op);bits=[]
        if row is not None:before=features(trees['A'],trees['B'])
        trees['A'],da=replay(trees['A'],x,'A',op,bits if row is not None else None)
        db=0
        if mode=='K':trees['B'],db=replay(trees['B'],x,'B',op,bits if row is not None else None)
        a=(da+1)//2;q=db//2;A+=a;Q+=q
        if row is not None:
            after=features(trees['A'],trees['B'])
            assert (row['mode'],row['target'],row['a'],row['q_B'])==(mode,x,a,q)
            assert row['before']==before and row['after']==after
            assert row['delta']==[v-u for u,v in zip(before,after)]
            assert row['bits']==bits
    assert all(state(trees[a])==s['initial_'+a] for a in ('A','B'))
    result=w['result'];assert (A,Q,TOTAL-start)==(result['A'],result['Q_B'],result['period_real_rotations'])
    out={'label':item['label'],'name':s['name'],'N':len(s['initial_A']['children']),'KEEP_support':len(keep_support),'operations':len(s['operations']),'period_rotations':TOTAL-start,'selected_rows':len(saved),'A':A,'Q_B':Q,'complete_pair_closure':True,'reaching_prefix':True,'all_period_operations':True,'all_selected_bits_and_features':True}
    print(json.dumps(out),flush=True);return out


def main():
    assert not (HERE/'FINAL_MANIFEST.json').exists()
    audit=json.loads((HERE/'AUDIT_RESULTS.json').read_text(encoding='utf-8'))
    result=[verify(item) for item in audit['cases']]
    cert=json.loads((HERE/'SYMBOLIC_SYNTHESIS_CERTIFICATE.json').read_text(encoding='utf-8'))
    rows=cert['necessary_limit_inequalities'];weights=list(map(Fraction,cert['exact_Farkas_multipliers']))
    lhs=[sum(w*Fraction(row['lhs'][i]) for w,row in zip(weights,rows)) for i in range(11)]
    rhs=sum(w*Fraction(row['rhs']) for w,row in zip(weights,rows))
    assert all(w>=0 for w in weights) and lhs==[0]*11 and rhs==-3
    out={'passed':True,'cases':result,'sources':len(result),'original_operations':sum(x['operations'] for x in result),'period_rotations':sum(x['period_rotations'] for x in result),'prefix_inclusive_rotations':TOTAL,'selected_rows':sum(x['selected_rows'] for x in result),'cpu_seconds':time.process_time()-START,'exact_Farkas_lhs':list(map(str,lhs)),'exact_Farkas_rhs':str(rhs),'independence':'Immutable functional replay and RMQ feature recomputation; imports no current producer/model. Same-agent implementation independence only.','scope':'All original operations and exact full pair closure; every bit and feature in selected rows only. Symbolic all-parameter proof is a separate mathematical derivation, not inferred from this finite audit.'}
    (HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='cases'}),flush=True)


if __name__=='__main__':main()
