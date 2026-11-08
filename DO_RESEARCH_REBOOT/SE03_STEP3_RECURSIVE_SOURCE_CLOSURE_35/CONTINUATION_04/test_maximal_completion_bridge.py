"""Exact counterexample search for a proposed maximal-core completion bridge.
Uses complete accepted B table; no new source-engine query. A pass is NOT
a universal bridge proof. A nilpotent word has a full finite ranking proof.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    table=json.loads((F/'full_B_actions.json').read_text());gram=json.loads((F/'maximal_B_grammar.json').read_text());base=json.loads((F/'complete_product_model_k0.json').read_text())
    marks=gram['marks'];words=[[1,13,3,11,5,9,7],[1,13,7,3,11,5,9],[1,5,9,13,3,7,11],[1,13,3,5,7,9,11],[1,3,5,7,9,11,13]]
    results=[];counter=None
    for word in words:
        starts=[i for i,t in enumerate(gram['trees']) if t[0]==word[-1]];index=set(starts);nxt={};failure={}
        for s in starts:
            b=s
            for j,key in enumerate(word):
                row=table['actions'][b][marks.index(key)]
                if not row['admissible']:
                    failure[s]={'word_offset':j,'B_before':b,'key':key,'H':row['H'],'q':row['q']};b=-1;break
                b=row['destination']
            nxt[s]=b;assert b<0 or b in index
        remaining=set(starts);rank={};layer=0
        while remaining:
            remove=[s for s in remaining if nxt[s]<0 or nxt[s] in rank]
            if not remove:break
            layer+=1
            for s in remove:rank[s]=layer
            remaining.difference_update(remove)
        result={'word':word,'starting_core_states':len(starts),'nilpotent':not remaining,'rank_bound':layer,'cyclic_survivors':len(remaining)};results.append(result)
        if remaining:continue
        counter={'word':word,'starts':starts,'next':nxt,'rank':rank,'failure':failure,'rank_bound':layer};break
    out={'status':'MAXIMAL_COMPLETION_REFUTED' if counter else 'NO_COUNTER_IN_SELECTED_WORDS','results':results,'counter':counter,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'candidate_refuted_if_found':'every original seven-key cyclic KEEP word admits a paired-closed maximal-core13 B completion after adding only never-accessed keys',
      'input_sha256':{p:sha(F/p) for p in ('full_B_actions.json','maximal_B_grammar.json','complete_product_model_k0.json')}}
    if counter:
        word=counter['word'];cols=[marks.index(k) for k in word]
        seen={};copies=[];state=0
        while state not in seen:
            seen[state]=len(copies);copies.append(state)
            for x in cols:state=base['A_destination'][state][x]
        warm=seen[state];period_copies=len(copies)-warm;initial=state
        out['ordinary_mark_only_source']={'initial_A_B_native7_state':initial,'word_copies_per_A_B_period':period_copies,'warm_search_copies_not_part_of_source':warm}
    with (F/'maximal_completion_bridge_result.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('counter','input_sha256')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof220_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
