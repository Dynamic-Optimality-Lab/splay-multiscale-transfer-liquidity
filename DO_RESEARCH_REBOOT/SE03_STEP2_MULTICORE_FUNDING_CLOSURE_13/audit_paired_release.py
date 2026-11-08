"""Correct source packet test: actual q5 followed by actual q1.
Natural q5 H2 failure is not silently substituted for a paired failure.
"""
import collections,importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('original_pair_A13',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p);calls=0
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def tree(t,lo=1,hi=6):return 'F'+str(hi) if t is None else (t[0],tree(t[1],lo,t[0]-1),tree(t[2],t[0]+1,hi))
def compact(t):return None if isinstance(t,str) else (t[0],compact(t[1]),compact(t[2]))
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def main():
    global calls
    src=json.loads((B/'cheap_A_comparison.json').read_text());r=src['reports'][2];ats=r['A_trees'];aid={freeze(t):i for i,t in enumerate(ats)}
    h1=collections.defaultdict(set);h2=collections.defaultdict(set)
    for a,raw in enumerate(ats):
        t=tree(raw)
        for x in range(1,7):
            if 1<=len(p.path(t,x))<=2:
                calls+=1;dest,_,ev=p.trace(t,x);assert len(ev)==1;h1[a,x].add(aid[compact(dest)])
    basis=json.loads((B/'h2_transition_basis.json').read_text())
    for a,x,b in basis['transition_basis']:h2[a,x].add(b)
    states=[tuple(v) for v in r['states']];ix={v:i for i,v in enumerate(states)};D=r['debt'];marks=r['BF_marks'];rank={x:i+1 for i,x in enumerate(marks)}
    bf=json.loads((B/'bf11_comparison.json').read_text());edges=bf['edges'];adj=collections.defaultdict(list)
    for a,b,x,q in edges:adj[a].append((b,x,q))
    byB=collections.defaultdict(list)
    for i,(a,b) in enumerate(states):byB[b].append(D[i])
    singleton_bad=[];pair_bad=[];high_bad=[];singlecount=paircount=pairsectors=0
    for s,t,x,q in edges:
        xx=rank[x]
        if q<=4:
            for a in range(len(ats)):
                if (a,s) not in ix:continue
                for b in h2[a,xx]:
                    value=4-q+D[ix[b,t]]-D[ix[a,s]];singlecount+=1
                    if value<0:singleton_bad.append((a,s,b,t,x,q,value))
            continue
        assert q==5
        for end,y,q1 in adj[t]:
            if q1!=1 or y not in (marks[0],marks[-1]):continue
            yy=rank[y];pairsectors+=1
            if 2+min(byB[end])-max(byB[s])<0:high_bad.append((s,t,end,x,y))
            for a in range(len(ats)):
                if (a,s) not in ix:continue
                for first,second,label in ((h1,h2,'H1_H2'),(h2,h1,'H2_H1')):
                    for middle in first[a,xx]:
                        for final in second[middle,yy]:
                            value=D[ix[final,end]]-D[ix[a,s]];paircount+=1
                            if value<0 and len(pair_bad)<20:pair_bad.append({'A_source':a,'A_midpoint':middle,'A_target':final,
                                'BF_source':s,'BF_midpoint':t,'BF_target':end,'targets':[x,y],'split':label,'H':3,'Q':6,'signed_residual':value,
                                'status':'necessary source comparison edge; full closed period not inferred'})
    result={'status':'PAIRED_ORIGINAL_SOURCE_RELEASE_AUDIT','singleton_H2_Qle4_edges':singlecount,'singleton_adverse_count':len(singleton_bad),
        'singleton_adverse_examples':singleton_bad[:20],'actual_q5_extreme_q1_sectors':pairsectors,
        'Hsum3_paired_compositions':paircount,'paired_adverse_examples':pair_bad,'Hsum_ge4_unconstrained_shape_adverse':high_bad,
        'cheap_Hsum2':'already telescopes exact H1 inequalities across SAME actual midpoint',
        'scope':'A marked core6 at each natural macro boundary only; arbitrary original A boundary ancestors remain outside',
        'not_claimed':'natural H2q5 failures alone refute original packet; no Step2 or full core11 promotion','source_engine_calls':calls}
    out('paired_release_audit.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('singleton_adverse_examples','paired_adverse_examples','Hsum_ge4_unconstrained_shape_adverse')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_paired_release_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':calls})
