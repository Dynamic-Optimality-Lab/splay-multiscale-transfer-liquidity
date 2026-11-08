"""Bounded SOURCE discovery: retain actual full B instead of only its root.
Not a claimed universal proof. All original query/CPU controllers remain outside.
"""
import json,pickle,time,hashlib,collections,itertools
from pathlib import Path
from interior_projection_source_tools import *
B=Path(__file__).resolve().parent
def run(serial,cap):
    start=time.process_time();Z=json.loads((B/'native10_source_actions.json').read_text());S=Lift(Z);T=S.T;N=len(T);mir=Z['mirror'];payload=B/'native10_debt_03.pkl';raw=payload.read_bytes();pin=hashlib.sha256(raw).hexdigest();receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());assert pin==receipt['input_sha256'];level=pickle.loads(raw)['level'];del raw
    def debt(a,b):return level.get(min(a*N+b,mir[a]*N+mir[b]),0)
    if serial==1:work={'labels':{},'upper':{},'edges':{},'outgoing':{},'derivation':[],'contradiction':None,'next_coefficient':0,'coefficients_exhausted':False,'source_couplings':0,'source_pin':pin}
    else:
        with (B/('B_sensitive_contraction_work_%02d.pkl'%(serial-1))).open('rb') as f:work=pickle.load(f)
        assert work['source_pin']==pin and work['contradiction'] is None
    labels,upper,edges,outgoing=map(work.get,('labels','upper','edges','outgoing'))
    def feature(b,values):
        m=sum(1<<v for v in set(values));code=16*b+m
        if code not in labels:labels[code]=m.bit_length()-1 if m&(m-1)==0 else 0;upper[code]=m.bit_length()-1 if m&(m-1)==0 else 3
        assert len(labels)<2000000;return code
    def add(e,source_values,target_values):
        if work['contradiction']:return
        s=feature(e['source_B_core_index'],source_values);t=feature(e['B_target_core_index'],target_values);key=s,t
        if key in edges and edges[key]['price']<=e['price']:return
        e=e.copy();e.update(source_feature=s,target_feature=t,source_value_set=sorted(set(source_values)),target_value_set=sorted(set(target_values)));edges[key]=e;outgoing.setdefault(s,{})[t]=e;assert len(edges)<=5000000
        queue=collections.deque([s]);pending={s}
        while queue:
            u=queue.popleft();pending.remove(u)
            for v,edge in outgoing.get(u,{}).items():
                need=labels[u]-edge['price']
                if need<=labels[v]:continue
                work['derivation'].append({'edge':edge.copy(),'source_label':labels[u],'old_target_label':labels[v],'new_target_label':need});labels[v]=need
                if need>upper[v]:work['contradiction']={'feature':v,'required':need,'upper':upper[v]};return
                if v not in pending:queue.append(v);pending.add(v)
    if serial==1:
        for name in ('interior_max_contraction_closed_source.json','root_aware_contraction_first_closed_source.json','root_aware_contraction_second_closed_source.json'):
            e=json.loads((B/name).read_text())['candidate'];z=e['private_key'];ps=[S.idx[v] for v in projections(fr(e['source_A']),z)];pt=[S.idx[v] for v in projections(fr(e['actual_A_target']),z)];add(e,[debt(a,e['source_B_core_index']) for a in ps],[debt(a,e['B_target_core_index']) for a in pt])
    motifs={};begin=work['next_coefficient'];complete=False
    for j,(code,ds) in enumerate(itertools.islice(level.items(),begin,None),begin):
        if work['contradiction']:break
        if time.process_time()-start>cap-2:break
        a,b=divmod(code,N)
        for aa,bb in ((a,b),(mir[a],mir[b])):
            if T[aa][0]!=1:continue
            if aa not in motifs:
                g,A,R=T[aa]
                if not isnode(R) or not isnode(R[1]):motifs[aa]=None
                else:
                    x=R[0];z=3;As=(2,scale(A),(z,'new_gap',scale(R)));At,h=S.access(As,2*x);assert h==1;pt=tuple(S.idx[v] for v in projections(At,z));successors=[]
                    for y in known(At):
                        if y==z or y==At[0] or len(path(At,y))>2:continue
                        Att,hy=S.access(At,y);assert hy==1;ptt=tuple(S.idx[v] for v in projections(Att,z));successors.append((y,Att,ptt))
                    motifs[aa]=x,As,At,pt,successors
            if motifs[aa] is None:continue
            x,As,At,pt,successors=motifs[aa];bt=Z['destination'][bb][x-1];q=Z['Q'][bb][x-1];dst=[debt(a,bt) for a in pt];work['source_couplings']+=1
            add({'source_A':As,'actual_A_target':At,'private_key':3,'source_B_core_index':bb,'B_target_core_index':bt,'target_actual_key':2*x,'H':1,'Q':q,'price':2-q,'source_kind':'unary_RR'},[ds],dst)
            for y,Att,ptt in successors:
                btt=Z['destination'][bt][y//2-1];qy=Z['Q'][bt][y//2-1];add({'source_A':At,'actual_A_target':Att,'private_key':3,'source_B_core_index':bt,'B_target_core_index':btt,'target_actual_key':y,'H':1,'Q':qy,'price':2-qy,'source_kind':'actual_successor'},dst,[debt(a,btt) for a in ptt])
                if work['contradiction']:break
            if work['contradiction']:break
        work['next_coefficient']=j+1
    else:complete=True;work['coefficients_exhausted']=True
    with (B/('B_sensitive_contraction_work_%02d.pkl'%serial)).open('xb') as f:pickle.dump(work,f,protocol=5)
    result={'status':'B_SENSITIVE_CONTRACTION_FORMULA_COUNTERCERTIFICATE_CANDIDATE' if work['contradiction'] else 'B_SENSITIVE_SOURCE_RULE_DISCOVERY_OPEN','serial':serial,'next_coefficient':work['next_coefficient'],'restricted_positive_source_stream_exhausted':complete,'source_couplings':work['source_couplings'],'variables':len(labels),'edge_records':len(edges),'contradiction':work['contradiction'],'new_source_identity_instantiations':S.calls,'source_queries':0,'source_engine_calls':0,'actual_source_scope':'fixed private gap1; actual full B plus projection-debt set; agrees with old singleton debt, candidate width3','not_a_universal_passing_test':'even exhaustion of this source stream omits other source schemas and arbitrary support','principal_U33':'OPEN'}
    with (B/('B_sensitive_contraction_result_%02d.json'%serial)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
