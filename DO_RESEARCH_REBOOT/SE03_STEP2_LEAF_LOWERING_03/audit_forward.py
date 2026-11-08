"""Finite free-term closure with explicit universal source-completeness guards.
No closure claim is made if an H2/helper or paired-zero branch is encountered.
"""
import collections,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01';PREV=B.parent/'SE03_STEP2_FORCED_ZERO_INCOMING_02'
sys.path.insert(0,str(OLD))
from source_model import trace,core,labels
M=(1,3,5,7,9,11);account={'source_engine_calls':0,'new_finite_tests':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(v):return tuple(freeze(q) for q in v) if isinstance(v,list) else v
def step(t,x):
    account['source_engine_calls']+=1
    return trace(t,x)
def leaf(t):return 0 if t is None else int(t[0] in M) if t[1] is None and t[2] is None else leaf(t[1])+leaf(t[2])
def closure(name,a,b,budget):
    todo=collections.deque([(a,b,0)]);ids={(a,b,0):0};states=[];edges=[];unknown=[];possibleF=[]
    while todo:
        a,b,c=todo.popleft();index=ids[(a,b,c)];observations=[]
        for x in M:
            if x==b[0]:continue
            nb,pb,be=step(b,x)
            if not all(q['kind']=='DOUBLE' and q['case'] in ('LL','RR') and q['G'] in M and q['P'] not in M for q in be):continue
            if labels(core(nb,set(M)))!=set(range(1,12)):continue
            na,pa,ae=step(a,x);q=len(be);h=len(ae)
            observations.append({'target':x,'A_path':pa,'B_path':pb,'a':h,'q':q})
            if q>=4 and h==1:possibleF.append({'state':index,'target':x,'q':q})
            if q==4 or (q==3 and c<budget) or q==5:
                unknown.append({'state':index,'target':x,'q':q,'cost_spent':c,
                    'reason':'arbitrary H2 helper/paired branch not classified here'})
            if h!=1 or q not in (1,2):continue
            w=2-q
            if c+w>budget:continue
            key=(na,nb,c+w)
            if key not in ids:
                assert len(ids)<1000
                ids[key]=len(ids);todo.append(key)
            edges.append({'source':index,'target':ids[key],'KEEP':x,'H':1,'Q':q,'w':w,
                'A_path':pa,'B_path':pb,'leaf_change':leaf(core(nb,set(M)))-leaf(core(b,set(M)))})
        states.append({'id':index,'A':a,'BF':b,'cost':c,'marked_leaves':leaf(core(b,set(M))),
            'observations':observations})
    return {'name':name,'budget':budget,'states':states,'edges':edges,'unknown_branches':unknown,
        'possible_F_states':possibleF,'universal_projection_closure_verified':not unknown,
        'no_F_geometry':not possibleF,
        'scope':'all actual source zero/+1 paths from THESE A/B terms, arbitrary gaps/BE/recent; proof requires no unknown branches'}
def main():
    records=json.loads((PREV/'forced_regions.json').read_text())['records'];results=[]
    for r in records:
        t=r['T_state'];results.append(closure(r['family']+'_T',freeze(t['A']),freeze(t['BF']),1))
    f=json.loads((B/'pattern_family.json').read_text())
    for idx,label in ((0,'before_two_losses'),(2,'after_two_losses')):
        row=f['pattern'][idx];a,b,_=row['before']
        results.append(closure(label,freeze(a),freeze(b),0))
    out('forward_closure.json',{'status':'EXPLICIT_FREE_TERM_SOURCE_CLOSURES','results':results,
        'no_B_E_or_chart_factorization_assumed_for_debt':True,
        'exclusion_bridge':'source grammar projects every admitted affordable packet into listed unique H1 A/B edges if unknown_branches empty',
        'new_weighted_universal_graph':False,**account})
    print(json.dumps({'results':[{'name':r['name'],'states':len(r['states']),'edges':len(r['edges']),
        'unknown':len(r['unknown_branches']),'possible_F':r['possible_F_states']} for r in results],**account}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_forward_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
