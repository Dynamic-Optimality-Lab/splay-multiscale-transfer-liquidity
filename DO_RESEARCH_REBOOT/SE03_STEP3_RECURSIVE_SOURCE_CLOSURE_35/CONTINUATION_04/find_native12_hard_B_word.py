"""Choose a source cycle where H>=1 alone cannot finance the B demands."""
import functools,hashlib,importlib.util,json,pickle,random,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
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
    with (F/'native12_tree_basis.pkl').open('rb') as f:basis=pickle.load(f)
    with (F/'probe11_source_actions.pkl').open('rb') as f:old=pickle.load(f)
    T=basis['trees'];index={t:i for i,t in enumerate(T)};oi={t:i for i,t in enumerate(old['trees'])}
    prior=json.loads((F/'native12_fixed_B_word.json').read_text());known={(a['source'],a['target_key']):(a['destination'],a['H'],a['Q']) for a in prior['fresh_Hamiltonian_actions']}
    sp=importlib.util.spec_from_file_location('native12_hard_B_new_Hamiltonian',B/'audit_core39.py');V=importlib.util.module_from_spec(sp);sp.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    lifts=0;fresh=[]
    @functools.lru_cache(maxsize=50000)
    def action(s,x):
        nonlocal lifts
        if (s,x) in known:return known[s,x]
        t=T[s];y=next((v for v in leaves(t) if v!=x),None)
        if y is None:
            after,h,q,ev=V.splay(t,x,True);out=(index[after],h,q)
            known[s,x]=out;fresh.append({'source':s,'target_key':x,'destination':out[0],'H':h,'Q':q,'events':ev});return out
        a=oi[lower(t,y)];xx=x-(x>y);o=old['trees'][int(old['destination'][a,xx-1])]
        lifts+=1;return index[insert(raise_tree(o,y),y)],int(old['H'][a,xx-1]),int(old['Q'][a,xx-1])
    rng=random.Random(35122160);best=None;trials=0
    while trials<5000 and time.process_time()-START<CAP-4:
        trials+=1;word=list(range(1,13));rng.shuffle(word);s=0;seen={s:0};copies=[]
        for copy in range(4):
            rows=[]
            for x in word:
                a=s;s,h,q=action(s,x);rows.append({'KEEP':x,'B_source':a,'B_target':s,'Q':q})
            copies.append(rows)
            if s in seen:u=seen[s];L=copy+1-u;break
            seen[s]=copy+1
        else:continue
        if L!=1:continue
        rows=copies[u];Q=sum(r['Q'] for r in rows)
        if best is None or Q>best['Q']:
            best={'word':word,'prefix_B_copies':u,'period_B_copies':L,'rows':rows,'Q':Q}
        if Q>=28:break
    assert best is not None
    best.update({'status':'LITERAL_CLOSED_NATIVE12_HARD_B_WORD','next_key_by_root':{T[r['B_source']][0]:r['KEEP'] for r in best['rows']},
      'native12_states':len(T),'root_counts':basis['root_counts'],'root_offsets':basis['root_offsets'],
      'sampled_permutations':trials,'B_only_minimum_A_event_margin':24-best['Q'],
      'source_cached_substitutions':lifts,'fresh_Hamiltonian_actions':fresh,'source_queries':V.CALLS,'source_engine_calls':V.CALLS,
      'basis_sha256':sha(F/'native12_tree_basis.pkl'),'JR35':'OPEN',
      'input_sha256':{p:sha(F/p) for p in ('probe11_source_actions.pkl','independent_probe11_source_actions.json','native12_fixed_B_word.json')}})
    with (F/'native12_hard_B_word.json').open('x',encoding='utf8') as f:json.dump(best,f,indent=2)
    print(json.dumps({k:v for k,v in best.items() if k not in ('rows','fresh_Hamiltonian_actions','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        n=0 if V is None else V.CALLS
        with (B/'audit_core54_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':n,'source_engine_calls':n},f)
