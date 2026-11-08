"""Bounded exact cut search in a specified, larger first-loss eligibility graph.

Source transitions are applications of independently accepted complete
native11 primitives. No primitive is evaluated afresh. Passing trials
have no universal proof status. An exact cut refutes only this rule.
"""
import collections,functools,hashlib,json,pickle,random,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4]);sys.setrecursionlimit(10000)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    cp=F/'probe11_source_actions.pkl';ac=F/'independent_probe11_source_actions.json'
    with cp.open('rb') as f:p=pickle.load(f)
    T,AD,H,Q=p['trees'],p['destination'],p['H'],p['Q'];N=len(T)
    desc=np.zeros((N,11),dtype=np.uint16);ids=np.array([1<<i for i in range(11)],dtype=np.uint16)
    for i,t in enumerate(T):
        def walk(u):
            if u is None:return 0
            mask=walk(u[1])|walk(u[2])|(1<<(u[0]-1));desc[i,u[0]-1]=mask;return mask
        walk(t)
    one=[np.flatnonzero(H[i]==1).tolist() for i in range(N)]
    assert N*11*2+N*2<2000000
    rng=random.Random(350216000+BATCH);attempts=[];witness=None;generated=0
    def match(graph):
        owner={};out={}
        def aug(d,seen):
            for u in sorted(graph[d]):
                if u in seen:continue
                seen.add(u)
                if u not in owner or aug(owner[u],seen):owner[u]=d;out[d]=u;return True
            return False
        for d in sorted(graph):aug(d,set())
        S=set(graph)-set(out);pending=list(S);neigh=set()
        while pending:
            for u in graph[pending.pop()]:
                neigh.add(u);assert u in owner
                if owner[u] not in S:S.add(owner[u]);pending.append(owner[u])
        assert len(S)-len(neigh)==len(graph)-len(out)
        return out,S,neigh
    while time.process_time()-START<CAP-4 and generated<2000:
        generated+=1;a=rng.randrange(N);states=[a];seen={a:0};keys=[];previous=-1
        for _ in range(500):
            choices=[x for x in one[a] if x!=previous] or one[a]
            x=rng.choice(choices);previous=(T[a][0]-1);keys.append(x+1);a=int(AD[a,x])
            states.append(a)
            if a in seen:lo=seen[a];break
            seen[a]=len(keys)
        else:continue
        keys=keys[lo:];initial=states[lo]
        if not 16<=len(keys)<=160:continue
        word=[('K' if rng.random()<0.84 else 'D',x) for x in keys]
        if len({x for k,x in word if k=='K'})<7:continue
        A=BF=BE=initial;cf=ce=();t=0;copies=[];boundary={(A,BF,BE,cf,ce):0}
        for copy in range(10):
            rr=[]
            for kind,x in word:
                t+=1;ab,bf,be=A,BF,BE;h=int(H[A,x-1]);assert h==1;A=int(AD[A,x-1]);q=qe=0;gen=ge=False
                if kind=='K':
                    gen=T[BF][0]!=x;q=int(Q[BF,x-1]);BF=int(AD[BF,x-1])
                    if gen:cf=(x,)+tuple(y for y in cf if y!=x)
                    if x!=2:
                        ge=T[BE][0]!=x;qe=int(Q[BE,x-1]);BE=int(AD[BE,x-1])
                        if ge:ce=(x,)+tuple(y for y in ce if y!=x)
                rr.append({'t':t,'kind':kind,'key':x,'a':h,'qF':q,'qE':qe,'genuine_F':gen,'genuine_E':ge,
                  'A_before':ab,'A_after':A,'BF_before':bf,'BF_after':BF,'BE_before':be,'BE_after':BE,'chart_F':cf,'chart_E':ce})
            assert A==initial;copies.append(rr);state=(A,BF,BE,cf,ce)
            if state in boundary:u=boundary[state];v=copy+1;break
            boundary[state]=copy+1
        else:attempts.append({'generated':generated,'status':'CLOSURE_NOT_FOUND_WITHIN_BOUND'});continue
        rows=sum(copies[u:v],[]);rkeys={r['key'] for r in rows if r['genuine_F']}
        if len(rkeys)<7:continue
        n=len(rows);ends=[i for i,r in enumerate(rows) if r['genuine_F']]
        def arc(a,b,include=True):
            length=(b-a)%n or n
            return [rows[(a+j)%n] for j in range(1,length+int(include))]
        by={r['t']:i for i,r in enumerate(rows)}
        @functools.lru_cache(maxsize=20000)
        def core(s,V):return sum(1<<j for j in range(11) if int(desc[s,j])&V)
        graph={};info=[];h0={}
        for j,e in enumerate(ends):
            row=rows[e];x=row['key'];bit=1<<(x-1)
            prev=next(ends[(j-k)%len(ends)] for k in range(1,len(ends)+1) if rows[ends[(j-k)%len(ends)]]['key']==x)
            V=bit;cur=bit;tags={};latest={}
            for r in arc(prev,e,False):
                assert core(r['BF_before'],V)==cur
                y=r['key'];first=r['genuine_F'] and not(V>>(y-1)&1)
                if r['genuine_F']:latest[y]=by[r['t']]
                Vnew=V|(1<<(y-1)) if first else V;new=core(r['BF_after'],Vnew);growth=new&~cur
                if first:
                    assert growth.bit_count()<=2
                    for k in range(11):
                        if growth>>k&1:tags.setdefault(k+1,(r['t'],y))
                else:assert not growth
                V=Vnew;cur=new
            node=T[row['BF_before']];path=[]
            while True:
                path.append(node[0])
                if node[0]==x:break
                node=node[1] if x<node[0] else node[2]
            local=arc(ends[j-1],e)
            units=[(r['t'],1,b) for r in local for b in (0,1)];dd=[(row['t'],k) for k in range(1,row['qF']+1)]
            h0.update(zip(dd,units))
            for k,d in enumerate(dd,1):
                y1,y2=(tags[path[-2*k-1]][1],tags[path[-2*k]][1]);g=set(units);tr=[]
                for y in sorted({y1,y2}):
                    first=next(r for r in arc(latest[y],e) if int(desc[r['A_before'],y-1])&bit and not(int(desc[r['A_after'],y-1])&bit))
                    g.update((first['t'],1,b) for b in (0,1));tr.append({'proxy':y,'last_genuine_t':rows[latest[y]]['t'],'first_loss_access_t':first['t']})
                graph[d]=g;info.append({'demand':d,'target':x,'tag_proxy_choices':[y1,y2],'first_loss_accesses':tr,'candidate_units':sorted(g)})
        out,S,neigh=match(graph);Acount=len(rows);qtotal=sum(r['qF'] for r in rows)
        attempts.append({'generated':generated,'word_length':len(word),'r':len(rkeys),'period_copies':v-u,'A':Acount,'QF':qtotal,
          'matched':len(out),'deficiency':len(S)-len(neigh),'word':word})
        if S:
            witness={'initial_tree_index':initial,'initial_diagonal':T[initial],'word':word,'erased_key':2,
              'prefix_rows':sum(copies[:u],[]),'period_rows':rows,'period':[rows[0]['t'],rows[-1]['t']],'preperiod_copies':u,'period_copies':v-u,
              'physical_keys':list(range(1,12)),'M':sorted(rkeys),'A':Acount,'QF':qtotal,
              'source_demand_edges':info,'candidate_cut':{'demands':sorted(S),'neighborhood':sorted(neigh),'deficiency':len(S)-len(neigh)},
              'candidate_maximum_matching':[{'demand':d,'unit':u} for d,u in sorted(out.items())],
              'h0':[{'demand':d,'unit':u} for d,u in sorted(h0.items())]}
            assert qtotal<=2*Acount
            break
        core.cache_clear()
    report={'status':'FP_ACCESS_RULE_EXACT_CLOSED_COUNTERCUT' if witness else 'BOUNDED_FP_ACCESS_CUT_SEARCH_CHECKPOINT',
      'candidate_relation':'all own-macro bits plus both source-tag proxies first-loss whole-access bits; A actions H1',
      'seed':350216000+BATCH,'generated_walks':generated,'closed_trials':len(attempts),'attempts':attempts,'witness':witness,
      'passing_search_is_not_universal':True,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','Coarse_Double_counterexample':False,
      'input_sha256':{str(p):sha(p) for p in (cp,ac,F/'FRESH_PROXY_LOSS_THEOREM.md')}}
    with (F/f'FP_access_countercut_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('attempts','witness','input_sha256')}),flush=True)
    if witness:print(json.dumps({'period':witness['period'],'A':witness['A'],'QF':witness['QF'],'cut':witness['candidate_cut']}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
