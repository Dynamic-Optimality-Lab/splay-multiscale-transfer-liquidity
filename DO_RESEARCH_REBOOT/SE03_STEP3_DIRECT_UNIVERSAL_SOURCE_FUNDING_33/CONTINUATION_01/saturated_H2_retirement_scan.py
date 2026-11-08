"""Complete fixed-ten coefficient scan for direct H2 saturated retirement.
Implicit source debt0 is automatic. Only old positive coefficients are
scanned; all geometric source frames are symbolic free-tree constructions.
"""
import collections,hashlib,json,pickle,time,itertools
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def run(serial,cap):
    start=time.process_time();Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);N=len(S.T);mir=Z['mirror'];raw=(B/'native10_debt_03.pkl').read_bytes();pin=json.loads((B/'native10_complete_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==pin['input_sha256'];saved=pickle.loads(raw);L=saved['level'];assert not saved['queue'] and len(L)==1769616;del raw,saved
    if serial==1:w={'cursor':0,'automatic_positive_records':0,'explicit_retirement_couplings':0,'canonical_records_total':len(L),'counter':None}
    else:w=json.loads((B/('saturated_H2_retirement_work_%02d.json'%(serial-1))).read_text())
    maximum=[max(v) for v in Z['Q']];cache=collections.OrderedDict();frame_records=0
    def source(a,j,side):
        p=2*j+(1 if side=='L' else -1)
        def replace(t):
            if not isnode(t):return t
            if t[0]==2*j:return (p,(2*j,t[1],'E'),t[2]) if side=='L' else (p,t[1],(2*j,'E',t[2]))
            return t[0],replace(t[1]),replace(t[2])
        return replace(scale(S.T[a])),p
    def frames(a):
        nonlocal frame_records
        if a in cache:cache.move_to_end(a);return cache[a]
        result=[];T=S.T[a]
        for side,child,other in (('L',1,2),('R',2,1)):
            v=T[child];depth=1
            while isnode(v) and depth<=3:
                j=v[0]
                if isnode(v[other]):
                    xs=[]
                    if depth in (2,3):xs.append(j)
                    if depth in (1,2) and isnode(v[child]):xs.append(v[child][0])
                    if xs:
                        As,p=source(a,j,side)
                        for x in xs:
                            At,H=S.access(As,2*x);assert H==2;pt=S.sub(At,p);assert not isnode(pt[1]) or not isnode(pt[2]);pi=projections(At,p);assert len(pi)==1;result.append((p,x,S.idx[pi[0]],side,j,depth))
                v=v[child];depth+=1
        cache[a]=result;frame_records+=len(result)
        if len(cache)>1024:_,removed=cache.popitem(last=False);frame_records-=len(removed)
        assert len(L)+3*N+frame_records+len(cache)<1850000
        return result
    begin=w['cursor'];complete=False
    for i,(code,d) in enumerate(itertools.islice(L.items(),begin,None),begin):
        if time.process_time()-start>cap-3:break
        a,b=divmod(code,N)
        if d<=4-maximum[b]:w['automatic_positive_records']+=1;w['cursor']=i+1;continue
        for p,x,at,side,j,depth in frames(a):
            q=Z['Q'][b][x-1];price=4-q
            if d<=price:continue
            bt=Z['destination'][b][x-1];dt=L.get(min(at*N+bt,mir[at]*N+mir[bt]),0);w['explicit_retirement_couplings']+=1
            if price+dt-d<0:
                As,p0=source(a,j,side);At,H=S.access(As,2*x);assert p==p0 and H==2
                w['counter']={'source_A':As,'actual_A_target':At,'private_key':p,'source_B_core_index':b,'B_target_core_index':bt,'target_actual_key':2*x,'H':2,'Q':q,'price':price,'DELETE_helper':None,'operation_word':[['K',2*x]],'old_source_A_index':a,'old_projected_target_index':at,'D_source':d,'D_target':dt,'signed_margin':price+dt-d,'saturated_side':side,'fringe_anchor':j,'fringe_old_depth':depth,'source_contraction_indices':tuple(S.idx[t] for t in projections(As,p)),'target_contraction_indices':(at,)};break
        w['cursor']=i+1
        if w['counter']:break
    else:complete=True
    w.update(status='SATURATED_H2_RETIREMENT_RAW_PULLBACK_FAILURE' if w['counter'] else 'COMPLETE_FIXED_TEN_SATURATED_H2_RETIREMENT_COEFFICIENT_CHECK' if complete else 'SATURATED_H2_RETIREMENT_SCAN_OPEN',complete=complete,source_identity_instantiations_this_phase=S.calls,source_queries=0,source_engine_calls=0,principal_U33='OPEN')
    with (B/('saturated_H2_retirement_work_%02d.json'%serial)).open('x') as f:json.dump(w,f,indent=2)
    print(json.dumps({k:v for k,v in w.items() if k!='counter'}))
