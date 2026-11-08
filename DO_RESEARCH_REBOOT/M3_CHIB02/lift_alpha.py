"""Exact finite original-alpha lift of the fixed negative B-event cycle."""
import sys,json,time
from pathlib import Path
from functools import lru_cache
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_GAPINT01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
from framework_v2 import S,V,iscore
BASE=Path('DO_RESEARCH_REBOOT/M3_CHIB02');KEYS=(-8,0,16,24,32,48,64,80,96,112,128)
@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (S.LEAF,)
    return tuple(S.node(KEYS[k],l,r) for k in range(lo,hi) for l in trees(lo,k) for r in trees(k+1,hi))
def shadow(t):
    def at(path):
        n=t
        for s in path:
            if n[0]=='leaf':return (2,0,0)
            n=n[2+s]
        return (2,0,0) if n[0]=='leaf' else (0,int(iscore(n[1])),n[1]//16 if iscore(n[1]) else 0)
    return tuple(at(p) for p in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))
def main():
    out=BASE/'alpha_lift.json';assert not out.exists();start=time.process_time();c=json.loads((BASE/'completion.json').read_text());cy=c['cycle'];L=len(cy)
    assert c['status']=='NEGATIVE_EVENT_CYCLE_RAW' and all(r['marked'] for r in cy)
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']]
    nodes=[];ids={};adj=[];edges=[];seen=set();queries=0
    def ident(phase,a):
        key=(phase,a)
        if key not in ids:ids[key]=len(nodes);nodes.append(key);adj.append([])
        return ids[key]
    for phase,r in enumerate(cy):
        root=16*bt[r['source_B']][1];ri=KEYS.index(root);x=16*r['target']
        for l in trees(0,ri):
            for rr in trees(ri+1,len(KEYS)):
                t=S.node(root,l,rr);queries+=1;h=S.lookup(t,x)[1]
                if h not in (1,2):continue
                dest=S.trace(t,x)[0];u=ident(phase,shadow(t));v=ident((phase+1)%L,shadow(dest))
                if (u,v) not in seen:
                    seen.add((u,v));e=len(edges);edges.append({'source':u,'destination':v,'phase':phase,'w':r['w'],'A_source_codes':V.serial(t),'A_depth':h});adj[u].append(e)
        assert queries<900000 and len(nodes)<2000000 and len(edges)<5000000 and time.process_time()-start<120
    color=bytearray(len(nodes));found=None
    for first in range(len(nodes)):
        if color[first]:continue
        stack=[[first,0]];positions={first:0};path=[];color[first]=1
        while stack and found is None:
            u,i=stack[-1]
            if i==len(adj[u]):
                stack.pop();positions.pop(u);color[u]=2
                if path:path.pop()
                continue
            e=adj[u][i];stack[-1][1]+=1;v=edges[e]['destination']
            if color[v]==0:positions[v]=len(stack);color[v]=1;path.append(e);stack.append([v,0])
            elif color[v]==1:found=path[positions[v]:]+[e]
        if found is not None:break
    result={'status':'LOW_ALPHA_CYCLE_CANDIDATE' if found is not None else 'NO_ALPHA_CYCLE_IN_REGISTERED_CORPUS',
      'mu':cy[0]['mu'],'sigma':[1,0,1]+[0]*7,'B_period':L,'B_period_weight':sum(r['w'] for r in cy),
      'source_tree_access_queries':queries,'alpha_vertices':len(nodes),'alpha_edges':len(edges),'cpu_seconds':round(time.process_time()-start,3),
      'full_original_roots_verified':False,'negative_original_mixed_cycle_certified':False}
    if found is not None:
        rows=[]
        for e in found:
            r=edges[e];rows.append({**r,'source_alpha':nodes[r['source']][1],'destination_alpha':nodes[r['destination']][1],'B_edge':cy[r['phase']]})
        assert all(a['destination']==b['source'] for a,b in zip(rows,rows[1:]+rows[:1]));weight=sum(r['w'] for r in rows);assert weight<0
        result.update(cycle=rows,cycle_weight=weight)
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='cycle'},indent=2),flush=True)
if __name__=='__main__':main()
