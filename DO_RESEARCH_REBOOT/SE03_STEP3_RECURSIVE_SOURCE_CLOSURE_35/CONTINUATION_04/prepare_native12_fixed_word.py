"""Twelve-key source basis and one literal closed B word.

Every off-target-leaf instance is a proof substitution into the already
independently accepted native11 table, as in the accepted native11 build.
Only a genuinely new Hamiltonian leaf action uses the source engine.
"""
import functools,hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
@functools.lru_cache(None)
def family(a,b):
    if a>b:return (None,)
    return tuple((x,l,r) for x in range(a,b+1) for l in family(a,x-1) for r in family(x+1,b))
def leaves(t):
    if t[1] is None and t[2] is None:return [t[0]]
    return ([] if t[1] is None else leaves(t[1]))+([] if t[2] is None else leaves(t[2]))
def lower(t,y):
    if t is None:return None
    if t[0]==y:assert t[1] is None and t[2] is None;return None
    return (t[0]-(t[0]>y),lower(t[1],y),lower(t[2],y))
def raise_tree(t,y):
    if t is None:return None
    return (t[0]+(t[0]>=y),raise_tree(t[1],y),raise_tree(t[2],y))
def insert(t,y):
    if t is None:return (y,None,None)
    return (t[0],insert(t[1],y),t[2]) if y<t[0] else (t[0],t[1],insert(t[2],y))
def main():
    global V
    cp=F/'probe11_source_actions.pkl'
    with cp.open('rb') as f:old=pickle.load(f)
    oldindex={t:i for i,t in enumerate(old['trees'])}
    trees=family(1,12);assert len(trees)==208012;index={t:i for i,t in enumerate(trees)}
    counts=[sum(t[0]==g for t in trees) for g in range(1,13)];offsets=[0]
    for c in counts:offsets.append(offsets[-1]+c)
    assert sum(counts)==208012 and counts[0]==counts[-1]==58786
    sp=importlib.util.spec_from_file_location('native12_new_B_primitive',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    lifts=0;fresh=[]
    def action(s,x):
        nonlocal lifts
        t=trees[s];ls=leaves(t);y=next((y for y in ls if y!=x),None)
        if y is None:
            after,h,q,ev=V.splay(t,x,True);fresh.append({'source':s,'target_key':x,'destination':index[after],'H':h,'Q':q,'events':ev})
            return index[after],h,q,'NEW_HAMILTONIAN_ENGINE_ACTION'
        a=oldindex[lower(t,y)];xx=x-(x>y);out=old['trees'][int(old['destination'][a,xx-1])]
        result=insert(raise_tree(out,y),y);lifts+=1
        return index[result],int(old['H'][a,xx-1]),int(old['Q'][a,xx-1]),'ACCEPTED_OFF_PATH_LEAF_SUBSTITUTION'
    word=[v for lo in range(1,7) for v in (lo,13-lo)];assert len(set(word))==12
    state=0;seen={state:0};copies=[];cf=()
    for copy in range(6):
        rows=[]
        for x in word:
            before=state;state,h,q,method=action(state,x);cf=(x,)+tuple(y for y in cf if y!=x)
            rows.append({'KEEP':x,'B_source':before,'B_target':state,'Q':q,'method':method})
        copies.append(rows)
        if state in seen:u=seen[state];L=copy+1-u;break
        seen[state]=copy+1
    else:raise AssertionError('bounded preparation did not find the B cycle')
    cycle=sum(copies[u:u+L],[]);assert cycle[0]['B_source']==cycle[-1]['B_target']
    assert all(trees[r['B_source']][0]!=r['KEEP'] for r in cycle)
    assert L==1 # This chosen model uses one B phase per root; otherwise redesign explicitly.
    nextkey={trees[r['B_source']][0]:r['KEEP'] for r in cycle};assert len(nextkey)==12
    basis={'trees':trees,'root_counts':counts,'root_offsets':offsets,'source_state_count':len(trees),
      'source_grammar':'all ordered BSTs by Catalan root/left/right recursion','private_scope':'rigid off-path ordered hangers only'}
    with (F/'native12_tree_basis.pkl').open('xb') as f:pickle.dump(basis,f,protocol=5)
    data={'status':'LITERAL_CLOSED_NATIVE12_B_WORD_PREPARED','word':word,'prefix_B_copies':u,'period_B_copies':L,
      'rows':cycle,'next_key_by_root':nextkey,'Q':sum(r['Q'] for r in cycle),
      'root_counts':counts,'root_offsets':offsets,'native12_states':len(trees),
      'cached_source_substitutions':lifts,'fresh_Hamiltonian_actions':fresh,
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'JR35':'OPEN',
      'input_sha256':{str(p):sha(p) for p in (cp,F/'independent_probe11_source_actions.json',B/'OFF_PATH_LEAF_SOURCE_LIFT.md')},
      'basis_sha256':sha(F/'native12_tree_basis.pkl')}
    with (F/'native12_fixed_B_word.json').open('x',encoding='utf8') as f:json.dump(data,f,indent=2)
    print(json.dumps({k:v for k,v in data.items() if k not in ('rows','fresh_Hamiltonian_actions','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_core53_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
