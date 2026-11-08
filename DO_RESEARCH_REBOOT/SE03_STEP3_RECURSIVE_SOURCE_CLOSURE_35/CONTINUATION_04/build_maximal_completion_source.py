"""Original diagonal, erased-closed source for the failed completion word.
All operations compose accepted native7 action identities; no fresh query.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    counter=json.loads((F/'maximal_completion_bridge_result.json').read_text());m=json.loads((F/'complete_product_model_k0.json').read_text());native=json.loads((B/'native10_source_actions.json').read_text())
    assert counter['status']=='MAXIMAL_COMPLETION_REFUTED';word=counter['counter']['word'];marks=m['A_keys'];cols=[marks.index(k) for k in word]
    initial=counter['ordinary_mark_only_source']['initial_A_B_native7_state'];periodbase=counter['ordinary_mark_only_source']['word_copies_per_A_B_period'];erased=3
    estate=initial;seen={};copy=0
    while estate not in seen:
        seen[estate]=copy
        for _ in range(periodbase):
            for key,col in zip(word,cols):
                if key!=erased:estate=m['A_destination'][estate][col]
        copy+=1;assert copy<400
    warm=seen[estate];eperiod=copy-warm;prefix_copies=(warm+eperiod)*periodbase;period_copies=eperiod*periodbase
    def physical(t):return None if t is None else [marks[t[0]-1],physical(t[1]),physical(t[2])]
    A=BE=initial;cf=[];ce=[];rows=[];boundary=None
    def push(chart,key):return ([key]+[k for k in chart if k!=key])[:5]
    length=prefix_copies+period_copies
    for c in range(length):
        if c==prefix_copies:boundary=(A,BE,tuple(cf),tuple(ce))
        for key,x in zip(word,cols):
            t=len(rows)+1;beforeA=A;beforeE=BE;g=marks[m['A_trees'][A][0]-1]!=key
            h=m['A_H'][A][x];q=native['Q'][m['A_native10_indices'][A]][m['A_native10_columns'][x]]
            A=m['A_destination'][A][x];qe=0;ge=False
            if g:cf=push(cf,key)
            if key!=erased:
                ge=marks[m['A_trees'][BE][0]-1]!=key;qe=native['Q'][m['A_native10_indices'][BE]][m['A_native10_columns'][x]]
                BE=m['A_destination'][BE][x]
                if ge:ce=push(ce,key)
            rows.append({'t':t,'kind':'K','key':key,'A_before':physical(m['A_trees'][beforeA]),'BF_before':physical(m['A_trees'][beforeA]),'BE_before':physical(m['A_trees'][beforeE]),
              'A_after':physical(m['A_trees'][A]),'BF_after':physical(m['A_trees'][A]),'BE_after':physical(m['A_trees'][BE]),
              'a':h,'qF':q,'qE':qe,'genuine_F':g,'genuine_E':ge,'chart_F':cf[:],'chart_E':ce[:]})
    assert boundary==(A,BE,tuple(cf),tuple(ce));start=prefix_copies*len(word)+1;period=[r for r in rows if r['t']>=start]
    h0=[]
    for r in period:
        units=[(r['t'],j,b) for j in range(1,r['a']+1) for b in (0,1)];assert r['qF']<=len(units)
        h0.extend({'demand':(r['t'],k),'unit':units[k-1]} for k in range(1,r['qF']+1))
    out={'status':'ORIGINAL_DIAGONAL_PAIRED_CLOSED_SOURCE','word':word,'erased_genuine_key':erased,
      'initial_diagonal':physical(m['A_trees'][initial]),'prefix_rows':[r for r in rows if r['t']<start],'period_rows':period,
      'period':[start,len(rows)],'prefix_word_copies':prefix_copies,'period_word_copies':period_copies,
      'full_genuine_support':sorted({r['key'] for r in period if r['genuine_F']}),'A_events':sum(r['a'] for r in period),
      'QF':sum(r['qF'] for r in period),'QE':sum(r['qE'] for r in period),'h0_full_own':h0,
      'source_cache_accesses':len(rows)+sum(r['key']!=erased for r in rows),'source_queries':0,'source_engine_calls':0,
      'maximal_completion':'IMPOSSIBLE_BY_COMPLETE_CORE13_RANK_CERTIFICATE','Coarse_Double_counterexample':False,'JR35':'OPEN',
      'input_sha256':{p:sha(F/p) for p in ('maximal_completion_bridge_result.json','complete_product_model_k0.json')}}
    with (F/'maximal_completion_original_source.json').open('x',encoding='utf-8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k in ('status','word','period','prefix_word_copies','period_word_copies','A_events','QF','QE','source_queries','full_genuine_support')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof221_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
