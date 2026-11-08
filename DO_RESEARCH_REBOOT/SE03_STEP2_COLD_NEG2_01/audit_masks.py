"""Gate E controls for all16 necessary masks; no universal realization claim."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
sys.path.insert(0,str(ROOT/'python'))
from independent import splay as source
account={'new_finite_tests':0,'source_engine_calls':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def marked_core(t,marks):
    if t==source.LEAF:return set()
    l=marked_core(t[2],marks);r=marked_core(t[3],marks)
    return {t[1]}|l|r if t[1] in marks or l or r else set()
def apply(t,word):
    rows=[]
    for x in word:
        before=t;t,ev=source.trace(t,x);account['source_engine_calls']+=1
        rows.append({'key':x,'a':len(ev),'q':sum(q[0]!='ZIG' for q in ev),'genuine':before[1]!=x})
    return t,rows
def main():
    records=[]
    for code in range(16):
        P=[0]+[(code>>j)&1 for j in range(4)]+[1]
        gaps=[1+P[j]-P[j+1] for j in range(5)];marks=[1]
        for u in gaps:marks.append(marks[-1]+u+1)
        assert marks[-1]==10 and len(set(marks))==6 and sum(gaps)==4
        # Actual common-tree diagonal, even when this initial marked mask
        # does NOT satisfy the closed-period density at its right-vine cut.
        initial=source.vine(10);word=[marks[-1],marks[0]]+marks[1:]+list(reversed(marks[:-1]))
        seen={};t=initial;states=[];costs=[];period=None
        for turn in range(33):
            if t in seen:period=(seen[t],turn-seen[t]);break
            seen[t]=turn;states.append(t);t,rows=apply(t,word);costs.append(rows)
        if period is None:
            records.append({'P':P,'initial_marks':marks,'status':'NO_CLOSURE_FOUND_WITHIN32_COPIES','unrealizable_claimed':False})
        else:
            u,L=period;start=states[u];final=start;closedrows=[]
            for j in range(L):final,rows=apply(final,word);closedrows+=rows
            assert final==start and set(q['key'] for q in closedrows if q['genuine'])==set(marks)
            S=marked_core(start,set(marks));c=len(S)
            records.append({'P':P,'gaps':gaps,'initial_marks':marks,'word':word,'reaching_copies':u,'period_copies':L,
                'recurrent_tree':start,'full_pair_closed':True,'actual_recurrent_core':sorted(S),'actual_core_size':c,
                'initial_mask_realized_at_core10':c==10,'A':sum(q['a'] for q in closedrows),
                'QF':sum(q['q'] for q in closedrows),'unrealizable_claimed':False,
                'test_meaning':'all KEEP diagonal A=B control; no NEG2 inequality is inferred'})
        account['new_finite_tests']+=1
    assert len({tuple(r['initial_marks']) for r in records})==16
    out('mask_replay.json',{'status':'PASS_ALL16_NECESSARY_MASK_SOURCE_CONTROLS','records':records,
        'actual_core10_masks_found':[r['initial_marks'] for r in records if r.get('initial_mask_realized_at_core10')],
        'failure_to_retain_a_mask_is_not_impossibility':True,'source_graph_built':False,'new_weighted_graph':False,
        'universal_NEG2_claimed':False,**account})
    print(json.dumps({'status':'PASS_ALL16_NECESSARY_MASK_SOURCE_CONTROLS','core10_realizations':sum(r.get('initial_mask_realized_at_core10',False) for r in records),**account}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_masks_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
