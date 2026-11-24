"""Separate immutable-tree operation and gap verifier; no primary rotations."""
import json
import time
from pathlib import Path
import sharp01_tuple_reference as ref

def tuple_state(state):
    ch={int(k):v for k,v in state['children'].items()}; built={None:ref.LEAF}
    todo=[] if state['root'] is None else [(state['root'],False)]
    while todo:
        k,done=todo.pop()
        if done:
            l,r=ch[k]; built[k]=ref.node(k,built[l],built[r])
        else:
            todo.append((k,True)); todo.extend((c,False) for c in ch[k] if c is not None)
    return built[state['root']]

def validate(source,ledger):
    a=b=tuple_state(source.get('diagonal_initial',source['initial_A']))
    for tag,x in source.get('reaching_prefix',[]):
        a,_=ref.trace(a,x)
        if tag=='K':b,_=ref.trace(b,x)
    assert a==tuple_state(source['initial_A']) and b==tuple_state(source['initial_B'])
    start=(a,b); snapshots=[start]; aa=[]; qq=[]
    for (tag,x),row in zip(source['operations'],ledger['operations']):
        assert ref.lookup(a,x)[0] and ref.lookup(b,x)[0]
        da=ref.lookup(a,x)[1]; db=ref.lookup(b,x)[1]
        a,ea=ref.trace(a,x); eb=[]
        if tag=='K':b,eb=ref.trace(b,x)
        ac=(da+1)//2; qc=db//2 if tag=='K' else 0
        assert ac==row['a'] and qc==row['q'] and len(ea)==ac
        assert sum(e[0]!='ZIG' for e in eb)==qc
        assert a==tuple_state(ledger['states'][row['post'][0]])
        assert b==tuple_state(ledger['states'][row['post'][1]])
        ps=ledger['steps'][slice(*row['step_range'])]
        assert [s['case'] for s in ps if s['id'][0]=='A']==[e[0] for e in ea]
        assert [s['case'] for s in ps if s['id'][0]=='B']==[e[0] for e in eb]
        aa.append(ac); qq.append(qc); snapshots.append((a,b))
    assert (a,b)==start
    # Construct the partition by unwrapping AFTER the last KEEP, not by
    # the primary oracle's previous-KEEP modular interval algorithm.
    ks=[i for i,(tag,x) in enumerate(source['operations']) if tag=='K']
    built={}
    if ks:
        first=(ks[-1]+1)%len(aa); order=list(range(first,len(aa)))+list(range(first))
        block=[]; prev=ks[-1]
        for k in order:
            block.append(k)
            if source['operations'][k][0]=='K':
                x=source['operations'][k][1]; sa,sb=snapshots[prev+1]
                H=sum(aa[z] for z in block); p=(ref.lookup(sa,x)[1]+1)//2; q=ref.lookup(sb,x)[1]//2
                built[k+1]=([z+1 for z in block],H,p,q,max(q-2*p,0),2*H-min(q,2*p))
                block=[]; prev=k
        assert not block
        for g in ledger['gaps']:
            assert built[g['KEEP_operation_id']]==(g['operation_ids'],g['H'],g['p'],g['q'],g['u'],g['c'])
    assert sum(aa)==ledger['summary']['A'] and sum(qq)==ledger['summary']['Q']
    return len(aa)

def main():
    base=Path(__file__).resolve().parent; started=time.process_time(); wall=time.perf_counter()
    sources=json.loads((base/'SHARP01_SOURCE_WITNESSES.json').read_text())['sources']
    index=json.loads((base/'SHARP01_GAP_LEDGER.json').read_text())['ledgers']
    count=0
    for src,item in zip(sources,index):
        assert src['name']==item['name']
        ledger=json.loads((base/item['path']).read_text())
        count+=validate(src,ledger)
        assert time.process_time()-started<120,'new SHARP verification ceiling'
    result={'status':'PASS','sources':len(sources),'operation_transitions':count,
            'cpu_seconds':time.process_time()-started,'wall_seconds':time.perf_counter()-wall,
            'level':'same agent, distinct pointer and immutable implementations; no formal or external certification'}
    (base/'SHARP01_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result))

if __name__=='__main__':main()
