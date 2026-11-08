"""Fresh distinct ordinary-splay replay of deficit-inventory/profile refutations."""
import json,time,sys,hashlib,importlib.util
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    z=json.loads((B/'deficit_profile_source_countercertificates.json').read_text());assert all(hashlib.sha256((B/n).read_bytes()).hexdigest()==v for n,v in z['input_sha256'].items());T=list(map(fr,json.loads((B/'native10_source_actions.json').read_text())['trees']));anonymous=json.loads((B/z['anonymous_inventory_source']).read_text());witnesses=[('anonymous',anonymous)]+[('ordered_'+str(i),r['closed_history']) for i,r in enumerate(z['ordered_profile_cycle'])];sp=importlib.util.spec_from_file_location('independent_deficit_profiles33',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_independent2.py');I=importlib.util.module_from_spec(sp);sp.loader.exec_module(I)
    def tick():
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_AUDIT_CAP')
        queries+=1
    I.tick=tick
    def shape(t):
        def walk(v,hi):return 'F'+str(hi) if v is None else (v.key,walk(v.left,v.key-1),walk(v.right,hi))
        return walk(t.root,10)
    def deficits(state):
        def depths(t):
            d={}
            def visit(t,h):
                if isinstance(t,str):return
                k,l,r=t;d[k]=h;visit(l,h+1);visit(r,h+1)
            visit(t,0);return d
        A=depths(state[0]);B=depths(state[1]);return [max(0,B[k]//2-2*((A[k]+1)//2)) for k in range(1,11)]
    results=[];fullpairs=[]
    for name,source in witnesses:
        tt=[I.Tree(T[source['initial_diagonal_index']]) for _ in range(3)];rows={r[0]:r for r in source['rows']};observed={};lru=[];elru=[];seam=None;start=None
        for copy in range(source['u']+source['L']):
            for local,(mode,x) in enumerate(source['word'],1):
                t=copy*len(source['word'])+local
                if t==source['period'][0]:seam=(lru[:],elru[:]);start=tuple(shape(v) for v in tt)
                before=tuple(shape(v) for v in tt);pa,ea=tt[0].access(x);pf=pe='';ef=ee=[]
                if mode=='K':pf,ef=tt[1].access(x)
                if mode=='K' and x!=10:pe,ee=tt[2].access(x)
                after=tuple(shape(v) for v in tt)
                if mode=='K':
                    if x in lru:lru.remove(x)
                    lru.insert(0,x)
                    if x!=10:
                        if x in elru:elru.remove(x)
                        elru.insert(0,x)
                if t in rows:
                    r=rows[t];assert (mode,x)==(r[1],r[2]) and before==tuple(T[i] for i in r[3:6]) and after==tuple(T[i] for i in r[6:9]);assert (len(ea),len(pf)//2,len(pe)//2)==tuple(r[9:12]);observed[t]=(before,after,len(ea),len(pf)//2)
        assert len(observed)==len(rows) and (lru,elru)==seam and tuple(shape(v) for v in tt)==start;genuine={r[2] for r in source['rows'] if r[1]=='K' and T[r[4]][0]!=r[2]};assert genuine==set(range(1,11));lo,hi=source['natural_packet'];assert rows[lo-1][1]=='K' and T[rows[lo-1][4]][0]!=rows[lo-1][2] and rows[hi][1]=='K' and T[rows[hi][4]][0]!=rows[hi][2];before=observed[lo][0];after=observed[hi][1];profile0=deficits(before);profile1=deficits(after);H=sum(observed[t][2] for t in range(lo,hi+1));Q=sum(observed[t][3] for t in range(lo,hi+1));A=sum(r[9] for r in source['rows']);QF=sum(r[10] for r in source['rows']);assert (H,Q)==(source['H'],source['Q']) and 2*A-QF>=0
        if name=='anonymous':assert sorted(v for v in profile0 if v)==sorted(v for v in profile1 if v)==[1] and (H,Q)==(1,3)
        else:i=int(name.split('_')[1]);r=z['ordered_profile_cycle'][i];assert profile0==r['ordered_profile_before'] and profile1==r['ordered_profile_after'] and (H,Q)==(r['source']['H'],r['source']['Q']);fullpairs.append((before[:2],after[:2]))
        results.append({'witness':name,'period':source['period'],'natural_packet':[lo,hi],'profile_before':profile0,'profile_after':profile1,'H':H,'Q':Q,'price':2*H-Q,'A':A,'QF':QF,'CD_margin':2*A-QF})
    ordered=results[1:];assert ordered[0]['profile_after']==ordered[1]['profile_before'] and ordered[1]['profile_after']==ordered[0]['profile_before'] and sum(r['price'] for r in ordered)==-1;assert any(fullpairs[i][1]!=fullpairs[(i+1)%2][0] for i in range(2));out('deficit_profile_independent_source_audit.json',{'status':'PASS_SOURCE_EXACT_ANY_POSITIVE_DEFICIT_PROFILE_DEBT_REFUTATION','anonymous_inventory_any_function_refuted':True,'complete_ordered_positive_profile_any_function_refuted':True,'witnesses':results,'ordered_profile_cycle_price':-1,'full_tree_states_do_NOT_form_an_actual_cycle':True,'all_actual_source_and_chart_seams_closed':True,'uniform_lifting':'same source term identities admit arbitrary rigid private gap BSTs and reflection, preserving every marked-key path; proof supplied separately','source_queries':queries,'not_a_Coarse_Double_counterexample':True,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('deficit_profile_source_countercertificates.json','positive_deficit_inventory_closed_source.json','native10_source_actions.json')}});print(json.dumps({'status':'PASS_ANY_POSITIVE_DEFICIT_PROFILE_REFUTATION','source_histories':len(results),'ordered_cycle_prices':[r['price'] for r in ordered],'source_queries':queries,'CD_margins':[r['CD_margin'] for r in results]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify29_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
