"""Deterministic arbitrary-fringe source construction; Gate E authorized."""
import json,time
from pathlib import Path
from source_model import N,vine,operations,omega_plus,gamma_pair,singleton_sigma,core10_control,replay,packets,cyclic_path_min,charts,shadow,core,labels,inorder,trace
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;account={'new_finite_tests':0,'source_engine_calls':0}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    bank=json.loads((B.parent/'M3_LDR01/negative_run_census.json').read_text())
    ids={freeze(q['tree']):i for i,q in enumerate(bank['nodes'])}
    psi=[q['psi'] for q in bank['nodes']]
    results=[]
    specs=[('Omega_plus',vine(11),omega_plus(),3,[1,3,5,7,9,11],21,22),
        ('Gamma_pair',vine(11),gamma_pair(),3,[1,3,5,7,9,11],13,14),
        ('Sigma_singleton',vine(11),singleton_sigma(),7,[1,3,5,7,9,11],47,47)]
    for name,initial,w,z,marks,lo,hi in specs:
        first,end=replay(initial,w,z);account['source_engine_calls']+=len(w)+sum(m=='K' for m,k in w)+sum(m=='K' and k!=z for m,k in w)
        assert end[:2]==(initial,initial),(name,'full pair does not close')
        rows,end2=replay(initial,w,z,end[2]);account['source_engine_calls']+=len(w)+sum(m=='K' for m,k in w)+sum(m=='K' and k!=z for m,k in w)
        assert end2[:2]==(initial,initial)
        assert end2[2]==end[2],(name,'auxiliary needs longer recurrent period')
        assert all(labels(core(r['after'][1],set(marks)))==set(range(1,12)) for r in rows)
        cs=charts(rows,marks);assert all(c['old_chart']['size']==c['new_chart']['size']==9 for c in cs)
        ps=packets(rows);critical=next(p for p in ps if p['end']==hi and lo in p['occurrences'])
        assert critical['H']==(2 if hi>lo else 1) and critical['Q']==(6 if hi>lo else 4) and critical['w']==-2
        assert rows[lo-1]['genuine_F'] and cs[lo-1]['cold']
        old=cs[lo-1]['old_chart'];new=cs[hi-1]['new_chart'];a=rows[lo-1]['before'][0]
        ashadow=shadow(a,old['Scores'])
        if name!='Gamma_pair':
            assert ashadow['R'].get('key')==3
            assert old['Scores'][2]==3 and old['tree'][0]==0
            Dsource=1
        else:Dsource=0
        ni=ids[freeze(new['tree'])];newpsi=psi[ni]
        costA=sum(r['a'] for r in rows);QF=sum(r['qF'] for r in rows);QE=sum(r['qE'] for r in rows)
        row={'name':name,'word':[{'occurrence':i,'mode':m,'key':k} for i,(m,k) in enumerate(w,1)],
            'erased_key':z,'initial_full_diagonal':initial,'auxiliary_recurrent_start':end[2],
            'preperiod_copies':1,'aligned_period_copies':1,'AF_closure':True,'E_closure':True,
            'first_QE':sum(r['qE'] for r in first),'A':costA,'QF':QF,'QE':QE,'original_slack':2*costA-QF,
            'rows':rows,'charts':cs,'packets':ps,'critical_packet':critical,'critical_occurrences':[lo,hi],
            'critical_old_A':a,'critical_old_BF':rows[lo-1]['before'][1],
            'critical_end_A':rows[hi-1]['after'][0],'critical_end_BF':rows[hi-1]['after'][1],
            'old_chart':old,'new_chart':new,'old_A_shadow_known_real_Scores':ashadow,
            'normalized_source_debt':Dsource,'target_seed_psi_reused':newpsi,
            'target_debt_interval':[0,2],'residual_upper':-2+2-Dsource,
            'path_deficit_check':cyclic_path_min(ps),'all_gap_variables_conserved':True,
            'source_replay_type':'all F0..F11 are free ordered BST terms, never searched internally'}
        if name=='Omega_plus':assert (costA,QF,QE)==(48,32,24)
        if name=='Gamma_pair':assert (costA,QF,QE)==(36,30,24)
        if name=='Sigma_singleton':
            f=['F'+str(i) for i in range(12)]
            expected=N(1,f[0],N(2,f[1],N(3,f[2],N(4,f[3],N(5,f[4],N(6,f[5],N(9,N(8,N(7,f[6],f[7]),f[8]),N(10,f[9],N(11,f[10],f[11])))))))))
            assert row['critical_old_BF']==expected
            assert row['old_chart']['Scores']==[1,2,3,4,5,6,9,10,11]
            assert rows[46]['A_path']=='RR' and len(rows[46]['BF_path'])==8 and row['QF']==42
            hypothetical=vine(11);target_after,_,_=trace(hypothetical,7)
            assert target_after==row['critical_end_BF']
            # The alternate fixed nine-Score chart1..9 contains marked7;
            # original H1/q4 M3 forces Dtarget2 at precisely the NEW chart.
            assert row['new_chart']['Scores']==list(range(1,10))
            row['target_debt_interval']=[2,2];row['target_debt_proof']='original fixed-chart H1/q4 edge on Scores1..9, marks1,3,5,7,9; range2; target B non-Hamiltonian'
            row['residual_upper']=-1
        if newpsi==2 and new['tree'][1] is not None and new['tree'][2] is not None:row['target_debt_interval']=[2,2]
        # Exact physical C2 units and demands, in the chosen recurrent copy.
        row['A_units']=[(len(w)+r['occurrence'],j,bit) for r in rows for j in range(1,r['a']+1) for bit in (0,1)]
        row['BF_demands']=[(len(w)+r['occurrence'],j) for r in rows for j in range(1,r['qF']+1)]
        assert len(set(row['A_units']))==2*costA and len(set(row['BF_demands']))==QF
        results.append(row)
    s,w=core10_control();rows,end=replay(s,w,10)
    account['source_engine_calls']+=len(w)+sum(m=='K' for m,k in w)+sum(m=='K' and k!=10 for m,k in w)
    assert end[:2]==(s,s) and len(labels(core(s,{1,3,5,7,9,10})))==10
    control={'name':'core10_B_return_control','initial':s,'word':w,'A':sum(r['a'] for r in rows),
        'QF':sum(r['qF'] for r in rows),'full_pair_closed':True,'marked_mask':[1,3,5,7,9,10],'rows':rows,
        'scope':'one actual necessary deficiency mask, not all16 masks'}
    out('symbolic_replay.json',{'status':'PASS_EXACT_SOURCE_FAMILIES','families':results,'core10_control':control,
        'new_singleton_source_family':True,'frozen_graph_changed':False,'old_compiler_rows_replayed':0})
    print(json.dumps({'status':'PASS_EXACT_SOURCE_FAMILIES','families':[{'name':r['name'],'A':r['A'],'QF':r['QF'],'QE':r['QE'],
        'source_Dhat':r['normalized_source_debt'],'target_interval':r['target_debt_interval'],'psi_target':r['target_seed_psi_reused'],
        'critical':r['critical_packet'],'min_path':r['path_deficit_check']['minimum']} for r in results]}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_replay_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**account})
