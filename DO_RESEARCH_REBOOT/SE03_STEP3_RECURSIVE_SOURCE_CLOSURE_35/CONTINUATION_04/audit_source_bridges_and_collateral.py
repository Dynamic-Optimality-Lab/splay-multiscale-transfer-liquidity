"""New independent original-source controls, with all fresh queries charged.
No producer kernel imported. Complete source semantics + owner/bank audit.
"""
import collections,hashlib,importlib.util,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eq(a,b):return json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True)
def tree(t):return None if t is None else (t[0],tree(t[1]),tree(t[2]))
def clusters(t,M):
    out=set()
    def go(t):
        if t is None:return frozenset()
        s=go(t[1])|go(t[2])|({t[0]} if t[0] in M else set())
        if s:out.add(frozenset(s))
        return s
    go(t);return out
def main():
    global V
    spec=importlib.util.spec_from_file_location('new_CCR_mutable',B/'audit_verify79.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    def replay(z,diagonal_reuse=False):
        A=V.Mutable(z['initial_diagonal']);BF=None if diagonal_reuse else V.Mutable(z['initial_diagonal']);BE=V.Mutable(z['initial_diagonal'])
        cf=[];ce=[];boundary=None;actual=[];M=set(z.get('full_genuine_support',[1,3,5,7,9,11,13]));rotations=0
        def push(c,k):return [k]+[v for v in c if v!=k]
        for r in z['prefix_rows']+z['period_rows']:
            if r['t']==z['period'][0]:boundary=(A.snapshot(),A.snapshot() if BF is None else BF.snapshot(),BE.snapshot(),tuple(cf[:5]),tuple(ce[:5]))
            assert eq(A.snapshot(),r['A_before']) and eq(A.snapshot() if BF is None else BF.snapshot(),r['BF_before']) and eq(BE.snapshot(),r['BE_before'])
            fullroot=A.root.k if BF is None else BF.root.k;h,qa,ae=A.splay(r['key'],True);q=qe=0;gf=ge=False
            if r['kind']=='K':
                gf=fullroot!=r['key']
                if BF is None:q=qa
                else:_,q,_=BF.splay(r['key'],False)
                if gf:cf=push(cf,r['key'])
                if r['key']!=z.get('erased_key',z.get('erased_genuine_key')):
                    ge=BE.root.k!=r['key'];_,qe,_=BE.splay(r['key'],False)
                    if ge:ce=push(ce,r['key'])
            assert (h,q,qe,gf,ge)==(r['a'],r['qF'],r['qE'],r['genuine_F'],r['genuine_E'])
            assert eq(A.snapshot(),r['A_after']) and eq(A.snapshot() if BF is None else BF.snapshot(),r['BF_after']) and eq(BE.snapshot(),r['BE_after'])
            assert cf[:5]==r['chart_F'] and ce[:5]==r['chart_E']
            if 'A_events' in r:assert eq(ae,r['A_events'])
            for event in ae:
                for rot in event['rotations']:
                    before=clusters(rot['before'],M);after=clusters(rot['after'],M)
                    assert len(before-after)<=1 and len(after-before)<=1;rotations+=1
            actual.append({**r,'A_events':ae})
        assert boundary==(A.snapshot(),A.snapshot() if BF is None else BF.snapshot(),BE.snapshot(),tuple(cf[:5]),tuple(ce[:5]))
        return [r for r in actual if r['t']>=z['period'][0]],rotations
    # Completion bridge: replay a real paired-closed NONmaximal source.
    completion=read(F/'maximal_completion_original_source.json');cr,cr_rots=replay(completion,True)
    assert {r['key'] for r in cr if r['genuine_F']}=={1,3,5,7,9,11,13}
    old=read(F/'maximal_completion_bridge_result.json');counter=old['counter'];table=read(F/'full_B_actions.json');gram=read(F/'maximal_B_grammar.json')
    marks=gram['marks'];word=counter['word'];starts=[i for i,t in enumerate(gram['trees']) if t[0]==word[-1]]
    assert starts==counter['starts'] and len(starts)==144
    for s in starts:
        cur=s
        for k in word:
            e=table['actions'][cur][marks.index(k)]
            if not e['admissible']:cur=-1;break
            cur=e['destination']
        assert cur==int(counter['next'][str(s)])
        if cur>=0:assert counter['rank'][str(cur)]<counter['rank'][str(s)]
    assert counter['rank_bound']==1 and all(v<0 for v in counter['next'].values())
    # New dirty CCR source: actual A, full B, erased B and both charts close.
    z=read(F/'cluster_collateral_closed_source.json');rows,nrot=replay(z,False);M={r['key'] for r in rows if r['genuine_F']}
    assert M=={1,3,5,7,9,11,13} and len({r['key'] for r in rows if r['genuine_E']})==6
    mm=[];start=0;h0={}
    for end,r in enumerate(rows):
        if not r['genuine_F']:continue
        rr=rows[start:end+1];units=[(v['t'],j,b) for v in rr for j in range(1,v['a']+1) for b in (0,1)];demands=[(v['t'],k) for v in rr for k in range(1,v['qF']+1)]
        h0.update(zip(demands,units));mm.append({'rows':rr,'units':units,'demands':demands,'H':len(units)//2,'Q':len(demands)});start=end+1
    assert start==len(rows);assert h0=={tuple(v['demand']):tuple(v['unit']) for v in z['h0']}
    h={tuple(v['demand']):tuple(v['unit']) for v in z['full_h']};loans={};witnesses=0
    for block in z['blocks']:
        i=block['macro_indices'][0];recovery=mm[i];assert block['macro_indices']==list(range(i,i+4)) and recovery['Q']==2
        assert all(mm[j]['Q']==3 and mm[j]['H']==1 for j in range(i+1,i+4))
        rr=recovery['rows'];lost=clusters(rr[0]['A_before'],M)-clusters(rr[-1]['A_after'],M);assert len(lost)==6
        first={}
        for row in rr:
            for event in row['A_events']:
                for rot in event['rotations']:
                    for c in lost&(clusters(rot['before'],M)-clusters(rot['after'],M)):first.setdefault(c,(row['t'],event['j'],rot['bit']))
        assert set(first)==lost and len(set(first.values()))==6
        own={h0[d] for d in recovery['demands']};spare=sorted(u for u in first.values() if u not in own);assert len(spare)>=3
        missing=[d for j in range(i+1,i+4) for d in mm[j]['demands'] if d not in h0];assert len(missing)==3
        expected=dict(zip(missing,spare[:3]));assert all(h[d]==u for d,u in expected.items());loans.update(expected);witnesses+=len(first)
        assert any(row['genuine_F'] and row['a']==0 for row in rr),'the zero-A terminal correction must be present'
    D={(r['t'],k) for r in rows for k in range(1,r['qF']+1)};U={(r['t'],j,b) for r in rows for j in range(1,r['a']+1) for b in (0,1)}
    assert set(h)==D and len(set(h.values()))==len(h) and set(h.values())<=U and all(h[d]==u for d,u in h0.items())
    inverse_own={u:d for d,u in h0.items()};inverse_loan={u:d for d,u in loans.items()};bank=set();admitted=set();paid={};trace=[];peak=0
    for macro in mm:
        for row in macro['rows']:
            for event in row['A_events']:
                before=sorted(bank);peak=max(peak,len(bank)+2);actions=[]
                for bit in (0,1):
                    unit=(row['t'],event['j'],bit);assert unit not in admitted;admitted.add(unit)
                    if unit in inverse_own:
                        d=inverse_own[unit];assert d not in paid;paid[d]=unit;actions.append({'unit':unit,'action':'emit_own','demand':d})
                    elif unit in inverse_loan:bank.add(unit);actions.append({'unit':unit,'action':'store_selected_collateral','demand':inverse_loan[unit]})
                    else:assert unit not in h.values();actions.append({'unit':unit,'action':'release','demand':None})
                assert len(bank)<=3;trace.append({'t':row['t'],'j':event['j'],'before':before,'admitted':2,'actions':actions,'after':sorted(bank)})
        for d in macro['demands']:
            if d in paid:continue
            u=h[d];assert u in bank and loans[d]==u;bank.remove(u);paid[d]=u;trace.append({'consume_at_macro_end':d,'unit':u,'after':sorted(bank)})
    assert not bank and admitted==U and paid==h and peak==5
    with (F/'independent_cluster_collateral_bank_trace.json').open('x',encoding='utf-8') as f:json.dump({'status':'PASS','working_peak':peak,'period':z['period'],'trace':trace},f,indent=2)
    report={'status':'PASS_ORIGINAL_SOURCE_BRIDGES_AND_CLUSTER_COLLATERAL','maximal_completion':'REFUTED_BY_ORIGINAL_WORD_AND_ALL144_SOURCE_STATES',
      'completion_source_period':completion['period'],'completion_source_costs':{'A':completion['A_events'],'Q':completion['QF']},
      'CCR_source_period':z['period'],'CCR_source_costs':{'A':z['A_events'],'QF':z['QF'],'QE':z['QE']},'CCR_full_demands_paid':len(D),
      'CCR_natural_owners_literal':len(h0),'CCR_distinct_collateral_pairs':len(loans),'CCR_first_cluster_witnesses':witnesses,'CCR_working_bank':peak,
      'single_rotation_cluster_interfaces_checked':cr_rots+nrot,'zero_A_terminal_KEEPs_checked':sum(r['genuine_F'] and r['a']==0 for r in rows),
      'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'scope':'universal CCR derivation plus two exact source controls; maximal completion mechanism refutation only',
      'no_universal_CCR_partition_proved':True,'all_support_JR35':'OPEN','Coarse_Double_counterexample':False,
      'trust':'fresh independent mutable original A/B/E source execution, original charts/closure, witness ownership and actual bank; same agent, not external/formal review',
      'input_sha256':{p:sha(F/p) for p in ('maximal_completion_original_source.json','maximal_completion_bridge_result.json','cluster_collateral_closed_source.json','CLUSTER_COLLATERAL_REPAYMENT.md','MARKED_CLUSTER_WORK_LOWER_BOUND.md')}}
    with (F/'independent_source_bridges_collateral_audit.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        calls=0 if V is None else V.CALLS
        with (B/'audit_verify111_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':calls,'source_engine_calls':calls},f)
