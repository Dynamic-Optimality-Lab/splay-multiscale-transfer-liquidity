"""Exact complete unary source inequalities; no finite-population inference.
Try contraction, fixed-base extension, then unrestricted state correction.
Adverse paths are comparison obstructions, not source/CD counterexamples.
"""
import collections,json,sys,time
from array import array
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
started=time.process_time();LIMIT=float(sys.argv[1])-3
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    G=read(B/'unary_grammar.json');base=read(OLD/'cheap_A_comparison.json')['reports'][0]
    bf=read(OLD/'bf9_comparison.json');nB=len(base['BF_trees']);nA=len(G['states']);size=nA*nB
    assert (nA,nB)==(1452,903) and size<2000000
    rank={x:i+1 for i,x in enumerate(base['BF_marks'])};roots=[t[0]//1000 for t in G['states']]
    ar=collections.defaultdict(list)
    for a,r in enumerate(roots):ar[r].append(a)
    adjB=[[] for _ in range(nB)]
    for s,t,x,q in bf['edges']:
        if s<nB:adjB[s].append((t,rank[x],q))
    adjA=[collections.defaultdict(list) for a in range(nA)]
    for H,name in ((1,'H1'),(2,'H2')):
        for a,x,b in G[name]:adjA[a][x].append((b,H))
    valid=[a*nB+b for b,t in enumerate(base['BF_trees']) for a in ar[rank[t[0]]]]
    assert len(valid)==344982
    old=array('b',[-9])*(132*nB)
    for (a,b),d in zip(base['states'],base['debt']):old[a*nB+b]=d
    zerofail=[];counts=collections.Counter();fails=collections.Counter()
    for sid in valid:
        a,b=divmod(sid,nB);da=old[G['contract_ids'][a]*nB+b]
        for bb,x,q in adjB[b]:
            for aa,H in adjA[a].get(x,()):
                value=2*H-q+old[G['contract_ids'][aa]*nB+bb]-da;counts[str(H)]+=1
                if value<0:
                    fails[str(H)]+=1
                    if len(zerofail)<16:zerofail.append({'source':[a,b],'target':[aa,bb],'x':x,'H':H,'Q':q,'residual':value})
    assert sum(counts.values())<5000000
    def solve(fixed=False,high=False,K=2):
        d=array('b',[-9])*size;proof=array('i',[-1])*size;inside=bytearray(size)
        ql=collections.deque(valid);nodes=[];maxD=[0]*nB;maxNode=[-1]*nB;hq=collections.deque();hset=set();updates=0
        for sid in valid:
            a,b=divmod(sid,nB);d[sid]=old[sid] if fixed and a<132 else 0;inside[sid]=1
            if d[sid]>maxD[b]:maxD[b]=d[sid];maxNode[b]=sid
        conflict=None
        def raise_to(dst,new,src,meta):
            nonlocal updates,conflict
            if new<=d[dst]:return
            aa,bb=divmod(dst,nB)
            rec={'target':dst,'required':new,'source':src,'source_value':d[src],
                'parent':proof[src],'edge':meta};nodes.append(rec);pi=len(nodes)-1
            assert len(nodes)<4000000
            if new>K or (fixed and aa<132 and new>old[dst]):
                chain=[];j=pi
                while j>=0:chain.append(nodes[j]);j=nodes[j]['parent']
                chain.reverse();conflict={'kind':'RANGE_BOUND' if new>K else 'FROZEN_BASE_VALUE',
                    'target':[aa,bb],'required':new,'allowed':K if aa>=132 or not fixed else old[dst],
                    'path':chain,'scope':'necessary source comparison only; complete original-period realization not assumed'};return
            d[dst]=new;proof[dst]=pi;updates+=1
            if not inside[dst]:ql.append(dst);inside[dst]=1
            if new>maxD[bb]:
                maxD[bb]=new;maxNode[bb]=dst
                if high and bb not in hset:hq.append(bb);hset.add(bb)
        while (ql or hq) and conflict is None:
            if time.process_time()-started>LIMIT:raise RuntimeError('bounded unary discovery phase CPU stop')
            if high and hq:
                b=hq.popleft();hset.remove(b)
                for bb,x,Q in adjB[b]:
                    lower=maxD[b]+Q-6
                    if lower<=0:continue
                    for a in ar[x]:
                        raise_to(a*nB+bb,lower,maxNode[b],{'H':3,'Q':Q,'x':x,'HIGH':True})
                        if conflict:break
                    if conflict:break
                continue
            sid=ql.popleft();inside[sid]=0;a,b=divmod(sid,nB);ds=d[sid]
            for bb,x,Q in adjB[b]:
                for aa,H in adjA[a].get(x,()):
                    raise_to(aa*nB+bb,ds+Q-2*H,sid,{'H':H,'Q':Q,'x':x,'HIGH':False})
                    if conflict:break
                if conflict:break
        result={'fixed_A6_numeric_values':fixed,'HIGH_included':high,'bound':K,'updates':updates,'proof_DAG_nodes':len(nodes),
            'status':'FEASIBLE_EXACT' if conflict is None else 'INFEASIBLE_BOUNDED_COMPARISON','conflict':conflict}
        if conflict is None:
            for sid in valid:
                a,b=divmod(sid,nB)
                for bb,x,Q in adjB[b]:
                    for aa,H in adjA[a].get(x,()):assert 2*H-Q+d[aa*nB+bb]-d[sid]>=0
            if high:
                mins=[min(d[a*nB+b] for a in ar[rank[t[0]]]) for b,t in enumerate(base['BF_trees'])]
                for b in range(nB):
                    for bb,x,Q in adjB[b]:assert 6-Q+mins[bb]-maxD[b]>=0
            result.update({'valid_states':valid,'debt':[d[s] for s in valid],'max_debt':max(d),
                'old_A6_values_changed':sum(d[a*nB+b]!=old[a*nB+b] for a,b in base['states'])})
        return result
    attempts=[];winner=None
    for fixed,high,K in ((True,False,2),(False,False,2),(False,True,21)):
        result=solve(fixed,high,K);attempts.append(result)
        if result['status']=='FEASIBLE_EXACT':winner=len(attempts)-1;break
    result={'status':'UNARY_SIGNED_CERTIFICATE_CONSTRUCTED' if winner is not None else 'UNARY_COMPARISON_OPEN',
        'scope':'original core9 first mask, zero/one unmarked unary A boundary ancestor, arbitrary free private BSTs',
        'core9_full':'OPEN; branching/multiple A ancestors and other BF masks not covered',
        'core10_11_full':'OPEN','A_states':nA,'BF_states':nB,'valid_pair_states':len(valid),'LOW_rows':dict(counts),
        'zero_correction_failures':dict(fails),'zero_correction_examples':zerofail,'attempts':attempts,'winner':winner,
        'BF_marks':base['BF_marks'],'BF_trees':base['BF_trees'],'source_engine_calls':0,
        'no_inherited_file_modified':True,'owners':'existing a/fE maps never input to formula search or reassigned'}
    out('unary_lift_certificate.json',result)
    print(json.dumps({'status':result['status'],'states':len(valid),'rows':dict(counts),'zero_correction_failures':dict(fails),
        'attempts':[{'fixed':v['fixed_A6_numeric_values'],'HIGH':v['HIGH_included'],'status':v['status'],'Dmax':v.get('max_debt'),'conflict':v['conflict']['kind'] if v['conflict'] else None} for v in attempts]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_lift_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})
